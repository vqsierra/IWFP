# Live room vote demonstration

A room votes on which survey factors belong in a model predicting past-year suicidal ideation, then the top-voted items go into a LASSO logistic regression, following the structure of [`../scripts/primary_analysis.do`](../scripts/primary_analysis.do).

**All modeling runs on synthetic data.** The 2,609 respondents are simulated and calibrated to published IWFP totals (Sierra 2025, [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/)). No CHKS respondent data are here. Results show how the method behaves. They are not findings about Native American youth, and effects for constructs IWFP didn't measure are demo settings.

Votes are collected in ChoachoakteVote. The saved notebook shows rehearsal votes.

## Files

| File | What it is |
|---|---|
| [`IWFP_live_vote_demo.ipynb`](IWFP_live_vote_demo.ipynb) | The notebook: votes, dataset, model, calibration, validation |
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

Open the notebook with that `.venv` as its interpreter and choose Run All. Set `BOARD_ID` in the Setup cell to a board, or `RESULTS_CSV` to a file. Reading vote tallies needs no login.

## Differences from the published analysis

| Step | Published (Stata) | Here (Python) |
|---|---|---|
| Penalty | `selection(cv)`, 10 folds | One-standard-error rule, 5 inner folds |
| Stability | Not used | Item must be kept in at least 70 of 100 bootstrap resamples |
| Calibration | GiViTI calibration belt | Groups of predicted risk and a recalibration slope |
| AUC interval | Bias-corrected bootstrap | Percentile bootstrap |
