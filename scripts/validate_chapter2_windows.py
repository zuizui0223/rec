#!/usr/bin/env python3
"""Validate the REC Chapter-2 truth/gate/entry observation-window contract.

Fail-closed: unavailable or non-evaluable primary observations are never silently
encoded as registered baseline.
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
    "primary_stream_expected",
    "primary_stream_available",
    "acquisition_status",
    "pregate_evidence_version",
    "gate_evaluable",
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
ENTRY_TYPES = {"trigger_only", "fixed_schedule", "hybrid", "postcapture_filter", "other"}
ACQUISITION_STATUSES = {
    "available",
    "planned_not_acquired",
    "hardware_failure",
    "corrupt_or_missing",
    "unknown_unavailable",
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


def parse_optional_bool(value: str, *, field: str, row_no: int) -> bool | None:
    text = str(value).strip()
    if not text:
        return None
    return parse_bool(text, field=field, row_no=row_no)


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
    if not parse_bool(
        row["exposure_defined_independently_of_gate"],
        field="exposure_defined_independently_of_gate",
        row_no=row_no,
    ):
        raise ValidationError(
            f"row {row_no}: REC exposure must be defined independently of the tested gate"
        )
    for field in ("exposure_grid_id", "exposure_source", "exposure_source_version"):
        require_text(row, field, row_no)

    split = row["development_or_heldout"].strip().lower()
    if split not in SPLITS:
        raise ValidationError(
            f"row {row_no}: development_or_heldout must be one of {sorted(SPLITS)}"
        )

    exposure = parse_positive_float(row["exposure_seconds"], field="exposure_seconds", row_no=row_no)
    primary_expected = parse_bool(
        row["primary_stream_expected"], field="primary_stream_expected", row_no=row_no
    )
    primary_available = parse_bool(
        row["primary_stream_available"], field="primary_stream_available", row_no=row_no
    )
    acquisition_status = row["acquisition_status"].strip().lower()
    if acquisition_status not in ACQUISITION_STATUSES:
        raise ValidationError(f"row {row_no}: invalid acquisition_status {acquisition_status!r}")
    if primary_available and acquisition_status != "available":
        raise ValidationError(
            f"row {row_no}: primary_stream_available=True requires acquisition_status='available'"
        )
    if not primary_available and acquisition_status == "available":
        raise ValidationError(
            f"row {row_no}: unavailable primary stream cannot use acquisition_status='available'"
        )
    if acquisition_status == "planned_not_acquired" and (
        primary_expected or primary_available
    ):
        raise ValidationError(
            f"row {row_no}: planned_not_acquired requires primary_stream_expected=False and unavailable stream"
        )
    require_text(row, "pregate_evidence_version", row_no)

    gate_evaluable = parse_bool(row["gate_evaluable"], field="gate_evaluable", row_no=row_no)
    gate_inputs_complete = parse_bool(
        row["gate_inputs_complete"], field="gate_inputs_complete", row_no=row_no
    )
    registered_deviation = parse_optional_bool(
        row["registered_deviation"], field="registered_deviation", row_no=row_no
    )

    if gate_evaluable:
        if not primary_available or not gate_inputs_complete:
            raise ValidationError(
                f"row {row_no}: evaluable gate requires available primary stream and complete gate inputs"
            )
        if registered_deviation is None:
            raise ValidationError(
                f"row {row_no}: evaluable gate requires registered_deviation true/false"
            )
    elif registered_deviation is not None:
        raise ValidationError(
            f"row {row_no}: non-evaluable gate must leave registered_deviation undefined, not false"
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

    entry_present = parse_bool(
        row["record_entry_present"], field="record_entry_present", row_no=row_no
    )
    entry_inputs_complete = parse_bool(
        row["entry_policy_inputs_complete"],
        field="entry_policy_inputs_complete",
        row_no=row_no,
    )
    entry_type = row["entry_policy_type"].strip().lower()
    if entry_type not in ENTRY_TYPES:
        raise ValidationError(f"row {row_no}: invalid entry_policy_type {entry_type!r}")
    require_text(row, "entry_policy_version", row_no)
    if entry_present and (not primary_available or not entry_inputs_complete):
        raise ValidationError(
            f"row {row_no}: record entry requires available primary stream and complete entry-policy inputs"
        )

    target_truth = row["target_truth"].strip().lower()
    if target_truth not in TRUTH:
        raise ValidationError(f"row {row_no}: invalid target_truth {target_truth!r}")
    require_text(row, "target_truth_source", row_no)
    require_text(row, "target_event_definition_version", row_no)

    truth_sampled = parse_bool(row["truth_sampled"], field="truth_sampled", row_no=row_no)
    parse_bool(row["annotator_blinded_to_gate"], field="annotator_blinded_to_gate", row_no=row_no)
    parse_bool(row["annotator_blinded_to_entry"], field="annotator_blinded_to_entry", row_no=row_no)
    parse_bool(row["annotator_blinded_to_scores"], field="annotator_blinded_to_scores", row_no=row_no)

    inclusion_probability = None
    sampling_weight = None
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
            row["truth_inclusion_probability"], field="truth_inclusion_probability", row_no=row_no
        )
        sampling_weight = parse_positive_float(
            row["truth_sampling_weight"], field="truth_sampling_weight", row_no=row_no
        )
        if not math.isclose(sampling_weight, 1.0 / inclusion_probability, rel_tol=1e-6, abs_tol=1e-9):
            raise ValidationError(
                f"row {row_no}: truth_sampling_weight must equal 1/inclusion_probability"
            )
    elif target_truth != "unresolved":
        raise ValidationError(
            f"row {row_no}: unsampled truth cannot carry resolved target_truth"
        )

    positive = truth_sampled and target_truth == "positive"
    threshold_absorbed = positive and gate_evaluable and registered_deviation is False
    shadow_event = positive and not entry_present

    if "threshold_absorbed_event" in row and row["threshold_absorbed_event"].strip():
        if not gate_evaluable:
            raise ValidationError(
                f"row {row_no}: threshold_absorbed_event is undefined when gate is not evaluable"
            )
        supplied = parse_bool(
            row["threshold_absorbed_event"], field="threshold_absorbed_event", row_no=row_no
        )
        if supplied != threshold_absorbed:
            raise ValidationError(
                f"row {row_no}: threshold_absorbed_event disagrees with truth/gate derivation"
            )
    if "shadow_event" in row and row["shadow_event"].strip():
        supplied = parse_bool(row["shadow_event"], field="shadow_event", row_no=row_no)
        if supplied != shadow_event:
            raise ValidationError(
                f"row {row_no}: shadow_event disagrees with truth/entry derivation"
            )

    return {
        "split": split,
        "exposure_seconds": exposure,
        "primary_stream_available": primary_available,
        "gate_evaluable": gate_evaluable,
        "registered_deviation": registered_deviation,
        "record_entry_present": entry_present,
        "target_truth": target_truth,
        "truth_sampled": truth_sampled,
        "threshold_absorbed": threshold_absorbed,
        "shadow_event": shadow_event,
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
        counts = Counter()

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

            counts["primary_available" if result["primary_stream_available"] else "acquisition_shadow"] += 1
            counts["gate_evaluable" if result["gate_evaluable"] else "gate_unevaluable"] += 1
            counts["entered" if result["record_entry_present"] else "nonentered"] += 1
            if result["truth_sampled"]:
                counts[f"truth_{result['target_truth']}"] += 1
                if result["threshold_absorbed"]:
                    counts["threshold_absorbed"] += 1
                if result["shadow_event"]:
                    counts["shadow_event"] += 1
            records.append(result)

    if not records:
        raise ValidationError("CSV contains no data rows")

    sampled_gate_b_resolved = [
        r for r in records
        if r["truth_sampled"] and r["gate_evaluable"]
        and r["registered_deviation"] is False
        and r["target_truth"] in {"positive", "negative"}
    ]
    if not sampled_gate_b_resolved:
        raise ValidationError(
            "Chapter 2 requires at least one truth-sampled, gate-evaluable registered-baseline window"
        )

    gate_positive = [
        r for r in records
        if r["truth_sampled"] and r["gate_evaluable"] and r["target_truth"] == "positive"
    ]
    nonentered_resolved = [
        r for r in records
        if r["truth_sampled"] and not r["record_entry_present"]
        and r["target_truth"] in {"positive", "negative"}
    ]
    all_positive = [r for r in records if r["truth_sampled"] and r["target_truth"] == "positive"]

    q_b = sum(r["threshold_absorbed"] for r in sampled_gate_b_resolved) / len(sampled_gate_b_resolved)
    a_r = (
        sum(r["threshold_absorbed"] for r in gate_positive) / len(gate_positive)
        if gate_positive else None
    )
    q_shadow = (
        sum(r["shadow_event"] for r in nonentered_resolved) / len(nonentered_resolved)
        if nonentered_resolved else None
    )
    a_k = (
        sum(r["shadow_event"] for r in all_positive) / len(all_positive)
        if all_positive else None
    )

    return {
        "schema": "rec-chapter2-window-validation-v3",
        "path": str(path),
        "row_count": len(records),
        "state_counts": dict(counts),
        "unweighted_descriptive_q_B_gate_evaluable": q_b,
        "unweighted_descriptive_event_absorption_given_gate_evaluable": a_r,
        "unweighted_descriptive_q_shadow": q_shadow,
        "unweighted_descriptive_event_nonentry": a_k,
        "note": (
            "Unweighted values are diagnostics only. Confirmatory estimates must use the frozen truth-sampling design, "
            "separate acquisition/gate/entry layers, and respect independent ecological units."
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
        raise SystemExit(f"REC Chapter-2 schema validation failed: {exc}") from exc

    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
