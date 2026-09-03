#!/usr/bin/env python3
"""Decompose BirdVox ecological distortion into upstream omission and false entry.

This diagnostic is deliberately additive to the frozen REC H1-H4 analysis. It does not
change Omega, the score, thresholds, or the ecological endpoint. For each frozen gate
it asks what ecological contrast would remain if a hypothetical perfect downstream
semantic stage removed every false entry but could not recover true events that never
entered the record.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


class OmissionError(ValueError):
    pass


def _bool(value: str, field: str) -> bool:
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y"}:
        return True
    if text in {"0", "false", "f", "no", "n"}:
        return False
    raise OmissionError(f"{field} must be boolean, got {value!r}")


def _float(value: str, field: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise OmissionError(f"{field} must be numeric, got {value!r}") from exc
    if not math.isfinite(out):
        raise OmissionError(f"{field} must be finite")
    return out


def _ratio(num: float, den: float) -> float | None:
    return num / den if den > 0 else None


def load_grid(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise OmissionError("grid has no header")
        needed = {
            "sensor_id",
            "split",
            "window_id",
            "window_start_seconds",
            "window_end_seconds",
            "truth_positive",
            "gate_evaluable",
            "max_score",
        }
        missing = needed - set(reader.fieldnames)
        if missing:
            raise OmissionError(f"grid missing: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise OmissionError("grid is empty")
    return rows


def summarize(rows: list[dict[str, str]], threshold: float) -> dict[str, Any]:
    heldout = [r for r in rows if r["split"].strip().lower() == "heldout"]
    if not heldout:
        raise OmissionError("no heldout rows")

    sensor_end: dict[str, float] = {}
    for row in heldout:
        sensor = row["sensor_id"].strip().zfill(2)
        sensor_end[sensor] = max(
            sensor_end.get(sensor, 0.0),
            _float(row["window_end_seconds"], "window_end_seconds"),
        )

    by_half: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    total = defaultdict(float)

    for row in heldout:
        sensor = row["sensor_id"].strip().zfill(2)
        truth = _bool(row["truth_positive"], "truth_positive")
        evaluable = _bool(row["gate_evaluable"], "gate_evaluable")
        score = _float(row["max_score"], "max_score") if evaluable else None
        registered = bool(evaluable and score is not None and score >= threshold)
        entered_true = truth and registered
        false_entry = (not truth) and registered

        start = _float(row["window_start_seconds"], "window_start_seconds")
        half = "early" if start < sensor_end[sensor] / 2.0 else "late"
        for d in (total, by_half[half]):
            d["windows"] += 1
            d["truth_positive"] += int(truth)
            d["registered"] += int(registered)
            d["entered_true_positive"] += int(entered_true)
            d["false_entry"] += int(false_entry)
            d["truth_negative"] += int(not truth)

    def half_summary(name: str) -> dict[str, float | int | None]:
        d = by_half[name]
        return {
            "window_count": int(d["windows"]),
            "truth_prevalence": _ratio(d["truth_positive"], d["windows"]),
            "raw_recorded_prevalence": _ratio(d["registered"], d["windows"]),
            "oracle_downstream_true_entry_prevalence": _ratio(
                d["entered_true_positive"], d["windows"]
            ),
            "false_entry_rate_given_truth_negative": _ratio(
                d["false_entry"], d["truth_negative"]
            ),
            "true_event_entry_rate": _ratio(
                d["entered_true_positive"], d["truth_positive"]
            ),
        }

    early = half_summary("early")
    late = half_summary("late")
    truth_contrast = late["truth_prevalence"] - early["truth_prevalence"]
    raw_contrast = (
        late["raw_recorded_prevalence"] - early["raw_recorded_prevalence"]
    )
    oracle_contrast = (
        late["oracle_downstream_true_entry_prevalence"]
        - early["oracle_downstream_true_entry_prevalence"]
    )

    return {
        "threshold": threshold,
        "by_half": {"early": early, "late": late},
        "truth_late_minus_early": truth_contrast,
        "raw_recorded_late_minus_early": raw_contrast,
        "oracle_downstream_true_entry_late_minus_early": oracle_contrast,
        "raw_absolute_contrast_error": abs(raw_contrast - truth_contrast),
        "upstream_omission_absolute_contrast_error": abs(
            oracle_contrast - truth_contrast
        ),
        "truth_contrast_retained_after_perfect_downstream_semantics": (
            None
            if truth_contrast == 0
            else oracle_contrast / truth_contrast
        ),
        "interpretation": (
            "The oracle-downstream series removes every false entry using truth labels but cannot add "
            "true events that never entered. Its residual contrast error therefore isolates the ecological "
            "consequence of upstream REC omission under this frozen gate, conditional on same-audio truth."
        ),
    }


def analyze(rows: list[dict[str, str]], thresholds: list[float]) -> dict[str, Any]:
    if not thresholds or any(not math.isfinite(t) for t in thresholds):
        raise OmissionError("finite threshold(s) required")
    return {
        "schema": "rec-birdvox-upstream-omission-v1",
        "analysis_scope": "heldout rows only; additive diagnostic to frozen H1-H4",
        "threshold_results": [summarize(rows, t) for t in thresholds],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("grid_csv", type=Path)
    parser.add_argument("--threshold", type=float, action="append", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(load_grid(args.grid_csv), args.threshold)
    except OmissionError as exc:
        raise SystemExit(f"BirdVox upstream omission analysis failed: {exc}") from exc
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
