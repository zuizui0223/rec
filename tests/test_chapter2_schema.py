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
    "system_id", "site_id", "camera_or_sensor_id", "recording_day",
    "recording_block_id", "window_id", "window_start", "window_end",
    "exposure_seconds", "development_or_heldout", "primary_stream_available",
    "pregate_evidence_version", "registered_deviation", "gate_type",
    "gate_version", "gate_configuration_id", "gate_threshold",
    "gate_inputs_complete", "target_truth", "target_truth_source",
    "target_event_definition_version", "truth_sampled",
    "truth_sampling_design_version", "truth_sampling_stratum",
    "truth_inclusion_probability", "truth_sampling_weight",
    "annotator_blinded_to_gate", "annotator_blinded_to_scores",
    "threshold_absorbed_event",
]


def base_row(**overrides):
    row = {
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
        "target_truth": "positive",
        "target_truth_source": "reference_camera",
        "target_event_definition_version": "event-v1",
        "truth_sampled": "true",
        "truth_sampling_design_version": "pilot-v1",
        "truth_sampling_stratum": "B",
        "truth_inclusion_probability": "0.5",
        "truth_sampling_weight": "2",
        "annotator_blinded_to_gate": "true",
        "annotator_blinded_to_scores": "true",
        "threshold_absorbed_event": "true",
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

    def test_valid_table_detects_absorbed_event(self):
        rows = [
            base_row(),
            base_row(
                window_id="w2",
                target_truth="negative",
                threshold_absorbed_event="false",
            ),
            base_row(
                window_id="w3",
                recording_day="2026-09-02",
                recording_block_id="B2",
                development_or_heldout="heldout",
                registered_deviation="true",
                target_truth="positive",
                truth_inclusion_probability="1",
                truth_sampling_weight="1",
                truth_sampling_stratum="deviation",
                threshold_absorbed_event="false",
            ),
        ]
        summary = mod.validate_csv(self.write_rows(rows))
        self.assertEqual(summary["sampled_truth_counts"]["threshold_absorbed"], 1)
        self.assertAlmostEqual(summary["unweighted_descriptive_q_B"], 0.5)
        self.assertAlmostEqual(summary["unweighted_descriptive_event_absorption"], 0.5)

    def test_derived_absorption_flag_must_match_truth_and_gate(self):
        path = self.write_rows([base_row(threshold_absorbed_event="false")])
        with self.assertRaisesRegex(mod.ValidationError, "disagrees"):
            mod.validate_csv(path)

    def test_chapter2_requires_truth_sampled_B(self):
        row = base_row(
            registered_deviation="true",
            threshold_absorbed_event="false",
            truth_sampling_stratum="deviation",
        )
        path = self.write_rows([row])
        with self.assertRaisesRegex(mod.ValidationError, "truth-sampled registered-B"):
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
