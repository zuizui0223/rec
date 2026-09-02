#!/usr/bin/env python3
"""Validate the Chapter-2 threshold-censoring observation-window contract.

This validator is intentionally fail-closed. It checks structural invariants that
must hold before a confirmatory Chapter-2 table is analyzed. It does not infer
missing truth, repair contradictory rows, or calibrate a gate.
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
    "target_truth",
    "target_truth_source",
    "target_event_definition_version",
    "truth_sampled",
    "truth_sampling_design_version",
    "truth_sampling_stratum",
    "truth_inclusion_probability",
    "truth_sampling_weight",
    "annotator_blinded_to_gate",
    "annotator_blinded_to_scores",
}

BOOL_TRUE = {"1", "true", "t", "yes", "y"}
BOOL_FALSE = {"0", "false", "f", "no", "n"}
SPLITS = {"development", "heldout"}
TRUTH = {"positive", "negative", "unresolved"}
GATE_TYPES = {"scalar", "composite"}


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


def validate_row(row: dict[str, str], row_no: int) -> dict[str, Any]:
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
    if not row["gate_version"].strip() or not row["gate_configuration_id"].strip():
        raise ValidationError(f"row {row_no}: gate version/configuration must be present")
    if not row["pregate_evidence_version"].strip():
        raise ValidationError(f"row {row_no}: pregate_evidence_version is required")

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

    target_truth = row["target_truth"].strip().lower()
    if target_truth not in TRUTH:
        raise ValidationError(f"row {row_no}: invalid target_truth {target_truth!r}")
    if not row["target_truth_source"].strip():
        raise ValidationError(f"row {row_no}: target_truth_source is required")
    if not row["target_event_definition_version"].strip():
        raise ValidationError(f"row {row_no}: target_event_definition_version is required")

    truth_sampled = parse_bool(row["truth_sampled"], field="truth_sampled", row_no=row_no)
    blinded_gate = parse_bool(
        row["annotator_blinded_to_gate"], field="annotator_blinded_to_gate", row_no=row_no
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
    else:
        if target_truth != "unresolved":
            raise ValidationError(
                f"row {row_no}: unsampled truth cannot carry resolved target_truth"
            )

    absorbed = truth_sampled and target_truth == "positive" and not registered_deviation

    if "threshold_absorbed_event" in row and row["threshold_absorbed_event"].strip():
        supplied_absorbed = parse_bool(
            row["threshold_absorbed_event"], field="threshold_absorbed_event", row_no=row_no
        )
        if supplied_absorbed != absorbed:
            raise ValidationError(
                f"row {row_no}: threshold_absorbed_event disagrees with truth/gate derivation"
            )

    return {
        "split": split,
        "exposure_seconds": exposure,
        "registered_deviation": registered_deviation,
        "target_truth": target_truth,
        "truth_sampled": truth_sampled,
        "threshold_absorbed": absorbed,
        "truth_inclusion_probability": inclusion_probability,
        "truth_sampling_weight": sampling_weight,
        "annotator_blinded_to_gate": blinded_gate,
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
        truth_counts = Counter()

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

            registered_counts["deviation" if result["registered_deviation"] else "B"] += 1
            if result["truth_sampled"]:
                truth_counts[result["target_truth"]] += 1
                if result["threshold_absorbed"]:
                    truth_counts["threshold_absorbed"] += 1
            records.append(result)

    if not records:
        raise ValidationError("CSV contains no data rows")

    sampled_b = sum(
        1 for r in records if r["truth_sampled"] and not r["registered_deviation"]
    )
    if sampled_b == 0:
        raise ValidationError(
            "Chapter 2 requires at least one truth-sampled registered-B window"
        )

    sampled_positive = truth_counts["positive"]
    sampled_b_resolved = sum(
        1
        for r in records
        if r["truth_sampled"]
        and not r["registered_deviation"]
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

    return {
        "schema": "rec-chapter2-window-validation-v1",
        "path": str(path),
        "row_count": len(records),
        "registered_state_counts": dict(registered_counts),
        "sampled_truth_counts": dict(truth_counts),
        "truth_sampled_registered_B": sampled_b,
        "unweighted_descriptive_q_B": q_b_unweighted,
        "unweighted_descriptive_event_absorption": absorption_unweighted,
        "note": (
            "Descriptive unweighted values are diagnostics only. Confirmatory population "
            "estimates must respect the frozen truth-sampling design and independent-unit structure."
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
        raise SystemExit(f"Chapter-2 schema validation failed: {exc}") from exc

    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
