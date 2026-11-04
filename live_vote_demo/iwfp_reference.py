"""Published IWFP values, for comparison only.

Source: Sierra VQ (2025). Predicting Suicidal Ideation Among Native American High
Schoolers in California. Archives of Suicide Research 30(1):80-97.
doi:10.1080/13811118.2025.2490154 (PMC12424082), Tables 1 and 2.
Domains follow Table 2 and scripts/primary_analysis.do. Item ids are this demo's
closest match to each IWFP predictor.
"""
import pandas as pd

# (domain, IWFP predictor, Stata variable, demo item id, retained in the published lasso)
PREDICTORS = pd.DataFrame([
    ("Individual", "Gender", "gender", "gender", False),
    ("Individual", "Gender minority status", "trans", "transgender", True),
    ("Individual", "Sexual minority status", "lgbt", "lgb", True),
    ("Individual", "Academic performance", "zacademic", "academic_performance", False),
    ("Individual", "Lifetime alcohol use", "zlifealc", "alcohol_use", True),
    ("Individual", "Lifetime cigarette use", "zlifecig", "tobacco_use", False),
    ("Individual", "Lifetime vape use", "zlifevape", "vaping", True),
    ("Individual", "Lifetime cannabis use", "zlifecan", "cannabis_use", True),
    ("Individual", "Lifetime other drug use", "zlifedrug", "other_drug_use", False),
    ("Emotional-Social", "Foster care placement", "foster", "fostercare", False),
    ("Emotional-Social", "Parent education level", "zparented", "parental_education", True),
    ("Emotional-Social", "Positive substance use education", "zdruged", "substance_risk_perceptions", False),
    ("Emotional-Social", "School-based victimization", "zbully", "bullying", True),
    ("Emotional-Social", "Access to drugs and alcohol", "zdrugaccess", "substance_access", True),
    ("Mental-Political", "Depressive symptoms", "depression", "depressive_symptoms", True),
    ("Physical-Economic", "Homelessness", "homeless", "homeless", False),
    ("Physical-Economic", "Breakfast consumption", "breakfast", "breakfast", True),
], columns=["domain", "predictor", "stata_variable", "item_id", "published_retained"])

# Table 1 prevalence (percent) next to the demo item that was calibrated to it.
TABLE_1 = [
    ("Past-year suicidal ideation", "si", 16.8),
    ("Female", "gender", 50.6),
    ("Transgender", "transgender", 2.95),
    ("Sexual minority", "lgb", 17.0),
    ("Depressive symptoms", "depressive_symptoms", 40.0),
    ("Foster care", "fostercare", 0.34),
    ("Homeless", "homeless", 2.53),
    ("Ate breakfast", "breakfast", 55.0),
]

PUBLISHED = {
    "predictors offered": 17, "predictors retained": 10,
    "auc": 0.87, "auc_low": 0.84, "auc_high": 0.88, "brier": 0.10,
    "risk_min": 0.0192, "risk_max": 0.9363, "risk_median": 0.0483, "risk_q1": 0.0264, "risk_q3": 0.2684,
}
