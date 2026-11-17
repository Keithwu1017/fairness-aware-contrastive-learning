import unittest

from metrics import load_demo, render, summarize, validate


class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.frame = load_demo()

    def test_known_gaps(self):
        summary = summarize(self.frame[self.frame.scenario == self.frame.scenario.iloc[0]])
        self.assertAlmostEqual(summary.iloc[0, 2], .22)
        self.assertAlmostEqual(summary.iloc[1, 2], .02)
        self.assertAlmostEqual(summary.iloc[0, 3], .14)
        self.assertAlmostEqual(summary.iloc[1, 3], .015)

    def test_rejects_invalid_inputs(self):
        for column, value in [("tpr", 1.1), ("n", 1.5), ("auroc", float("nan")),
                              ("tnr", float("inf")), ("group", ""), ("model", "Other")]:
            with self.subTest(column=column, value=value):
                bad = self.frame.astype({"n": "float64"}).copy()
                bad.loc[0, column] = value
                with self.assertRaises(ValueError):
                    validate(bad)

    def test_rejects_unmatched_cohorts(self):
        with self.assertRaises(ValueError):
            validate(self.frame.iloc[1:])
        bad = self.frame.copy()
        bad.loc[0, "n"] = 199
        with self.assertRaises(ValueError):
            validate(bad)

    def test_rejects_duplicate_and_missing_fields(self):
        import pandas as pd
        with self.assertRaises(ValueError):
            validate(pd.concat([self.frame, self.frame.iloc[:1]]))
        with self.assertRaises(ValueError):
            validate(self.frame.drop(columns="tpr"))

    def test_all_scenarios_and_metrics_render(self):
        for scenario in self.frame.scenario.unique():
            for metric in ["AUROC", "Recall / TPR", "Specificity / TNR"]:
                fig, gaps, summary, table, note = render(self.frame, scenario, metric, "合成示範數據")
                self.assertEqual(len(fig.data), 2)
                self.assertEqual(len(gaps.data), 2)
                self.assertEqual(len(table), 4)
                self.assertIn("合成示範數據", note)


if __name__ == "__main__":
    unittest.main()
