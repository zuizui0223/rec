#!/usr/bin/env python3
"""Retrospective cross-camera REC-H5 correction test on Findlay otter data.

Each camera type is held out in turn. Trigger propensities for wet/dry passes are
estimated only from the other camera types, then used to inverse-probability
reweight the held-out trigger-world wet/dry composition back toward the known
pass-world composition.

This is a retrospective transport/correction demonstration because the public
outcomes were already available before this REC analysis was designed. It is not
promoted as a protected confirmatory correction trial.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


class CorrectionError(ValueError):
    pass


def _trigger_state(value: str) -> bool | None:
    x = str(value).strip().lower()
    if x in {"1", "true", "t", "yes", "y"}:
        return True
    if x in {"0", "false", "f", "no", "n"}:
        return False
    if x in {"", "na", "nan", "none"}:
        return None
    raise CorrectionError(f"TRIGGER must be binary or unresolved, got {value!r}")


def _ratio(a: float, b: float) -> float | None:
    return a / b if b > 0 else None


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise CorrectionError("input has no header")
        needed = {"CAMERA.ID", "wet.dry", "TRIGGER"}
        missing = needed - set(reader.fieldnames)
        if missing:
            raise CorrectionError(f"input missing: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise CorrectionError("input is empty")
    for row in rows:
        camera = row["CAMERA.ID"].strip()
        condition = row["wet.dry"].strip().lower()
        if not camera:
            raise CorrectionError("blank CAMERA.ID")
        if condition not in {"wet", "dry"}:
            raise CorrectionError(f"wet.dry must be wet/dry, got {condition!r}")
        _trigger_state(row["TRIGGER"])
    return rows


def _condition_counts(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    out = {
        "wet": {"passes": 0, "resolved": 0, "triggered": 0, "unresolved": 0},
        "dry": {"passes": 0, "resolved": 0, "triggered": 0, "unresolved": 0},
    }
    for row in rows:
        condition = row["wet.dry"].strip().lower()
        state = _trigger_state(row["TRIGGER"])
        d = out[condition]
        d["passes"] += 1
        if state is None:
            d["unresolved"] += 1
        else:
            d["resolved"] += 1
            d["triggered"] += int(state)
    return out


def _propensity_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    counts = _condition_counts(rows)
    result: dict[str, Any] = {}
    for condition, d in counts.items():
        point = _ratio(d["triggered"], d["resolved"])
        lower = _ratio(d["triggered"], d["passes"])
        upper = _ratio(d["triggered"] + d["unresolved"], d["passes"])
        result[condition] = {
            **d,
            "trigger_probability_resolved_only": point,
            "trigger_probability_lower": lower,
            "trigger_probability_upper": upper,
            "reference_unresolved_fraction": _ratio(d["unresolved"], d["passes"]),
        }
    return result


def _ipw_wet(triggered_wet: int, triggered_dry: int, p_wet: float, p_dry: float) -> float | None:
    if p_wet <= 0 or p_dry <= 0:
        return None
    w_wet = triggered_wet / p_wet
    w_dry = triggered_dry / p_dry
    return _ratio(w_wet, w_wet + w_dry)


def _camera_evaluation(
    rows: list[dict[str, str]], heldout_camera: str, cameras: list[str]
) -> dict[str, Any]:
    train = [r for r in rows if r["CAMERA.ID"].strip() != heldout_camera]
    test = [r for r in rows if r["CAMERA.ID"].strip() == heldout_camera]
    if not train or not test:
        raise CorrectionError(f"invalid heldout camera {heldout_camera!r}")

    train_prop = _propensity_summary(train)
    heldout_counts = _condition_counts(test)

    total_passes = sum(d["passes"] for d in heldout_counts.values())
    truth_wet = _ratio(heldout_counts["wet"]["passes"], total_passes)
    tw = heldout_counts["wet"]["triggered"]
    td = heldout_counts["dry"]["triggered"]
    raw_wet = _ratio(tw, tw + td)

    p_w = train_prop["wet"]["trigger_probability_resolved_only"]
    p_d = train_prop["dry"]["trigger_probability_resolved_only"]
    if p_w is None or p_d is None:
        raise CorrectionError("training camera set lacks resolved trigger propensity")
    corrected = _ipw_wet(tw, td, p_w, p_d)

    # Partial-identification envelope induced only by unresolved training trigger states.
    # Corrected wet proportion decreases with larger p_wet and increases with larger p_dry.
    p_w_lo = train_prop["wet"]["trigger_probability_lower"]
    p_w_hi = train_prop["wet"]["trigger_probability_upper"]
    p_d_lo = train_prop["dry"]["trigger_probability_lower"]
    p_d_hi = train_prop["dry"]["trigger_probability_upper"]
    lower = None
    upper = None
    if None not in {p_w_lo, p_w_hi, p_d_lo, p_d_hi}:
        lower = _ipw_wet(tw, td, float(p_w_hi), float(p_d_lo))
        upper = _ipw_wet(tw, td, float(p_w_lo), float(p_d_hi))

    raw_error = None if raw_wet is None or truth_wet is None else abs(raw_wet - truth_wet)
    corrected_error = (
        None if corrected is None or truth_wet is None else abs(corrected - truth_wet)
    )
    improvement = (
        None
        if raw_error is None or corrected_error is None
        else raw_error - corrected_error
    )

    return {
        "heldout_camera": heldout_camera,
        "training_cameras": [c for c in cameras if c != heldout_camera],
        "training_trigger_propensities": train_prop,
        "heldout_pass_counts": heldout_counts,
        "truth_wet_pass_proportion": truth_wet,
        "raw_trigger_world_wet_proportion": raw_wet,
        "cross_camera_ipw_wet_proportion": corrected,
        "cross_camera_ipw_wet_proportion_unresolved_training_bounds": {
            "lower": lower,
            "upper": upper,
        },
        "absolute_error_raw": raw_error,
        "absolute_error_corrected": corrected_error,
        "absolute_error_improvement": improvement,
        "improved": improvement is not None and improvement > 0,
        "heldout_trigger_reference_unresolved_fraction": _ratio(
            heldout_counts["wet"]["unresolved"] + heldout_counts["dry"]["unresolved"],
            total_passes,
        ),
    }


def analyze(rows: list[dict[str, str]]) -> dict[str, Any]:
    cameras = sorted({r["CAMERA.ID"].strip() for r in rows})
    if len(cameras) < 3:
        raise CorrectionError("at least three camera types are required for leave-one-camera-out")

    evaluations = [_camera_evaluation(rows, camera, cameras) for camera in cameras]
    raw_errors = [x["absolute_error_raw"] for x in evaluations]
    corrected_errors = [x["absolute_error_corrected"] for x in evaluations]
    if any(x is None for x in raw_errors + corrected_errors):
        raise CorrectionError("correction evaluation is undefined for at least one camera")

    mean_raw = sum(float(x) for x in raw_errors) / len(raw_errors)
    mean_corrected = sum(float(x) for x in corrected_errors) / len(corrected_errors)
    reduction = mean_raw - mean_corrected
    relative = reduction / mean_raw if mean_raw > 0 else None
    all_improved = all(x["improved"] for x in evaluations)

    return {
        "schema": "rec-findlay-h5-cross-camera-correction-v1",
        "estimand": "wet proportion among independently observed otter passes",
        "correction": (
            "self-normalized inverse-probability weighting of held-out confirmed-trigger records; "
            "wet/dry trigger propensities are estimated only from the other camera types"
        ),
        "leave_one_camera_out": evaluations,
        "aggregate": {
            "camera_count": len(cameras),
            "mean_absolute_error_raw_trigger_world": mean_raw,
            "mean_absolute_error_cross_camera_ipw": mean_corrected,
            "mean_absolute_error_reduction": reduction,
            "relative_mean_absolute_error_reduction": relative,
            "cameras_improved": sum(int(x["improved"]) for x in evaluations),
            "all_cameras_improved": all_improved,
        },
        "REC_H5_recoverability": {
            "supported_retrospectively": all_improved and reduction > 0,
            "interpretation": (
                "A selection-aware correction learned from other camera types is useful only if it improves "
                "held-out camera composition without using that camera's trigger outcomes to estimate its propensity."
            ),
        },
        "governance_boundary": (
            "This is a retrospective cross-camera transport test on public outcomes already available before the REC-H5 analysis was designed. "
            "It is evidence that REC-style entry information can improve a downstream composition estimate, not a protected confirmatory correction trial. "
            "Trigger-reference-unresolved rows are never recoded as failures; point propensities are resolved-only and an uncertainty envelope is reported."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("otter_wetdry_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(_read(args.otter_wetdry_csv))
    except CorrectionError as exc:
        raise SystemExit(f"Findlay REC-H5 correction failed: {exc}") from exc
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
