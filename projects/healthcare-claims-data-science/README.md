# Healthcare Claims Data Science | Synthetic Denial-Risk Baseline

**Python · pandas · scikit-learn · healthcare claims · data quality · predictive modeling**

This reproducible educational project explores whether administrative attributes available **at claim submission** can support **early documentation review**. It includes synthetic data generation, profiling, exploratory analysis, and a logistic-regression classification baseline.

**All records are entirely fictional. There is no real patient data, protected health information (PHI), payer information, or prior employer material.**

## Business question
How might a claims operations team prioritize administrative data-quality review, while retaining human ownership of claim decisions?

## Reproducible workflow
1. Generate 1,600 synthetic claims with service lines, submission channels, fictional payer groups, billed amounts, filing delays, prior-auth and documentation flags.
2. Profile unique IDs, missing values, and simulated denial prevalence.
3. Produce service-line summaries for volume, simulated denial rates, and median billed amount.
4. Train a logistic-regression baseline with an **80/20 time-ordered holdout** (preprocessing fitted on training records only).
5. Evaluate **ROC AUC, average precision, Brier score**, and outcome base rate.

### Local reproducibility
Python 3.9+:

```bash
python -m pip install -r requirements.txt
python analysis.py --output-dir outputs
python -m unittest discover -s tests -v
```

The script writes `outputs/synthetic_claims.csv`, `outputs/service_line_summary.csv`, and `outputs/metrics.json`.

## Results from the synthetic test run
| Measure | Result |
|---|---:|
| Synthetic records | 1,600 |
| Training / holdout | 1,280 / 320 |
| Holdout simulated denial rate | 29.38% |
| ROC AUC | 0.6873 |
| Average precision | 0.4748 |
| Brier score | 0.1927 |

These numbers describe **only this invented dataset**, not expected performance in real healthcare operations.

## Governance and limitations
The artificial outcome-generation process deliberately embeds associations; these are **not real-world causal effects**. There are no clinical judgments or real adjudication outcomes. A production system would require outcome definitions, healthcare privacy/security safeguards, careful subgroup fairness checks, external/prospective validation, drift monitoring, and accountable human review. **Never use this educational model to deny claims or make care decisions.** No post-adjudication data is used as an input feature.
