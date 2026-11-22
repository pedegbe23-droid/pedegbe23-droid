import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validator import validate_csv, validate_rows


class ValidatorTests(unittest.TestCase):
    def test_valid_row(self):
        self.assertEqual(validate_rows([{
            "customer_id": "1", "email": "a@example.org", "country": "US", "onboarding_date": "2026-01-01"
        }]), [])

    def test_duplicate_missing_and_invalid_fields(self):
        rows = [
            {"customer_id": "1", "email": "a@example.org", "country": "US", "onboarding_date": "2026-01-01"},
            {"customer_id": "1", "email": "bad", "country": "", "onboarding_date": "2026-02-30"},
        ]
        self.assertEqual(len(validate_rows(rows)), 4)

    def test_example_file(self):
        path = Path(__file__).resolve().parents[1] / "data" / "sample_customers.csv"
        result = validate_csv(path)
        self.assertEqual(result["total_records"], 5)
        self.assertEqual(result["total_issues"], 5)


if __name__ == "__main__":
    unittest.main()
