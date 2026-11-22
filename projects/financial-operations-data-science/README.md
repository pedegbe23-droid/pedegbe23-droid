# Data Science for KYC, Claims & Disputes Case Queues

**Python · pandas · Isolation Forest · operations analytics · synthetic data**

This runnable data science example explores **queue prioritization**, not customer risk scoring. It generates 900 fictional case records across KYC, insurance claims, and payment disputes. Shared operational features include queue age, documentation count, missing fields, rework count, and reference amount.

## Questions
- What does the backlog look like across these three domains?
- Which cases have unusual operational profiles that warrant a manual data-quality review?
- How can an exception-scoring pipeline improve triage transparency?

## Method
1. Generate a deterministic, entirely fictional dataset with some injected process outliers.
2. Fit an unsupervised **Isolation Forest** with standardized numeric features.
3. Sort a queue by anomaly score; flag the top approximately 5% for **manual investigation**.
4. Summarize review candidates by domain.

## Run
Python 3.9+:

```bash
python -m pip install -r requirements.txt
python anomaly_review.py --output-dir outputs
python -m unittest discover -s tests -v
```

Outputs: `outputs/synthetic_queue_scored.csv` and `outputs/queue_summary.json`.

### Sample synthetic run
- 900 records processed
- 45 cases flagged for review
- Claims: 13 · Disputes: 18 · KYC: 14

## Responsible interpretation
**Outliers are not fraud, sanctions hits, wrongdoing, or proof of incorrect claim/dispute handling.** There are no fraud labels, and the model is not a compliance or claims decision engine. The 5% setting is an illustrative assumption, not a recommended policy. Real deployments need domain-specific baselines, access controls, quality owners, documented thresholds, false-positive monitoring, and human case review.
