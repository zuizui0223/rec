#!/usr/bin/env python3
"""Partition the REC exposure universe by record entry and reference resolvability."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


class PartitionError(ValueError):
    pass


def _bool(value: str, field: str) -> bool:
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y"}:
        return True
    if text in {"0", "false", "f", "no", "n"}:
        return False
    raise PartitionError(f"{field} must be boolean, got {value!r}")


def _weight(row: dict[str, str]) -> float:
    try:
        w = float(row["truth_sampling_weight"])
    except (TypeError, ValueError) as exc:
        raise PartitionError("sampled truth row requires numeric truth_sampling_weight") from exc
    if not math.isfinite(w) or w <= 0:
        raise PartitionError("truth_sampling_weight must be finite and >0")
    return w


def _ratio(num: float, den: float) -> float | None:
    return num / den if den > 0 else None


def load_ledger(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise PartitionError("exposure ledger has no header")
        needed = {"window_id", "record_entry_present"}
        missing = needed - set(reader.fieldnames)
        if missing:
            raise PartitionError(f"exposure ledger missing: {', '.join(sorted(missing))}")
        rows: dict[str, dict[str, str]] = {}
        for row in reader:
            wid = row["window_id"].strip()
            if not wid:
                raise PartitionError("exposure ledger contains blank window_id")
            if wid in rows:
                raise PartitionError(f"duplicate ledger window_id {wid!r}")
            rows[wid] = row
        return rows


def load_truth(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise PartitionError("truth table has no header")
        needed = {"window_id", "truth_sampled", "target_truth", "truth_sampling_weight"}
        missing = needed - set(reader.fieldnames)
        if missing:
            raise PartitionError(f"truth table missing: {', '.join(sorted(missing))}")
        rows: dict[str, dict[str, str]] = {}
        for row in reader:
            wid = row["window_id"].strip()
            if not wid:
                raise PartitionError("truth table contains blank window_id")
            if wid in rows:
                raise PartitionError(f"duplicate truth window_id {wid!r}")
            rows[wid] = row
        return rows


def reference_state(row: dict[str, str] | None) -> str:
    if row is None:
        return "not_audited"
    if not _bool(row["truth_sampled"], "truth_sampled"):
        return "not_sampled"
    truth = row["target_truth"].strip().lower()
    if truth in {"positive", "negative"}:
        return "resolved"
    if truth == "unresolved":
        return "unresolved"
    raise PartitionError(f"invalid target_truth {truth!r}")


def analyze(ledger_path: Path, truth_path: Path) -> dict[str, Any]:
    ledger = load_ledger(ledger_path)
    truth = load_truth(truth_path)

    missing_ledger = sorted(set(truth) - set(ledger))
    if missing_ledger:
        raise PartitionError(
            "truth table contains IDs absent from exposure ledger: " + ", ".join(missing_ledger[:5])
        )

    raw = Counter()
    weighted = defaultdict(float)
    weighted_truth = defaultdict(float)

    for wid, lrow in ledger.items():
        record = "entered" if _bool(lrow["record_entry_present"], "record_entry_present") else "shadow"
        trow = truth.get(wid)
        ref = reference_state(trow)
        raw[f"{record}__{ref}"] += 1

        if ref in {"resolved", "unresolved"}:
            assert trow is not None
            w = _weight(trow)
            weighted[f"{record}__{ref}"] += w
            if ref == "resolved":
                event = trow["target_truth"].strip().lower()
                weighted_truth[f"{record}__{event}"] += w

    shadow_resolved = weighted["shadow__resolved"]
    shadow_unresolved = weighted["shadow__unresolved"]
    shadow_sampled = shadow_resolved + shadow_unresolved
    shadow_positive = weighted_truth["shadow__positive"]

    entered_resolved = weighted["entered__resolved"]
    entered_unresolved = weighted["entered__unresolved"]
    entered_sampled = entered_resolved + entered_unresolved

    return {
        "schema": "rec-world-partition-v1",
        "ledger_path": str(ledger_path),
        "truth_path": str(truth_path),
        "exposure_count": len(ledger),
        "raw_partition_counts": dict(raw),
        "design_weighted_audited_partition": dict(weighted),
        "design_weighted_resolved_truth": dict(weighted_truth),
        "shadow_reference_resolved_event_rate": _ratio(shadow_positive, shadow_resolved),
        "shadow_reference_unresolved_fraction": _ratio(shadow_unresolved, shadow_sampled),
        "entered_reference_unresolved_fraction": _ratio(entered_unresolved, entered_sampled),
        "interpretation": {
            "reference_resolved_shadow": (
                "Primary record absent, but independently sampled reference truth resolves the event. "
                "This is the empirically recoverable REC shadow."
            ),
            "reference_unresolved_shadow": (
                "Primary record absent and sampled reference truth remains unresolved. "
                "This is REC dark mass and must remain uncertainty or be bounded."
            ),
            "not_sampled_or_not_audited": (
                "Exposure belongs to Omega but has no sampled reference truth. It is not negative truth."
            ),
            "outside_omega": (
                "Not represented in this output. Exposures not defined in the master ledger are outside the empirical study universe."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger_csv", type=Path)
    parser.add_argument("truth_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        result = analyze(args.ledger_csv, args.truth_csv)
    except PartitionError as exc:
        raise SystemExit(f"REC world-partition analysis failed: {exc}") from exc

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
