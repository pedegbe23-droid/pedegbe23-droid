"""Synthetic KYC, claims, and disputes queue analytics and anomaly review."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DOMAINS = ("kyc", "claims", "disputes")


def make_cases(n=900, seed=41):
    rng = np.random.default_rng(seed)
    domain = rng.choice(DOMAINS, n)
    age_days = rng.gamma(shape=2, scale=9, size=n).round().astype(int)
    missing_fields = rng.poisson(.3, n)
    document_count = rng.poisson(5, n)
    rework_count = rng.poisson(.5, n)
    amount = np.round(rng.lognormal(7, 1.0, n), 2)
    outliers = rng.choice(n, size=max(6, n // 25), replace=False)
    age_days[outliers] += 95
    missing_fields[outliers] += 4
    rework_count[outliers] += 5
    return pd.DataFrame({
        "case_id": [f"OPS-{i:05d}" for i in range(n)],
        "domain": domain, "queue_age_days": age_days,
        "missing_fields": missing_fields, "document_count": document_count,
        "rework_count": rework_count, "reference_amount": amount
    })


def score_cases(frame, contamination=.05):
    cols = ["queue_age_days", "missing_fields", "document_count", "rework_count", "reference_amount"]
    model = Pipeline([
        ("scale", StandardScaler()),
        ("detector", IsolationForest(n_estimators=150, contamination=contamination, random_state=41))
    ])
    output = frame.copy()
    output["anomaly_score"] = -model.fit(output[cols]).score_samples(output[cols])
    output["review_candidate"] = model.predict(output[cols]) == -1
    return output.sort_values("anomaly_score", ascending=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(exist_ok=True, parents=True)
    scored = score_cases(make_cases())
    scored.to_csv(out / "synthetic_queue_scored.csv", index=False)
    summary = {
        "total_cases": len(scored),
        "candidates_for_manual_review": int(scored.review_candidate.sum()),
        "candidates_by_domain": {k: int(v) for k, v in scored.groupby("domain").review_candidate.sum().items()},
        "limitations": "Anomaly flags are not evidence of fraud, noncompliance, claim invalidity, or wrongdoing."
    }
    (out / "queue_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
