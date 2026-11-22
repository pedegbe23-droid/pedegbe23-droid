"""Synthetic healthcare claims data science: EDA and denial-risk baseline."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORICAL = ["service_line", "claim_channel", "payer_group"]
NUMERIC = ["billed_amount", "days_to_submit", "prior_auth_present", "documentation_complete"]
FEATURES = CATEGORICAL + NUMERIC


def make_synthetic_claims(n=1600, seed=23):
    """Generate entirely fictional claim-level data with an artificial outcome."""
    rng = np.random.default_rng(seed)
    service = rng.choice(["primary_care", "imaging", "outpatient_surgery", "therapy"], n, p=[.35, .25, .2, .2])
    channel = rng.choice(["electronic", "paper"], n, p=[.9, .1])
    payer = rng.choice(["payer_A", "payer_B", "payer_C"], n)
    amount = np.round(rng.lognormal(6.9, .65, n), 2)
    days = rng.integers(0, 50, n)
    auth = rng.binomial(1, .76, n)
    docs = rng.binomial(1, .87, n)
    log_odds = (-2.4 + 1.0 * (docs == 0) + .72 * (auth == 0)
                + .028 * days + .5 * (channel == "paper")
                + .38 * (service == "outpatient_surgery") + .18 * (payer == "payer_C"))
    denied = rng.binomial(1, 1 / (1 + np.exp(-log_odds)))
    dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
    return pd.DataFrame({
        "claim_id": [f"HC-{i:05d}" for i in range(n)],
        "submission_date": dates, "service_line": service, "claim_channel": channel,
        "payer_group": payer, "billed_amount": amount, "days_to_submit": days,
        "prior_auth_present": auth, "documentation_complete": docs, "denied": denied
    }).sort_values("submission_date").reset_index(drop=True)


def quality_summary(frame):
    return {
        "rows": int(len(frame)), "unique_claims": int(frame.claim_id.nunique()),
        "missing_fields": {k: int(v) for k, v in frame.isna().sum().items()},
        "denial_rate": round(float(frame.denied.mean()), 4)
    }


def fit_evaluate(frame):
    frame = frame.sort_values(["submission_date", "claim_id"]).reset_index(drop=True)
    split = int(len(frame) * .8)
    train, test = frame.iloc[:split], frame.iloc[split:]
    preprocess = ColumnTransformer([
        ("categorical", Pipeline([("fill", SimpleImputer(strategy="most_frequent")),
                                  ("encode", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL),
        ("numeric", Pipeline([("fill", SimpleImputer(strategy="median")),
                              ("scale", StandardScaler())]), NUMERIC)
    ])
    model = Pipeline([("preprocess", preprocess),
                      ("classifier", LogisticRegression(max_iter=1000, random_state=23))])
    model.fit(train[FEATURES], train["denied"])
    p = model.predict_proba(test[FEATURES])[:, 1]
    y = test["denied"]
    return {
        "train_rows": len(train), "test_rows": len(test),
        "train_end": str(train.submission_date.max().date()),
        "test_start": str(test.submission_date.min().date()),
        "baseline_denial_rate": round(float(y.mean()), 4),
        "roc_auc": round(float(roc_auc_score(y, p)), 4),
        "average_precision": round(float(average_precision_score(y, p)), 4),
        "brier_score": round(float(brier_score_loss(y, p)), 4)
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    df = make_synthetic_claims()
    df.to_csv(out / "synthetic_claims.csv", index=False)
    df.groupby("service_line").agg(
        claim_count=("claim_id", "size"), denial_rate=("denied", "mean"),
        median_billed=("billed_amount", "median")
    ).round(4).to_csv(out / "service_line_summary.csv")
    report = {"data_quality": quality_summary(df), "model_evaluation": fit_evaluate(df)}
    (out / "metrics.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
