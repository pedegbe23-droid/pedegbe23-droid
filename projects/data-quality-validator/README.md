# Python Data Quality Validator

A small, runnable Python project that checks a **synthetic** customer dataset for basic data-quality issues. Built as a learning/demo example; it is not a production KYC or compliance decision system.

## Checks
- Missing customer IDs and countries
- Duplicate customer IDs
- Missing or malformed email addresses (simple format check, not full email validation)
- Invalid or missing onboarding dates (`YYYY-MM-DD`)

## Run
Requires Python 3.9+; no third-party packages.

```bash
python validator.py data/sample_customers.csv
python -m unittest discover -s tests -v
```

The command prints a JSON summary with record counts and row-level issues. The provided sample has **5 records and 5 issues**.

## Possible improvements
Configurable validation rules, structured logging, automated CI, and richer error handling. The example uses fictional sample data only.
