# Financial Operations Data Quality Lab

**Three domains · One Python rule engine · Synthetic case data · Reproducible exception reports**

A hands-on portfolio example exploring how data quality affects **KYC onboarding**, **insurance claims**, and **payment/card disputes**. Each sample dataset contains both clean and intentionally problematic records. The same CLI applies rule checks and produces JSON exception reports.

> This is a **self-contained demonstration built with fictional records**, not an employer deliverable, production compliance control, or evidence of past open-source maintainer work.

## Domain rulebook

| Domain | Representative rules | Why it matters |
|---|---|---|
| **KYC** | Missing/duplicate case IDs, invalid risk categories, review dates out of sequence, ownership percentage above 100%, high-risk EDD follow-up, completed cases with pending EDD | Supports more consistent onboarding/review queues and flags records requiring human review |
| **Claims** | Missing policy references, loss reported before occurrence, nonnumeric/negative amounts, reserves greater than claimed amount, closed cases missing decision dates | Helps spot intake, financial reconciliation, and lifecycle data exceptions |
| **Disputes** | Missing transaction links, disputes dated before transactions, disputed amount exceeding transaction amount, missing reason codes, resolved cases missing resolution dates | Supports transaction-to-case reconciliation and case status reporting |

## How to run

Python 3.9+; **no external dependencies**.

From this folder:

```bash
python quality_checks.py kyc data/kyc_cases.csv
python quality_checks.py claims data/claims_cases.csv
python quality_checks.py disputes data/dispute_cases.csv --output disputes_report.json
python -m unittest discover -s tests -v
```

A report contains: domain, records checked, total issues, counts by severity, and row-level findings with field, rule, and detail.

Example exception:

```json
{"row": 3, "field": "next_review_due", "rule": "date_order", "severity": "error", "detail": "Review due date precedes last review"}
```

## Quality approach

1. **Completeness:** required identifiers, reference fields, and decision dates.
2. **Uniqueness:** duplicate IDs within the input batch.
3. **Validity:** supported categories, ISO dates, and finite nonnegative amounts.
4. **Consistency:** date sequences, case-status expectations, and linked amounts.
5. **Exception handling:** deterministic, row-level findings that can be triaged by a human reviewer.

## Important boundaries

- **KYC:** The high-risk / EDD check is a *simplified illustrative internal policy rule*, not a statement that one universal regulation requires this exact workflow. An actual policy would vary by jurisdiction, product, and institution.
- **Claims:** A reserve larger than the submitted claim is a **warning for investigation**, not an automatic error or proof of incorrect reserving.
- **Disputes:** An amount larger than the source transaction is an exception to **reconcile**, not proof of an invalid dispute. This project deliberately does **not** assert regulatory dispute filing deadlines or automated case outcomes.
- These checks do not replace case investigation, sanctions screening, claims adjudication, consumer-protection analysis, or human decisions.

## Next improvements

Externalize validation rules into configuration; add event-level lineage, case history, masked PII controls, source-to-target reconciliation, and CI checks. Real-world deployments also require access controls, retention limits, data dictionaries, quality thresholds, and owner-approved exception management.

**Author:** Osa Edegbe · GitHub: [pedegbe23-droid](https://github.com/pedegbe23-droid)
