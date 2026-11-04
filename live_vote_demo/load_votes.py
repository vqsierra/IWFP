"""Load the room's vote tallies: live from the board, or from a saved or hand-typed file.

Reading tallies needs no key or login. The board's vote counts are readable by
anyone with its address, the same way the voting page reads them, and they hold
only a count per item.
"""
from __future__ import annotations

import csv
import json
import urllib.request
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ITEMS = [i for i in json.loads((HERE / "items.json").read_text()) if i["id"] != "si"]
LABELS = {i["id"]: i["label"][0].upper() + i["label"][1:] for i in json.loads((HERE / "items.json").read_text())}
VOTES_URL = ("https://firestore.googleapis.com/v1/projects/choachoaktevote/databases/(default)"
             "/documents/boards/{board}/votes?pageSize=300")


class DemoStop(Exception):
    """Stops Run All with a plain message instead of a long traceback."""

    def _render_traceback_(self):
        return [f"STOPPED: {self}"]


def fetch_board(board_id: str, timeout: float = 15) -> dict[str, int]:
    counts: dict[str, int] = {}
    url = VOTES_URL.format(board=board_id)
    while url:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            page = json.load(response)
        for doc in page.get("documents", []):
            counts[doc["name"].rsplit("/", 1)[-1]] = int(doc["fields"]["count"]["integerValue"])
        token = page.get("nextPageToken")
        url = f"{VOTES_URL.format(board=board_id)}&pageToken={token}" if token else None
    return counts


def read_tally(path: Path) -> dict[str, int]:
    """Read a saved results file or a paper tally. Blank counts are treated as 0."""
    known = set(LABELS)
    counts: dict[str, int] = {}
    with Path(path).open(newline="", encoding="utf-8") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            item = (row.get("item_id") or "").strip()
            value = (row.get("vote_count") or "").strip()
            if not item:
                continue
            if item not in known:
                raise DemoStop(f"{path}, line {line}: unknown item id '{item}'. Check the spelling.")
            try:
                counts[item] = int(value or 0)
            except ValueError:
                raise DemoStop(f"{path}, line {line}: '{value}' isn't a whole number.") from None
    return counts


def as_table(counts: dict[str, int]) -> pd.DataFrame:
    """One row per board item, in board order so ties stay in a stable order."""
    return pd.DataFrame([
        {"item_id": i["id"], "label": LABELS[i["id"]], "vote_count": counts.get(i["id"], 0)} for i in ITEMS
    ])


def load_votes(board_id: str, results_csv: str | None = None) -> tuple[pd.DataFrame, str]:
    """Return (tally table, sentence naming where the votes came from).

    Live results are saved to results/ straight away. If the connection fails,
    the last saved copy for this board is used, and the sentence says so.
    """
    saved = HERE / "results" / f"{board_id}-votes.csv"
    if results_csv:
        table = as_table(read_tally(Path(results_csv)))
        source = f"Votes from the file {results_csv}."
    else:
        try:
            table = as_table(fetch_board(board_id))
        except OSError as error:
            if not saved.exists():
                raise DemoStop(f"Can't reach board '{board_id}' ({error}) and no saved copy exists. "
                               "Try the phone hotspot, or set RESULTS_CSV.") from None
            table = as_table(read_tally(saved))
            source = f"NO CONNECTION: using the last saved copy for board '{board_id}'."
        else:
            source = f"Live votes from board '{board_id}'."
            if table["vote_count"].sum() > 0:
                saved.parent.mkdir(exist_ok=True)
                table.to_csv(saved, index=False)
                source += " Saved to results/."
    if table["vote_count"].sum() == 0:
        raise DemoStop(f"No votes recorded yet. {source} Rerun once the room has voted.")
    return table, source


def top_voted(table: pd.DataFrame, n: int = 30) -> tuple[pd.DataFrame, bool]:
    """Top n items with at least one vote. Items tied at the cutoff are all kept."""
    voted = table[table["vote_count"] > 0].sort_values("vote_count", ascending=False, kind="stable")
    if n <= 0 or len(voted) <= n:
        return voted.reset_index(drop=True), False
    cutoff = int(voted["vote_count"].iloc[n - 1])
    kept = voted[voted["vote_count"] >= cutoff].reset_index(drop=True)
    return kept, len(kept) > n
