import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "nighthawk_audit", ROOT / "scripts" / "analyze_nighthawk_manual_segments.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class NighthawkManualAuditTests(unittest.TestCase):
    def test_perfect_counts_have_identity_calibration(self):
        headers = ["filename", "Duration", "ManualCalls", "NighthawkCalls"]
        rows = [
            {"filename": "a.wav", "Duration": 900, "ManualCalls": 0, "NighthawkCalls": 0},
            {"filename": "b.wav", "Duration": 900, "ManualCalls": 2, "NighthawkCalls": 2},
            {"filename": "c.wav", "Duration": 900, "ManualCalls": 5, "NighthawkCalls": 5},
            {"filename": "d.wav", "Duration": 900, "ManualCalls": 8, "NighthawkCalls": 8},
        ]
        x = mod.analyze(headers, rows)
        o = x["overall"]
        self.assertAlmostEqual(o["pearson_r"], 1.0)
        self.assertAlmostEqual(o["spearman_rho"], 1.0)
        self.assertAlmostEqual(o["ols_slope_nighthawk_on_manual"], 1.0)
        self.assertAlmostEqual(o["ols_intercept_nighthawk_on_manual"], 0.0)
        self.assertAlmostEqual(o["mae"], 0.0)
        self.assertAlmostEqual(o["recorded_to_manual_total_ratio"], 1.0)

    def test_count_level_output_does_not_claim_event_shadow(self):
        headers = ["ManualCalls", "NighthawkCalls"]
        rows = [
            {"ManualCalls": 10, "NighthawkCalls": 10},
            {"ManualCalls": 0, "NighthawkCalls": 2},
            {"ManualCalls": 4, "NighthawkCalls": 1},
        ]
        x = mod.analyze(headers, rows)
        self.assertIn("cannot identify event-level", x["identification_boundary"])
        self.assertNotIn("q_shadow", x["overall"])
        self.assertEqual(x["manual_zero_segments"]["segments_with_positive_nighthawk_count"], 1)

    def test_missing_manual_count_column_fails_closed(self):
        with self.assertRaises(mod.NighthawkAuditError):
            mod.analyze(
                ["filename", "Duration", "NighthawkCalls"],
                [{"filename": "a", "Duration": 900, "NighthawkCalls": 2}],
            )

    def test_csv_loader_preserves_all_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "validation.csv"
            path.write_text(
                "filename,Duration,ManualCalls,NighthawkCalls\n"
                "a.wav,900,1,2\n"
                "a.wav,900,1,2\n",
                encoding="utf-8",
            )
            headers, rows = mod.load_table(path)
            self.assertEqual(len(rows), 2)
            x = mod.analyze(headers, rows)
            self.assertEqual(x["overall"]["n"], 2)


if __name__ == "__main__":
    unittest.main()
