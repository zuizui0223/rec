import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "chapter2_validator", ROOT / "scripts" / "validate_chapter2_windows.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)

FIELDS = [
    "exposure_grid_id", "exposure_source", "exposure_source_version",
    "exposure_defined_independently_of_gate", "system_id", "site_id",
    "camera_or_sensor_id", "recording_day", "recording_block_id", "window_id",
    "window_start", "window_end", "exposure_seconds", "development_or_heldout",
    "primary_stream_expected", "primary_stream_available", "acquisition_status",
    "pregate_evidence_version", "gate_evaluable", "registered_deviation",
    "gate_type", "gate_version", "gate_configuration_id", "gate_threshold",
    "gate_inputs_complete", "record_entry_present", "entry_policy_version",
    "entry_policy_type", "entry_policy_inputs_complete", "target_truth",
    "target_truth_source", "target_event_definition_version", "truth_sampled",
    "truth_sampling_design_version", "truth_sampling_stratum",
    "truth_inclusion_probability", "truth_sampling_weight",
    "annotator_blinded_to_gate", "annotator_blinded_to_entry",
    "annotator_blinded_to_scores", "threshold_absorbed_event", "shadow_event",
]


def base_row(**overrides):
    row = {
        "exposure_grid_id": "grid-v2",
        "exposure_source": "continuous_reference_stream",
        "exposure_source_version": "ref-v2",
        "exposure_defined_independently_of_gate": "true",
        "system_id": "A",
        "site_id": "S1",
        "camera_or_sensor_id": "C1",
        "recording_day": "2026-09-01",
        "recording_block_id": "B1",
        "window_id": "w1",
        "window_start": "2026-09-01T09:00:00",
        "window_end": "2026-09-01T09:00:10",
        "exposure_seconds": "10",
        "development_or_heldout": "development",
        "primary_stream_expected": "true",
        "primary_stream_available": "true",
        "acquisition_status": "available",
        "pregate_evidence_version": "v2",
        "gate_evaluable": "true",
        "registered_deviation": "false",
        "gate_type": "scalar",
        "gate_version": "g2",
        "gate_configuration_id": "cfg2",
        "gate_threshold": "0.5",
        "gate_inputs_complete": "true",
        "record_entry_present": "false",
        "entry_policy_version": "entry-v2",
        "entry_policy_type": "hybrid",
        "entry_policy_inputs_complete": "true",
        "target_truth": "positive",
        "target_truth_source": "reference_camera",
        "target_event_definition_version": "event-v2",
        "truth_sampled": "true",
        "truth_sampling_design_version": "pilot-v2",
        "truth_sampling_stratum": "gate_shadow",
        "truth_inclusion_probability": "0.5",
        "truth_sampling_weight": "2",
        "annotator_blinded_to_gate": "true",
        "annotator_blinded_to_entry": "true",
        "annotator_blinded_to_scores": "true",
        "threshold_absorbed_event": "true",
        "shadow_event": "true",
    }
    row.update(overrides)
    return row


