#!/usr/bin/env python3
"""Analyze BirdVox REC H1-H4 on a gate-independent exposure grid."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


class BirdVoxAnalysisError(ValueError):
    pass


def _bool(value: str, field: str) -> bool:
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y"}:
        return True
    if text in {"0", "false", "f", "no", "n"}:
        return False
    raise BirdVoxAnalysisError(f"{field} must be boolean, got {value!r}")


def _float(value: str, field: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise BirdVoxAnalysisError(f"{field} must be numeric, got {value!r}") from exc
    if not math.isfinite(out):
        raise BirdVoxAnalysisError(f"{field} must be finite")
    return out


def _ratio(num: float, den: float) -> float | None:
    return num / den if den > 0 else None


def load_grid(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise BirdVoxAnalysisError("grid has no header")
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
            raise BirdVoxAnalysisError(f"grid missing: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise BirdVoxAnalysisError("grid is empty")
    seen: set[str] = set()
    for row in rows:
        wid = row["window_id"].strip()
        if not wid or wid in seen:
            raise BirdVoxAnalysisError(f"blank/duplicate window_id {wid!r}")
        seen.add(wid)
        split = row["split"].strip().lower()
        if split not in {"development", "heldout"}:
            raise BirdVoxAnalysisError(f"{wid}: invalid split {split!r}")
        _bool(row["truth_positive"], "truth_positive")
        evaluable = _bool(row["gate_evaluable"], "gate_evaluable")
        if evaluable:
            _float(row["max_score"], "max_score")
        elif row["max_score"].strip():
            raise BirdVoxAnalysisError(f"{wid}: non-evaluable gate must not carry max_score")
    return rows


def _rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg
        i = j
    return ranks


def _pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) != len(y) or len(x) < 2:
        return None
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    den = math.sqrt(sum(v * v for v in dx) * sum(v * v for v in dy))
    return sum(a * b for a, b in zip(dx, dy)) / den if den > 0 else None


def _spearman(x: list[float], y: list[float]) -> float | None:
    return _pearson(_rank(x), _rank(y))


def _condition_summary(d: dict[str, float]) -> dict[str, float | int | None]:
    return {
        "window_count": int(d["windows"]),
        "truth_positive_windows": int(d["truth_positive"]),
        "truth_positive_gate_evaluable_windows": int(d["truth_positive_evaluable"]),
        "gate_unevaluable_positive_windows": int(d["gate_unevaluable_positive"]),
        "gate_baseline_positive_windows": int(d["gate_baseline_positive"]),
        "no_entry_positive_windows": int(d["no_entry_positive"]),
        "event_absorption_a_R": _ratio(
            d["gate_baseline_positive"], d["truth_positive_evaluable"]
        ),
        "event_nonentry_a_K": _ratio(d["no_entry_positive"], d["truth_positive"]),
    }


def _summary(rows: list[dict[str, str]], threshold: float) -> dict[str, Any]:
    counts = defaultdict(float)
    by_sensor: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    by_half: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))

    sensor_end: dict[str, float] = {}
    for row in rows:
        if row["split"].strip().lower() != "heldout":
            continue
        sensor = row["sensor_id"].strip().zfill(2)
        sensor_end[sensor] = max(
            sensor_end.get(sensor, 0.0),
            _float(row["window_end_seconds"], "window_end_seconds"),
        )

    for row in rows:
        if row["split"].strip().lower() != "heldout":
            continue
        sensor = row["sensor_id"].strip().zfill(2)
        truth = _bool(row["truth_positive"], "truth_positive")
        evaluable = _bool(row["gate_evaluable"], "gate_evaluable")
        score = _float(row["max_score"], "max_score") if evaluable else None
        registered = evaluable and score is not None and score >= threshold
        gate_baseline = evaluable and not registered
        no_entry = not registered

        counts["windows"] += 1
        counts["truth_positive"] += int(truth)
        counts["gate_evaluable"] += int(evaluable)
        counts["truth_positive_evaluable"] += int(truth and evaluable)
        counts["gate_unevaluable"] += int(not evaluable)
        counts["gate_unevaluable_positive"] += int(truth and not evaluable)
        counts["registered"] += int(registered)
        counts["registered_positive"] += int(truth and registered)
        counts["gate_baseline"] += int(gate_baseline)
        counts["gate_baseline_positive"] += int(truth and gate_baseline)
        counts["no_entry"] += int(no_entry)
        counts["no_entry_positive"] += int(truth and no_entry)

        d = by_sensor[sensor]
        d["windows"] += 1
        d["truth_positive"] += int(truth)
        d["gate_evaluable"] += int(evaluable)
        d["truth_positive_evaluable"] += int(truth and evaluable)
        d["gate_unevaluable_positive"] += int(truth and not evaluable)
        d["registered"] += int(registered)
        d["gate_baseline_positive"] += int(truth and gate_baseline)
        d["no_entry_positive"] += int(truth and no_entry)

        midpoint = sensor_end[sensor] / 2.0
        start = _float(row["window_start_seconds"], "window_start_seconds")
        half = "early" if start < midpoint else "late"
        h = by_half[half]
        h["windows"] += 1
        h["truth_positive"] += int(truth)
        h["gate_evaluable"] += int(evaluable)
        h["truth_positive_evaluable"] += int(truth and evaluable)
        h["gate_unevaluable_positive"] += int(truth and not evaluable)
        h["registered"] += int(registered)
        h["gate_baseline_positive"] += int(truth and gate_baseline)
        h["no_entry_positive"] += int(truth and no_entry)

    if counts["windows"] == 0:
        raise BirdVoxAnalysisError("no heldout windows")
    if counts["truth_positive"] == 0:
        raise BirdVoxAnalysisError("heldout grid has no positive truth windows")

    sensor_metrics: dict[str, Any] = {}
    truth_rates: list[float] = []
    recorded_rates: list[float] = []
    for sensor in sorted(by_sensor):
        d = by_sensor[sensor]
        truth_rate = d["truth_positive"] / d["windows"]
        recorded_rate = d["registered"] / d["windows"]
        sensor_metrics[sensor] = {
            **_condition_summary(d),
            "truth_event_window_prevalence": truth_rate,
            "recorded_window_prevalence": recorded_rate,
        }
        truth_rates.append(truth_rate)
        recorded_rates.append(recorded_rate)

    early = by_half["early"]
    late = by_half["late"]
    truth_early = _ratio(early["truth_positive"], early["windows"])
    truth_late = _ratio(late["truth_positive"], late["windows"])
    rec_early = _ratio(early["registered"], early["windows"])
    rec_late = _ratio(late["registered"], late["windows"])
    truth_contrast = (
        None if truth_early is None or truth_late is None else truth_late - truth_early
    )
    rec_contrast = None if rec_early is None or rec_late is None else rec_late - rec_early

    mae = sum(abs(a - b) for a, b in zip(truth_rates, recorded_rates)) / len(truth_rates)
    absorption_values = [
        v["event_absorption_a_R"]
        for v in sensor_metrics.values()
        if v["event_absorption_a_R"] is not None
    ]
    nonentry_values = [
        v["event_nonentry_a_K"]
        for v in sensor_metrics.values()
        if v["event_nonentry_a_K"] is not None
    ]

    return {
        "threshold": threshold,
        "heldout": {
            "window_count": int(counts["windows"]),
            "truth_positive_windows": int(counts["truth_positive"]),
            "truth_positive_gate_evaluable_windows": int(
                counts["truth_positive_evaluable"]
            ),
            "gate_evaluable_windows": int(counts["gate_evaluable"]),
            "gate_unevaluable_windows": int(counts["gate_unevaluable"]),
            "registered_windows": int(counts["registered"]),
            "registered_baseline_windows": int(counts["gate_baseline"]),
            "no_entry_windows": int(counts["no_entry"]),
        },
        "REC_H1_shadow_existence": {
            "no_entry_positive_windows": int(counts["no_entry_positive"]),
            "q_shadow_event_given_no_record": _ratio(
                counts["no_entry_positive"], counts["no_entry"]
            ),
            "a_K_event_not_entered": _ratio(
                counts["no_entry_positive"], counts["truth_positive"]
            ),
            "gate_baseline_positive_windows": int(counts["gate_baseline_positive"]),
            "q_B_event_given_registered_baseline": _ratio(
                counts["gate_baseline_positive"], counts["gate_baseline"]
            ),
            "a_R_event_absorbed_by_gate": _ratio(
                counts["gate_baseline_positive"], counts["truth_positive_evaluable"]
            ),
            "gate_unevaluable_positive_windows": int(
                counts["gate_unevaluable_positive"]
            ),
            "supported_no_entry": counts["no_entry_positive"] > 0,
            "supported_gate_absorption": counts["gate_baseline_positive"] > 0,
        },
        "REC_H2_structured_selection": {
            "by_sensor": sensor_metrics,
            "by_night_half": {
                half: _condition_summary(by_half[half]) for half in ("early", "late")
            },
            "sensor_event_absorption_range": (
                max(absorption_values) - min(absorption_values)
                if absorption_values
                else None
            ),
            "sensor_event_nonentry_range": (
                max(nonentry_values) - min(nonentry_values) if nonentry_values else None
            ),
            "interpretation": (
                "Descriptive held-out condition map by sensor and time-of-night half. "
                "Gate absorption a_R conditions on gate-evaluable true events; no-entry a_K also includes "
                "gate-unevaluable true events because the frozen entry policy creates no record for them. "
                "Grouped uncertainty belongs in the confirmatory extension."
            ),
        },
        "REC_H3_ecological_distortion": {
            "sensor_rate_mae": mae,
            "sensor_rate_spearman": _spearman(truth_rates, recorded_rates),
            "truth_late_minus_early_prevalence": truth_contrast,
            "recorded_late_minus_early_prevalence": rec_contrast,
            "absolute_temporal_contrast_error": (
                abs(rec_contrast - truth_contrast)
                if rec_contrast is not None and truth_contrast is not None
                else None
            ),
            "interpretation": (
                "The ecological endpoint is one-second flight-call event-window prevalence. "
                "Recorded prevalence uses K=1 only when the gate is evaluable and passes; "
                "gate-unevaluable windows therefore contribute to K=0 but not to R=0. "
                "This is an algorithmic record-entry consequence, not species abundance."
            ),
        },
    }


def analyze(rows: list[dict[str, str]], thresholds: list[float]) -> dict[str, Any]:
    if not thresholds:
        raise BirdVoxAnalysisError("at least one threshold is required")
    if any(not math.isfinite(t) for t in thresholds):
        raise BirdVoxAnalysisError("thresholds must be finite")
    summaries = [_summary(rows, t) for t in thresholds]
    gate_pairs = []
    for left, right in zip(summaries, summaries[1:]):
        l = left["REC_H1_shadow_existence"]
        r = right["REC_H1_shadow_existence"]
        gate_pairs.append(
            {
                "threshold_low": left["threshold"],
                "threshold_high": right["threshold"],
                "delta_event_absorption_a_R": (
                    r["a_R_event_absorbed_by_gate"] - l["a_R_event_absorbed_by_gate"]
                ),
                "delta_event_nonentry_a_K": (
                    r["a_K_event_not_entered"] - l["a_K_event_not_entered"]
                ),
                "delta_shadow_contamination": (
                    None
                    if l["q_shadow_event_given_no_record"] is None
                    or r["q_shadow_event_given_no_record"] is None
                    else r["q_shadow_event_given_no_record"]
                    - l["q_shadow_event_given_no_record"]
                ),
                "delta_sensor_rate_mae": (
                    right["REC_H3_ecological_distortion"]["sensor_rate_mae"]
                    - left["REC_H3_ecological_distortion"]["sensor_rate_mae"]
                ),
            }
        )
    return {
        "schema": "rec-birdvox-exposure-grid-analysis-v2",
        "analysis_scope": "heldout sensors only",
        "record_entry_semantics": (
            "R is defined only when the frozen gate is evaluable. K=1 requires an evaluable gate that passes; "
            "otherwise K=0 under this external replication entry policy. Therefore gate-unevaluable windows "
            "contribute to record non-entry a_K but are never recoded as R=0 gate absorption a_R. "
            "This audits algorithmic entry after audio acquisition and does not estimate microphone-level misses "
            "or a separate archive-loss stage."
        ),
        "threshold_results": summaries,
        "REC_H4_gate_semantics_sensitivity": gate_pairs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("grid_csv", type=Path)
    parser.add_argument("--threshold", type=float, action="append", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(load_grid(args.grid_csv), args.threshold)
    except BirdVoxAnalysisError as exc:
        raise SystemExit(f"BirdVox REC analysis failed: {exc}") from exc
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
