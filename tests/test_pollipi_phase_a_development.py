import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "phase_a_intake", ROOT / "scripts" / "audit_pollipi_phase_a_development.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


COLUMNS = sorted(mod.REQUIRED_COLUMNS)


def row(i: int) -> dict[str, str]:
    base = {k: "" for k in COLUMNS}
    base.update(
        {
            "log_schema_version": "tnoa-observation-log-1",
            "schema_version": "tnoa-shadow-1",
            "run_id": "run-dev-001",
            "probe_timestamp": f"2026-09-04T10:00:{i:02d}",
            "device_id": "pi-dev-01",
            "device_name": "pollipi-dev",
            "site_id": "site-a",
            "flower_id": "flower-a",
            "plant_species": "Cirsium-test",
            "comparison_session_id": "session-a",
            "camera_role": "primary",
            "method_mode": "plain",
            "record_kind": "image",
            "calibration_status": "unavailable",
            "observation_state": "U",
            "u_reason": "field_calibration_pending",
            "would_be_action": "observe_only",
            "action_applied": "False",
            "observability_frame_available": "True",
            "observability_actual_probe_interval_sec": "1.0",
        }
    )
    return base


def manifest(reference_recorded=True):
    return {
        "schema": "rec-pollipi-development-collection-v1",
        "collection_id": "dev-20260904-a",
        "prospective_role": "development",
        "recording_day": "2026-09-04",
        "focal_scene_id": "scene-a",
        "recording_block": "block-01",
        "reference_source_id": "reference-camera-a",
        "independent_reference_expected": True,
        "independent_reference_recorded": reference_recorded,
        "primary_device_id": "pi-dev-01",
        "site_id": "site-a",
        "flower_id": "flower-a",
        "comparison_session_id": "session-a",
    }


class PhaseADevelopmentIntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_csv(self, rows):
        path = self.root / "tnoa_observation_v1_run-dev-001.csv"
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_valid_development_log_is_phase_b_ready_with_reference(self):
        rows = [row(0), row(1), row(2)]
        result = mod.audit(rows, manifest(True), min_rows=3)
        self.assertTrue(result["structurally_valid_phase_a_development_log"])
        self.assertTrue(result["suitable_for_phase_b_truth_preparation"])
        self.assertEqual(result["structural_failures"], [])

    def test_reference_not_recorded_blocks_phase_b_but_not_primary_structure(self):
        result = mod.audit([row(0), row(1), row(2)], manifest(False), min_rows=3)
        self.assertTrue(result["structurally_valid_phase_a_development_log"])
        self.assertFalse(result["suitable_for_phase_b_truth_preparation"])
        self.assertFalse(result["checks"]["independent_reference_recorded"])

    def test_any_calibrated_support_or_action_fails_closed_contract(self):
        rows = [row(0), row(1), row(2)]
        rows[1]["target_calibrated_support"] = "True"
        rows[1]["action_applied"] = "True"
        result = mod.audit(rows, manifest(True), min_rows=3)
        self.assertFalse(result["structurally_valid_phase_a_development_log"])
        self.assertIn("fail_closed_shadow_only", result["structural_failures"])

    def test_metadata_mismatch_is_rejected(self):
        rows = [row(0), row(1), row(2)]
        m = manifest(True)
        m["site_id"] = "other-site"
        result = mod.audit(rows, m, min_rows=3)
        self.assertFalse(result["structurally_valid_phase_a_development_log"])
        self.assertIn("manifest_metadata_matches_log", result["structural_failures"])

    def test_heldout_role_cannot_enter_development_intake(self):
        m = manifest(True)
        m["prospective_role"] = "heldout"
        with self.assertRaises(mod.PhaseAIntakeError):
            mod.audit([row(0), row(1), row(2)], m, min_rows=3)

    def test_csv_loader_enforces_required_schema(self):
        path = self.write_csv([row(0), row(1), row(2)])
        loaded = mod._load_csv(path)
        self.assertEqual(len(loaded), 3)


if __name__ == "__main__":
    unittest.main()
