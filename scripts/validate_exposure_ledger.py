#!/usr/bin/env python3
"""Validate the REC master exposure ledger and optional Chapter-2 audit join."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {
    "exposure_grid_id",
    "window_id",
    "system_id",
    "site_id",
    "camera_or_sensor_id",
    "recording_day",
    "recording_block_id",
    "window_start",
    "window_end",
    "exposure_seconds",
    "exposure_source",
    "exposure_source_version",
    "exposure_expected",
    "primary_stream_expected",
    "record_entry_present",
    "record_entry_policy_version",
    "record_entry_id",
    "record_entry_timestamp",
    "record_entry_reason",
}

BOOL_TRUE = {"1", "true", "t", "yes", "y"}
BOOL_FALSE = {"0", "false", "f", "no", "n"}
REASONS = {
    "entered",
    "gate_rejected",
    "archive_policy_excluded",
    "storage_failure",
    "primary_stream_failure",
    "unknown",
    "not_applicable",
}


class ValidationError(ValueError):
    pass


def parse_bool(value: str, *, field: str, row_no: int) -> bool:
    text = str(value).strip().lower()
    if text in BOOL_TRUE:
        return True
    if text in BOOL_FALSE:
        return False
    raise ValidationError(f"row {row_no}: {field} must be boolean, got {value!r}")


def parse_positive_float(value: str, *, field: str, row_no: int) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"row {row_no}: {field} must be numeric") from exc
    if not math.isfinite(x) or x <= 0:
        raise ValidationError(f"row {row_no}: {field} must be finite and > 0")
    return x


def load_window_ids(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or "window_id" not in reader.fieldnames:
            raise ValidationError("Chapter-2 window table must contain window_id")
        ids: set[str] = set()
        for row_no, row in enumerate(reader, start=2):
            window_id = row["window_id"].strip()
            if not window_id:
                raise ValidationError(f"window table row {row_no}: window_id is required")
            if window_id in ids:
                raise ValidationError(
                    f"window table row {row_no}: duplicate window_id {window_id!r}"
                )
            ids.add(window_id)
        return ids


def validate_ledger(path: Path, window_table: Path | None = None) -> dict[str, Any]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValidationError("ledger CSV has no header")
        missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames))
        if missing:
            raise ValidationError(f"missing required columns: {', '.join(missing)}")

        seen_windows: set[str] = set()
        seen_entries: set[str] = set()
        entry_counts = Counter()
        reason_counts = Counter()
        grid_ids: set[str] = set()
        total_exposure_seconds = 0.0

        for row_no, row in enumerate(reader, start=2):
            window_id = row["window_id"].strip()
            if not window_id:
                raise ValidationError(f"row {row_no}: window_id is required")
            if window_id in seen_windows:
                raise ValidationError(f"row {row_no}: duplicate window_id {window_id!r}")
            seen_windows.add(window_id)

            grid_id = row["exposure_grid_id"].strip()
            if not grid_id:
                raise ValidationError(f"row {row_no}: exposure_grid_id is required")
            grid_ids.add(grid_id)

            for field in (
                "system_id",
                "site_id",
                "camera_or_sensor_id",
                "recording_day",
                "recording_block_id",
                "window_start",
                "window_end",
                "exposure_source",
                "exposure_source_version",
                "record_entry_policy_version",
            ):
                if not row[field].strip():
                    raise ValidationError(f"row {row_no}: {field} is required")

            total_exposure_seconds += parse_positive_float(
                row["exposure_seconds"], field="exposure_seconds", row_no=row_no
            )

            exposure_expected = parse_bool(
                row["exposure_expected"], field="exposure_expected", row_no=row_no
            )
            primary_expected = parse_bool(
                row["primary_stream_expected"],
                field="primary_stream_expected",
                row_no=row_no,
            )
            entry_present = parse_bool(
                row["record_entry_present"],
                field="record_entry_present",
                row_no=row_no,
            )

            if not exposure_expected:
                raise ValidationError(
                    f"row {row_no}: ledger members must have exposure_expected=True"
                )

            reason = row["record_entry_reason"].strip().lower()
            if reason not in REASONS:
                raise ValidationError(
                    f"row {row_no}: invalid record_entry_reason {reason!r}"
                )

            entry_id = row["record_entry_id"].strip()
            entry_ts = row["record_entry_timestamp"].strip()

            if entry_present:
                if not primary_expected:
                    raise ValidationError(
                        f"row {row_no}: record entry cannot exist when primary_stream_expected=False"
                    )
                if not entry_id or not entry_ts:
                    raise ValidationError(
                        f"row {row_no}: entered exposure requires record_entry_id and timestamp"
                    )
                if reason != "entered":
                    raise ValidationError(
                        f"row {row_no}: record_entry_present=True requires reason='entered'"
                    )
                if entry_id in seen_entries:
                    raise ValidationError(
                        f"row {row_no}: duplicate record_entry_id {entry_id!r}"
                    )
                seen_entries.add(entry_id)
            else:
                if entry_id or entry_ts:
                    raise ValidationError(
                        f"row {row_no}: non-entered exposure must not fabricate record_entry_id/timestamp"
                    )
                if reason == "entered":
                    raise ValidationError(
                        f"row {row_no}: record_entry_present=False cannot use reason='entered'"
                    )

            entry_counts["entered" if entry_present else "shadow"] += 1
            reason_counts[reason] += 1

    if not seen_windows:
        raise ValidationError("ledger contains no exposure rows")

    missing_audit_ids: list[str] = []
    if window_table is not None:
        audit_ids = load_window_ids(window_table)
        missing_audit_ids = sorted(audit_ids - seen_windows)
        if missing_audit_ids:
            preview = ", ".join(missing_audit_ids[:5])
            raise ValidationError(
                f"Chapter-2 window table contains IDs absent from exposure ledger: {preview}"
            )

    n = len(seen_windows)
    entered = entry_counts["entered"]
    shadow = entry_counts["shadow"]
    return {
        "schema": "rec-master-exposure-ledger-validation-v1",
        "path": str(path),
        "exposure_grid_ids": sorted(grid_ids),
        "exposure_count": n,
        "total_exposure_seconds": total_exposure_seconds,
        "record_entry_counts": dict(entry_counts),
        "record_entry_reason_counts": dict(reason_counts),
        "record_entry_fraction": entered / n,
        "shadow_fraction": shadow / n,
        "window_table_crosschecked": window_table is not None,
        "note": (
            "The ledger establishes the exposure denominator and record-entry provenance only; "
            "biological event truth requires the separate Chapter-2 reference audit."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger_csv", type=Path)
    parser.add_argument("--window-table", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()

    try:
        summary = validate_ledger(args.ledger_csv, args.window_table)
    except ValidationError as exc:
        raise SystemExit(f"REC exposure-ledger validation failed: {exc}") from exc

    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
