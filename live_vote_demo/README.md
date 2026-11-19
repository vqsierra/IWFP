# Live room vote demonstration

A room votes on which survey factors belong in a model predicting past-year suicidal ideation, then the top-voted items go into a LASSO logistic regression, following the structure of [`../scripts/primary_analysis.do`](../scripts/primary_analysis.do).

**All modeling runs on synthetic data.** The 2,609 respondents are simulated and calibrated to published IWFP totals (Sierra 2026, [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/)). No CHKS respondent data are here. Results show how the method behaves. They are not findings about Native American youth, and effects for constructs IWFP didn't measure are demo settings.

Votes are collected in mVote. This folder holds the code and the blank notebooks to start from. Saved runs from past sessions live with each talk in [`../talks/`](../talks/README.md).

## Files

| File | What it is |
|---|---|
| [`IWFP_live_vote_demo.ipynb`](IWFP_live_vote_demo.ipynb) | **Blank notebook** with no saved output: votes, dataset, model, calibration, validation. Start here for your own room. |
| [`P4HE_live_vote_demo.ipynb`](P4HE_live_vote_demo.ipynb), `p4he_items.json`, `p4he_rehearsal_votes.csv` | **Blank highlights notebook**, first used at the Nov 19, 2026 P4HE workshop: 25 plain-language factors, five steps, large fonts for screen sharing, with details in an appendix |
| `synthetic_data.py` | Builds the synthetic dataset (seeded, reproducible) |
| `pipeline.py` | LASSO with the one-SE penalty, nested cross-validation, bootstrap stability check |
| `load_votes.py` | Loads tallies from the live board or a file |
| `figures.py` | Charts |
| `iwfp_reference.py` | Published values and domains, for comparison |
| `items.json` | The survey factors on the board |
| `paper_tally_template.csv` | For typing in sticky-dot counts if the app can't be used |
| `rehearsal_votes.csv` | Rehearsal votes, as a last-resort backup |

## Run it

```bash
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
```

Open the blank notebook with that `.venv` as its interpreter and choose Run All. Set `BOARD_ID` in the Setup cell to a board, or `RESULTS_CSV` to a file (for example `../talks/2026-11-05-aim-ahead-lab/run/nov5_lab_votes.csv` to reproduce the Nov 5 run without a live board). Reading vote tallies needs no login. Keep the blank copy clean: save your own runs under another name.

## Differences from the published analysis

| Step | Published (Stata) | Here (Python) |
|---|---|---|
| Penalty | `selection(cv)`, 10 folds | One-standard-error rule, 5 inner folds |
| Stability | Not used | Item must be kept in at least 70 of 100 bootstrap resamples |
| Calibration | GiViTI calibration belt | Groups of predicted risk and a recalibration slope |
| AUC interval | Bias-corrected bootstrap | Percentile bootstrap |
