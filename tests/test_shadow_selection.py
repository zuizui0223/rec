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

        # Gate unevaluability is counted only after primary acquisition exists;
        # acquisition failure is not double-counted as a gate failure.
        self.assertAlmostEqual(
            est["q_gate_unevaluable_event_given_gate_unevaluable"], 0.0
        )
        self.assertAlmostEqual(est["a_gate_unevaluable_given_event"], 0.0)

        self.assertAlmostEqual(
            est["q_B_event_given_registered_baseline_gate_evaluable"], 1.0
        )
        self.assertAlmostEqual(
            est["a_R_registered_baseline_given_event_gate_evaluable"], 2 / 3
        )
        self.assertAlmostEqual(est["q_shadow_event_given_no_record_entry"], 0.75)
        self.assertAlmostEqual(est["a_K_no_record_entry_given_event"], 0.75)

    def test_reference_unresolved_mass_is_bounded_not_dropped(self):
        source = ROOT / "examples" / "chapter2_windows.csv"
        with source.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
            fields = list(rows[0].keys())

        for row in rows:
            if row["window_id"] == "w4":
                row["target_truth"] = "unresolved"
                break

        tmp = tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))

        result = mod.analyze(ROOT / "examples" / "exposure_ledger.csv", path)
        pi = result["partial_identification"]

        q_shadow = pi["q_event_given_no_record_entry_K0"]
        self.assertAlmostEqual(q_shadow["lower"], 0.75)
        self.assertAlmostEqual(q_shadow["upper"], 1.0)
        self.assertAlmostEqual(q_shadow["reference_unresolved_fraction"], 0.25)

        a_shadow = pi["a_no_record_entry_given_event"]
        self.assertAlmostEqual(a_shadow["lower"], 0.75)
        self.assertAlmostEqual(a_shadow["upper"], 0.8)

        q_gate_unresolved = pi["q_event_given_gate_unevaluable_after_acquisition_G0"]
        self.assertIsNone(q_gate_unresolved["resolved_only_estimate"])
        self.assertAlmostEqual(q_gate_unresolved["lower"], 0.0)
        self.assertAlmostEqual(q_gate_unresolved["upper"], 1.0)

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
