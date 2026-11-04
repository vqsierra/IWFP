"""Live feature-selection step: LASSO logistic regression on the audience's
top-voted items, mirroring IWFP's actual methodology (a LASSO logistic
regression identifying predictors of past-year suicidal ideation from CHKS
data), reimplemented in Python/scikit-learn instead of Stata so it runs in
seconds in front of an audience. Runs on the synthetic dataset from
synthetic_data.py, never on real CHKS data (see that module's docstring).

The penalty is chosen with the one-standard-error rule (glmnet's lambda.1se;
lassopack's cvlasso reports it as `lse`): the strongest penalty whose
cross-validated AUC is within one SE of the best. Tuning purely for best AUC
lets weak noise features survive with small, arbitrary-direction effects --
which on a projector reads as a finding.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

OUTCOME_COLUMN = "si"
C_GRID = np.logspace(-3, 1, 30)  # small C = strong penalty
NEGLIGIBLE_LOG_OR = 0.02  # |ln OR| below this (OR within ~0.98-1.02) is reported as negligible
N_BOOTSTRAP = 100
STABLE_SHARE = 0.7  # kept in at least 70% of bootstrap resamples to count as a finding


def _l1_model(C: float) -> LogisticRegression:
    return LogisticRegression(C=C, l1_ratio=1.0, solver="liblinear", max_iter=2000)


def _fit(model: LogisticRegression, X, y) -> LogisticRegression:
    # scikit-learn 1.9 is mid-transition on its penalty API and warns about
    # it; harmless with pinned versions (requirements.txt), but the warnings
    # would flood the projector screen during the live run.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        warnings.simplefilter("ignore", UserWarning)
        return model.fit(X, y)


def _choose_C_1se(X: np.ndarray, y: np.ndarray, seed: int = 0) -> float:
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    scores = np.zeros((len(C_GRID), folds.get_n_splits()))
    for j, (train, test) in enumerate(folds.split(X, y)):
        scaler = StandardScaler().fit(X[train])
        X_train, X_test = scaler.transform(X[train]), scaler.transform(X[test])
        for i, C in enumerate(C_GRID):
            model = _fit(_l1_model(C), X_train, y[train])
            scores[i, j] = roc_auc_score(y[test], model.decision_function(X_test))
    mean = scores.mean(axis=1)
    se = scores.std(axis=1, ddof=1) / np.sqrt(scores.shape[1])
    best = int(np.argmax(mean))
    within_1se = np.where(mean >= mean[best] - se[best])[0]
    return float(C_GRID[within_1se.min()])


def run_lasso(df: pd.DataFrame, candidate_features: list[str], outcome: str = OUTCOME_COLUMN) -> dict:
    """Fit an L1-penalized logistic regression on `candidate_features`.

    Returns a dict with the odds ratio per feature (1.0 for features LASSO
    zeroed out, i.e. not selected), the features that survived selection,
    and a nested cross-validated AUC (penalty re-chosen inside each outer
    fold, so the reported AUC isn't flattered by the tuning step).
    """
    missing = [f for f in candidate_features if f not in df.columns]
    if missing:
        raise ValueError(f"Unknown feature id(s), not in the dataset: {missing}")

    X = df[candidate_features].to_numpy(dtype=float)
    y = df[outcome].to_numpy()

    outer = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
    outer_auc = []
    for train, test in outer.split(X, y):
        C = _choose_C_1se(X[train], y[train])
        scaler = StandardScaler().fit(X[train])
        model = _fit(_l1_model(C), scaler.transform(X[train]), y[train])
        outer_auc.append(roc_auc_score(y[test], model.decision_function(scaler.transform(X[test]))))

    C_final = _choose_C_1se(X, y)
    final = _fit(_l1_model(C_final), StandardScaler().fit_transform(X), y)
    coefs = final.coef_[0]

    # Per one standard deviation of each item, since inputs are standardized.
    odds_ratios = {f: round(float(np.exp(c)), 3) for f, c in zip(candidate_features, coefs)}
    selected = [f for f, c in zip(candidate_features, coefs) if abs(c) > 1e-6]

    # Stability check: refit at the chosen penalty on bootstrap resamples and
    # count how often each item is kept. One fit can keep a chance association
    # (in testing, "race" with no true effect); those rarely survive most resamples.
    rng = np.random.default_rng(2)
    kept_counts = np.zeros(len(candidate_features))
    for _ in range(N_BOOTSTRAP):
        idx = rng.integers(0, len(y), len(y))
        boot = _fit(_l1_model(C_final), StandardScaler().fit_transform(X[idx]), y[idx])
        kept_counts += np.abs(boot.coef_[0]) > 1e-6
    stability = {f: float(k / N_BOOTSTRAP) for f, k in zip(candidate_features, kept_counts)}

    return {
        "candidate_features": candidate_features,
        "odds_ratios": odds_ratios,
        "selected_features": selected,
        "stability": stability,
        "cv_auc_mean": round(float(np.mean(outer_auc)), 3),
        "cv_auc_std": round(float(np.std(outer_auc)), 3),
    }


def format_report(result: dict, labels: dict[str, str] | None = None) -> str:
    labels = labels or {}

    def label(feature_id: str) -> str:
        return labels.get(feature_id, feature_id)

    def finding(f: str) -> bool:
        """Kept, not negligible in size, and kept in most bootstrap resamples."""
        return (
            f in result["selected_features"]
            and abs(np.log(result["odds_ratios"][f])) >= NEGLIGIBLE_LOG_OR
            and result["stability"][f] >= STABLE_SHARE
        )

    lines = [f"Candidate features (audience's top {len(result['candidate_features'])}):"]
    for f in result["candidate_features"]:
        kept_pct = f"kept {result['stability'][f]:4.0%}"
        if finding(f):
            odds = result["odds_ratios"][f]
            direction = "higher risk" if odds > 1 else "protective"
            lines.append(f"  - {label(f):45s} odds ratio={odds:5.2f}  {kept_pct}  [{direction}]")
        elif f in result["selected_features"]:
            odds = result["odds_ratios"][f]
            lines.append(f"  - {label(f):45s} odds ratio={odds:5.2f}  {kept_pct}  [weak or unstable]")
        else:
            lines.append(f"  - {label(f):45s} {'':15s}  {kept_pct}  [dropped]")
    lines.append("")
    lines.append("'kept' = share of 100 bootstrap resamples in which LASSO kept the item.")
    lines.append(
        f"Cross-validated AUC: {result['cv_auc_mean']:.3f} (+/- {result['cv_auc_std']:.3f})"
    )

    findings = [f for f in result["candidate_features"] if finding(f)]
    by_strength = sorted(findings, key=lambda f: -abs(np.log(result["odds_ratios"][f])))
    risk = [label(f) for f in by_strength if result["odds_ratios"][f] > 1]
    protective = [label(f) for f in by_strength if result["odds_ratios"][f] < 1]
    lines.append("")
    lines.append(f"In plain terms (strongest first; {len(findings)} of {len(result['candidate_features'])} voted items hold up):")
    lines.append(f"  Risk factors:       {', '.join(risk) or 'none'}")
    lines.append(f"  Protective factors: {', '.join(protective) or 'none'}")
    lines.append(f"  The other {len(result['candidate_features']) - len(findings)} added little or nothing "
                 "beyond these, or didn't hold up across resamples.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Additions for the notebook: figures and validation steps that mirror
# primary_analysis.do (lasso cvplot, calibrationbelt, cvauroc, brier).
# ---------------------------------------------------------------------------

def classify(result: dict, feature: str) -> str:
    """The same four labels format_report prints."""
    if feature not in result["selected_features"]:
        return "dropped"
    odds = result["odds_ratios"][feature]
    if abs(np.log(odds)) >= NEGLIGIBLE_LOG_OR and result["stability"][feature] >= STABLE_SHARE:
        return "higher risk" if odds > 1 else "protective"
    return "weak or unstable"


def cv_curve(df: pd.DataFrame, features: list[str], outcome: str = OUTCOME_COLUMN, seed: int = 0) -> dict:
    """Cross-validated AUC at each penalty, plus the best and one-SE choices."""
    X = df[features].to_numpy(dtype=float)
    y = df[outcome].to_numpy()
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    scores = np.zeros((len(C_GRID), folds.get_n_splits()))
    for j, (train, test) in enumerate(folds.split(X, y)):
        scaler = StandardScaler().fit(X[train])
        X_train, X_test = scaler.transform(X[train]), scaler.transform(X[test])
        for i, C in enumerate(C_GRID):
            model = _fit(_l1_model(C), X_train, y[train])
            scores[i, j] = roc_auc_score(y[test], model.decision_function(X_test))
    mean = scores.mean(axis=1)
    se = scores.std(axis=1, ddof=1) / np.sqrt(scores.shape[1])
    best = int(np.argmax(mean))
    chosen = int(np.where(mean >= mean[best] - se[best])[0].min())
    return {"C": C_GRID, "mean": mean, "se": se, "best": best, "chosen": chosen}


def coefficient_path(df: pd.DataFrame, features: list[str], outcome: str = OUTCOME_COLUMN) -> pd.DataFrame:
    """Standardized coefficient of each feature at each penalty (rows follow C_GRID)."""
    X = StandardScaler().fit_transform(df[features].to_numpy(dtype=float))
    y = df[outcome].to_numpy()
    return pd.DataFrame([_fit(_l1_model(C), X, y).coef_[0] for C in C_GRID], columns=features, index=C_GRID)


def out_of_fold_risk(df: pd.DataFrame, features: list[str], outcome: str = OUTCOME_COLUMN,
                     n_splits: int = 10, seed: int = 1533) -> np.ndarray:
    """Predicted risk for each respondent from a model that never saw them.

    10 folds and seed 1533 follow primary_analysis.do. The penalty is re-chosen
    inside each fold, so these predictions aren't flattered by tuning.
    """
    X = df[features].to_numpy(dtype=float)
    y = df[outcome].to_numpy()
    risk = np.zeros(len(y))
    for train, test in StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed).split(X, y):
        C = _choose_C_1se(X[train], y[train])
        scaler = StandardScaler().fit(X[train])
        model = _fit(_l1_model(C), scaler.transform(X[train]), y[train])
        risk[test] = model.predict_proba(scaler.transform(X[test]))[:, 1]
    return risk


def performance(y: np.ndarray, risk: np.ndarray, n_boot: int = 500, seed: int = 1533) -> dict:
    """AUC with a percentile bootstrap 95% CI, Brier score, and the risk-score spread."""
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(y), len(y))
        if y[idx].min() != y[idx].max():
            boots.append(roc_auc_score(y[idx], risk[idx]))
    q1, median, q3 = np.percentile(risk, [25, 50, 75])
    return {
        "auc": float(roc_auc_score(y, risk)),
        "auc_low": float(np.percentile(boots, 2.5)),
        "auc_high": float(np.percentile(boots, 97.5)),
        "brier": float(np.mean((risk - y) ** 2)),
        "risk_min": float(risk.min()), "risk_max": float(risk.max()),
        "risk_median": float(median), "risk_q1": float(q1), "risk_q3": float(q3),
    }


def calibration_table(y: np.ndarray, risk: np.ndarray, bins: int = 10) -> pd.DataFrame:
    """Observed vs. predicted risk in equal-sized groups, with Wilson 95% intervals."""
    table = pd.DataFrame({"y": y, "risk": risk})
    table["group"] = pd.qcut(table["risk"], bins, labels=False, duplicates="drop")
    out = table.groupby("group").agg(n=("y", "size"), predicted=("risk", "mean"), observed=("y", "mean"))
    z = 1.96
    centre = (out["observed"] + z**2 / (2 * out["n"])) / (1 + z**2 / out["n"])
    half = z * np.sqrt(out["observed"] * (1 - out["observed"]) / out["n"] + z**2 / (4 * out["n"]**2)) / (1 + z**2 / out["n"])
    out["low"], out["high"] = centre - half, centre + half
    return out


def calibration_slope(y: np.ndarray, risk: np.ndarray) -> dict:
    """Logistic recalibration: slope 1 and intercept 0 mean perfectly calibrated."""
    clipped = np.clip(risk, 1e-6, 1 - 1e-6)
    logit = np.log(clipped / (1 - clipped)).reshape(-1, 1)
    model = _fit(LogisticRegression(C=1e6, solver="lbfgs", max_iter=2000), logit, y)
    return {"slope": float(model.coef_[0][0]), "intercept": float(model.intercept_[0])}


def per_100_people(y: np.ndarray, risk: np.ndarray, false_alarm: float = 0.2) -> dict:
    """Outcomes per 100 people at the cutoff that flags this share of people without the outcome."""
    cutoff = float(np.quantile(risk[y == 0], 1 - false_alarm))
    flagged = risk > cutoff
    return {
        "cutoff": cutoff,
        "flagged_with": float((flagged & (y == 1)).mean() * 100),
        "missed_with": float((~flagged & (y == 1)).mean() * 100),
        "flagged_without": float((flagged & (y == 0)).mean() * 100),
        "clear_without": float((~flagged & (y == 0)).mean() * 100),
    }
