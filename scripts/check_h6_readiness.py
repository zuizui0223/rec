#!/usr/bin/env python3
"""Fail-closed readiness audit for same-system REC -> TNOA H6 scoring."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class H6ReadinessError(ValueError):
    pass


def _present(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def audit(payload: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}

    checks["schema_known"] = payload.get("schema") == "tnoa-field-calibration-manifest-v1"
    checks["frozen_field_calibration"] = payload.get("status") == "frozen_field_calibration"
    checks["heldout_scoring_allowed"] = payload.get("heldout_scoring_allowed") is True
    checks["independent_reference_truth_required"] = (
        payload.get("independent_reference_truth_required") is True
    )

    split_group = payload.get("split_group")
    checks["grouped_split_declared"] = isinstance(split_group, list) and len(split_group) > 0
    details["split_group"] = split_group

    target = payload.get("target") if isinstance(payload.get("target"), dict) else {}
    checks["target_high_threshold_frozen"] = _present(target.get("high_threshold"))
    checks["target_low_threshold_frozen"] = _present(target.get("low_threshold"))
    checks["target_error_criterion_frozen"] = _present(
        target.get("operational_error_criterion")
    )

    nuisance = payload.get("nuisance") if isinstance(payload.get("nuisance"), dict) else {}
    checks["nuisance_error_criterion_frozen"] = _present(
        nuisance.get("familywise_false_attribution_alpha")
    )
    families = nuisance.get("families")
    checks["nuisance_families_declared"] = isinstance(families, list) and len(families) > 0

    observability = (
        payload.get("observability")
        if isinstance(payload.get("observability"), dict)
        else {}
    )
    checks["observability_support_rule_frozen"] = _present(
        observability.get("support_rule")
    )
    checks["observability_observable_thresholds_frozen"] = _present(
        observability.get("observable_thresholds")
    )
    checks["observability_unobservable_thresholds_frozen"] = _present(
        observability.get("unobservable_thresholds")
    )

    checks["source_observation_schema_declared"] = _present(
        payload.get("source_observation_schema")
    )
    checks["source_log_schema_declared"] = _present(payload.get("source_log_schema"))
    checks["truth_annotation_schema_declared"] = _present(
        payload.get("truth_annotation_schema")
    )

    minimum_double = payload.get("minimum_double_annotation_fraction")
    checks["double_annotation_fraction_valid"] = (
        isinstance(minimum_double, (int, float)) and 0 <= minimum_double <= 1
    )
    details["minimum_double_annotation_fraction"] = minimum_double

    hard_required = [
        "schema_known",
        "frozen_field_calibration",
        "heldout_scoring_allowed",
        "independent_reference_truth_required",
        "grouped_split_declared",
        "target_high_threshold_frozen",
        "target_low_threshold_frozen",
        "target_error_criterion_frozen",
        "nuisance_error_criterion_frozen",
        "nuisance_families_declared",
        "observability_support_rule_frozen",
        "observability_observable_thresholds_frozen",
        "observability_unobservable_thresholds_frozen",
        "source_observation_schema_declared",
        "source_log_schema_declared",
        "truth_annotation_schema_declared",
        "double_annotation_fraction_valid",
    ]
    failures = [name for name in hard_required if not checks.get(name, False)]

    return {
        "schema": "rec-h6-readiness-audit-v1",
        "manifest_schema": payload.get("schema"),
        "manifest_status": payload.get("status"),
        "heldout_scoring_allowed": payload.get("heldout_scoring_allowed"),
        "live_tnoa_capture_actions_allowed": payload.get(
            "live_tnoa_capture_actions_allowed"
        ),
        "ready_for_h6_heldout_scoring": not failures,
        "checks": checks,
        "hard_failures": failures,
        "details": details,
        "interpretation": (
            "This gate licenses only readiness for held-out H6 scoring. It does not establish REC-H6 itself, "
            "which additionally requires joined REC exposure/entry rows, TNOA field scores and independent held-out truth."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("calibration_manifest", type=Path)
    parser.add_argument("--output", type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--expect-ready", action="store_true")
    group.add_argument("--expect-not-ready", action="store_true")
    args = parser.parse_args()

    try:
        payload = json.loads(args.calibration_manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"H6 readiness audit failed to load manifest: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("H6 readiness audit requires a JSON object manifest")

    result = audit(payload)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")

    ready = bool(result["ready_for_h6_heldout_scoring"])
    if args.expect_ready and not ready:
        raise SystemExit("H6 readiness expectation failed: manifest is not ready")
    if args.expect_not_ready and ready:
        raise SystemExit("H6 readiness expectation failed: manifest unexpectedly became ready")


if __name__ == "__main__":
    main()
