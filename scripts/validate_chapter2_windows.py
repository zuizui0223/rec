#!/usr/bin/env python3
"""Validate the REC / Chapter-2 record-entry observation-window contract.

This validator is intentionally fail-closed. It checks structural invariants that
must hold before a confirmatory REC table is analyzed. It does not infer missing
truth, reconstruct an unknown exposure denominator, repair contradictory rows,
or calibrate a gate/entry policy.
"""
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
    "exposure_source",
    "exposure_source_version",
    "exposure_defined_independently_of_gate",
    "system_id",
    "site_id",
    "camera_or_sensor_id",
    "recording_day",
    "recording_block_id",
    "window_id",
    "window_start",
    "window_end",
    "exposure_seconds",
    "development_or_heldout",
    "primary_stream_available",
    "pregate_evidence_version",
    "registered_deviation",
    "gate_type",
    "gate_version",
    "gate_configuration_id",
    "gate_threshold",
    "gate_inputs_complete",
    "record_entry_present",
    "entry_policy_version",
    "entry_policy_type",
    "entry_policy_inputs_complete",
    "target_truth",
    "target_truth_source",
    "target_event_definition_version",
    "truth_sampled",
    "truth_sampling_design_version",
    "truth_sampling_stratum",
    "truth_inclusion_probability",
    "truth_sampling_weight",
    "annotator_blinded_to_gate",
    "annotator_blinded_to_entry",
    "annotator_blinded_to_scores",
}

BOOL_TRUE = {"1", "true", "t", "yes", "y"}
BOOL_FALSE = {"0", "false", "f", "no", "n"}
SPLITS = {"development", "heldout"}
TRUTH = {"positive", "negative", "unresolved"}
GATE_TYPES = {"scalar", "composite"}
ENTRY_POLICY_TYPES = {"trigger_only", "fixed_schedule", "hybrid", "postcapture_filter", "other"}


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


def parse_probability(value: str, *, field: str, row_no: int) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"row {row_no}: {field} must be numeric") from exc
    if not math.isfinite(x) or not (0 < x <= 1):
        raise ValidationError(f"row {row_no}: {field} must lie in (0,1]")
    return x


def require_text(row: dict[str, str], field: str, row_no: int) -> str:
    text = row[field].strip()
    if not text:
        raise ValidationError(f"row {row_no}: {field} is required")
    return text


