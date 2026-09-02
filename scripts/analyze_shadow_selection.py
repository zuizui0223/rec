#!/usr/bin/env python3
"""Estimate REC gate/entry shadow quantities from a validated exposure ledger and truth sample."""
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
        needed = {"window_id", "record_entry_present"}
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

        if not _bool(row["truth_sampled"], "truth_sampled"):
            continue
        truth = row["target_truth"].strip().lower()
        if truth not in {"positive", "negative"}:
            continue

        sampled_rows += 1
        w = _weight(row)
        r = _bool(row["registered_deviation"], "registered_deviation")
        k = _bool(ledger[wid]["record_entry_present"], "record_entry_present")
        positive = truth == "positive"

        totals["resolved"] += w
        if positive:
            totals["positive"] += w
        if not r:
            totals["R0_resolved"] += w
            if positive:
                totals["R0_positive"] += w
        if not k:
            totals["K0_resolved"] += w
            if positive:
                totals["K0_positive"] += w

    return {
        "schema": "rec-shadow-selection-analysis-v1",
        "ledger_path": str(ledger_path),
        "truth_path": str(truth_path),
        "joined_truth_rows": joined_rows,
        "weighted_resolved_truth_sample_rows": sampled_rows,
        "weighted_totals": dict(totals),
        "estimands": {
            "q_B_event_given_registered_baseline": _ratio(
                totals["R0_positive"], totals["R0_resolved"]
            ),
            "a_R_registered_baseline_given_event": _ratio(
                totals["R0_positive"], totals["positive"]
            ),
            "q_shadow_event_given_no_record_entry": _ratio(
                totals["K0_positive"], totals["K0_resolved"]
            ),
            "a_K_no_record_entry_given_event": _ratio(
                totals["K0_positive"], totals["positive"]
            ),
        },
        "interpretation_boundary": (
            "These are design-weighted descriptive estimands over reference-resolved sampled exposures. "
            "Confirmatory uncertainty must respect independent ecological units and the frozen sampling design."
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
