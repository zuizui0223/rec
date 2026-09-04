#!/usr/bin/env python3
"""Build a paper-readable horizontal recovery transport ladder."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output-dir", type=Path, default=Path("paper_figures"))
    args = parser.parse_args()

    t = _load(args.results_dir / "findlay_h5_transport_boundary_v1.json")
    s = _load(args.results_dir / "findlay_species_position_recovery_summary_v1.json")

    labels = [
        "Otter: matched camera context",
        "Otter: position shift within camera*",
        "Otter: camera + position shift",
        "Fox/badger: trigger position shift",
        "Fox/badger: capture position shift",
    ]
    raw = [
        t["matched_context_camera_holdout"]["mean_absolute_error_raw"],
        t["position_holdout_within_camera"]["mean_absolute_error_raw"],
        t["double_holdout_camera_and_position"]["mean_absolute_error_raw"],
        s["trigger"]["mean_absolute_error_raw"],
        s["capture"]["mean_absolute_error_raw"],
    ]
    correct = [
        t["matched_context_camera_holdout"]["mean_absolute_error_correct"],
        t["position_holdout_within_camera"]["mean_absolute_error_correct"],
        t["double_holdout_camera_and_position"]["mean_absolute_error_correct"],
        s["trigger"]["mean_absolute_error_correct"],
        s["capture"]["mean_absolute_error_correct"],
    ]

    y = list(range(len(labels)))
    height = 0.34
    fig, ax = plt.subplots(figsize=(8.8, 5.5))
    ax.barh([v + height / 2 for v in y], raw, height=height, label="Raw record")
    ax.barh([v - height / 2 for v in y], correct, height=height, label="Entry-aware correction")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Mean absolute composition error")
    ax.set_title("Correction helps within some calibration domains but not all", fontsize=11)
    ax.legend(loc="lower right")

    for i, (r, c) in enumerate(zip(raw, correct)):
        change = (c - r) / r * 100 if r > 0 else 0.0
        ax.text(max(r, c) + 0.004, i, f"{change:+.1f}%", va="center", fontsize=8)

    fig.subplots_adjust(left=0.35, bottom=0.16, right=0.95, top=0.90)
    fig.text(
        0.35,
        0.055,
        "*Exploratory diagnostic run after the frozen camera+position transport test; all other rows are pre-existing frozen/retrospective evaluations.",
        ha="left",
        fontsize=7.5,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_dir / "fig4_recovery_transport_ladder.png", dpi=240, bbox_inches="tight")
    plt.close(fig)
    print("polished Fig. 4 transport ladder")


if __name__ == "__main__":
    main()
