import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "findlay_h5", ROOT / "scripts" / "analyze_findlay_h5_correction.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class FindlayH5CorrectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "TRIGGER_OTTER_WET.DRY.csv"
        rows = ["CT.POS,CAMERA.ID,ORIENT,GAIT,DIST,wet.dry,LOIT,TRIGGER"]
        for camera in ["A", "BS", "BV"]:
            # True composition is 50:50 in each camera. Wet passes trigger 1/4,
            # dry passes 3/4, so raw trigger-world wet composition is 1/4.
            wet = [1, 0, 0, 0]
            dry = [1, 1, 1, 0]
            for i, trig in enumerate(wet):
                rows.append(f"P{i},{camera},L,W,1,wet,0,{trig}")
            for i, trig in enumerate(dry):
                rows.append(f"Q{i},{camera},L,W,1,dry,0,{trig}")
        self.path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_leave_one_camera_out_ipw_recovers_composition(self):
        result = mod.analyze(mod._read(self.path))
        self.assertTrue(result["REC_H5_recoverability"]["supported_retrospectively"])
        self.assertEqual(result["aggregate"]["cameras_improved"], 3)
        self.assertAlmostEqual(
            result["aggregate"]["mean_absolute_error_raw_trigger_world"], 0.25
        )
        self.assertAlmostEqual(result["aggregate"]["mean_absolute_error_cross_camera_ipw"], 0.0)
        for x in result["leave_one_camera_out"]:
            self.assertAlmostEqual(x["truth_wet_pass_proportion"], 0.5)
            self.assertAlmostEqual(x["raw_trigger_world_wet_proportion"], 0.25)
            self.assertAlmostEqual(x["cross_camera_ipw_wet_proportion"], 0.5)

    def test_unresolved_trigger_is_not_recoded_as_zero(self):
        text = self.path.read_text(encoding="utf-8")
        text = text.replace("P0,A,L,W,1,wet,0,1", "P0,A,L,W,1,wet,0,NA")
        self.path.write_text(text, encoding="utf-8")
        result = mod.analyze(mod._read(self.path))
        heldout_bs = next(
            x for x in result["leave_one_camera_out"] if x["heldout_camera"] == "BS"
        )
        wet = heldout_bs["training_trigger_propensities"]["wet"]
        self.assertGreater(wet["reference_unresolved_fraction"], 0)
        self.assertLessEqual(
            wet["trigger_probability_lower"], wet["trigger_probability_resolved_only"]
        )
        self.assertGreaterEqual(
            wet["trigger_probability_upper"], wet["trigger_probability_resolved_only"]
        )

    def test_requires_three_camera_types(self):
        rows = [r for r in mod._read(self.path) if r["CAMERA.ID"] != "BV"]
        with self.assertRaises(mod.CorrectionError):
            mod.analyze(rows)


if __name__ == "__main__":
    unittest.main()
