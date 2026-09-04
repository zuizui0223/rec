#!/usr/bin/env python3
"""Position-standardized H2→H3 robustness analysis for Findlay data.

The analysis asks whether pooled ecological composition shifts persist when the
reference and recorded worlds are compared under the same distribution of
physical CT positions. It is descriptive/robustness evidence, not a row-level
independence test.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Callable

MISSING = {"", "na", "nan", "none"}


class StandardizationError(ValueError):
    pass


def _optional_binary(value: str, field: str) -> bool | None:
    x = str(value).strip().lower()
    if x in {"1", "true", "t", "yes", "y"}:
        return True
    if x in {"0", "false", "f", "no", "n"}:
        return False
    if x in MISSING:
        return None
    raise StandardizationError(f"{field} must be binary or missing, got {value!r}")


def _read(path: Path, required: set[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise StandardizationError(f"{path} has no header")
        missing = required - set(reader.fieldnames)
        if missing:
            raise StandardizationError(f"{path} missing: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise StandardizationError(f"{path} is empty")
    return rows


def _ratio(a: float, b: float) -> float | None:
    return a / b if b > 0 else None


def _final_entry(row: dict[str, str]) -> bool | None:
    trigger = _optional_binary(row["TRIGGER"], "TRIGGER")
    capture = _optional_binary(row["CAPTURE"], "CAPTURE")
    if trigger is False:
        if capture is True:
            raise StandardizationError("CAPTURE=1 with TRIGGER=0")
        return False
    if trigger is True:
        return capture
    # If trigger is unresolved, retain any direct capture information but do not
    # infer a trigger state from it.
    return capture


def _position_composition(
    rows: list[dict[str, str]],
    *,
    group_fn: Callable[[dict[str, str]], str],
    focal_group: str,
    other_group: str,
    entry_fn: Callable[[dict[str, str]], bool | None],
) -> dict[str, Any] | None:
    counts = {
        focal_group: {"truth": 0, "entered": 0, "entry_resolved": 0, "entry_unresolved": 0},
        other_group: {"truth": 0, "entered": 0, "entry_resolved": 0, "entry_unresolved": 0},
    }
    for row in rows:
        g = group_fn(row)
        if g not in counts:
            continue
        d = counts[g]
        d["truth"] += 1
        state = entry_fn(row)
        if state is None:
            d["entry_unresolved"] += 1
        else:
            d["entry_resolved"] += 1
            d["entered"] += int(state)

    total_truth = counts[focal_group]["truth"] + counts[other_group]["truth"]
    total_entered = counts[focal_group]["entered"] + counts[other_group]["entered"]
    truth_prop = _ratio(counts[focal_group]["truth"], total_truth)
    recorded_prop = _ratio(counts[focal_group]["entered"], total_entered)
    focal_entry_p = _ratio(counts[focal_group]["entered"], counts[focal_group]["entry_resolved"])
    other_entry_p = _ratio(counts[other_group]["entered"], counts[other_group]["entry_resolved"])
    if truth_prop is None or recorded_prop is None:
        return None
    entry_diff = None
    if focal_entry_p is not None and other_entry_p is not None:
        entry_diff = focal_entry_p - other_entry_p
    return {
        "counts": counts,
        "truth_total": total_truth,
        "entered_total": total_entered,
        "truth_focal_proportion": truth_prop,
        "recorded_focal_proportion": recorded_prop,
        "composition_shift_recorded_minus_truth": recorded_prop - truth_prop,
        "focal_entry_probability_resolved_only": focal_entry_p,
        "other_entry_probability_resolved_only": other_entry_p,
        "entry_probability_difference_focal_minus_other": entry_diff,
    }


def _standardize(cells: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if not cells:
        raise StandardizationError("no evaluable positions")
    positions = sorted(cells)
    n = len(positions)
    equal = {p: 1.0 / n for p in positions}
    truth_total = sum(float(cells[p]["truth_total"]) for p in positions)
    if truth_total <= 0:
        raise StandardizationError("nonpositive truth total")
    pass_weights = {p: float(cells[p]["truth_total"]) / truth_total for p in positions}

    def calc(weights: dict[str, float]) -> dict[str, float]:
        truth = sum(weights[p] * float(cells[p]["truth_focal_proportion"]) for p in positions)
        recorded = sum(weights[p] * float(cells[p]["recorded_focal_proportion"]) for p in positions)
        return {
            "truth_focal_proportion": truth,
            "recorded_focal_proportion": recorded,
            "shift_recorded_minus_truth": recorded - truth,
        }

    shifts = [float(cells[p]["composition_shift_recorded_minus_truth"]) for p in positions]
    entry_diffs = [
        float(cells[p]["entry_probability_difference_focal_minus_other"])
        for p in positions
        if cells[p]["entry_probability_difference_focal_minus_other"] is not None
    ]
    return {
        "evaluable_positions": positions,
        "position_count": n,
        "equal_position_weighting": calc(equal),
        "reference_pass_weighting": calc(pass_weights),
        "positions_with_negative_composition_shift": sum(int(x < 0) for x in shifts),
        "positions_with_positive_composition_shift": sum(int(x > 0) for x in shifts),
        "positions_with_zero_composition_shift": sum(int(x == 0) for x in shifts),
        "positions_with_negative_entry_probability_difference": sum(int(x < 0) for x in entry_diffs),
        "positions_with_positive_entry_probability_difference": sum(int(x > 0) for x in entry_diffs),
        "entry_probability_difference_evaluable_positions": len(entry_diffs),
        "reference_pass_position_weights": pass_weights,
    }


def _otter(rows: list[dict[str, str]]) -> dict[str, Any]:
    cameras = sorted({r["CAMERA.ID"].strip() for r in rows})
    out: dict[str, Any] = {}
    for camera in cameras:
        cr = [r for r in rows if r["CAMERA.ID"].strip() == camera]
        positions = sorted({r["CT.POS"].strip() for r in cr})
        cells: dict[str, dict[str, Any]] = {}
        skipped: list[str] = []
        for pos in positions:
            pr = [r for r in cr if r["CT.POS"].strip() == pos]
            cell = _position_composition(
                pr,
                group_fn=lambda r: r["wet.dry"].strip().lower(),
                focal_group="wet",
                other_group="dry",
                entry_fn=lambda r: _optional_binary(r["TRIGGER"], "TRIGGER"),
            )
            if cell is None:
                skipped.append(pos)
            else:
                cells[pos] = cell
        std = _standardize(cells)
        out[camera] = {
            "focal_group": "wet",
            "other_group": "dry",
            "positions": cells,
            "skipped_positions": skipped,
            "standardized": std,
            "robust_support_equal_weight": std["equal_position_weighting"]["shift_recorded_minus_truth"] < 0,
            "robust_support_reference_pass_weight": std["reference_pass_weighting"]["shift_recorded_minus_truth"] < 0,
        }
    return out


def _fox_badger_stage(rows: list[dict[str, str]], stage: str) -> dict[str, Any]:
    positions = sorted({r["CT.POS"].strip() for r in rows})
    cells: dict[str, dict[str, Any]] = {}
    skipped: list[str] = []
    if stage == "trigger":
        entry_fn = lambda r: _optional_binary(r["TRIGGER"], "TRIGGER")
    elif stage == "capture":
        entry_fn = _final_entry
    else:
        raise StandardizationError(f"unknown stage {stage}")
    for pos in positions:
        pr = [r for r in rows if r["CT.POS"].strip() == pos]
        cell = _position_composition(
            pr,
            group_fn=lambda r: r["SPECIES"].strip().upper(),
            focal_group="BADGER",
            other_group="FOX",
            entry_fn=entry_fn,
        )
        if cell is None:
            skipped.append(pos)
        else:
            cells[pos] = cell
    std = _standardize(cells)
    return {
        "focal_group": "BADGER",
        "other_group": "FOX",
        "positions": cells,
        "skipped_positions": skipped,
        "standardized": std,
        "robust_support_equal_weight": std["equal_position_weighting"]["shift_recorded_minus_truth"] > 0,
        "robust_support_reference_pass_weight": std["reference_pass_weighting"]["shift_recorded_minus_truth"] > 0,
    }


def analyze(fox_badger: list[dict[str, str]], otter: list[dict[str, str]]) -> dict[str, Any]:
    otter_out = _otter(otter)
    fox_out = {
        "trigger": _fox_badger_stage(fox_badger, "trigger"),
        "capture": _fox_badger_stage(fox_badger, "capture"),
    }
    otter_all = all(
        x["robust_support_equal_weight"] and x["robust_support_reference_pass_weight"]
        for x in otter_out.values()
    )
    fox_all = all(
        x["robust_support_equal_weight"] and x["robust_support_reference_pass_weight"]
        for x in fox_out.values()
    )
    return {
        "schema": "rec-findlay-position-standardized-distortion-v1",
        "purpose": "test whether H2→H3 composition shifts persist when reference and recorded worlds use the same physical CT-position distribution",
        "otter_wet_dry_trigger": otter_out,
        "fox_badger": fox_out,
        "promotion_rule": {
            "otter_all_camera_settings_negative_under_both_weightings": otter_all,
            "fox_badger_trigger_and_capture_positive_under_both_weightings": fox_all,
            "all_frozen_criteria_met": otter_all and fox_all,
        },
        "governance_boundary": "Descriptive position-standardization robustness analysis; no row-level significance test is used because passes are not independent biological individuals.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("fox_badger_csv", type=Path)
    p.add_argument("otter_wetdry_csv", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    fox = _read(args.fox_badger_csv, {"SPECIES", "CT.POS", "TRIGGER", "CAPTURE"})
    otter = _read(args.otter_wetdry_csv, {"CT.POS", "CAMERA.ID", "wet.dry", "TRIGGER"})
    result = analyze(fox, otter)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
