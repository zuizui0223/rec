#!/usr/bin/env python3
"""Map Findlay camera-trap pass/trigger/capture data onto REC estimands.

Every input row is an independently observed animal pass. This supports event-conditioned
loss quantities such as P(no trigger | pass) and bounded P(no capture | pass), but not the
full time-denominator q_shadow = P(event | no record).

Missing TRIGGER and CAPTURE values are retained as reference-unresolved process states.
They are never silently converted to non-trigger/non-capture outcomes.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


class FindlayAnalysisError(ValueError):
    pass


MISSING = {"", "na", "nan", "none"}


def _optional_binary(value: str, field: str) -> bool | None:
    x = str(value).strip().lower()
    if x in MISSING:
        return None
    if x in {"1", "true", "t", "yes", "y"}:
        return True
    if x in {"0", "false", "f", "no", "n"}:
        return False
    raise FindlayAnalysisError(f"{field} must be binary or missing, got {value!r}")


def _ratio(a: float, b: float) -> float | None:
    return a / b if b else None


def _read(path: Path, required: set[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise FindlayAnalysisError(f"{path}: missing header")
        missing = required - set(reader.fieldnames)
        if missing:
            raise FindlayAnalysisError(f"{path}: missing {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise FindlayAnalysisError(f"{path}: empty")
    return rows


def _capture_state(row: dict[str, str]) -> tuple[bool | None, bool | None]:
    """Return trigger R and pass-level entry K; None means reference unresolved."""
    r = _optional_binary(row["TRIGGER"], "TRIGGER")
    k_observed = _optional_binary(row["CAPTURE"], "CAPTURE")

    if r is False:
        # A confirmed non-trigger cannot create a camera record from that pass.
        if k_observed is True:
            raise FindlayAnalysisError("confirmed non-triggered pass has positive CAPTURE")
        return False, False

    if r is True:
        # Missing CAPTURE after a confirmed trigger is registration dark mass.
        return True, k_observed

    # Trigger truth itself is unresolved. A separately recorded binary CAPTURE still
    # identifies K, but it must not be used to back-fill the missing R state.
    return None, k_observed


def _bounded_binary_summary(
    *, identified_false: int, identified_true: int, unresolved: int
) -> dict[str, float | int | None]:
    resolved = identified_false + identified_true
    total = resolved + unresolved
    return {
        "resolved_only_false_probability": _ratio(identified_false, resolved),
        "false_probability_bounds": {
            "lower": _ratio(identified_false, total),
            "upper": _ratio(identified_false + unresolved, total),
        },
        "identified_false": identified_false,
        "identified_true": identified_true,
        "unresolved": unresolved,
        "resolved": resolved,
        "total": total,
    }


def _stage_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    r_false = r_true = r_unresolved = 0
    k_false = k_true = k_unresolved = 0
    registration_evaluable_confirmed_trigger = 0
    registration_failure_confirmed_trigger = 0
    registration_unresolved_confirmed_trigger = 0

    for row in rows:
        r, k = _capture_state(row)
        if r is None:
            r_unresolved += 1
        elif r:
            r_true += 1
        else:
            r_false += 1

        if k is None:
            k_unresolved += 1
        elif k:
            k_true += 1
        else:
            k_false += 1

        if r is True:
            if k is None:
                registration_unresolved_confirmed_trigger += 1
            else:
                registration_evaluable_confirmed_trigger += 1
                registration_failure_confirmed_trigger += int(k is False)

    r_summary = _bounded_binary_summary(
        identified_false=r_false,
        identified_true=r_true,
        unresolved=r_unresolved,
    )
    k_summary = _bounded_binary_summary(
        identified_false=k_false,
        identified_true=k_true,
        unresolved=k_unresolved,
    )
    n = len(rows)
    return {
        "pass_count": n,
        "confirmed_triggered_passes": r_true,
        "trigger_unresolved_passes": r_unresolved,
        "trigger_unresolved_fraction_given_pass": r_unresolved / n,
        "confirmed_captured_passes": k_true,
        "capture_unresolved_passes": k_unresolved,
        "capture_unresolved_fraction_given_pass": k_unresolved / n,
        "a_R_no_trigger_given_pass_resolved_only": r_summary[
            "resolved_only_false_probability"
        ],
        "a_R_no_trigger_given_pass_bounds": r_summary["false_probability_bounds"],
        "a_K_no_capture_given_pass_resolved_only": k_summary[
            "resolved_only_false_probability"
        ],
        "a_K_no_capture_given_pass_bounds": k_summary["false_probability_bounds"],
        "registration_evaluable_confirmed_triggered_passes": registration_evaluable_confirmed_trigger,
        "registration_unresolved_confirmed_triggered_passes": registration_unresolved_confirmed_trigger,
        "registration_unresolved_fraction_given_confirmed_trigger": _ratio(
            registration_unresolved_confirmed_trigger, r_true
        ),
        "a_registration_failure_given_confirmed_trigger_evaluable": _ratio(
            registration_failure_confirmed_trigger,
            registration_evaluable_confirmed_trigger,
        ),
        "confirmed_trigger_rate_given_pass": r_true / n,
        "confirmed_capture_rate_given_pass": k_true / n,
        "interpretation": (
            "R and K are each partially identified when their source fields are missing. Resolved-only estimates "
            "are accompanied by worst/best-case bounds; unresolved values are never recoded as failures."
        ),
    }


def _group_stage(rows: list[dict[str, str]], field: str, min_n: int = 1) -> dict[str, Any]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        value = str(row.get(field, "")).strip()
        if value and value.lower() not in MISSING:
            groups[value].append(row)
    out = {k: _stage_summary(v) for k, v in sorted(groups.items()) if len(v) >= min_n}
    if not out:
        return {
            "levels": {},
            "a_R_resolved_only_range": None,
            "a_K_resolved_only_range": None,
        }
    ar = [
        x["a_R_no_trigger_given_pass_resolved_only"]
        for x in out.values()
        if x["a_R_no_trigger_given_pass_resolved_only"] is not None
    ]
    ak = [
        x["a_K_no_capture_given_pass_resolved_only"]
        for x in out.values()
        if x["a_K_no_capture_given_pass_resolved_only"] is not None
    ]
    return {
        "levels": out,
        "a_R_resolved_only_range": max(ar) - min(ar) if ar else None,
        "a_K_resolved_only_range": max(ak) - min(ak) if ak else None,
    }


def _composition(rows: list[dict[str, str]], field: str) -> dict[str, Any]:
    levels = sorted({str(r[field]).strip() for r in rows if str(r[field]).strip()})
    truth_counts = defaultdict(int)
    trigger_counts = defaultdict(int)
    capture_counts = defaultdict(int)
    unresolved_trigger_counts = defaultdict(int)
    unresolved_capture_counts = defaultdict(int)

    for row in rows:
        level = str(row[field]).strip()
        r, k = _capture_state(row)
        truth_counts[level] += 1
        trigger_counts[level] += int(r is True)
        capture_counts[level] += int(k is True)
        unresolved_trigger_counts[level] += int(r is None)
        unresolved_capture_counts[level] += int(k is None)

    truth_n = sum(truth_counts.values())
    trigger_n = sum(trigger_counts.values())
    capture_n = sum(capture_counts.values())
    level_results = {}
    for level in levels:
        tp = truth_counts[level] / truth_n if truth_n else None
        rp = trigger_counts[level] / trigger_n if trigger_n else None
        kp = capture_counts[level] / capture_n if capture_n else None
        level_results[level] = {
            "truth_pass_proportion": tp,
            "confirmed_trigger_world_proportion": rp,
            "confirmed_capture_world_proportion": kp,
            "trigger_unresolved_passes": unresolved_trigger_counts[level],
            "capture_unresolved_passes": unresolved_capture_counts[level],
            "confirmed_trigger_minus_truth": None if tp is None or rp is None else rp - tp,
            "confirmed_capture_minus_truth": None if tp is None or kp is None else kp - tp,
        }
    tv_trigger = (
        0.5 * sum(abs(v["confirmed_trigger_minus_truth"]) for v in level_results.values())
        if trigger_n
        else None
    )
    tv_capture = (
        0.5 * sum(abs(v["confirmed_capture_minus_truth"]) for v in level_results.values())
        if capture_n
        else None
    )
    return {
        "field": field,
        "levels": level_results,
        "confirmed_trigger_count": trigger_n,
        "confirmed_capture_count": capture_n,
        "trigger_unresolved_count": sum(unresolved_trigger_counts.values()),
        "capture_unresolved_count": sum(unresolved_capture_counts.values()),
        "total_variation_truth_vs_confirmed_trigger": tv_trigger,
        "total_variation_truth_vs_confirmed_capture": tv_capture,
        "composition_boundary": (
            "Trigger/capture compositions use only confirmed positive records. Missing process states remain explicit "
            "unresolved mass; composition shifts are therefore descriptive observed-world contrasts, not missingness-corrected estimates."
        ),
    }


def analyze_fox_badger(path: Path) -> dict[str, Any]:
    rows = _read(
        path,
        {"SPECIES", "CT.POS", "ORIENT", "GAIT", "DIST", "LOIT", "TRIGGER", "CAPTURE"},
    )
    species = _group_stage(rows, "SPECIES")
    return {
        "source_file": path.name,
        "overall": _stage_summary(rows),
        "REC_H1_event_conditioned_shadow": {
            "by_species": species,
            "supported": any(
                x["a_R_no_trigger_given_pass_bounds"]["lower"] > 0
                or x["a_K_no_capture_given_pass_bounds"]["lower"] > 0
                for x in species["levels"].values()
            ),
        },
        "REC_H2_structured_selection": {
            "by_species": species,
            "by_distance": _group_stage(rows, "DIST", min_n=5),
            "by_orientation": _group_stage(rows, "ORIENT", min_n=5),
            "by_gait": _group_stage(rows, "GAIT", min_n=5),
            "by_camera_position": _group_stage(rows, "CT.POS", min_n=5),
            "by_loitering": _group_stage(rows, "LOIT", min_n=5),
        },
        "REC_H3_ecological_composition_distortion": {
            "species": _composition(rows, "SPECIES"),
            "gait": _composition(rows, "GAIT"),
            "interpretation": (
                "All rows are known passes. Differences between pass-world and confirmed trigger/capture-world composition "
                "quantify observed record-entry distortion among true encounters; they are not occurrence or abundance estimates."
            ),
        },
    }


def _trigger_state(row: dict[str, str]) -> bool | None:
    return _optional_binary(row["TRIGGER"], "TRIGGER")


def _trigger_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    r_false = r_true = r_unresolved = 0
    for row in rows:
        r = _trigger_state(row)
        if r is None:
            r_unresolved += 1
        elif r:
            r_true += 1
        else:
            r_false += 1
    summary = _bounded_binary_summary(
        identified_false=r_false,
        identified_true=r_true,
        unresolved=r_unresolved,
    )
    n = len(rows)
    return {
        "pass_count": n,
        "confirmed_triggered_passes": r_true,
        "trigger_unresolved_passes": r_unresolved,
        "trigger_unresolved_fraction_given_pass": r_unresolved / n,
        "a_R_no_trigger_given_pass_resolved_only": summary[
            "resolved_only_false_probability"
        ],
        "a_R_no_trigger_given_pass_bounds": summary["false_probability_bounds"],
        "confirmed_trigger_rate_given_pass": r_true / n,
    }


def _group_trigger(rows: list[dict[str, str]], field: str, min_n: int = 1) -> dict[str, Any]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        value = str(row.get(field, "")).strip()
        if value and value.lower() not in MISSING:
            groups[value].append(row)
    out = {k: _trigger_summary(v) for k, v in sorted(groups.items()) if len(v) >= min_n}
    vals = [
        x["a_R_no_trigger_given_pass_resolved_only"]
        for x in out.values()
        if x["a_R_no_trigger_given_pass_resolved_only"] is not None
    ]
    return {
        "levels": out,
        "a_R_resolved_only_range": max(vals) - min(vals) if vals else None,
    }


def _trigger_composition(rows: list[dict[str, str]], field: str) -> dict[str, Any]:
    levels = sorted({str(r[field]).strip() for r in rows if str(r[field]).strip()})
    allc = defaultdict(int)
    trgc = defaultdict(int)
    unr = defaultdict(int)
    for row in rows:
        level = str(row[field]).strip()
        r = _trigger_state(row)
        allc[level] += 1
        trgc[level] += int(r is True)
        unr[level] += int(r is None)
    n = sum(allc.values())
    nt = sum(trgc.values())
    out = {}
    for level in levels:
        p = allc[level] / n if n else None
        q = trgc[level] / nt if nt else None
        out[level] = {
            "truth_pass_proportion": p,
            "confirmed_trigger_world_proportion": q,
            "trigger_unresolved_passes": unr[level],
            "confirmed_trigger_minus_truth": None if p is None or q is None else q - p,
        }
    tv = (
        0.5 * sum(abs(v["confirmed_trigger_minus_truth"]) for v in out.values())
        if nt
        else None
    )
    return {
        "field": field,
        "levels": out,
        "trigger_unresolved_count": sum(unr.values()),
        "total_variation_truth_vs_confirmed_trigger": tv,
    }


def analyze_otter_wetdry(path: Path) -> dict[str, Any]:
    rows = _read(
        path,
        {"CT.POS", "CAMERA.ID", "ORIENT", "GAIT", "DIST", "wet.dry", "LOIT", "TRIGGER"},
    )
    cameras = sorted({r["CAMERA.ID"].strip() for r in rows})
    per_camera = {}
    for camera in cameras:
        sub = [r for r in rows if r["CAMERA.ID"].strip() == camera]
        per_camera[camera] = {
            "overall": _trigger_summary(sub),
            "by_wet_dry": _group_trigger(sub, "wet.dry", min_n=5),
            "wet_dry_composition": _trigger_composition(sub, "wet.dry"),
            "by_distance": _group_trigger(sub, "DIST", min_n=5),
            "by_gait": _group_trigger(sub, "GAIT", min_n=5),
        }
    return {
        "source_file": path.name,
        "overall": _trigger_summary(rows),
        "REC_H1_event_conditioned_shadow": {
            "supported": any(
                v["overall"]["a_R_no_trigger_given_pass_bounds"]["lower"] > 0
                for v in per_camera.values()
            ),
            "by_camera": {k: v["overall"] for k, v in per_camera.items()},
        },
        "REC_H2_structured_selection": {"per_camera": per_camera},
        "REC_H3_condition_composition_distortion": {
            "wet_dry_by_camera": {k: v["wet_dry_composition"] for k, v in per_camera.items()},
            "interpretation": (
                "Wet/dry pass composition is compared with confirmed triggered-record composition separately for each camera type; "
                "unresolved trigger rows remain explicit."
            ),
        },
    }


def analyze(fox_badger: Path, otter_wetdry: Path) -> dict[str, Any]:
    return {
        "schema": "rec-findlay-camera-trap-external-validation-v3",
        "fox_badger_registration": analyze_fox_badger(fox_badger),
        "otter_wet_dry_trigger": analyze_otter_wetdry(otter_wetdry),
        "identification_boundary": (
            "These public tables are conditioned on independently observed animal passes. They identify event-conditioned "
            "trigger/capture loss and composition distortion among true passes, but they do not enumerate non-pass time exposure. "
            "Therefore q_shadow=P(event|no record) over a master temporal denominator is not identified and is intentionally not reported. "
            "Missing TRIGGER/CAPTURE values are retained as process-specific reference-unresolved dark mass and bounded rather than coerced to failure."
        ),
        "positioning_boundary": (
            "Findlay et al. explicitly studied component detection probabilities and false negatives. REC does not claim those empirical "
            "patterns as new; this analysis uses them as an external real-world validation that REC A/R/K-style record-entry estimands "
            "map onto an independently studied camera-trap observation process."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fox_badger_registration_csv", type=Path)
    parser.add_argument("otter_wetdry_trigger_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(args.fox_badger_registration_csv, args.otter_wetdry_trigger_csv)
    except FindlayAnalysisError as exc:
        raise SystemExit(f"Findlay REC analysis failed: {exc}") from exc
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
