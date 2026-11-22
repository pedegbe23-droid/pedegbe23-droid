import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis import make_synthetic_claims, quality_summary, fit_evaluate


class TestClaimsAnalytics(unittest.TestCase):
    def test_reproducible_data(self):
        a = make_synthetic_claims(n=100, seed=10)
        b = make_synthetic_claims(n=100, seed=10)
        self.assertTrue(a.equals(b))
        self.assertEqual(quality_summary(a)["unique_claims"], 100)

    def test_model_evaluation(self):
        metrics = fit_evaluate(make_synthetic_claims(n=700))
        self.assertEqual(metrics["train_rows"], 560)
        self.assertEqual(metrics["test_rows"], 140)
        self.assertTrue(0 <= metrics["roc_auc"] <= 1)


if __name__ == "__main__":
    unittest.main()
