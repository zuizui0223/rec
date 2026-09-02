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
    "primary_stream_available", "pregate_evidence_version", "registered_deviation",
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
        "exposure_grid_id": "grid-v1",
        "exposure_source": "reference_timeline",
        "exposure_source_version": "ref-v1",
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
        "primary_stream_available": "true",
        "pregate_evidence_version": "v1",
        "registered_deviation": "false",
        "gate_type": "scalar",
        "gate_version": "g1",
        "gate_configuration_id": "cfg1",
        "gate_threshold": "0.5",
        "gate_inputs_complete": "true",
        "record_entry_present": "false",
        "entry_policy_version": "entry-v1",
        "entry_policy_type": "hybrid",
        "entry_policy_inputs_complete": "true",
        "target_truth": "positive",
        "target_truth_source": "reference_camera",
        "target_event_definition_version": "event-v1",
        "truth_sampled": "true",
        "truth_sampling_design_version": "pilot-v1",
        "truth_sampling_stratum": "B_shadow",
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

    def test_valid_table_detects_gate_and_shadow_events(self):
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
                recording_day="2026-09-02",
                recording_block_id="B2",
                development_or_heldout="heldout",
                registered_deviation="true",
                record_entry_present="true",
                target_truth="positive",
                truth_inclusion_probability="1",
                truth_sampling_weight="1",
                truth_sampling_stratum="deviation_entered",
                threshold_absorbed_event="false",
                shadow_event="false",
            ),
        ]
        summary = mod.validate_csv(self.write_rows(rows))
        self.assertEqual(summary["sampled_truth_counts"]["threshold_absorbed"], 1)
        self.assertEqual(summary["sampled_truth_counts"]["shadow_event"], 1)
        self.assertAlmostEqual(summary["unweighted_descriptive_q_B"], 0.5)
        self.assertAlmostEqual(summary["unweighted_descriptive_event_absorption"], 0.5)
        self.assertAlmostEqual(summary["unweighted_descriptive_q_shadow"], 0.5)
        self.assertAlmostEqual(summary["unweighted_descriptive_event_nonentry"], 0.5)

    def test_exposure_universe_must_be_gate_independent(self):
        path = self.write_rows([base_row(exposure_defined_independently_of_gate="false")])
        with self.assertRaisesRegex(mod.ValidationError, "exposure universe defined independently"):
            mod.validate_csv(path)

    def test_derived_absorption_flag_must_match_truth_and_gate(self):
        path = self.write_rows([base_row(threshold_absorbed_event="false")])
        with self.assertRaisesRegex(mod.ValidationError, "threshold_absorbed_event disagrees"):
            mod.validate_csv(path)

    def test_derived_shadow_flag_must_match_truth_and_entry(self):
        path = self.write_rows([base_row(shadow_event="false")])
        with self.assertRaisesRegex(mod.ValidationError, "shadow_event disagrees"):
            mod.validate_csv(path)

    def test_nonentered_exposures_require_shadow_truth_sample(self):
        rows = [
            base_row(record_entry_present="true", shadow_event="false"),
            base_row(
                window_id="w2",
                record_entry_present="false",
                target_truth="unresolved",
                truth_sampled="false",
                truth_sampling_design_version="",
                truth_sampling_stratum="",
                truth_inclusion_probability="",
                truth_sampling_weight="",
                threshold_absorbed_event="false",
                shadow_event="false",
            ),
        ]
        path = self.write_rows(rows)
        with self.assertRaisesRegex(mod.ValidationError, "no truth-sampled record-entry shadow"):
            mod.validate_csv(path)

    def test_present_entry_requires_reproducible_entry_policy(self):
        path = self.write_rows([
            base_row(
                record_entry_present="true",
                entry_policy_inputs_complete="false",
                shadow_event="false",
            )
        ])
        with self.assertRaisesRegex(mod.ValidationError, "present record entry"):
            mod.validate_csv(path)

    def test_chapter2_requires_truth_sampled_B(self):
        row = base_row(
            registered_deviation="true",
            record_entry_present="true",
            threshold_absorbed_event="false",
            shadow_event="false",
            truth_sampling_stratum="deviation_entered",
        )
        path = self.write_rows([row])
        with self.assertRaisesRegex(mod.ValidationError, "truth-sampled logical registered-B"):
            mod.validate_csv(path)

    def test_composite_gate_cannot_invent_scalar_threshold(self):
        path = self.write_rows([base_row(gate_type="composite", gate_threshold="0.5")])
        with self.assertRaisesRegex(mod.ValidationError, "must not invent"):
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
        path = self.write_rows(rows)
        with self.assertRaisesRegex(mod.ValidationError, "leakage"):
            mod.validate_csv(path)

    def test_unsampled_truth_cannot_be_resolved(self):
        row = base_row(
            truth_sampled="false",
            truth_sampling_design_version="",
            truth_sampling_stratum="",
            truth_inclusion_probability="",
            truth_sampling_weight="",
        )
        path = self.write_rows([row])
        with self.assertRaisesRegex(mod.ValidationError, "unsampled truth"):
            mod.validate_csv(path)


if __name__ == "__main__":
    unittest.main()
