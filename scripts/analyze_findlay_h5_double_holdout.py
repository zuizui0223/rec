#!/usr/bin/env python3
"""Double-holdout robustness analysis for REC-H5 on Findlay otter wet/dry data.

For each held-out (camera, CT position) cell, wet/dry trigger propensities are
estimated only from rows that use neither the held-out camera nor the held-out
physical CT position. The held-out cell is then evaluated on wet composition
among independently observed passes.

This is a retrospective robustness analysis of public data. It is intentionally
not presented as prospective confirmation or as independent-animal validation.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


class DoubleHoldoutError(ValueError):
    pass


MISSING = {"", "na", "nan", "none"}


def _trigger_state(value: str) -> bool | None:
    x = str(value).strip().lower()
    if x in {"1", "true", "t", "yes", "y"}:
        return True
    if x in {"0", "false", "f", "no", "n"}:
        return False
    if x in MISSING:
        return None
    raise DoubleHoldoutError(f"TRIGGER must be binary or unresolved, got {value!r}")


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise DoubleHoldoutError("input has no header")
        needed = {"CT.POS", "CAMERA.ID", "wet.dry", "TRIGGER"}
        missing = needed - set(reader.fieldnames)
        if missing:
            raise DoubleHoldoutError(f"input missing: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise DoubleHoldoutError("input is empty")
    for row in rows:
        if not row["CT.POS"].strip():
            raise DoubleHoldoutError("blank CT.POS")
        if not row["CAMERA.ID"].strip():
            raise DoubleHoldoutError("blank CAMERA.ID")
        condition = row["wet.dry"].strip().lower()
        if condition not in {"wet", "dry"}:
            raise DoubleHoldoutError(f"wet.dry must be wet/dry, got {condition!r}")
        _trigger_state(row["TRIGGER"])
    return rows


def _ratio(a: float, b: float) -> float | None:
    return a / b if b > 0 else None


def _counts(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    out = {
        "wet": {"passes": 0, "resolved": 0, "triggered": 0, "unresolved": 0},
        "dry": {"passes": 0, "resolved": 0, "triggered": 0, "unresolved": 0},
    }
    for row in rows:
        d = out[row["wet.dry"].strip().lower()]
        d["passes"] += 1
        state = _trigger_state(row["TRIGGER"])
        if state is None:
            d["unresolved"] += 1
        else:
            d["resolved"] += 1
            d["triggered"] += int(state)
    return out


def _propensity(rows: list[dict[str, str]]) -> dict[str, dict[str, float | int | None]]:
    counts = _counts(rows)
    out: dict[str, dict[str, float | int | None]] = {}
    for condition, d in counts.items():
        point = _ratio(d["triggered"], d["resolved"])
        lower = _ratio(d["triggered"], d["passes"])
        upper = _ratio(d["triggered"] + d["unresolved"], d["passes"])
        out[condition] = {
            **d,
            "point": point,
            "lower": lower,
            "upper": upper,
        }
    return out


def _weighted_wet(triggered_wet: int, triggered_dry: int, p_wet: float, p_dry: float) -> float | None:
    if p_wet <= 0 or p_dry <= 0:
        return None
    wet_weight = triggered_wet / p_wet
    dry_weight = triggered_dry / p_dry
    return _ratio(wet_weight, wet_weight + dry_weight)


def _abs_error(estimate: float | None, truth: float | None) -> float | None:
    if estimate is None or truth is None:
        return None
    return abs(estimate - truth)


def _evaluate_cell(
    rows: list[dict[str, str]], heldout_camera: str, heldout_position: str
) -> dict[str, Any] | None:
    train = [
        r
        for r in rows
        if r["CAMERA.ID"].strip() != heldout_camera
        and r["CT.POS"].strip() != heldout_position
    ]
    test = [
        r
        for r in rows
        if r["CAMERA.ID"].strip() == heldout_camera
        and r["CT.POS"].strip() == heldout_position
    ]
    if not train or not test:
        return None

    train_prop = _propensity(train)
    test_counts = _counts(test)
    total_passes = test_counts["wet"]["passes"] + test_counts["dry"]["passes"]
    truth_wet = _ratio(test_counts["wet"]["passes"], total_passes)
    triggered_wet = test_counts["wet"]["triggered"]
    triggered_dry = test_counts["dry"]["triggered"]
    raw_wet = _ratio(triggered_wet, triggered_wet + triggered_dry)

    p_w = train_prop["wet"]["point"]
    p_d = train_prop["dry"]["point"]
    if p_w is None or p_d is None or raw_wet is None or truth_wet is None:
        return None
    if p_w <= 0 or p_d <= 0:
        return None

    corrected = _weighted_wet(triggered_wet, triggered_dry, float(p_w), float(p_d))
    sham_swapped = _weighted_wet(triggered_wet, triggered_dry, float(p_d), float(p_w))

    # Equal propensities cancel under self-normalized weighting and must equal raw.
    uniform = _weighted_wet(triggered_wet, triggered_dry, 1.0, 1.0)
    if uniform is None or abs(uniform - raw_wet) > 1e-12:
        raise DoubleHoldoutError("uniform-propensity sanity check failed")

    p_w_lo = train_prop["wet"]["lower"]
    p_w_hi = train_prop["wet"]["upper"]
    p_d_lo = train_prop["dry"]["lower"]
    p_d_hi = train_prop["dry"]["upper"]
    bound_low = bound_high = None
    if None not in {p_w_lo, p_w_hi, p_d_lo, p_d_hi}:
        # Corrected wet proportion decreases as p_wet rises and increases as p_dry rises.
        bound_low = _weighted_wet(
            triggered_wet, triggered_dry, float(p_w_hi), float(p_d_lo)
        )
        bound_high = _weighted_wet(
            triggered_wet, triggered_dry, float(p_w_lo), float(p_d_hi)
        )

    raw_error = _abs_error(raw_wet, truth_wet)
    corrected_error = _abs_error(corrected, truth_wet)
    sham_error = _abs_error(sham_swapped, truth_wet)
    if raw_error is None or corrected_error is None or sham_error is None:
        return None

    bound_worst_error = None
    if bound_low is not None and bound_high is not None:
        bound_worst_error = max(abs(bound_low - truth_wet), abs(bound_high - truth_wet))

    return {
        "heldout_camera": heldout_camera,
        "heldout_position": heldout_position,
        "training_excludes_camera": heldout_camera,
        "training_excludes_position": heldout_position,
        "training_rows": len(train),
        "test_rows": len(test),
        "training_trigger_propensities": train_prop,
        "heldout_counts": test_counts,
        "truth_wet_pass_proportion": truth_wet,
        "raw_trigger_world_wet_proportion": raw_wet,
        "correct_ipw_wet_proportion": corrected,
        "sham_swapped_ipw_wet_proportion": sham_swapped,
        "correct_ipw_unresolved_training_bounds": {
            "lower": bound_low,
            "upper": bound_high,
        },
        "absolute_error_raw": raw_error,
        "absolute_error_correct": corrected_error,
        "absolute_error_sham": sham_error,
        "worst_case_absolute_error_correct_under_unresolved_training": bound_worst_error,
        "correct_improves_on_raw": corrected_error < raw_error,
        "correct_beats_sham": corrected_error < sham_error,
        "heldout_trigger_unresolved": (
            test_counts["wet"]["unresolved"] + test_counts["dry"]["unresolved"]
        ),
    }


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _aggregate_by(cells: list[dict[str, Any]], field: str) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for cell in cells:
        grouped[str(cell[field])].append(cell)
    out: dict[str, Any] = {}
    for level, sub in sorted(grouped.items()):
        raw = _mean([float(x["absolute_error_raw"]) for x in sub])
        correct = _mean([float(x["absolute_error_correct"]) for x in sub])
        sham = _mean([float(x["absolute_error_sham"]) for x in sub])
        worst = _mean(
            [
                float(x["worst_case_absolute_error_correct_under_unresolved_training"])
                for x in sub
                if x["worst_case_absolute_error_correct_under_unresolved_training"] is not None
            ]
        )
        out[level] = {
            "cell_count": len(sub),
            "mean_absolute_error_raw": raw,
            "mean_absolute_error_correct": correct,
            "mean_absolute_error_sham": sham,
            "mean_worst_case_error_correct_under_unresolved_training": worst,
            "correct_improves_on_raw": (
                raw is not None and correct is not None and correct < raw
            ),
            "correct_beats_sham": (
                sham is not None and correct is not None and correct < sham
            ),
        }
    return out


def analyze(rows: list[dict[str, str]]) -> dict[str, Any]:
    cameras = sorted({r["CAMERA.ID"].strip() for r in rows})
    positions = sorted({r["CT.POS"].strip() for r in rows})
    if len(cameras) < 3:
        raise DoubleHoldoutError("expected at least three camera IDs")
    if len(positions) < 2:
        raise DoubleHoldoutError("expected at least two CT positions")

    cells: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for camera in cameras:
        for position in positions:
            result = _evaluate_cell(rows, camera, position)
            if result is None:
                skipped.append({"camera": camera, "position": position})
            else:
                cells.append(result)
    if not cells:
        raise DoubleHoldoutError("no evaluable double-holdout cells")

    raw_errors = [float(x["absolute_error_raw"]) for x in cells]
    correct_errors = [float(x["absolute_error_correct"]) for x in cells]
    sham_errors = [float(x["absolute_error_sham"]) for x in cells]
    worst_errors = [
        float(x["worst_case_absolute_error_correct_under_unresolved_training"])
        for x in cells
        if x["worst_case_absolute_error_correct_under_unresolved_training"] is not None
    ]
    mean_raw = float(_mean(raw_errors))
    mean_correct = float(_mean(correct_errors))
    mean_sham = float(_mean(sham_errors))
    mean_worst = _mean(worst_errors)
    reduction = mean_raw - mean_correct

    by_camera = _aggregate_by(cells, "heldout_camera")
    by_position = _aggregate_by(cells, "heldout_position")
    cameras_all_improve = all(x["correct_improves_on_raw"] for x in by_camera.values())
    positions_all_improve = all(x["correct_improves_on_raw"] for x in by_position.values())
    cameras_all_beat_sham = all(x["correct_beats_sham"] for x in by_camera.values())
    positions_all_beat_sham = all(x["correct_beats_sham"] for x in by_position.values())
    unresolved_robust = mean_worst is not None and mean_worst < mean_raw

    promotion = {
        "aggregate_correct_lt_raw": mean_correct < mean_raw,
        "aggregate_correct_lt_sham": mean_correct < mean_sham,
        "all_camera_macros_improve": cameras_all_improve,
        "all_position_macros_improve": positions_all_improve,
        "all_camera_macros_beat_sham": cameras_all_beat_sham,
        "all_position_macros_beat_sham": positions_all_beat_sham,
        "unresolved_worst_case_mean_lt_raw": unresolved_robust,
    }
    promotion["all_frozen_criteria_met"] = all(promotion.values())

    return {
        "schema": "rec-findlay-h5-double-holdout-v1",
        "estimand": "wet proportion among independently observed otter passes within held-out camera x CT-position cells",
        "design": (
            "For each test cell, training excludes both the held-out camera ID and the held-out CT position. "
            "This removes direct same-camera and same-position information from propensity estimation; it does not create independent animals."
        ),
        "camera_ids": cameras,
        "ct_positions": positions,
        "evaluable_cells": len(cells),
        "skipped_cells": skipped,
        "cells": cells,
        "aggregate": {
            "mean_absolute_error_raw": mean_raw,
            "mean_absolute_error_correct": mean_correct,
            "mean_absolute_error_sham": mean_sham,
            "mean_absolute_error_reduction_correct_vs_raw": reduction,
            "relative_mean_absolute_error_reduction_correct_vs_raw": (
                reduction / mean_raw if mean_raw > 0 else None
            ),
            "mean_worst_case_error_correct_under_unresolved_training": mean_worst,
            "cells_correct_improves_on_raw": sum(
                int(x["correct_improves_on_raw"]) for x in cells
            ),
            "cells_correct_beats_sham": sum(int(x["correct_beats_sham"]) for x in cells),
        },
        "by_camera": by_camera,
        "by_position": by_position,
        "promotion_rule": promotion,
        "governance_boundary": (
            "Retrospective public-data robustness analysis. CT position is a natural spatial/sensor-position holdout, "
            "but the otter study used the same captive animals and this analysis is not independent-individual or prospective confirmation."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("otter_wetdry_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(_read(args.otter_wetdry_csv))
    except DoubleHoldoutError as exc:
        raise SystemExit(f"Findlay H5 double-holdout failed: {exc}") from exc
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
