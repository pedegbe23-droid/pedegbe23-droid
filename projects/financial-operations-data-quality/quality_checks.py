"""Demo data-quality checks for synthetic KYC, insurance claims, and card disputes."""
import argparse
import csv
import json
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

SCHEMAS = {
    "kyc": ["case_id", "customer_type", "risk_rating", "review_date", "next_review_due", "ubo_percent", "pep_flag", "edd_status", "case_status"],
    "claims": ["claim_id", "policy_id", "loss_date", "reported_date", "claimed_amount", "reserve_amount", "status", "decision_date"],
    "disputes": ["dispute_id", "transaction_id", "transaction_date", "dispute_date", "transaction_amount", "disputed_amount", "reason_code", "status", "resolution_date"],
}
STATUS = {
    "kyc": {"open", "pending", "completed"},
    "claims": {"open", "investigating", "closed"},
    "disputes": {"open", "investigating", "resolved"},
}


def check_records(domain, records):
    if domain not in SCHEMAS:
        raise ValueError("Unsupported domain")
    issues = []
    seen = set()
    id_field = SCHEMAS[domain][0]

    def flag(row_no, field, rule, detail, severity="error"):
        issues.append({"row": row_no, "field": field, "rule": rule, "severity": severity, "detail": detail})

    for row_no, original in enumerate(records, start=2):
        row = {k: str(original.get(k) or "").strip() for k in SCHEMAS[domain]}
        record_id = row[id_field]
        if not record_id:
            flag(row_no, id_field, "required", "Case identifier is missing")
        elif record_id in seen:
            flag(row_no, id_field, "duplicate", "Repeated case identifier")
        else:
            seen.add(record_id)

        def required(field):
            if not row[field]:
                flag(row_no, field, "required", "Required field is blank")

        def parsed_date(field, optional=False):
            value = row[field]
            if not value and optional:
                return None
            try:
                return date.fromisoformat(value)
            except ValueError:
                flag(row_no, field, "invalid_date", "Expected a real date in YYYY-MM-DD format")
                return None

        def amount(field):
            try:
                value = Decimal(row[field])
                if not value.is_finite() or value < 0:
                    raise InvalidOperation()
                return value
            except (InvalidOperation, ValueError):
                flag(row_no, field, "invalid_amount", "Expected a nonnegative finite number")
                return None

        if domain == "kyc":
            required("customer_type")
            if row["risk_rating"] not in {"low", "medium", "high"}:
                flag(row_no, "risk_rating", "invalid_category", "Use low, medium, or high")
            review = parsed_date("review_date")
            due = parsed_date("next_review_due")
            if review and due and due < review:
                flag(row_no, "next_review_due", "date_order", "Review due date precedes last review")
            owner = amount("ubo_percent")
            if owner is not None and owner > 100:
                flag(row_no, "ubo_percent", "out_of_range", "Ownership percentage exceeds 100")
            if row["pep_flag"] not in {"yes", "no", "unknown"}:
                flag(row_no, "pep_flag", "invalid_category", "Use yes, no, or unknown")
            if row["edd_status"] not in {"not_required", "pending", "complete"}:
                flag(row_no, "edd_status", "invalid_category", "Unexpected EDD status")
            if row["risk_rating"] == "high" and row["edd_status"] == "not_required":
                flag(row_no, "edd_status", "review_required", "Demo policy: high-risk case requires EDD review")
            if row["case_status"] not in STATUS[domain]:
                flag(row_no, "case_status", "invalid_category", "Unknown case status")
            if row["case_status"] == "completed" and row["edd_status"] == "pending":
                flag(row_no, "edd_status", "status_conflict", "Completed case has pending EDD")
        elif domain == "claims":
            required("policy_id")
            loss = parsed_date("loss_date")
            reported = parsed_date("reported_date")
            if loss and reported and reported < loss:
                flag(row_no, "reported_date", "date_order", "Reported date precedes loss date")
            claimed = amount("claimed_amount")
            reserve = amount("reserve_amount")
            if claimed is not None and reserve is not None and reserve > claimed:
                flag(row_no, "reserve_amount", "review_required", "Reserve exceeds claimed amount; investigate", "warning")
            if row["status"] not in STATUS[domain]:
                flag(row_no, "status", "invalid_category", "Unknown claim status")
            decision = parsed_date("decision_date", optional=True)
            if row["status"] == "closed" and not decision:
                flag(row_no, "decision_date", "required_for_status", "Closed claim needs a valid decision date")
            if decision and reported and decision < reported:
                flag(row_no, "decision_date", "date_order", "Decision precedes reported date")
        else:
            required("transaction_id")
            txn = parsed_date("transaction_date")
            disputed = parsed_date("dispute_date")
            if txn and disputed and disputed < txn:
                flag(row_no, "dispute_date", "date_order", "Dispute predates transaction")
            transaction_amount = amount("transaction_amount")
            disputed_amount = amount("disputed_amount")
            if transaction_amount is not None and disputed_amount is not None and disputed_amount > transaction_amount:
                flag(row_no, "disputed_amount", "amount_exceeds_transaction", "Disputed amount exceeds original transaction; reconcile")
            required("reason_code")
            if row["status"] not in STATUS[domain]:
                flag(row_no, "status", "invalid_category", "Unknown dispute status")
            resolution = parsed_date("resolution_date", optional=True)
            if row["status"] == "resolved" and not resolution:
                flag(row_no, "resolution_date", "required_for_status", "Resolved dispute needs a valid resolution date")
            if resolution and disputed and resolution < disputed:
                flag(row_no, "resolution_date", "date_order", "Resolution predates dispute")
    return issues


def inspect_csv(domain, path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("File is empty or lacks headers")
        missing = sorted(set(SCHEMAS[domain]) - set(reader.fieldnames))
        if missing:
            raise ValueError("Missing columns: " + ", ".join(missing))
        records = list(reader)
    issues = check_records(domain, records)
    return {
        "domain": domain,
        "records_checked": len(records),
        "total_issues": len(issues),
        "issues_by_severity": dict(sorted(Counter(i["severity"] for i in issues).items())),
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description="Synthetic financial operations data-quality checks")
    parser.add_argument("domain", choices=sorted(SCHEMAS))
    parser.add_argument("csv_file")
    parser.add_argument("--output", help="Optional JSON report file")
    args = parser.parse_args()
    report = inspect_csv(args.domain, args.csv_file)
    payload = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
