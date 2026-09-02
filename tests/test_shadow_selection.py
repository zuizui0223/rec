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
    def test_example_estimands(self):
        result = mod.analyze(
            ROOT / "examples" / "exposure_ledger.csv",
            ROOT / "examples" / "chapter2_windows.csv",
        )
        est = result["estimands"]
        self.assertAlmostEqual(est["q_B_event_given_registered_baseline"], 0.5)
        self.assertAlmostEqual(est["a_R_registered_baseline_given_event"], 2 / 3)
        self.assertAlmostEqual(est["q_shadow_event_given_no_record_entry"], 0.5)
        self.assertAlmostEqual(est["a_K_no_record_entry_given_event"], 2 / 3)

    def test_truth_window_must_exist_in_ledger(self):
        truth = (ROOT / "examples" / "chapter2_windows.csv").read_text(encoding="utf-8")
        truth = truth.replace("grid-v1,reference_timeline,ref-v1,true,A,S1,C1,2026-09-01,B1,w1,", "grid-v1,reference_timeline,ref-v1,true,A,S1,C1,2026-09-01,B1,missing,", 1)
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
        with tmp:
            tmp.write(truth)
        path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        with self.assertRaisesRegex(mod.AnalysisError, "absent from exposure ledger"):
            mod.analyze(ROOT / "examples" / "exposure_ledger.csv", path)


if __name__ == "__main__":
    unittest.main()
