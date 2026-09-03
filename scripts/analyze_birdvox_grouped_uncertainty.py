#!/usr/bin/env python3
"""Grouped uncertainty for the BirdVox REC external replication.

Resampling unit is never the one-second window. The bootstrap first resamples held-out
sensors, then fixed night blocks within each selected sensor. Leave-one-sensor-out
summaries expose dependence on any single recording.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any


class GroupedUncertaintyError(ValueError):
    pass


def _bool(value: str, field: str) -> bool:
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y"}:
        return True
    if text in {"0", "false", "f", "no", "n"}:
        return False
    raise GroupedUncertaintyError(f"{field} must be boolean, got {value!r}")


def _float(value: str, field: str) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError) as exc:
        raise GroupedUncertaintyError(f"{field} must be numeric") from exc
    if not math.isfinite(x):
        raise GroupedUncertaintyError(f"{field} must be finite")
    return x


def _ratio(a: float, b: float) -> float | None:
    return a / b if b > 0 else None


def load_grid(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise GroupedUncertaintyError("grid has no header")
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
            raise GroupedUncertaintyError(f"grid missing: {', '.join(sorted(missing))}")
        rows = [r for r in reader if r["split"].strip().lower() == "heldout"]
    if not rows:
        raise GroupedUncertaintyError("grid has no heldout rows")
    return rows


def _block_rows(
    rows: list[dict[str, str]], threshold: float, block_seconds: float
) -> dict[str, list[dict[str, float]]]:
    if block_seconds <= 0 or not math.isfinite(block_seconds):
        raise GroupedUncertaintyError("block_seconds must be finite and >0")
    sensor_end: dict[str, float] = defaultdict(float)
    for row in rows:
        s = row["sensor_id"].strip().zfill(2)
        sensor_end[s] = max(
            sensor_end[s], _float(row["window_end_seconds"], "window_end_seconds")
        )

    acc: dict[tuple[str, int, str], dict[str, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    for row in rows:
        s = row["sensor_id"].strip().zfill(2)
        start = _float(row["window_start_seconds"], "window_start_seconds")
        block = int(start // block_seconds)
        half = "early" if start < sensor_end[s] / 2.0 else "late"
        truth = _bool(row["truth_positive"], "truth_positive")
        evaluable = _bool(row["gate_evaluable"], "gate_evaluable")
        score = _float(row["max_score"], "max_score") if evaluable else None
        registered = bool(evaluable and score is not None and score >= threshold)
        d = acc[(s, block, half)]
        d["windows"] += 1
        d["truth_positive"] += int(truth)
        d["truth_positive_evaluable"] += int(truth and evaluable)
        d["missed_evaluable_positive"] += int(truth and evaluable and not registered)
        d["noentry_positive"] += int(truth and not registered)
        d["registered"] += int(registered)

    by_sensor: dict[str, list[dict[str, float]]] = defaultdict(list)
    for (s, block, half), d in sorted(acc.items()):
        out = dict(d)
        out["half_early"] = 1.0 if half == "early" else 0.0
        out["half_late"] = 1.0 if half == "late" else 0.0
        out["block_index"] = float(block)
        by_sensor[s].append(out)
    return dict(by_sensor)


def _metrics(blocks: list[dict[str, float]]) -> dict[str, float | None]:
    total = defaultdict(float)
    half = {"early": defaultdict(float), "late": defaultdict(float)}
    keys = [
        "windows",
        "truth_positive",
        "truth_positive_evaluable",
        "missed_evaluable_positive",
        "noentry_positive",
        "registered",
    ]
    for b in blocks:
        for k in keys:
            total[k] += b.get(k, 0.0)
        h = "early" if b.get("half_early", 0.0) > 0 else "late"
        for k in [
            "windows",
            "truth_positive",
            "truth_positive_evaluable",
            "missed_evaluable_positive",
            "registered",
        ]:
            half[h][k] += b.get(k, 0.0)

    a_r = _ratio(
        total["missed_evaluable_positive"], total["truth_positive_evaluable"]
    )
    a_k = _ratio(total["noentry_positive"], total["truth_positive"])
    early_ar = _ratio(
        half["early"]["missed_evaluable_positive"],
        half["early"]["truth_positive_evaluable"],
    )
    late_ar = _ratio(
        half["late"]["missed_evaluable_positive"],
        half["late"]["truth_positive_evaluable"],
    )
    truth_early = _ratio(
        half["early"]["truth_positive"], half["early"]["windows"]
    )
    truth_late = _ratio(
        half["late"]["truth_positive"], half["late"]["windows"]
    )
    rec_early = _ratio(half["early"]["registered"], half["early"]["windows"])
    rec_late = _ratio(half["late"]["registered"], half["late"]["windows"])

    h2 = None if early_ar is None or late_ar is None else late_ar - early_ar
    truth_contrast = (
        None if truth_early is None or truth_late is None else truth_late - truth_early
    )
    rec_contrast = (
        None if rec_early is None or rec_late is None else rec_late - rec_early
    )
    distortion = (
        None
        if truth_contrast is None or rec_contrast is None
        else rec_contrast - truth_contrast
    )
    sign_reversal = None
    if (
        truth_contrast is not None
        and rec_contrast is not None
        and truth_contrast != 0
        and rec_contrast != 0
    ):
        sign_reversal = float((truth_contrast > 0) != (rec_contrast > 0))

    return {
        "a_R_event_absorbed_by_gate": a_r,
        "a_K_event_not_entered": a_k,
        "late_minus_early_a_R": h2,
        "truth_late_minus_early_prevalence": truth_contrast,
        "recorded_late_minus_early_prevalence": rec_contrast,
        "recorded_minus_truth_temporal_contrast": distortion,
        "absolute_temporal_contrast_error": None if distortion is None else abs(distortion),
        "temporal_sign_reversal": sign_reversal,
    }


def _quantile(xs: list[float], q: float) -> float | None:
    if not xs:
        return None
    ys = sorted(xs)
    if len(ys) == 1:
        return ys[0]
    pos = (len(ys) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return ys[lo]
    frac = pos - lo
    return ys[lo] * (1 - frac) + ys[hi] * frac


def _ci(
    samples: list[dict[str, float | None]], key: str
) -> dict[str, float | int | None]:
    vals = [float(s[key]) for s in samples if s.get(key) is not None]
    return {
        "lower_2_5": _quantile(vals, 0.025),
        "median": _quantile(vals, 0.5),
        "upper_97_5": _quantile(vals, 0.975),
        "valid_replicates": len(vals),
    }


def analyze(
    rows: list[dict[str, str]],
    thresholds: list[float],
    *,
    block_seconds: float,
    bootstrap_reps: int,
    seed: int,
) -> dict[str, Any]:
    if bootstrap_reps < 1:
        raise GroupedUncertaintyError("bootstrap_reps must be >=1")
    rng = random.Random(seed)
    threshold_results = []

    for threshold in thresholds:
        by_sensor = _block_rows(rows, threshold, block_seconds)
        sensors = sorted(by_sensor)
        if len(sensors) < 2:
            raise GroupedUncertaintyError(
                "grouped uncertainty requires at least two heldout sensors"
            )
        observed_blocks = [b for s in sensors for b in by_sensor[s]]
        observed = _metrics(observed_blocks)

        loo = {}
        for omit in sensors:
            kept = [b for s in sensors if s != omit for b in by_sensor[s]]
            loo[omit] = _metrics(kept)

        boot = []
        for _ in range(bootstrap_reps):
            sampled_blocks: list[dict[str, float]] = []
            sampled_sensors = [rng.choice(sensors) for _ in sensors]
            for s in sampled_sensors:
                blocks = by_sensor[s]
                sampled_blocks.extend(rng.choice(blocks) for _ in range(len(blocks)))
            boot.append(_metrics(sampled_blocks))

        ci_keys = [
            "a_R_event_absorbed_by_gate",
            "a_K_event_not_entered",
            "late_minus_early_a_R",
            "truth_late_minus_early_prevalence",
            "recorded_late_minus_early_prevalence",
            "recorded_minus_truth_temporal_contrast",
            "absolute_temporal_contrast_error",
        ]
        cis = {k: _ci(boot, k) for k in ci_keys}
        sign_vals = [
            x["temporal_sign_reversal"]
            for x in boot
            if x.get("temporal_sign_reversal") is not None
        ]
        sign_prob = (
            sum(float(x) for x in sign_vals) / len(sign_vals) if sign_vals else None
        )

        threshold_results.append(
            {
                "threshold": threshold,
                "sensor_count": len(sensors),
                "sensors": sensors,
                "block_seconds": block_seconds,
                "block_count_by_sensor": {s: len(by_sensor[s]) for s in sensors},
                "observed": observed,
                "hierarchical_sensor_block_bootstrap_95pct": cis,
                "bootstrap_temporal_sign_reversal_fraction": sign_prob,
                "leave_one_sensor_out": loo,
            }
        )

    return {
        "schema": "rec-birdvox-grouped-uncertainty-v1",
        "resampling_design": (
            "Held-out sensor is the top-level bootstrap unit; fixed-duration night blocks are resampled within each selected sensor. "
            "One-second exposure windows are never treated as independent bootstrap replicates. Leave-one-sensor-out estimates are reported separately."
        ),
        "bootstrap_reps": bootstrap_reps,
        "seed": seed,
        "threshold_results": threshold_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("grid_csv", type=Path)
    parser.add_argument("--threshold", type=float, action="append", required=True)
    parser.add_argument("--block-seconds", type=float, default=1800.0)
    parser.add_argument("--bootstrap-reps", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260904)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(
            load_grid(args.grid_csv),
            args.threshold,
            block_seconds=args.block_seconds,
            bootstrap_reps=args.bootstrap_reps,
            seed=args.seed,
        )
    except GroupedUncertaintyError as exc:
        raise SystemExit(f"BirdVox grouped uncertainty failed: {exc}") from exc
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
