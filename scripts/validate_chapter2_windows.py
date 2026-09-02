#!/usr/bin/env python3
"""Validate the REC / Chapter-2 exposure, gate and record-entry contract.

Fail closed: the validator checks structural invariants only. It does not infer
missing truth, convert not-evaluable exposures to baseline, reconstruct an
unknown denominator, repair contradictory rows, or calibrate a gate.
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
    "gate_evaluable",
    "registered_deviation",
    "gate_not_evaluable_reason",
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
    require_text(row, "exposure_source", row_no)
    require_text(row, "exposure_source_version", row_no)
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
    require_text(row, "pregate_evidence_version", row_no)

    gate_evaluable = parse_bool(row["gate_evaluable"], field="gate_evaluable", row_no=row_no)
    registered_deviation = parse_bool(
        row["registered_deviation"], field="registered_deviation", row_no=row_no
    )
    gate_inputs_complete = parse_bool(
        row["gate_inputs_complete"], field="gate_inputs_complete", row_no=row_no
    )
    not_eval_reason = row["gate_not_evaluable_reason"].strip()

    if gate_evaluable:
        if not primary_available or not gate_inputs_complete:
            raise ValidationError(
                f"row {row_no}: evaluable gate requires available primary stream and complete gate inputs"
            )
        if not_eval_reason:
            raise ValidationError(
                f"row {row_no}: evaluable gate must not carry gate_not_evaluable_reason"
            )
    else:
        if registered_deviation:
            raise ValidationError(
                f"row {row_no}: not-evaluable gate cannot register a deviation"
            )
        if not not_eval_reason:
            raise ValidationError(
                f"row {row_no}: not-evaluable gate requires gate_not_evaluable_reason"
            )

    gate_type = row["gate_type"].strip().lower()
    if gate_type not in GATE_TYPES:
        raise ValidationError(f"row {row_no}: gate_type must be scalar or composite")
    require_text(row, "gate_version", row_no)
    require_text(row, "gate_configuration_id", row_no)

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

    record_entry_present = parse_bool(
        row["record_entry_present"], field="record_entry_present", row_no=row_no
    )
    require_text(row, "entry_policy_version", row_no)
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

    absorbed = (
        truth_sampled
        and target_truth == "positive"
        and gate_evaluable
        and not registered_deviation
    )
    unevaluable_event = truth_sampled and target_truth == "positive" and not gate_evaluable
    shadow_event = truth_sampled and target_truth == "positive" and not record_entry_present

    derived_flags = {
        "threshold_absorbed_event": absorbed,
        "gate_unevaluable_event": unevaluable_event,
        "shadow_event": shadow_event,
    }
    for field, expected in derived_flags.items():
        if field in row and row[field].strip():
            supplied = parse_bool(row[field], field=field, row_no=row_no)
            if supplied != expected:
                raise ValidationError(
                    f"row {row_no}: {field} disagrees with truth/pipeline derivation"
                )

    return {
        "exposure_grid_id": exposure_grid_id,
        "split": split,
        "exposure_seconds": exposure,
        "gate_evaluable": gate_evaluable,
        "registered_deviation": registered_deviation,
        "record_entry_present": record_entry_present,
        "target_truth": target_truth,
        "truth_sampled": truth_sampled,
        "threshold_absorbed": absorbed,
        "gate_unevaluable_event": unevaluable_event,
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
        gate_counts = Counter()
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
            if not result["gate_evaluable"]:
                gate_counts["not_evaluable"] += 1
            elif result["registered_deviation"]:
                gate_counts["deviation"] += 1
            else:
                gate_counts["baseline"] += 1
            entry_counts["entered" if result["record_entry_present"] else "shadow"] += 1

            if result["truth_sampled"]:
                truth_counts[result["target_truth"]] += 1
                if result["threshold_absorbed"]:
                    truth_counts["threshold_absorbed"] += 1
                if result["gate_unevaluable_event"]:
                    truth_counts["gate_unevaluable_event"] += 1
                if result["shadow_event"]:
                    truth_counts["shadow_event"] += 1
            records.append(result)

    if not records:
        raise ValidationError("CSV contains no data rows")

    sampled_baseline = sum(
        1
        for r in records
        if r["truth_sampled"] and r["gate_evaluable"] and not r["registered_deviation"]
    )
    if sampled_baseline == 0:
        raise ValidationError(
            "REC requires at least one truth-sampled evaluable logical-baseline window"
        )

    not_evaluable_exists = any(not r["gate_evaluable"] for r in records)
    sampled_not_evaluable = sum(
        1 for r in records if r["truth_sampled"] and not r["gate_evaluable"]
    )
    if not_evaluable_exists and sampled_not_evaluable == 0:
        raise ValidationError(
            "REC contains not-evaluable exposures but none are truth-sampled"
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
    sampled_baseline_resolved = sum(
        1
        for r in records
        if r["truth_sampled"]
        and r["gate_evaluable"]
        and not r["registered_deviation"]
        and r["target_truth"] in {"positive", "negative"}
    )
    sampled_unevaluable_resolved = sum(
        1
        for r in records
        if r["truth_sampled"]
        and not r["gate_evaluable"]
        and r["target_truth"] in {"positive", "negative"}
    )
    sampled_shadow_resolved = sum(
        1
        for r in records
        if r["truth_sampled"]
        and not r["record_entry_present"]
        and r["target_truth"] in {"positive", "negative"}
    )

    threshold_absorbed = truth_counts["threshold_absorbed"]
    unevaluable_events = truth_counts["gate_unevaluable_event"]
    shadow_events = truth_counts["shadow_event"]

    q_b = threshold_absorbed / sampled_baseline_resolved if sampled_baseline_resolved else None
    q_u = unevaluable_events / sampled_unevaluable_resolved if sampled_unevaluable_resolved else None
    a_b = threshold_absorbed / sampled_positive if sampled_positive else None
    a_u = unevaluable_events / sampled_positive if sampled_positive else None
    a_pre = (
        (threshold_absorbed + unevaluable_events) / sampled_positive
        if sampled_positive
        else None
    )
    q_shadow = shadow_events / sampled_shadow_resolved if sampled_shadow_resolved else None
    a_k = shadow_events / sampled_positive if sampled_positive else None

    return {
        "schema": "rec-record-entry-window-validation-v3",
        "path": str(path),
        "row_count": len(records),
        "exposure_grid_counts": dict(exposure_grids),
        "gate_state_counts": dict(gate_counts),
        "record_entry_counts": dict(entry_counts),
        "sampled_truth_counts": dict(truth_counts),
        "truth_sampled_evaluable_baseline_windows": sampled_baseline,
        "truth_sampled_not_evaluable_windows": sampled_not_evaluable,
        "truth_sampled_shadow_windows": sampled_shadow,
        "unweighted_descriptive_q_B": q_b,
        "unweighted_descriptive_q_gate_unevaluable": q_u,
        "unweighted_descriptive_event_baseline_absorption": a_b,
        "unweighted_descriptive_event_gate_unevaluable": a_u,
        "unweighted_descriptive_event_not_registered": a_pre,
        "unweighted_descriptive_q_shadow": q_shadow,
        "unweighted_descriptive_event_nonentry": a_k,
        "note": (
            "Descriptive unweighted values are diagnostics only. Confirmatory population "
            "estimates must respect the frozen truth-sampling design, master exposure universe, "
            "gate evaluability, entry policy and independent-unit structure."
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