def validate_row(row: dict[str, str], row_no: int) -> dict[str, Any]:
    exposure_grid_id = require_text(row, "exposure_grid_id", row_no)
    exposure_source = require_text(row, "exposure_source", row_no)
    exposure_source_version = require_text(row, "exposure_source_version", row_no)
    exposure_independent = parse_bool(
        row["exposure_defined_independently_of_gate"],
        field="exposure_defined_independently_of_gate",
        row_no=row_no,
    )
    if not exposure_independent:
        raise ValidationError(
            f"row {row_no}: REC requires an exposure universe defined independently of the tested gate"
        )

    split = row["development_or_heldout"].strip().lower()
    if split not in SPLITS:
        raise ValidationError(
            f"row {row_no}: development_or_heldout must be one of {sorted(SPLITS)}"
        )

    exposure = parse_positive_float(row["exposure_seconds"], field="exposure_seconds", row_no=row_no)
    primary_available = parse_bool(
        row["primary_stream_available"], field="primary_stream_available", row_no=row_no
    )
    registered_deviation = parse_bool(
        row["registered_deviation"], field="registered_deviation", row_no=row_no
    )
    gate_inputs_complete = parse_bool(
        row["gate_inputs_complete"], field="gate_inputs_complete", row_no=row_no
    )

    gate_type = row["gate_type"].strip().lower()
    if gate_type not in GATE_TYPES:
        raise ValidationError(f"row {row_no}: gate_type must be scalar or composite")
    require_text(row, "gate_version", row_no)
    require_text(row, "gate_configuration_id", row_no)
    require_text(row, "pregate_evidence_version", row_no)

    threshold_text = row["gate_threshold"].strip()
    if gate_type == "scalar":
        if not threshold_text:
            raise ValidationError(f"row {row_no}: scalar gate requires gate_threshold")
        try:
            threshold = float(threshold_text)
        except ValueError as exc:
            raise ValidationError(f"row {row_no}: gate_threshold must be numeric") from exc
        if not math.isfinite(threshold):
            raise ValidationError(f"row {row_no}: gate_threshold must be finite")
    elif threshold_text:
        raise ValidationError(
            f"row {row_no}: composite gate must not invent a scalar gate_threshold"
        )

    if registered_deviation and (not primary_available or not gate_inputs_complete):
        raise ValidationError(
            f"row {row_no}: registered deviation requires available primary stream and complete gate inputs"
        )

    record_entry_present = parse_bool(
        row["record_entry_present"], field="record_entry_present", row_no=row_no
    )
    entry_policy_version = require_text(row, "entry_policy_version", row_no)
    entry_policy_type = row["entry_policy_type"].strip().lower()
    if entry_policy_type not in ENTRY_POLICY_TYPES:
        raise ValidationError(
            f"row {row_no}: entry_policy_type must be one of {sorted(ENTRY_POLICY_TYPES)}"
        )
    entry_policy_inputs_complete = parse_bool(
        row["entry_policy_inputs_complete"],
        field="entry_policy_inputs_complete",
        row_no=row_no,
    )
    if record_entry_present and not entry_policy_inputs_complete:
        raise ValidationError(
            f"row {row_no}: present record entry requires complete entry-policy inputs"
        )

    target_truth = row["target_truth"].strip().lower()
    if target_truth not in TRUTH:
        raise ValidationError(f"row {row_no}: invalid target_truth {target_truth!r}")
    require_text(row, "target_truth_source", row_no)
    require_text(row, "target_event_definition_version", row_no)

    truth_sampled = parse_bool(row["truth_sampled"], field="truth_sampled", row_no=row_no)
    blinded_gate = parse_bool(
        row["annotator_blinded_to_gate"], field="annotator_blinded_to_gate", row_no=row_no
    )
    blinded_entry = parse_bool(
        row["annotator_blinded_to_entry"], field="annotator_blinded_to_entry", row_no=row_no
    )
    blinded_scores = parse_bool(
        row["annotator_blinded_to_scores"], field="annotator_blinded_to_scores", row_no=row_no
    )

    sampling_weight = None
    inclusion_probability = None
    if truth_sampled:
        for field in (
            "truth_sampling_design_version",
            "truth_sampling_stratum",
            "truth_inclusion_probability",
            "truth_sampling_weight",
        ):
            if not row[field].strip():
                raise ValidationError(f"row {row_no}: sampled truth requires {field}")
        inclusion_probability = parse_probability(
            row["truth_inclusion_probability"],
            field="truth_inclusion_probability",
            row_no=row_no,
        )
        sampling_weight = parse_positive_float(
            row["truth_sampling_weight"], field="truth_sampling_weight", row_no=row_no
        )
        expected = 1.0 / inclusion_probability
        if not math.isclose(sampling_weight, expected, rel_tol=1e-6, abs_tol=1e-9):
            raise ValidationError(
                f"row {row_no}: truth_sampling_weight must equal 1/inclusion_probability"
            )
    elif target_truth != "unresolved":
        raise ValidationError(
            f"row {row_no}: unsampled truth cannot carry resolved target_truth"
        )

    absorbed = truth_sampled and target_truth == "positive" and not registered_deviation
    shadow_event = truth_sampled and target_truth == "positive" and not record_entry_present

    if "threshold_absorbed_event" in row and row["threshold_absorbed_event"].strip():
        supplied_absorbed = parse_bool(
            row["threshold_absorbed_event"], field="threshold_absorbed_event", row_no=row_no
        )
        if supplied_absorbed != absorbed:
            raise ValidationError(
                f"row {row_no}: threshold_absorbed_event disagrees with truth/gate derivation"
            )

    if "shadow_event" in row and row["shadow_event"].strip():
        supplied_shadow = parse_bool(row["shadow_event"], field="shadow_event", row_no=row_no)
        if supplied_shadow != shadow_event:
            raise ValidationError(
                f"row {row_no}: shadow_event disagrees with truth/record-entry derivation"
            )

    return {
        "exposure_grid_id": exposure_grid_id,
        "exposure_source": exposure_source,
        "exposure_source_version": exposure_source_version,
        "split": split,
        "exposure_seconds": exposure,
        "registered_deviation": registered_deviation,
        "record_entry_present": record_entry_present,
        "entry_policy_version": entry_policy_version,
        "entry_policy_type": entry_policy_type,
        "target_truth": target_truth,
        "truth_sampled": truth_sampled,
        "threshold_absorbed": absorbed,
        "shadow_event": shadow_event,
        "truth_inclusion_probability": inclusion_probability,
        "truth_sampling_weight": sampling_weight,
        "annotator_blinded_to_gate": blinded_gate,
        "annotator_blinded_to_entry": blinded_entry,
        "annotator_blinded_to_scores": blinded_scores,
    }


