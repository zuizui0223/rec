#!/usr/bin/env python3
"""Compute design-weighted worst-case bounds induced by reference-unresolved truth.

These are ignorance/partial-identification bounds, not confidence intervals. They
condition on the frozen truth-sampling design and keep ordinary sampling
uncertainty separate.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_chapter2_windows import ValidationError, validate_csv  # noqa: E402


class BoundsError(ValueError):
    pass


def _bool(value: str, field: str) -> bool:
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y"}:
        return True
    if text in {"0", "false", "f", "no", "n"}:
        return False
    raise BoundsError(f"{field} must be boolean, got {value!r}")


def _optional_bool(value: str, field: str) -> bool | None:
    text = str(value).strip()
    if not text:
        return None
    return _bool(text, field)


def _weight(row: dict[str, str]) -> float:
    if not _bool(row["truth_sampled"], "truth_sampled"):
        return 0.0
    try:
        w = float(row["truth_sampling_weight"])
    except (TypeError, ValueError) as exc:
        raise BoundsError("truth-sampled row requires numeric truth_sampling_weight") from exc
    if not math.isfinite(w) or w <= 0:
        raise BoundsError("truth_sampling_weight must be finite and >0")
    return w


def _safe_ratio(num: float, den: float) -> float | None:
    return num / den if den > 0 else None


@dataclass
class WeightedTruth:
    positive: float = 0.0
    negative: float = 0.0
    unresolved: float = 0.0

    @property
    def total(self) -> float:
        return self.positive + self.negative + self.unresolved

    @property
    def resolved(self) -> float:
        return self.positive + self.negative

    def add(self, truth: str, weight: float) -> None:
        if truth == "positive":
            self.positive += weight
        elif truth == "negative":
            self.negative += weight
        elif truth == "unresolved":
            self.unresolved += weight
        else:
            raise BoundsError(f"invalid target_truth {truth!r}")

    def to_dict(self) -> dict[str, float]:
        return {
            "positive": self.positive,
            "negative": self.negative,
            "unresolved": self.unresolved,
            "resolved": self.resolved,
            "total": self.total,
        }


Predicate = Callable[[dict[str, Any]], bool]


def _contamination_bounds(h: WeightedTruth) -> dict[str, float | None]:
    resolved_only = _safe_ratio(h.positive, h.resolved)
    lower = _safe_ratio(h.positive, h.total)
    upper = _safe_ratio(h.positive + h.unresolved, h.total)
    width = None if lower is None or upper is None else upper - lower
    unresolved_fraction = _safe_ratio(h.unresolved, h.total)
    return {
        "resolved_only_estimate": resolved_only,
        "lower": lower,
        "upper": upper,
        "width": width,
        "unresolved_fraction": unresolved_fraction,
    }


def _loss_bounds(h: WeightedTruth, c: WeightedTruth) -> dict[str, float | None]:
    resolved_only = _safe_ratio(h.positive, h.positive + c.positive)
    lower = _safe_ratio(
        h.positive,
        h.positive + c.positive + c.unresolved,
    )
    upper = _safe_ratio(
        h.positive + h.unresolved,
        h.positive + h.unresolved + c.positive,
    )
    width = None if lower is None or upper is None else upper - lower
    return {
        "resolved_only_estimate": resolved_only,
        "lower": lower,
        "upper": upper,
        "width": width,
    }


def _normalize_row(row: dict[str, str]) -> dict[str, Any]:
    primary_available = _bool(row["primary_stream_available"], "primary_stream_available")
    gate_evaluable = _bool(row["gate_evaluable"], "gate_evaluable")
    registered = _optional_bool(row["registered_deviation"], "registered_deviation")
    entry = _bool(row["record_entry_present"], "record_entry_present")
    return {
        "raw": row,
        "primary_available": primary_available,
        "gate_evaluable": gate_evaluable,
        "registered_deviation": registered,
        "record_entry_present": entry,
        "truth": row["target_truth"].strip().lower(),
        "weight": _weight(row),
        "truth_sampled": _bool(row["truth_sampled"], "truth_sampled"),
    }


def _layer(
    rows: list[dict[str, Any]],
    *,
    name: str,
    h_predicate: Predicate,
    c_predicate: Predicate,
    target_predicate: Predicate | None = None,
    contamination_label: str,
    loss_label: str,
    conditioning: str,
) -> dict[str, Any]:
    h = WeightedTruth()
    c = WeightedTruth()
    target_total = WeightedTruth()

    for row in rows:
        if not row["truth_sampled"]:
            continue
        if target_predicate is not None and not target_predicate(row):
            continue
        weight = row["weight"]
        if weight <= 0:
            continue
        target_total.add(row["truth"], weight)
        in_h = h_predicate(row)
        in_c = c_predicate(row)
        if in_h and in_c:
            raise BoundsError(f"layer {name}: H and complement overlap")
        if not in_h and not in_c:
            raise BoundsError(f"layer {name}: target row is in neither H nor complement")
        (h if in_h else c).add(row["truth"], weight)

    return {
        "name": name,
        "conditioning": conditioning,
        "weighted_target_truth": target_total.to_dict(),
        "weighted_H_truth": h.to_dict(),
        "weighted_complement_truth": c.to_dict(),
        "contamination": {
            "estimand": contamination_label,
            **_contamination_bounds(h),
        },
        "event_loss": {
            "estimand": loss_label,
            **_loss_bounds(h, c),
        },
    }


def analyze(path: Path) -> dict[str, Any]:
    try:
        validation = validate_csv(path)
    except ValidationError as exc:
        raise BoundsError(f"input failed REC Chapter-2 validation: {exc}") from exc

    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise BoundsError("CSV has no header")
        rows = [_normalize_row(row) for row in reader]

    sampled = [r for r in rows if r["truth_sampled"]]
    overall = WeightedTruth()
    for row in sampled:
        overall.add(row["truth"], row["weight"])

    layers = [
        _layer(
            rows,
            name="acquisition_shadow",
            h_predicate=lambda r: not r["primary_available"],
            c_predicate=lambda r: r["primary_available"],
            contamination_label="P(E=1 | primary_stream_available=False)",
            loss_label="P(primary_stream_available=False | E=1)",
            conditioning="all truth-sampled master-exposure rows represented by the frozen design",
        ),
        _layer(
            rows,
            name="gate_unevaluable_shadow",
            h_predicate=lambda r: r["primary_available"] and not r["gate_evaluable"],
            c_predicate=lambda r: not (r["primary_available"] and not r["gate_evaluable"]),
            contamination_label="P(E=1 | primary available, gate_evaluable=False)",
            loss_label="P(primary available, gate_evaluable=False | E=1)",
            conditioning="all truth-sampled master-exposure rows represented by the frozen design",
        ),
        _layer(
            rows,
            name="gate_baseline_shadow",
            target_predicate=lambda r: r["gate_evaluable"],
            h_predicate=lambda r: r["registered_deviation"] is False,
            c_predicate=lambda r: r["registered_deviation"] is True,
            contamination_label="P(E=1 | R=0, gate_evaluable=True)",
            loss_label="P(R=0 | E=1, gate_evaluable=True)",
            conditioning="truth-sampled gate-evaluable exposures only",
        ),
        _layer(
            rows,
            name="record_nonentry_shadow",
            h_predicate=lambda r: not r["record_entry_present"],
            c_predicate=lambda r: r["record_entry_present"],
            contamination_label="P(E=1 | K=0)",
            loss_label="P(K=0 | E=1)",
            conditioning="all truth-sampled master-exposure rows represented by the frozen design",
        ),
    ]

    return {
        "schema": "rec-reference-unresolved-bounds-v1",
        "path": str(path),
        "chapter2_validation_schema": validation.get("schema"),
        "weighted_overall_truth": overall.to_dict(),
        "overall_reference_unresolved_fraction": _safe_ratio(overall.unresolved, overall.total),
        "layers": {layer["name"]: layer for layer in layers},
        "interpretation_boundary": (
            "Bounds are design-weighted worst-case envelopes induced only by truth-sampled reference-unresolved exposures. "
            "They are not confidence intervals, do not include sampling variance, and are not automatically exact finite-population identification intervals."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("truth_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        result = analyze(args.truth_csv)
    except BoundsError as exc:
        raise SystemExit(f"REC unresolved-bounds analysis failed: {exc}") from exc

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
