# Indigenous Wholistic Factors Project (IWFP)

**Lead Author**: Valentín Quiroz de la Sierra, PhD, MSW <br>
**Tribal Affiliation**: Yo'eme <br>
**Academic Affiliation**: Johns Hopkins Bloomberg School of Public Health, Center for Indigenous Health <br>
**Last updated**: November 2026

## Overview

The Indigenous Wholistic Factors Project (IWFP) studies risk and protective factors for suicide among Native American youth in California, using community-centered data science grounded in Indigenous knowledge. This repository holds the code and supporting materials for the published article:

**Sierra, V. Q.** (2026). Predicting Suicidal Ideation Among Native American High Schoolers in California. *Archives of Suicide Research, 30*(1), 80–97. [https://doi.org/10.1080/13811118.2025.2490154](https://doi.org/10.1080/13811118.2025.2490154)

The study draws on the 2019–20 California Healthy Kids Survey (CHKS) and is guided by Indigenous Wholistic Theory and the Indigenous Computational Approach. A LASSO logistic regression identified predictors of past-year suicidal ideation among Native American high school students.

## Project Goals

- Build culturally grounded knowledge of risk and protective factors that can inform suicide prevention for Native American youth in California
- Apply community-centered machine learning through the Indigenous Computational Approach
- Practice open science in line with Indigenous Data Sovereignty principles

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

/live_vote_demo/                      # Interactive teaching demonstration (synthetic data)
/talks/                               # Talks that featured the demonstration

README.md                             # Main project documentation
```

## Live Vote Demonstration

[`live_vote_demo/`](live_vote_demo/README.md) is an interactive teaching version of the IWFP method. Participants vote on survey factors with the free [mVote](https://mvote.app) app, and their top choices go into a LASSO model run live in a Python notebook. The demonstration uses **synthetic data** and contains no California Healthy Kids Survey responses, so its results serve as teaching examples only.

## Talks

[`talks/`](talks/README.md) lists the talks and workshops that featured the demonstration, with event details and the results from each session.

## Software Requirements

The analyses require **Stata/SE 17.0 or later** and these user-written packages:

- `lasso2` – Penalized regression
- `cvauroc` – AUC estimation
- `calibrationbelt` – Model calibration assessment
- `moremata` – Matrix and math utilities

Install them in Stata with:

```stata
ssc install lasso2
ssc install cvauroc
ssc install calibrationbelt
ssc install moremata
```

## Data Availability

The California Healthy Kids Survey (CHKS) data are kept out of this repository to protect the privacy of young people and school districts. Researchers can request access from WestEd or local education agencies, subject to IRB approval.

## Open Science Framework

Study materials, including supplementary documentation, appendices and the preregistration, are archived on OSF at [osf.io/4dpwt](https://osf.io/4dpwt/).

## Contributing

Contributions that support transparent, ethical and collaborative research in Indigenous health are welcome. To propose a change, fork the repository and open a pull request that describes it. Contributions should respect Indigenous research ethics and Indigenous Data Sovereignty principles.

## Citation

If you use or adapt any part of this repository, please cite:

**Sierra, V. Q.** (2026). Predicting Suicidal Ideation Among Native American High Schoolers in California. *Archives of Suicide Research, 30*(1), 80–97. [https://doi.org/10.1080/13811118.2025.2490154](https://doi.org/10.1080/13811118.2025.2490154)

The Indigenous Computational Approach is described in:

**de la Sierra, V. Q.** (2026). A Guide to Constructing Indigenous Statistical Spaces for Prevention Science Research. *Prevention Science, 27*(7), 1239–1252. [https://doi.org/10.1007/s11121-026-01911-5](https://doi.org/10.1007/s11121-026-01911-5)

## Contact

For questions, collaborations or data requests, contact:  
**Valentín Quiroz de la Sierra, PhD, MSW** (Yo'eme) <br>
Postdoctoral Fellow <br>
Johns Hopkins Bloomberg School of Public Health <br>
Center for Indigenous Health <br>
[vsierra4@jh.edu](mailto:vsierra4@jh.edu)
