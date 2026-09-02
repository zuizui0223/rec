import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "exposure_ledger_validator", ROOT / "scripts" / "validate_exposure_ledger.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)

FIELDS = [
    "exposure_grid_id", "window_id", "system_id", "site_id",
    "camera_or_sensor_id", "recording_day", "recording_block_id",
    "window_start", "window_end", "exposure_seconds", "exposure_source",
    "exposure_source_version", "exposure_expected", "primary_stream_expected",
    "primary_stream_available", "acquisition_status", "gate_evaluable",
    "record_entry_present", "record_entry_policy_version", "record_entry_id",
    "record_entry_timestamp", "record_entry_reason",
]


def base_row(**overrides):
    row = {
        "exposure_grid_id": "grid-v2",
        "window_id": "w1",
        "system_id": "A",
        "site_id": "S1",
        "camera_or_sensor_id": "C1",
        "recording_day": "2026-09-01",
        "recording_block_id": "B1",
        "window_start": "2026-09-01T09:00:00",
        "window_end": "2026-09-01T09:00:10",
        "exposure_seconds": "10",
        "exposure_source": "fixed_clock",
        "exposure_source_version": "grid-rule-v2",
        "exposure_expected": "true",
        "primary_stream_expected": "true",
        "primary_stream_available": "true",
        "acquisition_status": "available",
        "gate_evaluable": "true",
        "record_entry_present": "false",
        "record_entry_policy_version": "entry-v2",
        "record_entry_id": "",
        "record_entry_timestamp": "",
        "record_entry_reason": "gate_rejected",
    }
    row.update(overrides)
    return row


class ExposureLedgerTests(unittest.TestCase):
    def write_rows(self, rows, fields=FIELDS):
        tmp = tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return Path(tmp.name)

    def test_valid_ledger_separates_shadow_layers(self):
        rows = [
            base_row(),
            base_row(
                window_id="w2",
                primary_stream_available="false",
                acquisition_status="hardware_failure",
                gate_evaluable="false",
                record_entry_reason="primary_stream_failure",
            ),
            base_row(
                window_id="w3",
                primary_stream_expected="false",
                primary_stream_available="false",
                acquisition_status="planned_not_acquired",
                gate_evaluable="false",
                record_entry_reason="not_applicable",
            ),
            base_row(
                window_id="w4",
                gate_evaluable="false",
                record_entry_reason="gate_not_evaluable",
            ),
            base_row(
                window_id="w5",
                record_entry_present="true",
                record_entry_id="evt-5",
                record_entry_timestamp="2026-09-01T09:00:41",
                record_entry_reason="entered",
            ),
        ]
        summary = mod.validate_ledger(self.write_rows(rows))
        states = summary["operational_state_counts"]
        self.assertEqual(states["gate_shadow"], 1)
        self.assertEqual(states["acquisition_failure_shadow"], 1)
        self.assertEqual(states["planned_nonacquisition_shadow"], 1)
        self.assertEqual(states["gate_unevaluable_shadow"], 1)
        self.assertEqual(states["entered"], 1)
        self.assertAlmostEqual(summary["shadow_fraction"], 4 / 5)

    def test_duplicate_window_id_fails(self):
        path = self.write_rows([base_row(), base_row()])
        with self.assertRaisesRegex(mod.ValidationError, "duplicate window_id"):
            mod.validate_ledger(path)

    def test_nonentered_row_cannot_fabricate_record_id(self):
        path = self.write_rows([base_row(record_entry_id="fake")])
        with self.assertRaisesRegex(mod.ValidationError, "must not fabricate"):
            mod.validate_ledger(path)

    def test_entered_row_requires_available_stream_id_and_timestamp(self):
        path = self.write_rows([
            base_row(record_entry_present="true", record_entry_reason="entered")
        ])
        with self.assertRaisesRegex(mod.ValidationError, "requires record_entry_id"):
            mod.validate_ledger(path)

    def test_gate_rejection_requires_evaluable_gate(self):
        path = self.write_rows([base_row(gate_evaluable="false")])
        with self.assertRaisesRegex(mod.ValidationError, "gate_rejected requires"):
            mod.validate_ledger(path)

    def test_gate_cannot_be_evaluable_without_acquisition(self):
        path = self.write_rows([
            base_row(
                primary_stream_available="false",
                acquisition_status="hardware_failure",
                gate_evaluable="true",
                record_entry_reason="primary_stream_failure",
            )
        ])
        with self.assertRaisesRegex(mod.ValidationError, "gate cannot be evaluable"):
            mod.validate_ledger(path)

    def test_planned_nonacquisition_cannot_be_expected(self):
        path = self.write_rows([
            base_row(
                primary_stream_available="false",
                acquisition_status="planned_not_acquired",
                gate_evaluable="false",
                record_entry_reason="not_applicable",
            )
        ])
        with self.assertRaisesRegex(mod.ValidationError, "planned_not_acquired requires"):
            mod.validate_ledger(path)

    def test_primary_stream_failure_requires_unavailable_stream(self):
        path = self.write_rows([base_row(record_entry_reason="primary_stream_failure")])
        with self.assertRaisesRegex(mod.ValidationError, "requires unavailable"):
            mod.validate_ledger(path)

    def test_window_table_ids_must_exist_in_ledger(self):
        ledger = self.write_rows([base_row()])
        window = self.write_rows([{"window_id": "missing"}], fields=["window_id"])
        with self.assertRaisesRegex(mod.ValidationError, "absent from exposure ledger"):
            mod.validate_ledger(ledger, window)

    def test_window_table_acquisition_state_must_match(self):
        ledger = self.write_rows([base_row()])
        fields = ["window_id", "primary_stream_available", "gate_evaluable"]
        window = self.write_rows([
            {
                "window_id": "w1",
                "primary_stream_available": "false",
                "gate_evaluable": "true",
            }
        ], fields=fields)
        with self.assertRaisesRegex(mod.ValidationError, "disagrees"):
            mod.validate_ledger(ledger, window)


if __name__ == "__main__":
    unittest.main()
