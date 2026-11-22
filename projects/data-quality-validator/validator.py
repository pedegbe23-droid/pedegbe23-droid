"""Validate a synthetic customer CSV using the Python standard library."""
import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

REQUIRED_COLUMNS = ("customer_id", "email", "country", "onboarding_date")


def validate_rows(rows):
    """Return row-level issues; first data row is CSV line 2."""
    issues = []
    seen_ids = set()
    for line_number, row in enumerate(rows, start=2):
        customer_id = (row.get("customer_id") or "").strip()
        email = (row.get("email") or "").strip()
        country = (row.get("country") or "").strip()
        date_text = (row.get("onboarding_date") or "").strip()
        if not customer_id:
            issues.append({"row": line_number, "field": "customer_id", "issue": "missing"})
        elif customer_id in seen_ids:
            issues.append({"row": line_number, "field": "customer_id", "issue": "duplicate"})
        else:
            seen_ids.add(customer_id)
        if not email or email.count("@") != 1 or "." not in email.split("@")[-1]:
            issues.append({"row": line_number, "field": "email", "issue": "invalid_or_missing"})
        if not country:
            issues.append({"row": line_number, "field": "country", "issue": "missing"})
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            issues.append({"row": line_number, "field": "onboarding_date", "issue": "invalid_or_missing"})
    return issues


def validate_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV must have a header row")
        missing = sorted(set(REQUIRED_COLUMNS) - set(reader.fieldnames))
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))
        rows = list(reader)
    issues = validate_rows(rows)
    return {"total_records": len(rows), "total_issues": len(issues),
            "issues_by_type": dict(sorted(Counter(i["issue"] for i in issues).items())),
            "issues": issues}


def main():
    parser = argparse.ArgumentParser(description="Validate synthetic customer CSV records")
    parser.add_argument("csv_path", help="Path to input CSV")
    args = parser.parse_args()
    print(json.dumps(validate_csv(args.csv_path), indent=2))


if __name__ == "__main__":
    main()
