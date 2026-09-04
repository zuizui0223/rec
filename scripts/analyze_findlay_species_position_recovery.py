#!/usr/bin/env python3
"""Secondary REC recovery/transport endpoint on Findlay fox/badger data.

For each physical CT position, estimate species-specific trigger and final-entry
probabilities from all other positions, then evaluate whether self-normalized IPW
moves the held-out position's recorded badger composition toward the CCTV pass
composition. A species-swapped propensity is a falsification control.

This is a retrospective secondary-endpoint robustness analysis. It is not
independent-animal or prospective confirmation.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


MISSING = {"", "na", "nan", "none"}
SPECIES = ("BADGER", "FOX")


class SpeciesRecoveryError(ValueError):
    pass


def _optional_binary(value: str, field: str) -> bool | None:
    x = str(value).strip().lower()
    if x in {"1", "true", "t", "yes", "y"}:
        return True
    if x in {"0", "false", "f", "no", "n"}:
        return False
    if x in MISSING:
        return None
    raise SpeciesRecoveryError(f"{field} must be binary or missing, got {value!r}")


def _states(row: dict[str, str]) -> tuple[bool | None, bool | None]:
    """Return trigger R and final record entry K for one known animal pass."""
    r = _optional_binary(row["TRIGGER"], "TRIGGER")
    capture = _optional_binary(row["CAPTURE"], "CAPTURE")
    if r is False:
        if capture is True:
            raise SpeciesRecoveryError("non-trigger pass cannot have positive capture")
        return False, False
    if r is True:
        return True, capture
    # Missing trigger may coexist with separately coded capture; do not backfill R.
    return None, capture


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise SpeciesRecoveryError("input has no header")
        required = {"SPECIES", "CT.POS", "TRIGGER", "CAPTURE"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise SpeciesRecoveryError(f"input missing: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise SpeciesRecoveryError("input is empty")
    for row in rows:
        sp = row["SPECIES"].strip().upper()
        if sp not in SPECIES:
            raise SpeciesRecoveryError(f"unexpected species {sp!r}")
        if not row["CT.POS"].strip():
            raise SpeciesRecoveryError("blank CT.POS")
        _states(row)
    return rows


def _ratio(a: float, b: float) -> float | None:
    return a / b if b > 0 else None


def _stage_counts(rows: list[dict[str, str]], stage: str) -> dict[str, dict[str, int]]:
    if stage not in {"trigger", "capture"}:
        raise SpeciesRecoveryError(f"invalid stage {stage}")
    out = {
        sp: {"passes": 0, "resolved": 0, "entered": 0, "unresolved": 0}
        for sp in SPECIES
    }
    for row in rows:
        sp = row["SPECIES"].strip().upper()
        r, k = _states(row)
        state = r if stage == "trigger" else k
        d = out[sp]
        d["passes"] += 1
        if state is None:
            d["unresolved"] += 1
        else:
            d["resolved"] += 1
            d["entered"] += int(state)
    return out


def _propensities(rows: list[dict[str, str]], stage: str) -> dict[str, dict[str, float | int | None]]:
    counts = _stage_counts(rows, stage)
    out: dict[str, dict[str, float | int | None]] = {}
    for sp, d in counts.items():
        out[sp] = {
            **d,
            "point": _ratio(d["entered"], d["resolved"]),
            "lower": _ratio(d["entered"], d["passes"]),
            "upper": _ratio(d["entered"] + d["unresolved"], d["passes"]),
        }
    return out


def _weighted_badger(entered_badger: int, entered_fox: int, p_badger: float, p_fox: float) -> float | None:
    if p_badger <= 0 or p_fox <= 0:
        return None
    wb = entered_badger / p_badger
    wf = entered_fox / p_fox
    return _ratio(wb, wb + wf)


def _evaluate_stage(
    rows: list[dict[str, str]], heldout_position: str, stage: str
) -> dict[str, Any] | None:
    train = [r for r in rows if r["CT.POS"].strip() != heldout_position]
    test = [r for r in rows if r["CT.POS"].strip() == heldout_position]
    if not train or not test:
        return None

    prop = _propensities(train, stage)
    test_counts = _stage_counts(test, stage)
    total_passes = sum(test_counts[sp]["passes"] for sp in SPECIES)
    truth_badger = _ratio(test_counts["BADGER"]["passes"], total_passes)
    eb = test_counts["BADGER"]["entered"]
    ef = test_counts["FOX"]["entered"]
    raw_badger = _ratio(eb, eb + ef)
    p_b = prop["BADGER"]["point"]
    p_f = prop["FOX"]["point"]
    if None in {truth_badger, raw_badger, p_b, p_f}:
        return None
    if float(p_b) <= 0 or float(p_f) <= 0:
        return None

    corrected = _weighted_badger(eb, ef, float(p_b), float(p_f))
    sham = _weighted_badger(eb, ef, float(p_f), float(p_b))
    if corrected is None or sham is None:
        return None

    p_b_lo, p_b_hi = prop["BADGER"]["lower"], prop["BADGER"]["upper"]
    p_f_lo, p_f_hi = prop["FOX"]["lower"], prop["FOX"]["upper"]
    lower = upper = None
    if None not in {p_b_lo, p_b_hi, p_f_lo, p_f_hi}:
        # Badger weighted share decreases with larger badger propensity and
        # increases with larger fox propensity.
        lower = _weighted_badger(eb, ef, float(p_b_hi), float(p_f_lo))
        upper = _weighted_badger(eb, ef, float(p_b_lo), float(p_f_hi))

    raw_err = abs(float(raw_badger) - float(truth_badger))
    corr_err = abs(corrected - float(truth_badger))
    sham_err = abs(sham - float(truth_badger))
    worst_corr = None
    if lower is not None and upper is not None:
        worst_corr = max(abs(lower - float(truth_badger)), abs(upper - float(truth_badger)))

    return {
        "heldout_position": heldout_position,
        "stage": stage,
        "training_rows": len(train),
        "test_rows": len(test),
        "training_species_entry_propensities": prop,
        "heldout_counts": test_counts,
        "truth_badger_pass_proportion": truth_badger,
        "raw_recorded_badger_proportion": raw_badger,
        "correct_ipw_badger_proportion": corrected,
        "sham_swapped_ipw_badger_proportion": sham,
        "correct_ipw_unresolved_training_bounds": {"lower": lower, "upper": upper},
        "absolute_error_raw": raw_err,
        "absolute_error_correct": corr_err,
        "absolute_error_sham": sham_err,
        "worst_case_absolute_error_correct_under_unresolved_training": worst_corr,
        "correct_improves_on_raw": corr_err < raw_err,
        "correct_beats_sham": corr_err < sham_err,
    }


def _mean(values: list[float]) -> float:
    if not values:
        raise SpeciesRecoveryError("empty aggregate")
    return sum(values) / len(values)


def _aggregate(cells: list[dict[str, Any]]) -> dict[str, Any]:
    raw = _mean([float(x["absolute_error_raw"]) for x in cells])
    corr = _mean([float(x["absolute_error_correct"]) for x in cells])
    sham = _mean([float(x["absolute_error_sham"]) for x in cells])
    worst_vals = [
        float(x["worst_case_absolute_error_correct_under_unresolved_training"])
        for x in cells
        if x["worst_case_absolute_error_correct_under_unresolved_training"] is not None
    ]
    return {
        "position_count": len(cells),
        "mean_absolute_error_raw": raw,
        "mean_absolute_error_correct": corr,
        "mean_absolute_error_sham": sham,
        "relative_error_reduction_correct_vs_raw": ((raw - corr) / raw if raw > 0 else None),
        "positions_improved": sum(int(x["correct_improves_on_raw"]) for x in cells),
        "positions_beating_sham": sum(int(x["correct_beats_sham"]) for x in cells),
        "mean_worst_case_error_correct_under_unresolved_training": (
            _mean(worst_vals) if worst_vals else None
        ),
    }


def analyze(rows: list[dict[str, str]]) -> dict[str, Any]:
    positions = sorted({r["CT.POS"].strip() for r in rows})
    stages: dict[str, Any] = {}
    for stage in ("trigger", "capture"):
        cells: list[dict[str, Any]] = []
        skipped: list[str] = []
        for pos in positions:
            result = _evaluate_stage(rows, pos, stage)
            if result is None:
                skipped.append(pos)
            else:
                cells.append(result)
        if not cells:
            raise SpeciesRecoveryError(f"no evaluable {stage} cells")
        stages[stage] = {
            "cells": cells,
            "skipped_positions": skipped,
            "aggregate": _aggregate(cells),
        }
    return {
        "schema": "rec-findlay-species-position-recovery-v1",
        "estimand": "badger proportion among CCTV-confirmed fox/badger passes within held-out CT positions",
        "design": "leave one physical CT position out; estimate species-specific entry probability on all other positions using the same Bushnell-video observation system",
        "positions": positions,
        "stages": stages,
        "governance_boundary": "Retrospective secondary-endpoint robustness analysis. It tests spatial/position transport within the same camera system, not independent animals or prospective confirmation.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("fox_badger_csv", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = analyze(_read(args.fox_badger_csv))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
