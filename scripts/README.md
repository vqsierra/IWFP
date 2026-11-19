# Scripts

Stata code for the analyses in *Predicting Suicidal Ideation Among Native American High Schoolers in California* (Sierra, 2026). The analysis uses LASSO penalized regression to identify risk and protective factors for suicidal ideation in the 2019–20 California Healthy Kids Survey (CHKS).

| File | Purpose |
|---|---|
| `primary_analysis.do` | Main prediction model, a LASSO logistic regression with 10-fold cross-validation |
| `sensitivity_clustered.do` | Sensitivity analysis that accounts for students clustered within schools |
| `sensitivity_imputed.do` | Sensitivity analysis that uses multiple imputation for missing data |

## Outcome

All variables come from the CHKS Core Module. The outcome is past-year suicidal ideation, measured by the item "During the last 12 months, did you ever seriously consider attempting suicide?"

## Requirements

The scripts need Stata/SE 17.0 or later and four user-written packages: `lasso2` for penalized regression, `cvauroc` for AUC estimation, `calibrationbelt` for calibration and `moremata` for matrix functions. Install them with `ssc install` (see the main [README](../README.md)).

## Reproducing the analysis

1. Obtain access to the CHKS data (see [`../rawdata/`](../rawdata/README.md)).
2. Rename variables if needed so they match the names in the scripts.
3. Run each `.do` file in Stata. The scripts can run in order or one at a time.

## Ethical use

The study was exempt from IRB review as a secondary analysis of existing data. Please cite the article when using this code, and do not use it for commercial purposes.

Questions: Valentín Quiroz de la Sierra, PhD, MSW, Johns Hopkins Center for Indigenous Health ([vsierra4@jh.edu](mailto:vsierra4@jh.edu))
