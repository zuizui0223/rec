#!/usr/bin/env python3
"""Construct shadow-world completions with identical entered event logs."""
from __future__ import annotations

import argparse
import json


def build_world(q_shadow: float, *, entered: int = 4, shadow: int = 10) -> dict:
    if not 0 <= q_shadow <= 1:
        raise ValueError("q_shadow must be in [0,1]")
    shadow_positive = round(q_shadow * shadow)
    shadow_negative = shadow - shadow_positive
    event_log = [
        {"record_entry_id": f"r{i+1}", "K": 1, "entered_state": "recorded"}
        for i in range(entered)
    ]
    shadow_truth = [1] * shadow_positive + [0] * shadow_negative
    return {
        "observed_event_log": event_log,
        "shadow_exposure_count": shadow,
        "shadow_truth": shadow_truth,
        "q_shadow": shadow_positive / shadow if shadow else None,
    }


def witness() -> dict:
    worlds = [build_world(q) for q in (0.0, 0.5, 1.0)]
    fingerprints = [json.dumps(w["observed_event_log"], sort_keys=True) for w in worlds]
    return {
        "schema": "rec-eventlog-nonidentifiability-witness-v1",
        "same_observed_event_log": len(set(fingerprints)) == 1,
        "worlds": worlds,
        "interpretation": (
            "Identical entered event logs are compatible with different event prevalence "
            "inside the non-entered exposure set. Event-log-only q_shadow is therefore "
            "not identified without an external exposure denominator plus truth/assumptions."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    print(json.dumps(witness(), indent=2 if args.pretty else None, sort_keys=True))


if __name__ == "__main__":
    main()
