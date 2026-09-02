#!/usr/bin/env python3
"""Estimate REC acquisition/gate/entry shadow quantities from validated tables."""
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

    totals = defaultdict(float)
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
        if truth not in {"positive", "negative"}:
            continue

        sampled_rows += 1
        w = _weight(row)
        positive = truth == "positive"

        totals["resolved"] += w
        if positive:
            totals["positive"] += w

        if not primary_available:
            totals["A0_resolved"] += w
            if positive:
                totals["A0_positive"] += w

        if not gate_evaluable:
            totals["gate_unevaluable_resolved"] += w
            if positive:
                totals["gate_unevaluable_positive"] += w
        else:
            totals["gate_evaluable_resolved"] += w
            if positive:
                totals["gate_evaluable_positive"] += w
            r = _optional_bool(row["registered_deviation"], "registered_deviation")
            if r is None:
                raise AnalysisError(
                    f"window {wid!r}: gate-evaluable truth row lacks registered_deviation"
                )
            if not r:
                totals["R0_resolved"] += w
                if positive:
                    totals["R0_positive"] += w

        if not k:
            totals["K0_resolved"] += w
            if positive:
                totals["K0_positive"] += w

    return {
        "schema": "rec-shadow-selection-analysis-v2",
        "ledger_path": str(ledger_path),
        "truth_path": str(truth_path),
        "joined_truth_rows": joined_rows,
        "weighted_resolved_truth_sample_rows": sampled_rows,
        "weighted_totals": dict(totals),
        "estimands": {
            "q_acquisition_shadow_event_given_primary_unavailable": _ratio(
                totals["A0_positive"], totals["A0_resolved"]
            ),
            "a_A_primary_unavailable_given_event": _ratio(
                totals["A0_positive"], totals["positive"]
            ),
            "q_gate_unevaluable_event_given_gate_unevaluable": _ratio(
                totals["gate_unevaluable_positive"], totals["gate_unevaluable_resolved"]
            ),
            "a_gate_unevaluable_given_event": _ratio(
                totals["gate_unevaluable_positive"], totals["positive"]
            ),
            "q_B_event_given_registered_baseline_gate_evaluable": _ratio(
                totals["R0_positive"], totals["R0_resolved"]
            ),
            "a_R_registered_baseline_given_event_gate_evaluable": _ratio(
                totals["R0_positive"], totals["gate_evaluable_positive"]
            ),
            "q_shadow_event_given_no_record_entry": _ratio(
                totals["K0_positive"], totals["K0_resolved"]
            ),
            "a_K_no_record_entry_given_event": _ratio(
                totals["K0_positive"], totals["positive"]
            ),
        },
        "interpretation_boundary": (
            "Design-weighted descriptive estimands are separated by acquisition, gate-evaluability and entry layer. "
            "Confirmatory uncertainty must respect independent ecological units, the master exposure universe, "
            "and the frozen truth-sampling design."
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
