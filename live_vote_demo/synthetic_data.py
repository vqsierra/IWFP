"""Synthetic CHKS-structured dataset for the Nov 4 demo, calibrated to IWFP.

NOT real CHKS data. Real CHKS respondent data is privacy-protected (see the
public IWFP repo's "Data Availability") and its sensitive items shouldn't be
run live in a room. Every value here is simulated.

What it's calibrated to (published aggregates only, never respondent data):
  Sierra VQ (2026). Predicting Suicidal Ideation Among Native American High
  Schoolers in California. Archives of Suicide Research 30(1):80-97.
  doi:10.1080/13811118.2025.2490154 (PMC12424082), Table 1 and LASSO results:
  n = 2,609; past-year SI 16.8%; 50.6% female; 2.95% transgender; 17.0% sexual
  minority; 40.0% depressive symptoms; 0.34% foster care; 2.53% homeless;
  55.0% ate breakfast; LASSO retained depressive symptoms (largest), school
  victimization, sexual minority status, and small effects for vaping, drug
  access, alcohol, skipping breakfast and cannabis; AUC 0.87.

How it's built: real survey items cluster, so each respondent gets five
correlated latent factors (distress, victimization, substance involvement,
connectedness/support, structural adversity), and every item is a noisy
indicator of one or more of them, cut to a CHKS-style response format and
marginal distribution. Sexual and gender minority status raise distress and
victimization (minority stress). SI depends on the factors plus the observed
items IWFP found. Effects for constructs IWFP did not measure (hopelessness,
loneliness, connectedness, ...) are assumptions from the broader youth-suicide
literature, set to plausible directions and modest sizes. They are demo
settings, not findings.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ITEMS_PATH = Path(__file__).resolve().parent / "items.json"
OUTCOME_ITEM = "si"
N_RESPONDENTS = 2609     # IWFP analytic sample
SI_PREVALENCE = 0.168    # IWFP Table 1

FACTORS = ["D", "V", "S", "C", "E"]  # distress, victimization, substance, connectedness, adversity
FACTOR_CORR = np.array([
    #  D     V     S     C     E
    [1.00, 0.40, 0.25, -0.35, 0.15],
    [0.40, 1.00, 0.35, -0.25, 0.15],
    [0.25, 0.35, 1.00, -0.20, 0.15],
    [-0.35, -0.25, -0.20, 1.00, -0.15],
    [0.15, 0.15, 0.15, -0.15, 1.00],
])

# Response formats (category probabilities, lowest category first).
LIKERT4 = [0.08, 0.17, 0.45, 0.30]          # strongly disagree .. strongly agree
LIKERT5 = [0.06, 0.12, 0.30, 0.32, 0.20]
DISTRESS_FREQ = [0.25, 0.27, 0.22, 0.15, 0.11]  # never .. almost always

# id -> (format, loadings on latent factors). Format is either
# ("binary", prevalence) or ("ordinal", [category probabilities]).
# Higher values always mean "more of what the label says"
# (e.g. school_safety high = feels safe, breakfast 1 = ate breakfast).
ITEM_SPECS: dict[str, tuple[tuple, dict[str, float]]] = {
    # Demographics (IWFP Table 1 where published)
    "gender": (("binary", 0.506), {}),                      # 1 = female
    "transgender": (("binary", 0.0295), {}),
    "lgb": (("binary", 0.170), {}),
    "race": (("binary", 0.45), {}),                         # 1 = multiple racial identities
    "immigration_background": (("binary", 0.05), {"E": 0.15}),
    "language": (("binary", 0.15), {"E": 0.2}),             # non-English language at home
    "military_family": (("binary", 0.08), {}),
    "homeless": (("binary", 0.0253), {"E": 0.5}),
    "fostercare": (("binary", 0.0034), {"E": 0.5}),
    "economic_disadvantage": (("binary", 0.62), {"E": 0.7}),
    "special_education": (("binary", 0.13), {"E": 0.2, "D": 0.1}),
    "parental_education": (("ordinal", [0.10, 0.25, 0.22, 0.08, 0.20, 0.15]), {"E": -0.7}),
    "breakfast": (("binary", 0.55), {"E": -0.3, "D": -0.15}),
    "remote_learning": (("binary", 0.20), {}),
    # School
    "academic_performance": (("ordinal", [0.04, 0.08, 0.18, 0.25, 0.25, 0.20]),
                             {"C": 0.15, "S": -0.2, "E": -0.25}),
    "attendance": (("ordinal", [0.70, 0.15, 0.08, 0.04, 0.03]), {"S": 0.35, "C": -0.3, "D": 0.15}),
    "academic_engagement": (("ordinal", LIKERT4), {"C": 0.55}),
    "educational_aspirations": (("ordinal", LIKERT4), {"C": 0.45, "E": -0.2}),
    "school_connectedness": (("ordinal", LIKERT5), {"C": 0.75}),
    "teacher_support": (("ordinal", LIKERT4), {"C": 0.6}),
    "school_participation": (("ordinal", LIKERT4), {"C": 0.55}),
    "school_climate": (("ordinal", LIKERT4), {"C": 0.6, "V": -0.2}),
    "school_discipline": (("ordinal", LIKERT4), {"C": 0.35, "V": -0.2}),
    "school_safety": (("ordinal", [0.04, 0.08, 0.38, 0.35, 0.15]), {"V": -0.55, "C": 0.2}),
    "inclusive_school_climate": (("ordinal", LIKERT4), {"C": 0.5}),
    "lgbtq_support": (("ordinal", LIKERT4), {"C": 0.35}),
    "school_facilities": (("ordinal", [0.12, 0.25, 0.43, 0.20]), {"C": 0.25, "E": -0.15}),
    "school_services": (("ordinal", LIKERT4), {"C": 0.35}),
    "afterschool_activities": (("ordinal", [0.35, 0.25, 0.25, 0.15]), {"C": 0.35, "E": -0.15}),
    # Family, peers, community
    "family_support": (("ordinal", LIKERT4), {"C": 0.65, "D": -0.15}),
    "parental_involvement": (("ordinal", LIKERT4), {"C": 0.55}),
    "family_participation": (("ordinal", LIKERT4), {"C": 0.45}),
    "peer_support": (("ordinal", LIKERT4), {"C": 0.55}),
    "positive_peer_influence": (("ordinal", LIKERT4), {"C": 0.5, "S": -0.3}),
    "community_support": (("ordinal", LIKERT4), {"C": 0.6}),
    "community_connectedness": (("ordinal", LIKERT4), {"C": 0.6}),
    "community_participation": (("ordinal", [0.35, 0.30, 0.22, 0.13]), {"C": 0.45}),
    "mental_health_support": (("ordinal", [0.20, 0.30, 0.30, 0.20]), {"C": 0.4}),
    # Safety and violence (victimization)
    "neighborhood_safety": (("ordinal", [0.04, 0.08, 0.38, 0.35, 0.15]), {"V": -0.4, "E": -0.3}),
    "family_safety": (("ordinal", [0.02, 0.04, 0.14, 0.35, 0.45]), {"V": -0.4, "D": -0.15}),
    "police_relations": (("ordinal", [0.15, 0.25, 0.40, 0.20]), {"V": -0.3, "C": 0.2, "E": -0.15}),
    "bullying": (("ordinal", [0.62, 0.18, 0.10, 0.06, 0.04]), {"V": 0.75}),
    "physical_violence": (("ordinal", [0.75, 0.13, 0.06, 0.04, 0.02]), {"V": 0.65}),
    "dating_violence": (("binary", 0.12), {"V": 0.6, "S": 0.2}),
    "sexual_violence": (("binary", 0.10), {"V": 0.7}),
    "weapons": (("ordinal", [0.90, 0.05, 0.03, 0.02]), {"V": 0.5, "S": 0.3}),
    "gang_involvement": (("binary", 0.07), {"V": 0.4, "S": 0.4, "E": 0.2}),
    "adult_risk_exposure": (("ordinal", [0.55, 0.25, 0.12, 0.08]), {"V": 0.35, "S": 0.45, "E": 0.3}),
    "delinquency": (("ordinal", [0.80, 0.10, 0.05, 0.03, 0.02]), {"S": 0.45, "V": 0.35}),
    "gambling": (("ordinal", [0.85, 0.08, 0.04, 0.02, 0.01]), {"S": 0.3}),
    # Distress and wellbeing
    "depressive_symptoms": (("binary", 0.40), {"D": 0.8}),
    "hopeless": (("ordinal", [0.35, 0.25, 0.18, 0.12, 0.10]), {"D": 0.75}),
    "anxiety": (("ordinal", [0.20, 0.25, 0.25, 0.18, 0.12]), {"D": 0.75}),
    "psychological_distress": (("ordinal", DISTRESS_FREQ), {"D": 0.8}),
    "trauma_symptoms": (("ordinal", [0.35, 0.27, 0.18, 0.12, 0.08]), {"D": 0.65, "V": 0.25}),
    "self_harm": (("binary", 0.20), {"D": 0.6, "V": 0.2}),
    "loneliness": (("ordinal", [0.30, 0.27, 0.20, 0.13, 0.10]), {"D": 0.65, "C": -0.25}),
    "life_satisfaction": (("ordinal", LIKERT5), {"C": 0.45, "D": -0.5}),
    "positive_wellbeing": (("ordinal", LIKERT5), {"C": 0.4, "D": -0.55}),
    "optimism": (("ordinal", LIKERT4), {"C": 0.4, "D": -0.5}),
    "gratitude": (("ordinal", LIKERT4), {"C": 0.5, "D": -0.2}),
    "self_efficacy": (("ordinal", LIKERT4), {"C": 0.45, "D": -0.35}),
    "self_awareness": (("ordinal", LIKERT4), {"C": 0.45, "D": -0.2}),
    "emotion_regulation": (("ordinal", LIKERT4), {"C": 0.35, "D": -0.45}),
    "empathy": (("ordinal", LIKERT4), {"C": 0.4}),
    # Physical health
    "sleep": (("ordinal", [0.12, 0.25, 0.33, 0.22, 0.08]), {"D": -0.4}),          # hours, higher = more
    "physical_health": (("ordinal", [0.04, 0.12, 0.32, 0.32, 0.20]), {"D": -0.35}),
    "somatic_symptoms": (("ordinal", [0.30, 0.30, 0.20, 0.12, 0.08]), {"D": 0.5}),
    "asthma": (("binary", 0.18), {}),
    "healthcare_access": (("ordinal", [0.15, 0.30, 0.55]), {"E": -0.4}),
    "dental_care": (("ordinal", [0.20, 0.30, 0.50]), {"E": -0.45}),
    "physical_activity": (("ordinal", [0.15, 0.20, 0.25, 0.22, 0.18]), {"C": 0.2, "D": -0.2}),
    "diet": (("ordinal", [0.10, 0.22, 0.33, 0.25, 0.10]), {"C": 0.15, "E": -0.2}),
    "screen_time": (("ordinal", [0.08, 0.17, 0.25, 0.25, 0.25]), {"D": 0.15, "C": -0.1}),
    "body_image": (("ordinal", [0.30, 0.30, 0.25, 0.15]), {"D": 0.4}),
    # Substance use (lifetime frequency, zero-heavy)
    "tobacco_use": (("ordinal", [0.90, 0.05, 0.03, 0.01, 0.01]), {"S": 0.55}),
    "vaping": (("ordinal", [0.70, 0.12, 0.08, 0.05, 0.05]), {"S": 0.75}),
    "alcohol_use": (("ordinal", [0.65, 0.15, 0.10, 0.06, 0.04]), {"S": 0.75}),
    "cannabis_use": (("ordinal", [0.72, 0.11, 0.07, 0.05, 0.05]), {"S": 0.75}),
    "other_drug_use": (("ordinal", [0.92, 0.04, 0.02, 0.01, 0.01]), {"S": 0.5}),
    "substance_risk_perceptions": (("ordinal", [0.15, 0.25, 0.30, 0.30]), {"S": -0.45}),
    "substance_access": (("ordinal", [0.25, 0.20, 0.25, 0.30]), {"S": 0.55}),
}

# Log-odds effects on SI. Latent-factor terms carry most of the signal so
# correlated items share it the way real survey items do; the direct terms
# give specific items a unique contribution.
#
# Connectedness/support gets an independent protective effect (C, plus direct
# terms per response step for family, community and school connectedness),
# not only one routed through lower distress. Without it, LASSO drops every
# support item whenever distress items are also in the model. Direction follows
# the protective-factor literature for American Indian/Alaska Native youth
# (e.g. family connectedness, Borowsky et al. 1999; community/cultural
# continuity, Chandler & Lalonde 1998); the sizes are demo settings.
SI_LATENT_EFFECTS = {"D": 1.3, "V": 0.6, "S": 0.2, "C": -0.5, "E": 0.05}
SI_DIRECT_EFFECTS = {
    # IWFP-retained items
    "depressive_symptoms": 1.1,
    "lgb": 0.35,
    "transgender": 0.1,
    "breakfast": -0.1,
    # Protective factors IWFP didn't measure (per response step)
    "family_support": -0.2,
    "community_connectedness": -0.2,
    "school_connectedness": -0.15,
}


def load_item_ids() -> list[str]:
    return [i["id"] for i in json.loads(ITEMS_PATH.read_text()) if i["id"] != OUTCOME_ITEM]


def _cut(x: np.ndarray, probs: list[float]) -> np.ndarray:
    """Cut a continuous score into ordered categories with the given marginals."""
    cum = np.cumsum(probs)[:-1]
    return np.searchsorted(np.quantile(x, cum), x, side="right")


def _indicator(factors: dict[str, np.ndarray], loadings: dict[str, float], rng, n) -> np.ndarray:
    signal = sum(w * factors[f] for f, w in loadings.items()) if loadings else np.zeros(n)
    noise_sd = np.sqrt(max(0.15, 1 - sum(w * w for w in loadings.values())))
    return signal + rng.normal(0, noise_sd, n)


# Seed rule: the first seed (scanning from 0) where no item with zero true
# effect (race, military_family, remote_learning, asthma, age, grade) correlates
# with SI at p < 0.3 and SI prevalence is within 0.5 points of 16.8%. A chance
# sample association in synthetic data would otherwise surface as a "finding"
# (seed 4 showed race as a stable risk factor despite having no effect).
DEFAULT_SEED = 19


def generate(n_respondents: int = N_RESPONDENTS, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    item_ids = load_item_ids()
    unspecified = set(item_ids) - set(ITEM_SPECS) - {"age", "grade"}
    if unspecified:
        raise ValueError(f"No synthetic spec for item(s): {sorted(unspecified)}")

    latent = rng.multivariate_normal(np.zeros(len(FACTORS)), FACTOR_CORR, size=n_respondents)
    factors = {f: latent[:, i] for i, f in enumerate(FACTORS)}

    data: dict[str, np.ndarray] = {}
    # Demographics that shift the latent factors come first.
    for item_id in ("gender", "transgender", "lgb"):
        (_, p), _ = ITEM_SPECS[item_id]
        data[item_id] = (rng.random(n_respondents) < p).astype(int)
    # Minority stress and internalizing differences (directions from the
    # literature; sizes are demo settings).
    factors["D"] = factors["D"] + 0.35 * data["lgb"] + 0.40 * data["transgender"] + 0.15 * data["gender"]
    factors["V"] = factors["V"] + 0.30 * data["lgb"] + 0.35 * data["transgender"]

    grade = rng.choice([9, 10, 11, 12], size=n_respondents, p=[0.27, 0.26, 0.24, 0.23])
    data["grade"] = grade
    data["age"] = np.clip(grade + 5 + rng.choice([0, 0, 0, 1, -1], size=n_respondents), 13, 18)

    for item_id in item_ids:
        if item_id in data:
            continue
        (kind, spec), loadings = ITEM_SPECS[item_id]
        x = _indicator(factors, loadings, rng, n_respondents)
        probs = [1 - spec, spec] if kind == "binary" else spec
        data[item_id] = _cut(x, probs)

    df = pd.DataFrame({item_id: data[item_id] for item_id in item_ids})

    lin = sum(w * factors[f] for f, w in SI_LATENT_EFFECTS.items())
    lin = lin + sum(w * df[item] for item, w in SI_DIRECT_EFFECTS.items())
    lin = np.asarray(lin, dtype=float)
    # Choose the intercept so expected prevalence matches IWFP's 16.8%.
    lo, hi = -10.0, 10.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + lin)))).mean() > SI_PREVALENCE:
            hi = mid
        else:
            lo = mid
    p_si = 1 / (1 + np.exp(-(lo + lin)))
    df[OUTCOME_ITEM] = rng.binomial(1, p_si)
    return df


if __name__ == "__main__":
    df = generate()
    out_path = Path(__file__).parent / "synthetic_chks_dataset.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} synthetic respondents x {len(df.columns)} columns to {out_path}")
    print(f"SI prevalence: {df[OUTCOME_ITEM].mean():.1%} (IWFP: 16.8%)")
