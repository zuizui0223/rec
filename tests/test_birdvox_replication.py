import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GRID_SPEC = importlib.util.spec_from_file_location(
    "birdvox_grid", ROOT / "scripts" / "build_birdvox_exposure_grid.py"
)
grid_mod = importlib.util.module_from_spec(GRID_SPEC)
assert GRID_SPEC and GRID_SPEC.loader
GRID_SPEC.loader.exec_module(grid_mod)

AN_SPEC = importlib.util.spec_from_file_location(
    "birdvox_analysis", ROOT / "scripts" / "analyze_birdvox_exposure_grid.py"
)
analysis_mod = importlib.util.module_from_spec(AN_SPEC)
assert AN_SPEC and AN_SPEC.loader
AN_SPEC.loader.exec_module(analysis_mod)


class BirdVoxReplicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

        (self.dir / "manifest.csv").write_text(
            "sensor_id,duration_seconds,split\n"
            "01,4,development\n"
            "02,4,heldout\n"
            "03,4,heldout\n",
            encoding="utf-8",
        )
        (self.dir / "BirdVox-full-night_csv-annotations_unit01.csv").write_text(
            "Time (s),Freq (Hz)\n0.2,5000\n", encoding="utf-8"
        )
        (self.dir / "BirdVox-full-night_csv-annotations_unit02.csv").write_text(
            "Time (s),Freq (Hz)\n0.2,5000\n2.2,5000\n", encoding="utf-8"
        )
        (self.dir / "BirdVox-full-night_csv-annotations_unit03.csv").write_text(
            "Time (s),Freq (Hz)\n1.2,5000\n3.2,5000\n", encoding="utf-8"
        )
        (self.dir / "scores.csv").write_text(
            "sensor_id,time_seconds,score\n"
            "01,0.1,80\n01,1.1,20\n01,2.1,20\n01,3.1,20\n"
            "02,0.1,80\n02,1.1,20\n02,2.1,40\n02,3.1,20\n"
            "03,0.1,20\n03,1.1,80\n03,2.1,20\n03,3.1,40\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _grid(self):
        manifest = grid_mod.load_manifest(self.dir / "manifest.csv")
        annotations = grid_mod.load_annotations(
            [
                self.dir / "BirdVox-full-night_csv-annotations_unit01.csv",
                self.dir / "BirdVox-full-night_csv-annotations_unit02.csv",
                self.dir / "BirdVox-full-night_csv-annotations_unit03.csv",
            ]
        )
        scores = grid_mod.load_scores(self.dir / "scores.csv")
        rows = grid_mod.build_grid(manifest, annotations, scores, window_seconds=1.0)
        path = self.dir / "grid.csv"
        grid_mod.write_grid(path, rows)
        return path, rows

    def test_grid_is_defined_from_manifest_not_detector_hits(self):
        _, rows = self._grid()
        self.assertEqual(len(rows), 12)
        heldout = [r for r in rows if r["split"] == "heldout"]
        self.assertEqual(len(heldout), 8)
        positives = [r for r in heldout if r["truth_positive"] == "true"]
        self.assertEqual(len(positives), 4)

    def test_missing_score_is_gate_unevaluable_not_negative(self):
        scores = self.dir / "scores.csv"
        lines = scores.read_text(encoding="utf-8").splitlines()
        scores.write_text(
            "\n".join(line for line in lines if "02,3.1" not in line) + "\n",
            encoding="utf-8",
        )
        _, rows = self._grid()
        row = next(
            r for r in rows if r["sensor_id"] == "02" and r["window_index"] == "3"
        )
        self.assertEqual(row["gate_evaluable"], "false")
        self.assertEqual(row["max_score"], "")

    def test_h1_h3_and_gate_sensitivity_are_computed_on_heldout(self):
        path, _ = self._grid()
        result = analysis_mod.analyze(analysis_mod.load_grid(path), [30.0, 70.0])
        low, high = result["threshold_results"]
        self.assertEqual(low["heldout"]["window_count"], 8)
        self.assertEqual(low["REC_H1_shadow_existence"]["shadow_positive_windows"], 0)
        self.assertEqual(high["REC_H1_shadow_existence"]["shadow_positive_windows"], 2)
        self.assertAlmostEqual(
            high["REC_H1_shadow_existence"]["a_R_event_absorbed_by_gate"], 0.5
        )
        self.assertGreater(
            high["REC_H3_ecological_distortion"]["absolute_temporal_contrast_error"],
            0.0,
        )
        gate = result["REC_H4_gate_semantics_sensitivity"][0]
        self.assertGreater(gate["delta_event_absorption"], 0.0)

    def test_out_of_duration_annotation_fails_closed(self):
        bad = self.dir / "BirdVox-full-night_csv-annotations_unit02.csv"
        bad.write_text("Time (s),Freq (Hz)\n4.2,5000\n", encoding="utf-8")
        manifest = grid_mod.load_manifest(self.dir / "manifest.csv")
        annotations = grid_mod.load_annotations(
            [
                self.dir / "BirdVox-full-night_csv-annotations_unit01.csv",
                bad,
                self.dir / "BirdVox-full-night_csv-annotations_unit03.csv",
            ]
        )
        scores = grid_mod.load_scores(self.dir / "scores.csv")
        with self.assertRaises(grid_mod.BirdVoxGridError):
            grid_mod.build_grid(manifest, annotations, scores, window_seconds=1.0)


if __name__ == "__main__":
    unittest.main()
