"""Charts for the live vote notebook, sized to read on a projector."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve

INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#a3a29c"
GROUP_COLORS = {"higher risk": ORANGE, "protective": BLUE, "weak or unstable": GREY, "dropped": GREY}

plt.rcParams.update({
    "font.size": 13, "axes.titlesize": 16, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.labelcolor": MUTED, "axes.edgecolor": GRID, "xtick.color": MUTED, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.8, "axes.axisbelow": True, "figure.dpi": 110, "savefig.bbox": "tight",
    "legend.frameon": False,
})


def _rows(n: int) -> float:
    return max(3.0, 0.34 * n + 1.2)


def votes_chart(ranked, title="What the room voted for"):
    fig, ax = plt.subplots(figsize=(11, _rows(len(ranked))))
    y = np.arange(len(ranked))
    ax.barh(y, ranked["vote_count"], color=BLUE, height=0.72)
    ax.set_yticks(y, ranked["label"])
    ax.invert_yaxis()
    for i, v in enumerate(ranked["vote_count"]):
        ax.text(v + 0.08, i, str(v), va="center", color=INK)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.set_xlabel("Dots")
    ax.grid(axis="y", visible=False)
    ax.set_title(title)
    return fig


def cv_chart(curve):
    fig, ax = plt.subplots(figsize=(11, 4.6))
    penalty = 1 / curve["C"]
    ax.plot(penalty, curve["mean"], color=BLUE, linewidth=2)
    ax.fill_between(penalty, curve["mean"] - curve["se"], curve["mean"] + curve["se"], color=BLUE, alpha=0.15, linewidth=0)
    ax.set_xscale("log")
    for key, text, ls, height in (("best", "best AUC", ":", 0.55), ("chosen", "chosen: one-SE rule", "--", 0.40)):
        x = penalty[curve[key]]
        ax.axvline(x, color=INK, linestyle=ls, linewidth=1.2)
        ax.annotate(text, (x, height), xycoords=("data", "axes fraction"), xytext=(-6, 0), textcoords="offset points",
                    ha="right", color=INK)
    ax.set_xlabel("Penalty strength (1/C): stronger penalty, fewer items kept")
    ax.set_ylabel("Cross-validated AUC")
    ax.set_title("Choosing the penalty")
    return fig


def path_chart(path, curve, labels, label_top=6):
    fig, ax = plt.subplots(figsize=(11, 5.4))
    penalty = 1 / path.index.to_numpy()
    chosen = path.iloc[curve["chosen"]]
    top = list(chosen.abs().sort_values(ascending=False).head(label_top).index)
    top = [f for f in top if abs(chosen[f]) > 1e-6]
    for feature in path.columns:
        if feature not in top:
            ax.plot(penalty, path[feature], color=GREY, linewidth=1, alpha=0.6)
    for feature in top:
        ax.plot(penalty, path[feature], color=ORANGE if chosen[feature] > 0 else BLUE, linewidth=2)
    ax.set_xscale("log")
    ax.axvline(penalty[curve["chosen"]], color=INK, linestyle="--", linewidth=1.2)
    ax.axhline(0, color=MUTED, linewidth=0.8)
    # Name the leaders at the weak-penalty end, nudged apart so labels don't collide.
    placed = []
    span = float(path.to_numpy().max() - path.to_numpy().min()) or 1.0
    for feature in sorted(top, key=lambda f: path[f].iloc[-1]):
        y = float(path[feature].iloc[-1])
        if placed and y - placed[-1] < 0.055 * span:
            y = placed[-1] + 0.055 * span
        placed.append(y)
        ax.annotate(labels.get(feature, feature), (penalty[-1], y), xytext=(-6, 0), textcoords="offset points",
                    ha="right", va="center", color=INK, fontsize=11)
    ax.set_xlim(penalty.min() / 60, penalty.max() * 1.5)
    ax.set_xlabel("Penalty strength (1/C): stronger penalty, fewer items kept")
    ax.set_ylabel("Coefficient per 1 SD")
    ax.set_title("Items drop out as the penalty grows")
    return fig


def odds_chart(result, labels, classify):
    kept = [f for f in result["candidate_features"] if f in result["selected_features"]]
    kept.sort(key=lambda f: -result["odds_ratios"][f])
    fig, ax = plt.subplots(figsize=(11, _rows(len(kept))))
    for i, f in enumerate(kept):
        odds = result["odds_ratios"][f]
        group = classify(result, f)
        ax.plot([1, odds], [i, i], color=GROUP_COLORS[group], linewidth=2)
        ax.plot(odds, i, "o", color=GROUP_COLORS[group], markersize=9)
        ax.annotate(f"{odds:.2f}", (odds, i), xytext=(10 if odds >= 1 else -10, 0), textcoords="offset points",
                    ha="left" if odds >= 1 else "right", va="center", color=INK)
    ax.axvline(1, color=INK, linewidth=1)
    ax.set_xscale("log")
    ax.set_yticks(range(len(kept)), [labels.get(f, f) for f in kept])
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.margins(x=0.12)
    low, high = ax.get_xlim()
    ticks = [t for t in (0.25, 0.33, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.25, 1.5, 2, 3, 4) if low <= t <= high]
    ax.set_xticks(ticks, [f"{t:g}" for t in ticks])
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlabel("Odds ratio per 1 SD (log scale)")
    handles = [plt.Line2D([], [], color=GROUP_COLORS[g], marker="o", linewidth=2, label=g)
               for g in ("higher risk", "protective", "weak or unstable")]
    ax.legend(handles=handles, loc="lower right")
    ax.set_title("What the model kept")
    return fig


def stability_chart(result, labels, classify, threshold=0.7):
    items = sorted(result["candidate_features"], key=lambda f: -result["stability"][f])
    fig, ax = plt.subplots(figsize=(11, _rows(len(items))))
    shares = [result["stability"][f] * 100 for f in items]
    ax.barh(range(len(items)), shares, color=[GROUP_COLORS[classify(result, f)] for f in items], height=0.72)
    for i, s in enumerate(shares):
        ax.text(s + 1, i, f"{s:.0f}%", va="center", color=INK)
    ax.axvline(threshold * 100, color=INK, linestyle="--", linewidth=1.2)
    ax.annotate("70% needed to count as a finding", (threshold * 100, len(items) - 1), xytext=(-6, 0),
                textcoords="offset points", ha="right", va="center", color=INK)
    ax.set_yticks(range(len(items)), [labels.get(f, f) for f in items])
    ax.invert_yaxis()
    ax.set_xlim(0, 110)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Share of 100 resamples in which LASSO kept the item")
    ax.set_title("What held up across resamples")
    return fig


def calibration_chart(table):
    fig, ax = plt.subplots(figsize=(7, 6.4))
    top = max(table["high"].max(), table["predicted"].max()) * 1.05
    ax.plot([0, top], [0, top], color=MUTED, linewidth=1, linestyle="--", label="Perfect calibration")
    ax.errorbar(table["predicted"], table["observed"],
                yerr=[table["observed"] - table["low"], table["high"] - table["observed"]],
                fmt="o", color=BLUE, markersize=8, linewidth=2, capsize=0, label="Tenths of predicted risk, 95% CI")
    ax.set_xlim(0, top)
    ax.set_ylim(0, top)
    ax.set_xlabel("Predicted risk")
    ax.set_ylabel("Observed share with SI")
    ax.legend(loc="upper left")
    ax.set_title("Calibration")
    return fig


def roc_chart(y, curves):
    """curves: list of (name, risk, auc), at most two, with direct labels."""
    fig, ax = plt.subplots(figsize=(7, 6.4))
    ax.plot([0, 1], [0, 1], color=MUTED, linewidth=1, linestyle="--", label="No better than chance")
    for (name, risk, auc), color, ls in zip(curves, (BLUE, ORANGE), ("-", "--")):
        fpr, tpr, _ = roc_curve(y, risk)
        ax.plot(fpr, tpr, color=color, linewidth=2, linestyle=ls, label=f"{name}: AUC {auc:.2f}")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.legend(loc="lower right")
    ax.set_title("Discrimination: cross-validated ROC")
    return fig


def risk_chart(y, risk):
    fig, ax = plt.subplots(figsize=(11, 4.6))
    bins = np.linspace(0, 1, 41)
    for value, name, color, ls in ((0, "Did not report SI", BLUE, "-"), (1, "Reported SI", ORANGE, "--")):
        ax.hist(risk[y == value], bins=bins, histtype="step", linewidth=2, color=color, linestyle=ls,
                density=True, label=name)
    ax.set_xlabel("Predicted risk")
    ax.set_ylabel("Density")
    ax.legend(loc="upper right")
    ax.set_title("Distribution of risk scores")
    return fig
