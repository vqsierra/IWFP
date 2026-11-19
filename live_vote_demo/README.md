# Live Vote Demonstration

This folder holds an interactive teaching demonstration of the IWFP method. Participants vote on which survey factors should go into a model that predicts past-year suicidal ideation. Their top choices then go into a LASSO logistic regression, the same kind of model used in the published analysis ([`../scripts/primary_analysis.do`](../scripts/primary_analysis.do)).

**The demonstration uses synthetic data only.** The 2,609 simulated students are calibrated to the published IWFP totals (Sierra, 2026, [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/)). The folder contains no California Healthy Kids Survey responses. Results illustrate how the method responds to a group's choices and should be read as a teaching example only. Effects for factors that IWFP did not measure are illustrative settings.

Votes are collected with [mVote](https://mvote.app), a free voting app that needs no accounts or names. Results from past sessions are in [`../talks/`](../talks/README.md).

## Notebooks

| Notebook | Use it for |
|---|---|
| [`IWFP_live_vote_demo.ipynb`](IWFP_live_vote_demo.ipynb) | The full demonstration: votes, synthetic dataset, model, calibration and validation. Best for research and methods audiences. |
| [`P4HE_live_vote_demo.ipynb`](P4HE_live_vote_demo.ipynb) | A shorter version with 25 plain-language factors, five steps and large fonts for screen sharing. Best for general audiences. Technical details are in its appendix. |

## Other files

| File | Contents |
|---|---|
| `synthetic_data.py` | Builds the synthetic dataset (seeded and reproducible) |
| `pipeline.py` | LASSO with the one-standard-error penalty, nested cross-validation and a bootstrap stability check |
| `load_votes.py` | Reads vote totals from mVote or from a file |
| `figures.py` | Charts |
| `iwfp_reference.py` | Published IWFP values, for comparison |
| `items.json`, `p4he_items.json` | The factors shown to voters in each notebook |
| `paper_tally_template.csv` | A template for entering sticky-dot counts by hand when the app is unavailable |
| `rehearsal_votes.csv`, `p4he_rehearsal_votes.csv` | Example votes for practice runs |

## Running the demonstration

Set up Python once:

```bash
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
```

Open a notebook with that environment and choose Run All. In the Setup cell, set `BOARD_ID` to your mVote board, or set `RESULTS_CSV` to a file of vote totals. To reproduce the Nov 5, 2026 session, for example, set `RESULTS_CSV` to `../talks/2026-11-05-aim-ahead-lab/run/nov5_lab_votes.csv`. Reading votes requires no login. Save your own runs under a new file name so the original notebook stays blank for the next group.

## How the demonstration differs from the published analysis

| Step | Published analysis (Stata) | Demonstration (Python) |
|---|---|---|
| Penalty | Cross-validated, 10 folds | One-standard-error rule, 5 inner folds |
| Stability | Not used | A factor must be kept in at least 70 of 100 bootstrap resamples |
| Calibration | GiViTI calibration belt | Groups of predicted risk and a recalibration slope |
| AUC interval | Bias-corrected bootstrap | Percentile bootstrap |
