#!/usr/bin/env python3
"""Retrospective within-camera, leave-one-position-out REC-H5 transport analysis.

This diagnostic follows the adverse double-holdout result. For each camera and
physical CT position, wet/dry trigger propensities are learned from the same
camera at all other CT positions and evaluated at the held-out position.

The purpose is to identify whether H5 transport fails because entry propensities
are position-specific, camera-specific, or require at least one shared axis.
This is exploratory robustness analysis, not protected confirmation.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

MISSING = {"", "na", "nan", "none"}


class PositionTransportError(ValueError):
    pass


def _state(value: str) -> bool | None:
    x = str(value).strip().lower()
    if x in {"1", "true", "t", "yes", "y"}:
        return True
    if x in {"0", "false", "f", "no", "n"}:
        return False
    if x in MISSING:
        return None
    raise PositionTransportError(f"invalid TRIGGER {value!r}")


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise PositionTransportError("missing header")
        required = {"CT.POS", "CAMERA.ID", "wet.dry", "TRIGGER"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise PositionTransportError(f"missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise PositionTransportError("empty input")
    return rows


def _counts(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    out = {
        "wet": {"passes": 0, "resolved": 0, "triggered": 0, "unresolved": 0},
        "dry": {"passes": 0, "resolved": 0, "triggered": 0, "unresolved": 0},
    }
    for row in rows:
        condition = row["wet.dry"].strip().lower()
        if condition not in out:
            raise PositionTransportError(f"invalid wet.dry {condition!r}")
        d = out[condition]
        d["passes"] += 1
        s = _state(row["TRIGGER"])
        if s is None:
            d["unresolved"] += 1
        else:
            d["resolved"] += 1
            d["triggered"] += int(s)
    return out


def _ratio(a: float, b: float) -> float | None:
    return a / b if b > 0 else None


def _propensity(rows: list[dict[str, str]]) -> dict[str, dict[str, float | int | None]]:
    c = _counts(rows)
    out: dict[str, dict[str, float | int | None]] = {}
    for condition, d in c.items():
        out[condition] = {
            **d,
            "point": _ratio(d["triggered"], d["resolved"]),
            "lower": _ratio(d["triggered"], d["passes"]),
            "upper": _ratio(d["triggered"] + d["unresolved"], d["passes"]),
        }
    return out


def _ipw(tw: int, td: int, p_w: float, p_d: float) -> float | None:
    if p_w <= 0 or p_d <= 0:
        return None
    ww = tw / p_w
    wd = td / p_d
    return _ratio(ww, ww + wd)


def _eval(rows: list[dict[str, str]], camera: str, position: str) -> dict[str, Any] | None:
    train = [r for r in rows if r["CAMERA.ID"].strip() == camera and r["CT.POS"].strip() != position]
    test = [r for r in rows if r["CAMERA.ID"].strip() == camera and r["CT.POS"].strip() == position]
    if not train or not test:
        return None
    prop = _propensity(train)
    tc = _counts(test)
    total = tc["wet"]["passes"] + tc["dry"]["passes"]
    truth = _ratio(tc["wet"]["passes"], total)
    tw = tc["wet"]["triggered"]
    td = tc["dry"]["triggered"]
    raw = _ratio(tw, tw + td)
    p_w = prop["wet"]["point"]
    p_d = prop["dry"]["point"]
    if None in {truth, raw, p_w, p_d}:
        return None
    correct = _ipw(tw, td, float(p_w), float(p_d))
    sham = _ipw(tw, td, float(p_d), float(p_w))
    if correct is None or sham is None:
        return None
    raw_err = abs(float(raw) - float(truth))
    corr_err = abs(correct - float(truth))
    sham_err = abs(sham - float(truth))
    return {
        "camera": camera,
        "heldout_position": position,
        "training_rows": len(train),
        "test_rows": len(test),
        "training_trigger_propensities": prop,
        "heldout_counts": tc,
        "truth_wet_pass_proportion": truth,
        "raw_trigger_world_wet_proportion": raw,
        "correct_ipw_wet_proportion": correct,
        "sham_swapped_ipw_wet_proportion": sham,
        "absolute_error_raw": raw_err,
        "absolute_error_correct": corr_err,
        "absolute_error_sham": sham_err,
        "correct_improves_on_raw": corr_err < raw_err,
        "correct_beats_sham": corr_err < sham_err,
    }


def _mean(xs: list[float]) -> float:
    if not xs:
        raise PositionTransportError("empty aggregate")
    return sum(xs) / len(xs)


def analyze(rows: list[dict[str, str]]) -> dict[str, Any]:
    cameras = sorted({r["CAMERA.ID"].strip() for r in rows})
    positions = sorted({r["CT.POS"].strip() for r in rows})
    cells: list[dict[str, Any]] = []
    for camera in cameras:
        for position in positions:
            r = _eval(rows, camera, position)
            if r is not None:
                cells.append(r)
    if not cells:
        raise PositionTransportError("no evaluable cells")
    by_camera: dict[str, Any] = {}
    for camera in cameras:
        sub = [x for x in cells if x["camera"] == camera]
        if not sub:
            continue
        raw = _mean([x["absolute_error_raw"] for x in sub])
        corr = _mean([x["absolute_error_correct"] for x in sub])
        sham = _mean([x["absolute_error_sham"] for x in sub])
        by_camera[camera] = {
            "cell_count": len(sub),
            "mean_absolute_error_raw": raw,
            "mean_absolute_error_correct": corr,
            "mean_absolute_error_sham": sham,
            "correct_improves_on_raw": corr < raw,
            "correct_beats_sham": corr < sham,
        }
    by_position: dict[str, Any] = {}
    for position in positions:
        sub = [x for x in cells if x["heldout_position"] == position]
        if not sub:
            continue
        raw = _mean([x["absolute_error_raw"] for x in sub])
        corr = _mean([x["absolute_error_correct"] for x in sub])
        sham = _mean([x["absolute_error_sham"] for x in sub])
        by_position[position] = {
            "cell_count": len(sub),
            "mean_absolute_error_raw": raw,
            "mean_absolute_error_correct": corr,
            "mean_absolute_error_sham": sham,
            "correct_improves_on_raw": corr < raw,
            "correct_beats_sham": corr < sham,
        }
    mean_raw = _mean([x["absolute_error_raw"] for x in cells])
    mean_corr = _mean([x["absolute_error_correct"] for x in cells])
    mean_sham = _mean([x["absolute_error_sham"] for x in cells])
    return {
        "schema": "rec-findlay-h5-position-transport-v1",
        "design": "within each camera ID, estimate wet/dry trigger propensities from all other CT positions and evaluate the held-out position",
        "cells": cells,
        "by_camera": by_camera,
        "by_position": by_position,
        "aggregate": {
            "evaluable_cells": len(cells),
            "mean_absolute_error_raw": mean_raw,
            "mean_absolute_error_correct": mean_corr,
            "mean_absolute_error_sham": mean_sham,
            "relative_error_reduction_correct_vs_raw": ((mean_raw - mean_corr) / mean_raw if mean_raw > 0 else None),
            "cells_improved": sum(int(x["correct_improves_on_raw"]) for x in cells),
            "cells_beating_sham": sum(int(x["correct_beats_sham"]) for x in cells),
            "all_camera_macros_improve": all(v["correct_improves_on_raw"] for v in by_camera.values()),
            "all_position_macros_improve": all(v["correct_improves_on_raw"] for v in by_position.values()),
        },
        "governance_boundary": "Exploratory retrospective transport diagnostic after the frozen double-holdout failed. It identifies the transport boundary; it is not a replacement confirmatory endpoint.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("otter_wetdry_csv", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = analyze(_read(args.otter_wetdry_csv))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
