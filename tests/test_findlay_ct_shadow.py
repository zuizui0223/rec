import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "findlay_rec", ROOT / "scripts" / "analyze_findlay_ct_shadow.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class FindlayRECMappingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.fb = self.root / "REGISTRATION_FOX_BADGER.csv"
        self.ot = self.root / "TRIGGER_OTTER_WET.DRY.csv"
        self.fb.write_text(
            "SPECIES,CT.POS,ORIENT,GAIT,DIST,LOIT,TRIGGER,CAPTURE\n"
            "FOX,A,L,W,1,0,1,1\n"
            "FOX,A,L,W,5,0,0,NA\n"
            "BADGER,B,L,R,1,0,1,0\n"
            "BADGER,B,L,R,5,0,1,1\n"
            "FOX,B,L,W,3,0,1,NA\n"
            "FOX,B,L,W,4,0,NA,NA\n",
            encoding="utf-8",
        )
        self.ot.write_text(
            "CT.POS,CAMERA.ID,ORIENT,GAIT,DIST,wet.dry,LOIT,TRIGGER\n"
            "A,X,L,W,1,wet,0,1\n"
            "A,X,L,W,5,dry,0,0\n"
            "A,X,L,W,3,wet,0,NA\n"
            "A,Y,L,W,1,wet,0,0\n"
            "A,Y,L,W,5,dry,0,1\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_pass_trigger_capture_layers_are_separate_and_bounded(self):
        out = mod.analyze(self.fb, self.ot)
        s = out["fox_badger_registration"]["overall"]
        self.assertEqual(s["pass_count"], 6)
        self.assertEqual(s["confirmed_triggered_passes"], 4)
        self.assertEqual(s["trigger_unresolved_passes"], 1)
        self.assertAlmostEqual(s["a_R_no_trigger_given_pass_resolved_only"], 0.2)
        self.assertAlmostEqual(s["a_R_no_trigger_given_pass_bounds"]["lower"], 1 / 6)
        self.assertAlmostEqual(s["a_R_no_trigger_given_pass_bounds"]["upper"], 2 / 6)
        self.assertEqual(s["capture_unresolved_passes"], 2)
        self.assertAlmostEqual(s["a_K_no_capture_given_pass_resolved_only"], 0.5)
        self.assertAlmostEqual(s["a_K_no_capture_given_pass_bounds"]["lower"], 2 / 6)
        self.assertAlmostEqual(s["a_K_no_capture_given_pass_bounds"]["upper"], 4 / 6)
        self.assertAlmostEqual(
            s["a_registration_failure_given_confirmed_trigger_evaluable"], 1 / 3
        )

    def test_missing_process_states_are_not_coerced_to_failure(self):
        r, k = mod._capture_state({"TRIGGER": "1", "CAPTURE": "NA"})
        self.assertTrue(r)
        self.assertIsNone(k)
        r, k = mod._capture_state({"TRIGGER": "NA", "CAPTURE": "NA"})
        self.assertIsNone(r)
        self.assertIsNone(k)
        s = mod._trigger_summary(
            [{"TRIGGER": "1"}, {"TRIGGER": "0"}, {"TRIGGER": "NA"}]
        )
        self.assertAlmostEqual(s["a_R_no_trigger_given_pass_resolved_only"], 0.5)
        self.assertEqual(
            s["a_R_no_trigger_given_pass_bounds"],
            {"lower": 1 / 3, "upper": 2 / 3},
        )

    def test_species_composition_can_change_at_trigger(self):
        out = mod.analyze(self.fb, self.ot)
        c = out["fox_badger_registration"]["REC_H3_ecological_composition_distortion"]["species"]
        self.assertAlmostEqual(c["levels"]["FOX"]["truth_pass_proportion"], 4 / 6)
        self.assertAlmostEqual(c["levels"]["FOX"]["confirmed_trigger_world_proportion"], 0.5)
        self.assertGreater(c["total_variation_truth_vs_confirmed_trigger"], 0)
        self.assertEqual(c["trigger_unresolved_count"], 1)
        self.assertEqual(c["capture_unresolved_count"], 2)

    def test_event_conditioned_data_do_not_claim_q_shadow(self):
        out = mod.analyze(self.fb, self.ot)
        self.assertIn("not identified", out["identification_boundary"])
        self.assertIn("reference-unresolved", out["identification_boundary"])
        self.assertNotIn("q_shadow", out["fox_badger_registration"]["overall"])


if __name__ == "__main__":
    unittest.main()
