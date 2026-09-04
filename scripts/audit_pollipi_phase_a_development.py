#!/usr/bin/env python3
"""Audit a PolliPi Phase-A TNOA log before it can enter H6 development calibration.

This is an intake/provenance gate, not a field-calibration procedure. It verifies
that a prospectively designated development/calibration recording is structurally
complete, fail-closed, joinable, and accompanied by an independent-reference plan.
It never licenses held-out scoring.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


class PhaseAIntakeError(ValueError):
    pass


REQUIRED_COLUMNS = {
    "log_schema_version",
    "run_id",
    "probe_timestamp",
    "device_id",
    "device_name",
    "site_id",
    "flower_id",
    "plant_species",
    "comparison_session_id",
    "camera_role",
    "method_mode",
    "record_kind",
    "schema_version",
    "calibration_status",
    "observation_state",
    "u_reason",
    "would_be_action",
    "action_applied",
    "target_calibrated_support",
    "nuisance_calibrated_support",
    "observability_calibrated_support",
    "coupled_calibrated_support",
    "absence_calibrated_support",
    "observability_frame_available",
    "observability_actual_probe_interval_sec",
}


def _bool(value: str, field: str) -> bool:
    x = str(value).strip().lower()
    if x in {"1", "true", "t", "yes", "y"}:
        return True
    if x in {"0", "false", "f", "no", "n"}:
        return False
    raise PhaseAIntakeError(f"{field} must be boolean, got {value!r}")


def _float_or_none(value: str, field: str) -> float | None:
    x = str(value).strip()
    if not x:
        return None
    try:
        out = float(x)
    except ValueError as exc:
        raise PhaseAIntakeError(f"{field} must be numeric when present") from exc
    if not math.isfinite(out):
        raise PhaseAIntakeError(f"{field} must be finite")
    return out


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise PhaseAIntakeError("Phase-A log has no header")
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise PhaseAIntakeError(
                "Phase-A log missing: " + ", ".join(sorted(missing))
            )
        rows = list(reader)
    if not rows:
        raise PhaseAIntakeError("Phase-A log is empty")
    return rows


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PhaseAIntakeError(f"invalid collection manifest: {exc}") from exc
    if not isinstance(data, dict):
        raise PhaseAIntakeError("collection manifest must be a JSON object")
    return data


def audit(
    rows: list[dict[str, str]], manifest: dict[str, Any], *, min_rows: int = 3
) -> dict[str, Any]:
    if min_rows < 1:
        raise PhaseAIntakeError("min_rows must be >=1")

    role = str(manifest.get("prospective_role", "")).strip().lower()
    if role not in {"development", "calibration"}:
        raise PhaseAIntakeError(
            "prospective_role must be development or calibration for this intake gate"
        )

    required_manifest = [
        "collection_id",
        "prospective_role",
        "recording_day",
        "focal_scene_id",
        "recording_block",
        "reference_source_id",
        "primary_device_id",
        "site_id",
        "flower_id",
        "comparison_session_id",
    ]
    missing_manifest = [
        key for key in required_manifest if not str(manifest.get(key, "")).strip()
    ]

    reference_expected = manifest.get("independent_reference_expected") is True
    reference_recorded = manifest.get("independent_reference_recorded") is True

    run_ids = {r["run_id"].strip() for r in rows}
    device_ids = {r["device_id"].strip() for r in rows}
    site_ids = {r["site_id"].strip() for r in rows}
    flower_ids = {r["flower_id"].strip() for r in rows}
    sessions = {r["comparison_session_id"].strip() for r in rows}
    camera_roles = {r["camera_role"].strip() for r in rows}
    methods = {r["method_mode"].strip() for r in rows}

    timestamps: list[datetime] = []
    frame_available = 0
    timed_rows = 0
    duplicate_time_keys = 0
    seen_time_keys: set[tuple[str, str]] = set()
    fail_closed_violations: list[int] = []
    schema_violations: list[int] = []

    for idx, row in enumerate(rows, start=2):
        if (
            row["log_schema_version"].strip() != "tnoa-observation-log-1"
            or row["schema_version"].strip() != "tnoa-shadow-1"
        ):
            schema_violations.append(idx)

        action_applied = _bool(row["action_applied"], "action_applied")
        calibrated_fields = [
            row["target_calibrated_support"].strip(),
            row["nuisance_calibrated_support"].strip(),
            row["observability_calibrated_support"].strip(),
            row["coupled_calibrated_support"].strip(),
            row["absence_calibrated_support"].strip(),
        ]
        if not (
            row["calibration_status"].strip() == "unavailable"
            and row["observation_state"].strip() == "U"
            and row["would_be_action"].strip() == "observe_only"
            and not action_applied
            and not any(calibrated_fields)
        ):
            fail_closed_violations.append(idx)

        timestamp_text = row["probe_timestamp"].strip()
        try:
            ts = datetime.fromisoformat(timestamp_text)
        except ValueError as exc:
            raise PhaseAIntakeError(
                f"row {idx}: invalid probe_timestamp {timestamp_text!r}"
            ) from exc
        timestamps.append(ts)
        key = (row["run_id"].strip(), timestamp_text)
        if key in seen_time_keys:
            duplicate_time_keys += 1
        seen_time_keys.add(key)

        frame_available += int(
            _bool(row["observability_frame_available"], "observability_frame_available")
        )
        if _float_or_none(
            row["observability_actual_probe_interval_sec"],
            "observability_actual_probe_interval_sec",
        ) is not None:
            timed_rows += 1

    chronological = all(a <= b for a, b in zip(timestamps, timestamps[1:]))
    elapsed_seconds = (
        (max(timestamps) - min(timestamps)).total_seconds() if len(timestamps) > 1 else 0.0
    )

    metadata_match = {
        "primary_device_id": device_ids == {str(manifest.get("primary_device_id", "")).strip()},
        "site_id": site_ids == {str(manifest.get("site_id", "")).strip()},
        "flower_id": flower_ids == {str(manifest.get("flower_id", "")).strip()},
        "comparison_session_id": sessions
        == {str(manifest.get("comparison_session_id", "")).strip()},
    }

    checks = {
        "minimum_rows_met": len(rows) >= min_rows,
        "single_run_id": len(run_ids) == 1 and "" not in run_ids,
        "single_device_id": len(device_ids) == 1 and "" not in device_ids,
        "site_id_present": len(site_ids) == 1 and "" not in site_ids,
        "flower_id_present": len(flower_ids) == 1 and "" not in flower_ids,
        "comparison_session_present": len(sessions) == 1 and "" not in sessions,
        "camera_role_present": len(camera_roles) == 1 and "" not in camera_roles,
        "method_mode_present": len(methods) == 1 and "" not in methods,
        "schemas_valid": not schema_violations,
        "fail_closed_shadow_only": not fail_closed_violations,
        "timestamps_chronological": chronological,
        "probe_time_keys_unique": duplicate_time_keys == 0,
        "all_frames_available": frame_available == len(rows),
        "measured_probe_timing_present": timed_rows > 0,
        "collection_manifest_complete": not missing_manifest,
        "prospective_role_not_heldout": role in {"development", "calibration"},
        "independent_reference_expected": reference_expected,
        "independent_reference_recorded": reference_recorded,
        "manifest_metadata_matches_log": all(metadata_match.values()),
    }

    structural_required = [
        "minimum_rows_met",
        "single_run_id",
        "single_device_id",
        "site_id_present",
        "flower_id_present",
        "comparison_session_present",
        "camera_role_present",
        "method_mode_present",
        "schemas_valid",
        "fail_closed_shadow_only",
        "timestamps_chronological",
        "probe_time_keys_unique",
        "all_frames_available",
        "measured_probe_timing_present",
        "collection_manifest_complete",
        "prospective_role_not_heldout",
        "independent_reference_expected",
        "manifest_metadata_matches_log",
    ]
    structural_failures = [name for name in structural_required if not checks[name]]

    # Reference material may be intentionally collected by a separate system and
    # archived after the primary log. Structural intake can pass before that file
    # arrives, but calibration truth preparation cannot.
    suitable_for_phase_b_preparation = not structural_failures and reference_recorded

    return {
        "schema": "rec-pollipi-phase-a-development-intake-v1",
        "collection_id": manifest.get("collection_id"),
        "prospective_role": role,
        "row_count": len(rows),
        "run_ids": sorted(run_ids),
        "elapsed_seconds": elapsed_seconds,
        "frame_available_fraction": frame_available / len(rows),
        "timed_row_fraction": timed_rows / len(rows),
        "metadata": {
            "device_ids": sorted(device_ids),
            "site_ids": sorted(site_ids),
            "flower_ids": sorted(flower_ids),
            "comparison_session_ids": sorted(sessions),
            "camera_roles": sorted(camera_roles),
            "method_modes": sorted(methods),
            "recording_day": manifest.get("recording_day"),
            "focal_scene_id": manifest.get("focal_scene_id"),
            "recording_block": manifest.get("recording_block"),
            "reference_source_id": manifest.get("reference_source_id"),
        },
        "checks": checks,
        "structural_failures": structural_failures,
        "metadata_match": metadata_match,
        "schema_violation_rows": schema_violations,
        "fail_closed_violation_rows": fail_closed_violations,
        "duplicate_probe_time_keys": duplicate_time_keys,
        "structurally_valid_phase_a_development_log": not structural_failures,
        "suitable_for_phase_b_truth_preparation": suitable_for_phase_b_preparation,
        "interpretation": (
            "Passing this audit only establishes that the prospectively designated Phase-A development/calibration log is structurally suitable for blinded Phase-B truth preparation. "
            "It does not freeze field thresholds, license held-out scoring, or establish REC-H6. Independent reference material must also be recorded before truth annotation begins."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase_a_csv", type=Path)
    parser.add_argument("collection_manifest_json", type=Path)
    parser.add_argument("--min-rows", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-phase-b-ready", action="store_true")
    args = parser.parse_args()

    try:
        result = audit(
            _load_csv(args.phase_a_csv),
            _load_manifest(args.collection_manifest_json),
            min_rows=args.min_rows,
        )
    except PhaseAIntakeError as exc:
        raise SystemExit(f"PolliPi Phase-A development intake failed: {exc}") from exc

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")

    if result["structural_failures"]:
        raise SystemExit("Phase-A development intake failed structural checks")
    if args.require_phase_b_ready and not result["suitable_for_phase_b_truth_preparation"]:
        raise SystemExit("Phase-A development intake is not ready for Phase-B truth preparation")


if __name__ == "__main__":
    main()
