import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "unresolved_bounds", ROOT / "scripts" / "analyze_unresolved_bounds.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class UnresolvedBoundsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = mod.analyze(ROOT / "examples" / "chapter2_windows.csv")
        cls.layers = cls.result["layers"]

    def test_overall_unresolved_fraction_is_exercised(self):
        self.assertAlmostEqual(self.result["overall_reference_unresolved_fraction"], 0.4)

    def test_acquisition_shadow_bounds(self):
        layer = self.layers["acquisition_shadow"]
        q = layer["contamination"]
        a = layer["event_loss"]
        self.assertAlmostEqual(q["resolved_only_estimate"], 1.0)
        self.assertAlmostEqual(q["lower"], 0.5)
        self.assertAlmostEqual(q["upper"], 1.0)
        self.assertAlmostEqual(a["resolved_only_estimate"], 0.25)
        self.assertAlmostEqual(a["lower"], 1 / 7)
        self.assertAlmostEqual(a["upper"], 0.4)

    def test_gate_unevaluable_bounds(self):
        layer = self.layers["gate_unevaluable_shadow"]
        q = layer["contamination"]
        a = layer["event_loss"]
        self.assertAlmostEqual(q["resolved_only_estimate"], 0.0)
        self.assertAlmostEqual(q["lower"], 0.0)
        self.assertAlmostEqual(q["upper"], 0.5)
        self.assertAlmostEqual(a["lower"], 0.0)
        self.assertAlmostEqual(a["upper"], 0.2)

    def test_gate_baseline_bounds_condition_on_evaluable_gate(self):
        layer = self.layers["gate_baseline_shadow"]
        q = layer["contamination"]
        a = layer["event_loss"]
        self.assertEqual(layer["weighted_H_truth"]["positive"], 2.0)
        self.assertEqual(layer["weighted_H_truth"]["negative"], 1.0)
        self.assertEqual(layer["weighted_H_truth"]["unresolved"], 1.0)
        self.assertAlmostEqual(q["resolved_only_estimate"], 2 / 3)
        self.assertAlmostEqual(q["lower"], 0.5)
        self.assertAlmostEqual(q["upper"], 0.75)
        self.assertAlmostEqual(q["width"], 0.25)
        self.assertAlmostEqual(a["resolved_only_estimate"], 2 / 3)
        self.assertAlmostEqual(a["lower"], 0.5)
        self.assertAlmostEqual(a["upper"], 0.75)

    def test_record_nonentry_bounds(self):
        layer = self.layers["record_nonentry_shadow"]
        q = layer["contamination"]
        a = layer["event_loss"]
        self.assertAlmostEqual(q["resolved_only_estimate"], 0.6)
        self.assertAlmostEqual(q["lower"], 0.375)
        self.assertAlmostEqual(q["upper"], 0.75)
        self.assertAlmostEqual(a["resolved_only_estimate"], 0.75)
        self.assertAlmostEqual(a["lower"], 0.6)
        self.assertAlmostEqual(a["upper"], 6 / 7)

    def test_bounds_are_not_labeled_confidence_intervals(self):
        text = self.result["interpretation_boundary"].lower()
        self.assertIn("not confidence intervals", text)
        self.assertIn("sampling variance", text)


if __name__ == "__main__":
    unittest.main()
