import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "shadow_selection", ROOT / "scripts" / "analyze_shadow_selection.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class ShadowSelectionTests(unittest.TestCase):
    def test_example_estimands_are_layer_specific(self):
        result = mod.analyze(
            ROOT / "examples" / "exposure_ledger.csv",
            ROOT / "examples" / "chapter2_windows.csv",
        )
        est = result["estimands"]
        self.assertAlmostEqual(
            est["q_acquisition_shadow_event_given_primary_unavailable"], 1.0
        )
        self.assertAlmostEqual(est["a_A_primary_unavailable_given_event"], 0.25)
        self.assertAlmostEqual(
            est["q_gate_unevaluable_event_given_gate_unevaluable"], 0.5
        )
        self.assertAlmostEqual(est["a_gate_unevaluable_given_event"], 0.25)
        self.assertAlmostEqual(
            est["q_B_event_given_registered_baseline_gate_evaluable"], 1.0
        )
        self.assertAlmostEqual(
            est["a_R_registered_baseline_given_event_gate_evaluable"], 2 / 3
        )
        self.assertAlmostEqual(est["q_shadow_event_given_no_record_entry"], 0.75)
        self.assertAlmostEqual(est["a_K_no_record_entry_given_event"], 0.75)

    def test_truth_window_must_exist_in_ledger(self):
        source = ROOT / "examples" / "chapter2_windows.csv"
        with source.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
            fields = list(rows[0].keys())
        rows[0]["window_id"] = "missing"
        tmp = tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        with self.assertRaisesRegex(mod.AnalysisError, "absent from exposure ledger"):
            mod.analyze(ROOT / "examples" / "exposure_ledger.csv", path)

    def test_gate_evaluability_must_match_ledger(self):
        source = ROOT / "examples" / "chapter2_windows.csv"
        with source.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
            fields = list(rows[0].keys())
        rows[0]["gate_evaluable"] = "false"
        rows[0]["registered_deviation"] = ""
        tmp = tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        with self.assertRaisesRegex(mod.AnalysisError, "gate_evaluable disagrees"):
            mod.analyze(ROOT / "examples" / "exposure_ledger.csv", path)


if __name__ == "__main__":
    unittest.main()
