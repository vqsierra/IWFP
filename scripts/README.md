# Scripts

## Overview
This project supports the manuscript titled *Predicting Suicidal Ideation among Native American High Schoolers in California* by Dr. Valentín Quiroz Sierra. The analysis applies lasso penalized regression to identify risk factors for suicidal ideation using the 2019–2020 California Healthy Kids Survey (CHKS) dataset.

## Files
- `primary_analysis.do`: Main predictive model using lasso regression with 10-fold cross-validation.
- `sensitivity_clustered.do`: Sensitivity analysis accounting for clustering at the school level.
- `sensitivity_imputed.do`: Sensitivity analysis using multiple imputation for missing data.

## Data Source
All variables are derived from the CHKS Core Module. Suicidal ideation is assessed via the item: "During the last 12 months, did you ever seriously consider attempting suicide?"

## Software
Stata/SE 17.0 or higher is required. Required user-written packages:
- `lasso2` for penalized regression
- `cvauroc` for AUC estimation
- `calibrationbelt` for model calibration assessment
- `moremata` for matrix operations required by some user-written commands 

## Reproducibility
To reproduce the analysis:
1. Load each `.do` file into Stata.
2. Ensure access to CHKS data and rename relevant variables if needed.
3. Run the scripts in sequence or independently as needed.

## Ethical Use
This research was approved under IRB exemption for secondary data analysis. Please cite responsibly and do not use for commercial purposes.

## Contact
Valentín Quiroz Sierra, PhD, MSW
Yo'eme
Postdoctoral Fellow  
Johns Hopkins Bloomberg School of Public Health  
Center for Indigenous Health
vsierra4@jh.edu