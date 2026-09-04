import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "h6_readiness", ROOT / "scripts" / "check_h6_readiness.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def ready_manifest():
    return {
        "schema": "tnoa-field-calibration-manifest-v1",
        "status": "frozen_field_calibration",
        "source_observation_schema": "tnoa-shadow-1",
        "source_log_schema": "tnoa-observation-log-1",
        "truth_annotation_schema": "tnoa-independent-truth-1",
        "independent_reference_truth_required": True,
        "split_group": ["recording_day", "focal_scene_id", "recording_block"],
        "minimum_double_annotation_fraction": 0.2,
        "target": {
            "high_threshold": 0.8,
            "low_threshold": 0.2,
            "operational_error_criterion": "heldout-FPR<=0.05",
        },
        "nuisance": {
            "familywise_false_attribution_alpha": 0.05,
            "families": ["wind_target_motion", "camera_shake"],
        },
        "observability": {
            "support_rule": "all-required-diagnostics-pass",
            "observable_thresholds": {"dark_fraction_max": 0.25},
            "unobservable_thresholds": {"dark_fraction_min": 0.9},
        },
        "coupled": {
            "response_threshold": None,
            "target_link_threshold": None,
            "enabled_for_target_rescue": False,
        },
        "target_absence": {"channel_status": "unavailable", "rule": None},
        "heldout_scoring_allowed": True,
        "live_tnoa_capture_actions_allowed": False,
    }


class H6ReadinessTests(unittest.TestCase):
    def test_frozen_manifest_can_license_h6_scoring_without_live_actions(self):
        result = mod.audit(ready_manifest())
        self.assertTrue(result["ready_for_h6_heldout_scoring"])
        self.assertEqual(result["hard_failures"], [])
        self.assertFalse(result["live_tnoa_capture_actions_allowed"])

    def test_current_unfrozen_shape_fails_closed(self):
        payload = ready_manifest()
        payload["status"] = "unfrozen_predata"
        payload["heldout_scoring_allowed"] = False
        payload["target"]["high_threshold"] = None
        payload["target"]["low_threshold"] = None
        payload["target"]["operational_error_criterion"] = None
        payload["nuisance"]["familywise_false_attribution_alpha"] = None
        payload["observability"]["support_rule"] = None
        payload["observability"]["observable_thresholds"] = None
        payload["observability"]["unobservable_thresholds"] = None

        result = mod.audit(payload)
        self.assertFalse(result["ready_for_h6_heldout_scoring"])
        failures = set(result["hard_failures"])
        self.assertIn("frozen_field_calibration", failures)
        self.assertIn("heldout_scoring_allowed", failures)
        self.assertIn("target_high_threshold_frozen", failures)
        self.assertIn("target_low_threshold_frozen", failures)
        self.assertIn("target_error_criterion_frozen", failures)
        self.assertIn("nuisance_error_criterion_frozen", failures)
        self.assertIn("observability_support_rule_frozen", failures)

    def test_missing_independent_truth_requirement_blocks_readiness(self):
        payload = ready_manifest()
        payload["independent_reference_truth_required"] = False
        result = mod.audit(payload)
        self.assertFalse(result["ready_for_h6_heldout_scoring"])
        self.assertIn(
            "independent_reference_truth_required", result["hard_failures"]
        )

    def test_missing_grouped_split_blocks_readiness(self):
        payload = ready_manifest()
        payload["split_group"] = []
        result = mod.audit(payload)
        self.assertFalse(result["ready_for_h6_heldout_scoring"])
        self.assertIn("grouped_split_declared", result["hard_failures"])


if __name__ == "__main__":
    unittest.main()
