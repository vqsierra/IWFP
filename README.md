# Indigenous Wholistic Factors Project (IWFP)

**Lead Author**: Valentín Quiroz de la Sierra, PhD, MSW <br>
**Tribal Affiliation**: Yo'eme <br>
**Academic Affiliation**: Johns Hopkins Bloomberg School of Public Health, Center for Indigenous Health <br>
**Last Updated**: November 2026

## Overview

The Indigenous Wholistic Factors Project (IWFP) is a community-centered, data-driven initiative aimed at advancing culturally grounded understandings of suicide risk and protective factors among Native American youth in California. This repository supports the published article:

**Sierra, V. Q.** (2026). Predicting Suicidal Ideation Among Native American High Schoolers in California. *Archives of Suicide Research, 30*(1), 80–97. [https://doi.org/10.1080/13811118.2025.2490154](https://doi.org/10.1080/13811118.2025.2490154)

This project uses data from the 2019–2020 California Healthy Kids Survey (CHKS) and is guided by Indigenous Wholistic Theory and the Indigenous Computational Approach. A LASSO logistic regression model was used to identify predictors of past-year suicidal ideation among Native American high school students.

## Project Goals

- Advance culturally grounded knowledge of risk and protective factors to support suicide prevention among Native American youth in California
- Apply community-centered machine learning methods through the Indigenous Computational Approach to support ethical, culturally grounded public health research
- Promote open science practices that align with Indigenous Data Sovereignty principles

## Repository Contents

```
/data/                                # Placeholder for analysis-ready data (not included)
/rawdata/                             # Placeholder for raw CHKS data (not included)
/documentation/
  ├── calschls-2019-20-crosswalk.pdf  # Survey item crosswalk
  ├── cschls_researchsum2018.pdf      # CHKS codebook and methodology
  └── appendixa.pdf                   # Construction of predictor variables

/output/
  ├── appendixb.pdf                   # School-level clustering sensitivity analysis
  └── appendixc.pdf                   # Missing data imputation sensitivity analysis

/paper/                               # Citation for the published article

/scripts/
  ├── primary_analysis.do             # LASSO model and predictors
  ├── sensitivity_clustered.do        # Clustered schools sensitivity analysis
  └── sensitivity_imputed.do          # Missing data imputation analysis

/live_vote_demo/                      # Live session notebook using synthetic data

README.md                             # Main project documentation
```

## Live Vote Demonstration

[`live_vote_demo/`](live_vote_demo/) holds a Python notebook used in a live session: a room votes on survey factors, and their top-voted items go into a LASSO model. It runs on **synthetic data**, not CHKS responses, and its results are not findings.

## Software Requirements

Analyses require **Stata/SE 17.0 or higher** and the following user-written packages:

- `lasso2` – Penalized regression
- `cvauroc` – AUC estimation
- `calibrationbelt` – Model calibration assessment
- `moremata` – Matrix and math utilities

Install them in Stata using:

```stata
ssc install lasso2
ssc install cvauroc
ssc install calibrationbelt
ssc install moremata
```

## Data Availability

The California Healthy Kids Survey (CHKS) data are **not publicly shared** in this repository due to privacy protections for youth and school districts. Researchers may request access from WestEd or local education authorities subject to IRB approval.

## OSF Link

All study materials — including supplemental documentation, appendices, and pre-registration — are archived at the Open Science Framework (OSF): 
🔗 [https://osf.io/4dpwt/](https://osf.io/4dpwt/)

## Contributing

This repository is intended to support transparent, ethical, and collaborative computational research in Indigenous health. If you'd like to adapt or contribute to this project:

1. Fork the repository and submit a pull request
2. Include a description of your proposed changes
3. Ensure your contributions respect Indigenous research ethics and Indigenous Data Sovereignty principles

## Citation

If you use or adapt any portion of this repository, please cite:

**Sierra, V. Q.** (2026). Predicting Suicidal Ideation Among Native American High Schoolers in California. *Archives of Suicide Research, 30*(1), 80–97. [https://doi.org/10.1080/13811118.2025.2490154](https://doi.org/10.1080/13811118.2025.2490154)

The Indigenous Computational Approach used in this project is described in:

**de la Sierra, V. Q.** (2026). A Guide to Constructing Indigenous Statistical Spaces for Prevention Science Research. *Prevention Science, 27*(7), 1239–1252. [https://doi.org/10.1007/s11121-026-01911-5](https://doi.org/10.1007/s11121-026-01911-5)


## Contact

For questions, collaboration opportunities, or data requests, contact:  
**Valentín Quiroz de la Sierra, PhD, MSW** (Yo'eme) <br>
Postdoctoral Fellow <br>
Johns Hopkins Bloomberg School of Public Health <br>
Center for Indigenous Health <br>
[vsierra4@jh.edu](mailto:vsierra4@jh.edu)
