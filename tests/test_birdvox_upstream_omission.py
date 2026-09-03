import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "birdvox_omission", ROOT / "scripts" / "analyze_birdvox_upstream_omission.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class BirdVoxUpstreamOmissionTests(unittest.TestCase):
    def test_perfect_downstream_semantics_cannot_restore_omitted_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "grid.csv"
            path.write_text(
                "sensor_id,split,window_id,window_start_seconds,window_end_seconds,truth_positive,gate_evaluable,max_score\n"
                "02,heldout,w0,0,1,false,true,3\n"
                "02,heldout,w1,1,2,true,true,1\n"
                "02,heldout,w2,2,3,true,true,3\n"
                "02,heldout,w3,3,4,true,true,1\n",
                encoding="utf-8",
            )
            result = mod.analyze(mod.load_grid(path), [2.0])
            r = result["threshold_results"][0]
            # Truth rises from 0.5 early to 1.0 late: +0.5.
            self.assertAlmostEqual(r["truth_late_minus_early"], 0.5)
            # Raw record falls because the early false entry compensates the missed true event.
            self.assertAlmostEqual(r["raw_recorded_late_minus_early"], -0.5)
            # Perfect downstream semantics removes the false entry but cannot restore omissions.
            self.assertAlmostEqual(
                r["oracle_downstream_true_entry_late_minus_early"], 0.0
            )
            self.assertAlmostEqual(
                r["upstream_omission_absolute_contrast_error"], 0.5
            )
            self.assertAlmostEqual(
                r["truth_contrast_retained_after_perfect_downstream_semantics"], 0.0
            )


if __name__ == "__main__":
    unittest.main()