class Chapter2SchemaTests(unittest.TestCase):
    def write_rows(self, rows):
        tmp = tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return Path(tmp.name)

    def test_valid_table_separates_acquisition_shadow_from_gate_absorption(self):
        rows = [
            base_row(),
            base_row(
                window_id="w2",
                target_truth="negative",
                threshold_absorbed_event="false",
                shadow_event="false",
            ),
            base_row(
                window_id="w3",
                primary_stream_available="false",
                acquisition_status="hardware_failure",
                gate_evaluable="false",
                registered_deviation="",
                gate_inputs_complete="false",
                entry_policy_inputs_complete="false",
                truth_inclusion_probability="1",
                truth_sampling_weight="1",
                truth_sampling_stratum="acquisition_shadow",
                threshold_absorbed_event="",
                shadow_event="true",
            ),
            base_row(
                window_id="w4",
                recording_day="2026-09-02",
                recording_block_id="B2",
                development_or_heldout="heldout",
                registered_deviation="true",
                record_entry_present="true",
                truth_inclusion_probability="1",
                truth_sampling_weight="1",
                truth_sampling_stratum="entered",
                threshold_absorbed_event="false",
                shadow_event="false",
            ),
        ]
        summary = mod.validate_csv(self.write_rows(rows))
        self.assertAlmostEqual(summary["unweighted_descriptive_q_B_gate_evaluable"], 0.5)
        self.assertAlmostEqual(
            summary["unweighted_descriptive_event_absorption_given_gate_evaluable"], 0.5
        )
        self.assertAlmostEqual(summary["unweighted_descriptive_q_shadow"], 2 / 3)
        self.assertAlmostEqual(summary["unweighted_descriptive_event_nonentry"], 2 / 3)
        self.assertEqual(summary["state_counts"]["acquisition_shadow"], 1)
        self.assertEqual(summary["state_counts"]["threshold_absorbed"], 1)

    def test_nonevaluable_gate_cannot_be_encoded_as_false(self):
        row = base_row(gate_evaluable="false", gate_inputs_complete="false")
        path = self.write_rows([row])
        with self.assertRaisesRegex(mod.ValidationError, "must leave registered_deviation undefined"):
            mod.validate_csv(path)

    def test_nonevaluable_gate_allows_undefined_registered_state(self):
        rows = [
            base_row(),
            base_row(
                window_id="w2",
                primary_stream_available="false",
                acquisition_status="hardware_failure",
                gate_evaluable="false",
                registered_deviation="",
                gate_inputs_complete="false",
                entry_policy_inputs_complete="false",
                target_truth="negative",
                truth_inclusion_probability="1",
                truth_sampling_weight="1",
                truth_sampling_stratum="acquisition_shadow",
                threshold_absorbed_event="",
                shadow_event="false",
            ),
        ]
        summary = mod.validate_csv(self.write_rows(rows))
        self.assertEqual(summary["state_counts"]["gate_unevaluable"], 1)

    def test_threshold_absorbed_is_undefined_when_gate_not_evaluable(self):
        row = base_row(
            primary_stream_available="false",
            acquisition_status="hardware_failure",
            gate_evaluable="false",
            registered_deviation="",
            gate_inputs_complete="false",
            entry_policy_inputs_complete="false",
            threshold_absorbed_event="false",
        )
        path = self.write_rows([base_row(), row | {"window_id": "w2"}])
        with self.assertRaisesRegex(mod.ValidationError, "undefined when gate is not evaluable"):
            mod.validate_csv(path)

    def test_evaluable_gate_requires_complete_primary_inputs(self):
        path = self.write_rows([base_row(gate_inputs_complete="false")])
        with self.assertRaisesRegex(mod.ValidationError, "evaluable gate requires"):
            mod.validate_csv(path)

    def test_shadow_flag_must_match_truth_and_entry(self):
        path = self.write_rows([base_row(shadow_event="false")])
        with self.assertRaisesRegex(mod.ValidationError, "shadow_event disagrees"):
            mod.validate_csv(path)

    def test_exposure_source_must_be_independent_of_gate(self):
        path = self.write_rows([base_row(exposure_defined_independently_of_gate="false")])
        with self.assertRaisesRegex(mod.ValidationError, "independently"):
            mod.validate_csv(path)

    def test_group_level_split_leakage_fails(self):
        rows = [
            base_row(),
            base_row(
                window_id="w2",
                development_or_heldout="heldout",
                target_truth="negative",
                threshold_absorbed_event="false",
                shadow_event="false",
            ),
        ]
        with self.assertRaisesRegex(mod.ValidationError, "leakage"):
            mod.validate_csv(self.write_rows(rows))

    def test_unsampled_truth_cannot_be_resolved(self):
        row = base_row(
            truth_sampled="false",
            truth_sampling_design_version="",
            truth_sampling_stratum="",
            truth_inclusion_probability="",
            truth_sampling_weight="",
        )
        with self.assertRaisesRegex(mod.ValidationError, "unsampled truth"):
            mod.validate_csv(self.write_rows([row]))


if __name__ == "__main__":
    unittest.main()
