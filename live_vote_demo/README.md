# Live room vote demonstration

A room votes on which survey factors belong in a model predicting past-year suicidal ideation, then the top-voted items go into a LASSO logistic regression, following the structure of [`../scripts/primary_analysis.do`](../scripts/primary_analysis.do).

**All modeling runs on synthetic data.** The 2,609 respondents are simulated and calibrated to published IWFP totals (Sierra 2026, [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/)). No CHKS respondent data are here. Results show how the method behaves. They are not findings about Native American youth, and effects for constructs IWFP didn't measure are demo settings.

Votes are collected in mVote. This folder holds two copies of the notebook: a **blank** one to start from, and the **saved run** from the Nov 5, 2026 room (below).

## Nov 5, 2026 run

The demo ran live with the room at the AIHEC AIM-AHEAD AMC lab, using the board `nov4-talk` (84 items, with the outcome `si` left off). The session's official record is kept in the mVote repo, which is private for now. This copy stays here as a public example of a finished run.

- **Votes:** 13 participant records, 177 dots, 75 of the 84 items got at least one dot (most dots on one item: 6). Totals are in [`nov5_lab_votes.csv`](nov5_lab_votes.csv). This repo holds only per-item totals. The board itself also keeps one record per participant, with that person's votes and remaining dots, and those records are not published here.
- **Model:** 55 voted items entered the LASSO. Seven were kept as higher risk (depressive symptoms, other psychological distress, loneliness, feeling hopeless, trauma-related symptoms, bullying, self-harm), five as protective (emotion regulation, positive emotional wellbeing, family support, optimism, life satisfaction), and four were weak or unstable. The other 39 were dropped. The table is in [`nov5_lab_model_results.csv`](nov5_lab_model_results.csv).
- **Reading it:** these are synthetic-data results, so they show how the method treats the room's choices, not what predicts ideation among Native youth. Correlated items compete (anxiety was dropped while depressive symptoms, distress and hopelessness were kept), which is why the dropped list is not a list of unimportant factors.

## Files

| File | What it is |
|---|---|
| [`IWFP_live_vote_demo.ipynb`](IWFP_live_vote_demo.ipynb) | **Blank notebook** with no saved output: votes, dataset, model, calibration, validation. Start here for your own room. |
| [`IWFP_live_vote_demo_nov5-2026_run.ipynb`](IWFP_live_vote_demo_nov5-2026_run.ipynb) | **Saved run** of the same notebook on the Nov 5, 2026 room's votes, with every chart and table. Read it to see what a finished run looks like. |
| [`nov5_lab_votes.csv`](nov5_lab_votes.csv), [`nov5_lab_model_results.csv`](nov5_lab_model_results.csv) | The room's dot totals and the model's result table from that run |
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

Open the blank notebook with that `.venv` as its interpreter and choose Run All. Set `BOARD_ID` in the Setup cell to a board, or `RESULTS_CSV` to a file (for example `nov5_lab_votes.csv` to reproduce the Nov 5 run without a live board). Reading vote tallies needs no login. Keep the blank copy clean: save your own runs under another name.

## Differences from the published analysis

| Step | Published (Stata) | Here (Python) |
|---|---|---|
| Penalty | `selection(cv)`, 10 folds | One-standard-error rule, 5 inner folds |
| Stability | Not used | Item must be kept in at least 70 of 100 bootstrap resamples |
| Calibration | GiViTI calibration belt | Groups of predicted risk and a recalibration slope |
| AUC interval | Bias-corrected bootstrap | Percentile bootstrap |
