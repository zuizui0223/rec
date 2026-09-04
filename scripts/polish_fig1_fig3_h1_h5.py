#!/usr/bin/env python3
"""Polish the two paper panels that need layout-specific treatment.

This script overwrites Fig. 1 and Fig. 3 after the general figure builder runs.
Fig. 1 is schematic; Fig. 3 reads only committed BirdVox evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def _finish(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)


def build_fig1(outdir: Path) -> None:
    fig, ax = plt.subplots(figsize=(11.5, 4.1))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 4.15)
    ax.axis("off")

    xs = [0.25, 2.1, 3.95, 5.8, 7.65, 9.5]
    labels = [
        "External exposure /\nreference world",
        "Biological event /\npre-entry evidence",
        "Trigger / gate\nR",
        "Usable record\nentry K",
        "Semantic / AI\ndecision",
        "Ecological\nestimand",
    ]
    w, h, y = 1.4, 1.12, 1.75

    for x, label in zip(xs, labels):
        ax.add_patch(
            FancyBboxPatch(
                (x, y), w, h, boxstyle="round,pad=0.04", fill=False, linewidth=1.35
            )
        )
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9)

    for x1, x2 in zip(xs[:-1], xs[1:]):
        ax.annotate(
            "",
            xy=(x2, y + h / 2),
            xytext=(x1 + w, y + h / 2),
            arrowprops={"arrowstyle": "->", "linewidth": 1.15},
        )

    # Event-table-visible portion begins at record entry, not at the reference/gate stages.
    ax.add_patch(
        FancyBboxPatch(
            (5.64, 1.46),
            5.34,
            1.72,
            boxstyle="round,pad=0.04",
            fill=False,
            linestyle="--",
            linewidth=1.1,
        )
    )
    ax.text(8.31, 3.34, "Event-table-visible world", ha="center", fontsize=9)

    # Shadow branch terminates before usable record entry.
    ax.annotate(
        "",
        xy=(5.55, 1.55),
        xytext=(4.55, 0.88),
        arrowprops={"arrowstyle": "->", "linewidth": 1.1},
    )
    ax.text(3.7, 0.83, "true event lost before usable record", ha="center", fontsize=9)
    ax.text(
        3.7,
        0.38,
        "External reference can audit this branch; the final event table cannot.",
        ha="center",
        fontsize=9,
    )

    ax.set_title(
        "The event table begins after a selection process it cannot audit from its own rows",
        fontsize=12,
        pad=10,
    )
    _finish(fig, outdir / "fig1_auditable_record_entry_pipeline.png")


def build_fig3(results_dir: Path, outdir: Path) -> None:
    data = json.loads(
        (results_dir / "birdvox_protected_02_05_real_data_v1.json").read_text(encoding="utf-8")
    )
    records = [
        data["by_unit"]["02"]["2"],
        data["by_unit"]["05"]["2"],
        data["protected_pooled"]["2"],
    ]
    units = ["02", "05", "Pooled 02+05"]
    truth = [r["truth_late_minus_early"] for r in records]
    raw = [r["raw_recorded_late_minus_early"] for r in records]
    oracle = [r["oracle_downstream_true_entry_late_minus_early"] for r in records]

    x = list(range(3))
    width = 0.23
    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    ax.bar([v - width for v in x], truth, width=width, label="Reference truth")
    ax.bar(x, raw, width=width, label="Entered record")
    ax.bar([v + width for v in x], oracle, width=width, label="Oracle downstream")
    ax.axhline(0, linewidth=1)
    ax.set_xticks(x, units)
    ax.set_ylim(-0.027, 0.175)
    ax.set_ylabel("Late − early event-window prevalence")
    ax.set_title("Upstream omission persists after oracle-perfect downstream semantics", fontsize=11)
    ax.legend(loc="upper left")

    # Large truth values above their bars.
    for i, value in enumerate(truth):
        ax.text(i - width, value + 0.004, f"{value:+.3f}", ha="center", va="bottom", fontsize=8)

    # Small raw/oracle values are labelled in a dedicated near-zero strip to avoid overlap.
    for i, (rv, ov) in enumerate(zip(raw, oracle)):
        raw_y = -0.014 if rv < 0 else 0.009
        oracle_y = -0.022 if ov < 0 else 0.003
        ax.text(i, raw_y, f"record {rv:+.4f}", ha="center", va="center", fontsize=7.5)
        ax.text(i, oracle_y, f"oracle {ov:+.4f}", ha="center", va="center", fontsize=7.5)

    fig.subplots_adjust(bottom=0.20, top=0.88)
    fig.text(
        0.5,
        0.055,
        "Frozen z=2 gate. The annotation-naive score discriminated poorly in protected units; "
        "the panel is an irreversibility stress test, not a detector-performance benchmark.",
        ha="center",
        fontsize=8,
    )
    _finish(fig, outdir / "fig3_birdvox_irreversibility.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output-dir", type=Path, default=Path("paper_figures"))
    args = parser.parse_args()
    build_fig1(args.output_dir)
    build_fig3(args.results_dir, args.output_dir)
    print("polished Fig. 1 and Fig. 3")


if __name__ == "__main__":
    main()
