#!/usr/bin/env python3
"""Map Findlay camera-trap pass/trigger/capture data onto REC estimands.

Every input row is an independently observed animal pass. This supports event-conditioned
loss quantities such as P(no trigger | pass) and bounded P(no capture | pass), but not the
full time-denominator q_shadow = P(event | no record).

A triggered pass with missing CAPTURE is retained as reference-unresolved registration
mass. It is never silently converted to capture failure.
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


def _binary(value: str, field: str) -> bool:
    x = str(value).strip().lower()
    if x in {"1", "true", "t", "yes", "y"}:
        return True
    if x in {"0", "false", "f", "no", "n"}:
        return False
    raise FindlayAnalysisError(f"{field} must be binary, got {value!r}")


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


def _capture_state(row: dict[str, str]) -> tuple[bool, bool | None]:
    """Return trigger R and pass-level entry K; None means registration unresolved."""
    r = _binary(row["TRIGGER"], "TRIGGER")
    text = str(row["CAPTURE"]).strip().lower()
    if r:
        if text in MISSING:
            return True, None
        return True, _binary(text, "CAPTURE")

    # Without a trigger there is no camera-created record from that pass. Missing CAPTURE
    # therefore has known K=0 semantics, while a positive CAPTURE would be contradictory.
    if text not in MISSING | {"0", "false", "f", "no", "n"}:
        raise FindlayAnalysisError("non-triggered pass has positive CAPTURE")
    return False, False


def _stage_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    n = len(rows)
    trigger = 0
    capture = 0
    unresolved_triggered = 0
    evaluable_triggered = 0
    capture_fail_after_trigger = 0
    identified_no_entry = 0

    for row in rows:
        r, k = _capture_state(row)
        trigger += int(r)
        if r and k is None:
            unresolved_triggered += 1
            continue
        if r:
            evaluable_triggered += 1
            capture_fail_after_trigger += int(k is False)
        capture += int(k is True)
        identified_no_entry += int(k is False)

    resolved_k_passes = n - unresolved_triggered
    lower = identified_no_entry / n
    upper = (identified_no_entry + unresolved_triggered) / n
    return {
        "pass_count": n,
        "triggered_passes": trigger,
        "captured_passes_confirmed": capture,
        "registration_evaluable_triggered_passes": evaluable_triggered,
        "registration_unresolved_triggered_passes": unresolved_triggered,
        "registration_unresolved_fraction_given_trigger": _ratio(unresolved_triggered, trigger),
        "a_R_no_trigger_given_pass": 1.0 - trigger / n,
        "a_K_no_capture_given_pass_resolved_only": _ratio(identified_no_entry, resolved_k_passes),
        "a_K_no_capture_given_pass_bounds": {"lower": lower, "upper": upper},
        "a_registration_failure_given_trigger_evaluable": _ratio(
            capture_fail_after_trigger, evaluable_triggered
        ),
        "trigger_rate_given_pass": trigger / n,
        "confirmed_capture_rate_given_pass": capture / n,
        "interpretation": (
            "Triggered passes with missing CAPTURE are registration-unresolved. They are excluded from the "
            "resolved-only K estimate and assigned adversarially in the pass-level K bounds."
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
            "a_R_range": None,
            "a_K_resolved_only_range": None,
        }
    ar = [x["a_R_no_trigger_given_pass"] for x in out.values()]
    ak = [
        x["a_K_no_capture_given_pass_resolved_only"]
        for x in out.values()
        if x["a_K_no_capture_given_pass_resolved_only"] is not None
    ]
    return {
        "levels": out,
        "a_R_range": max(ar) - min(ar),
        "a_K_resolved_only_range": max(ak) - min(ak) if ak else None,
    }


def _composition(rows: list[dict[str, str]], field: str) -> dict[str, Any]:
    levels = sorted({str(r[field]).strip() for r in rows if str(r[field]).strip()})
    truth_counts = defaultdict(int)
    trigger_counts = defaultdict(int)
    capture_counts = defaultdict(int)
    unresolved_capture_counts = defaultdict(int)
    for row in rows:
        level = str(row[field]).strip()
        r, k = _capture_state(row)
        truth_counts[level] += 1
        trigger_counts[level] += int(r)
        capture_counts[level] += int(k is True)
        unresolved_capture_counts[level] += int(r and k is None)

    truth_n = sum(truth_counts.values())
    trigger_n = sum(trigger_counts.values())
    capture_n = sum(capture_counts.values())
    unresolved_n = sum(unresolved_capture_counts.values())
    level_results = {}
    for level in levels:
        tp = truth_counts[level] / truth_n if truth_n else None
        rp = trigger_counts[level] / trigger_n if trigger_n else None
        kp = capture_counts[level] / capture_n if capture_n else None
        level_results[level] = {
            "truth_pass_proportion": tp,
            "trigger_world_proportion": rp,
            "confirmed_capture_world_proportion": kp,
            "registration_unresolved_triggered_passes": unresolved_capture_counts[level],
            "trigger_minus_truth": None if tp is None or rp is None else rp - tp,
            "confirmed_capture_minus_truth": None if tp is None or kp is None else kp - tp,
        }
    tv_trigger = (
        0.5 * sum(abs(v["trigger_minus_truth"]) for v in level_results.values())
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
        "confirmed_capture_count": capture_n,
        "registration_unresolved_triggered_count": unresolved_n,
        "total_variation_truth_vs_trigger": tv_trigger,
        "total_variation_truth_vs_confirmed_capture": tv_capture,
        "capture_composition_boundary": (
            "Capture-world composition uses confirmed CAPTURE=1 rows only; triggered rows with missing "
            "CAPTURE remain explicit unresolved mass and are not recoded as non-captures."
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
                x["a_R_no_trigger_given_pass"] > 0
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
                "All rows are known passes. Differences between pass-world, trigger-world and confirmed-capture-world "
                "composition quantify record-entry distortion among true encounters; they are not occurrence or abundance estimates."
            ),
        },
    }


def _trigger_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    n = len(rows)
    trig = sum(_binary(r["TRIGGER"], "TRIGGER") for r in rows)
    return {
        "pass_count": n,
        "triggered_passes": trig,
        "a_R_no_trigger_given_pass": 1.0 - trig / n,
        "trigger_rate_given_pass": trig / n,
    }


def _group_trigger(rows: list[dict[str, str]], field: str, min_n: int = 1) -> dict[str, Any]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        value = str(row.get(field, "")).strip()
        if value and value.lower() not in MISSING:
            groups[value].append(row)
    out = {k: _trigger_summary(v) for k, v in sorted(groups.items()) if len(v) >= min_n}
    vals = [x["a_R_no_trigger_given_pass"] for x in out.values()]
    return {"levels": out, "a_R_range": max(vals) - min(vals) if vals else None}


def _trigger_composition(rows: list[dict[str, str]], field: str) -> dict[str, Any]:
    levels = sorted({str(r[field]).strip() for r in rows if str(r[field]).strip()})
    allc = defaultdict(int)
    trgc = defaultdict(int)
    for row in rows:
        level = str(row[field]).strip()
        allc[level] += 1
        trgc[level] += int(_binary(row["TRIGGER"], "TRIGGER"))
    n = sum(allc.values())
    nt = sum(trgc.values())
    out = {}
    for level in levels:
        p = allc[level] / n if n else None
        q = trgc[level] / nt if nt else None
        out[level] = {
            "truth_pass_proportion": p,
            "trigger_world_proportion": q,
            "trigger_minus_truth": None if p is None or q is None else q - p,
        }
    tv = 0.5 * sum(abs(v["trigger_minus_truth"]) for v in out.values()) if nt else None
    return {"field": field, "levels": out, "total_variation_truth_vs_trigger": tv}


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
                v["overall"]["a_R_no_trigger_given_pass"] > 0 for v in per_camera.values()
            ),
            "by_camera": {k: v["overall"] for k, v in per_camera.items()},
        },
        "REC_H2_structured_selection": {"per_camera": per_camera},
        "REC_H3_condition_composition_distortion": {
            "wet_dry_by_camera": {k: v["wet_dry_composition"] for k, v in per_camera.items()},
            "interpretation": (
                "Wet/dry pass composition is compared with the composition among triggered records separately for each camera type."
            ),
        },
    }


def analyze(fox_badger: Path, otter_wetdry: Path) -> dict[str, Any]:
    return {
        "schema": "rec-findlay-camera-trap-external-validation-v2",
        "fox_badger_registration": analyze_fox_badger(fox_badger),
        "otter_wet_dry_trigger": analyze_otter_wetdry(otter_wetdry),
        "identification_boundary": (
            "These public tables are conditioned on independently observed animal passes. They identify event-conditioned "
            "trigger/capture loss and composition distortion among true passes, but they do not enumerate non-pass time exposure. "
            "Therefore q_shadow=P(event|no record) over a master temporal denominator is not identified and is intentionally not reported. "
            "Missing CAPTURE after a trigger is retained as registration-unresolved dark mass and bounded rather than coerced to failure."
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
