import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_checks import check_records, inspect_csv


class QualityChecksTests(unittest.TestCase):
    def test_kyc_flags_high_risk_without_edd(self):
        row = dict(case_id="K1", customer_type="corporate", risk_rating="high",
                   review_date="2026-01-01", next_review_due="2027-01-01",
                   ubo_percent="25", pep_flag="no", edd_status="not_required", case_status="open")
        self.assertIn("review_required", [x["rule"] for x in check_records("kyc", [row])])

    def test_claims_date_order(self):
        row = dict(claim_id="C1", policy_id="P1", loss_date="2026-04-02",
                   reported_date="2026-04-01", claimed_amount="200", reserve_amount="100",
                   status="open", decision_date="")
        self.assertIn("date_order", [x["rule"] for x in check_records("claims", [row])])

    def test_disputes_amount_reconciliation(self):
        row = dict(dispute_id="D1", transaction_id="T1", transaction_date="2026-04-01",
                   dispute_date="2026-04-02", transaction_amount="100", disputed_amount="120",
                   reason_code="unauthorized", status="open", resolution_date="")
        self.assertIn("amount_exceeds_transaction", [x["rule"] for x in check_records("disputes", [row])])

    def test_valid_claims_record(self):
        row = dict(claim_id="C2", policy_id="P2", loss_date="2026-04-01",
                   reported_date="2026-04-03", claimed_amount="250", reserve_amount="200",
                   status="closed", decision_date="2026-04-10")
        self.assertEqual(check_records("claims", [row]), [])

    def test_missing_columns_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            path.write_text("claim_id\nC1\n")
            with self.assertRaisesRegex(ValueError, "Missing columns"):
                inspect_csv("claims", path)


if __name__ == "__main__":
    unittest.main()