def validate_csv(path: Path) -> dict[str, Any]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValidationError("CSV has no header")
        missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames))
        if missing:
            raise ValidationError(f"missing required columns: {', '.join(missing)}")

        seen_windows: set[str] = set()
        seen_groups: dict[tuple[str, str, str], str] = {}
        records: list[dict[str, Any]] = []
        registered_counts = Counter()
        entry_counts = Counter()
        truth_counts = Counter()
        exposure_grids = Counter()

        for row_no, row in enumerate(reader, start=2):
            window_id = row["window_id"].strip()
            if not window_id:
                raise ValidationError(f"row {row_no}: window_id is required")
            if window_id in seen_windows:
                raise ValidationError(f"row {row_no}: duplicate window_id {window_id!r}")
            seen_windows.add(window_id)

            result = validate_row(row, row_no)
            group = (
                row["recording_day"].strip(),
                row["camera_or_sensor_id"].strip(),
                row["recording_block_id"].strip(),
            )
            previous = seen_groups.get(group)
            if previous is not None and previous != result["split"]:
                raise ValidationError(
                    f"row {row_no}: development/heldout leakage within group {group}"
                )
            seen_groups[group] = result["split"]

            exposure_grids[result["exposure_grid_id"]] += 1
            registered_counts["deviation" if result["registered_deviation"] else "B"] += 1
            entry_counts["entered" if result["record_entry_present"] else "shadow"] += 1
            if result["truth_sampled"]:
                truth_counts[result["target_truth"]] += 1
                if result["threshold_absorbed"]:
                    truth_counts["threshold_absorbed"] += 1
                if result["shadow_event"]:
                    truth_counts["shadow_event"] += 1
            records.append(result)

    if not records:
        raise ValidationError("CSV contains no data rows")

    sampled_b = sum(
        1 for r in records if r["truth_sampled"] and not r["registered_deviation"]
    )
    if sampled_b == 0:
        raise ValidationError(
            "REC Chapter 2 requires at least one truth-sampled logical registered-B window"
        )

    nonentered_exists = any(not r["record_entry_present"] for r in records)
    sampled_shadow = sum(
        1 for r in records if r["truth_sampled"] and not r["record_entry_present"]
    )
    if nonentered_exists and sampled_shadow == 0:
        raise ValidationError(
            "REC contains non-entered exposures but no truth-sampled record-entry shadow window"
        )

    sampled_positive = truth_counts["positive"]
    sampled_b_resolved = sum(
        1
        for r in records
        if r["truth_sampled"]
        and not r["registered_deviation"]
        and r["target_truth"] in {"positive", "negative"}
    )
    sampled_shadow_resolved = sum(
        1
        for r in records
        if r["truth_sampled"]
        and not r["record_entry_present"]
        and r["target_truth"] in {"positive", "negative"}
    )

    q_b_unweighted = (
        truth_counts["threshold_absorbed"] / sampled_b_resolved
        if sampled_b_resolved
        else None
    )
    absorption_unweighted = (
        truth_counts["threshold_absorbed"] / sampled_positive if sampled_positive else None
    )
    q_shadow_unweighted = (
        truth_counts["shadow_event"] / sampled_shadow_resolved
        if sampled_shadow_resolved
        else None
    )
    nonentry_unweighted = (
        truth_counts["shadow_event"] / sampled_positive if sampled_positive else None
    )

    return {
        "schema": "rec-record-entry-window-validation-v2",
        "path": str(path),
        "row_count": len(records),
        "exposure_grid_counts": dict(exposure_grids),
        "registered_state_counts": dict(registered_counts),
        "record_entry_counts": dict(entry_counts),
        "sampled_truth_counts": dict(truth_counts),
        "truth_sampled_registered_B": sampled_b,
        "truth_sampled_shadow_windows": sampled_shadow,
        "unweighted_descriptive_q_B": q_b_unweighted,
        "unweighted_descriptive_event_absorption": absorption_unweighted,
        "unweighted_descriptive_q_shadow": q_shadow_unweighted,
        "unweighted_descriptive_event_nonentry": nonentry_unweighted,
        "note": (
            "Descriptive unweighted values are diagnostics only. Confirmatory population "
            "estimates must respect the frozen truth-sampling design, master exposure universe, "
            "entry policy and independent-unit structure."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()

    try:
        summary = validate_csv(args.csv_path)
    except ValidationError as exc:
        raise SystemExit(f"REC schema validation failed: {exc}") from exc

    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
