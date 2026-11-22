import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from anomaly_review import make_cases, score_cases


class TestQueueModel(unittest.TestCase):
    def test_ids_are_unique(self):
        df = make_cases(100)
        self.assertEqual(df.case_id.nunique(), 100)
        self.assertTrue(set(df.domain).issubset({"kyc", "claims", "disputes"}))

    def test_scoring(self):
        df = score_cases(make_cases(200))
        self.assertEqual(len(df), 200)
        self.assertGreater(df.review_candidate.sum(), 0)
        self.assertTrue(df.anomaly_score.is_monotonic_decreasing)


if __name__ == "__main__":
    unittest.main()
