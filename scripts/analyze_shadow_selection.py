#!/usr/bin/env python3
"""Estimate REC acquisition/gate/entry shadow quantities from validated tables.

The analysis is deliberately explicit about reference-unresolved mass. Resolved-only
point estimates are reported together with worst/best-case bounds that allow every
sampled unresolved truth label to be either positive or negative. No unresolved
window is silently converted to no-event.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


class AnalysisError(ValueError):
    pass


def _bool(value: str, field: str) -> bool:
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y"}:
        return True
    if text in {"0", "false", "f", "no", "n"}:
        return False
    raise AnalysisError(f"{field} must be boolean, got {value!r}")


def _optional_bool(value: str, field: str) -> bool | None:
    if not str(value).strip():
        return None
    return _bool(value, field)


def _weight(row: dict[str, str]) -> float:
    if not _bool(row["truth_sampled"], "truth_sampled"):
        return 0.0
    try:
        w = float(row["truth_sampling_weight"])
    except (TypeError, ValueError) as exc:
        raise AnalysisError("sampled truth row requires numeric truth_sampling_weight") from exc
    if not math.isfinite(w) or w <= 0:
        raise AnalysisError("truth_sampling_weight must be finite and >0")
    return w


def _ratio(num: float, den: float) -> float | None:
    return num / den if den > 0 else None


def _add_truth(totals: dict[str, float], prefix: str, truth: str, weight: float) -> None:
    totals[f"{prefix}_sampled"] += weight
    if truth == "unresolved":
        totals[f"{prefix}_unresolved"] += weight
        return
    totals[f"{prefix}_resolved"] += weight
    if truth == "positive":
        totals[f"{prefix}_positive"] += weight


def _q_summary(totals: dict[str, float], prefix: str) -> dict[str, float | None]:
    """P(E=1 | H) with unresolved truth bounded as unknown binary event status."""
    positive = totals[f"{prefix}_positive"]
    resolved = totals[f"{prefix}_resolved"]
    unresolved = totals[f"{prefix}_unresolved"]
    sampled = resolved + unresolved
    return {
        "resolved_only_estimate": _ratio(positive, resolved),
        "lower": _ratio(positive, sampled),
        "upper": _ratio(positive + unresolved, sampled),
        "weighted_resolved": resolved,
        "weighted_unresolved": unresolved,
        "reference_unresolved_fraction": _ratio(unresolved, sampled),
    }


def _a_summary(
    totals: dict[str, float], *, event_prefix: str, parent_prefix: str
) -> dict[str, float | None]:
    """P(H | E=1,parent) with unresolved truth assigned adversarially."""
    h_pos = totals[f"{event_prefix}_positive"]
    h_unres = totals[f"{event_prefix}_unresolved"]
    parent_pos = totals[f"{parent_prefix}_positive"]
    parent_unres = totals[f"{parent_prefix}_unresolved"]

    if h_pos > parent_pos + 1e-9 or h_unres > parent_unres + 1e-9:
        raise AnalysisError(
            f"internal layer accounting error: {event_prefix} is not nested in {parent_prefix}"
        )

    nonh_pos = parent_pos - h_pos
    nonh_unres = parent_unres - h_unres

    return {
        "resolved_only_estimate": _ratio(h_pos, parent_pos),
        "lower": _ratio(h_pos, h_pos + nonh_pos + nonh_unres),
        "upper": _ratio(h_pos + h_unres, h_pos + h_unres + nonh_pos),
        "weighted_parent_resolved_positive": parent_pos,
        "weighted_parent_unresolved": parent_unres,
    }


def load_ledger(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise AnalysisError("exposure ledger has no header")
        needed = {
            "window_id",
            "primary_stream_available",
            "gate_evaluable",
            "record_entry_present",
        }
        missing = needed - set(reader.fieldnames)
        if missing:
            raise AnalysisError(f"exposure ledger missing: {', '.join(sorted(missing))}")
        out: dict[str, dict[str, str]] = {}
        for row in reader:
            wid = row["window_id"].strip()
            if wid in out:
                raise AnalysisError(f"duplicate ledger window_id {wid!r}")
            out[wid] = row
        return out


def load_truth(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise AnalysisError("truth table has no header")
        needed = {
            "window_id",
            "primary_stream_available",
            "gate_evaluable",
            "registered_deviation",
            "target_truth",
            "truth_sampled",
            "truth_sampling_weight",
        }
        missing = needed - set(reader.fieldnames)
        if missing:
            raise AnalysisError(f"truth table missing: {', '.join(sorted(missing))}")
        return list(reader)


def analyze(ledger_path: Path, truth_path: Path) -> dict[str, Any]:
    ledger = load_ledger(ledger_path)
    truth_rows = load_truth(truth_path)

    totals: dict[str, float] = defaultdict(float)
    sampled_rows = 0
    joined_rows = 0

    for row in truth_rows:
        wid = row["window_id"].strip()
        if wid not in ledger:
            raise AnalysisError(f"truth window {wid!r} absent from exposure ledger")
        joined_rows += 1

        ledger_row = ledger[wid]
        primary_available = _bool(
            ledger_row["primary_stream_available"], "ledger.primary_stream_available"
        )
        gate_evaluable = _bool(ledger_row["gate_evaluable"], "ledger.gate_evaluable")
        k = _bool(ledger_row["record_entry_present"], "ledger.record_entry_present")

        if _bool(row["primary_stream_available"], "truth.primary_stream_available") != primary_available:
            raise AnalysisError(f"window {wid!r}: primary_stream_available disagrees across tables")
        if _bool(row["gate_evaluable"], "truth.gate_evaluable") != gate_evaluable:
            raise AnalysisError(f"window {wid!r}: gate_evaluable disagrees across tables")

        if not _bool(row["truth_sampled"], "truth_sampled"):
            continue

        truth = row["target_truth"].strip().lower()
        if truth not in {"positive", "negative", "unresolved"}:
            raise AnalysisError(f"window {wid!r}: invalid target_truth {truth!r}")

        sampled_rows += 1
        w = _weight(row)
        _add_truth(totals, "all", truth, w)

        if not primary_available:
            _add_truth(totals, "A0", truth, w)
        else:
            _add_truth(totals, "A1", truth, w)
            if not gate_evaluable:
                _add_truth(totals, "G0", truth, w)
            else:
                _add_truth(totals, "G1", truth, w)
                r = _optional_bool(row["registered_deviation"], "registered_deviation")
                if r is None:
                    raise AnalysisError(
                        f"window {wid!r}: gate-evaluable truth row lacks registered_deviation"
                    )
                if not r:
                    _add_truth(totals, "R0", truth, w)
                else:
                    _add_truth(totals, "R1", truth, w)

        if not k:
            _add_truth(totals, "K0", truth, w)
        else:
            _add_truth(totals, "K1", truth, w)

    if sampled_rows == 0:
        raise AnalysisError("truth table contains no probability-sampled rows")

    q_acquisition = _q_summary(totals, "A0")
    q_gate_unevaluable = _q_summary(totals, "G0")
    q_baseline = _q_summary(totals, "R0")
    q_shadow = _q_summary(totals, "K0")

    a_acquisition = _a_summary(totals, event_prefix="A0", parent_prefix="all")
    a_gate_unevaluable = _a_summary(totals, event_prefix="G0", parent_prefix="A1")
    a_baseline = _a_summary(totals, event_prefix="R0", parent_prefix="G1")
    a_no_entry = _a_summary(totals, event_prefix="K0", parent_prefix="all")

    legacy_estimands = {
        "q_acquisition_shadow_event_given_primary_unavailable": q_acquisition["resolved_only_estimate"],
        "a_A_primary_unavailable_given_event": a_acquisition["resolved_only_estimate"],
        "q_gate_unevaluable_event_given_gate_unevaluable": q_gate_unevaluable["resolved_only_estimate"],
        "a_gate_unevaluable_given_event": a_gate_unevaluable["resolved_only_estimate"],
        "q_B_event_given_registered_baseline_gate_evaluable": q_baseline["resolved_only_estimate"],
        "a_R_registered_baseline_given_event_gate_evaluable": a_baseline["resolved_only_estimate"],
        "q_shadow_event_given_no_record_entry": q_shadow["resolved_only_estimate"],
        "a_K_no_record_entry_given_event": a_no_entry["resolved_only_estimate"],
    }

    return {
        "schema": "rec-shadow-selection-analysis-v3",
        "ledger_path": str(ledger_path),
        "truth_path": str(truth_path),
        "joined_truth_rows": joined_rows,
        "probability_sampled_truth_rows": sampled_rows,
        "weighted_totals": dict(totals),
        "reference_resolution": {
            "overall": _q_summary(totals, "all"),
            "acquisition_shadow_A0": q_acquisition,
            "gate_unevaluable_after_acquisition_G0": q_gate_unevaluable,
            "gate_shadow_registered_baseline_R0": q_baseline,
            "record_shadow_no_entry_K0": q_shadow,
        },
        "estimands": legacy_estimands,
        "partial_identification": {
            "q_event_given_acquisition_shadow_A0": q_acquisition,
            "a_primary_unavailable_given_event": a_acquisition,
            "q_event_given_gate_unevaluable_after_acquisition_G0": q_gate_unevaluable,
            "a_gate_unevaluable_given_event_primary_available": a_gate_unevaluable,
            "q_event_given_registered_baseline_R0": q_baseline,
            "a_registered_baseline_given_event_gate_evaluable": a_baseline,
            "q_event_given_no_record_entry_K0": q_shadow,
            "a_no_record_entry_given_event": a_no_entry,
        },
        "interpretation_boundary": (
            "Resolved-only estimates are conditional on reference-resolved truth. Bounds treat every sampled "
            "reference-unresolved label as unknown positive/negative truth and expose the REC dark mass instead "
            "of converting it to no-event. Gate-unevaluable loss is conditioned on primary acquisition being "
            "available so acquisition and gate layers are not double-counted. Confirmatory uncertainty must also "
            "respect independent ecological units, the master exposure universe and the frozen truth-sampling design."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger_csv", type=Path)
    parser.add_argument("truth_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        result = analyze(args.ledger_csv, args.truth_csv)
    except AnalysisError as exc:
        raise SystemExit(f"REC shadow analysis failed: {exc}") from exc

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
