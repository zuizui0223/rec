#!/usr/bin/env python3
"""Build paper-facing REC H1–H5 figures from committed result JSON.

The script intentionally reads only committed machine-readable evidence. It does
not re-estimate the underlying models or select favourable subsets.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _finish(fig, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)


def fig2a_badger_composition(camera: dict, outdir: Path) -> None:
    comp = camera["fox_badger_registration"]["composition_distortion"]["species"]
    stages = ["Reference passes", "Triggered records", "Confirmed captures"]
    values = [
        comp["truth_badger"],
        comp["confirmed_trigger_badger"],
        comp["confirmed_capture_badger"],
    ]
    fig, ax = plt.subplots()
    ax.bar(stages, values)
    ax.set_ylabel("Badger proportion")
    ax.set_ylim(0, 0.6)
    ax.set_title("Fox/badger composition across record-entry stages")
    for i, value in enumerate(values):
        ax.text(i, value, f"{value:.3f}", ha="center", va="bottom")
    _finish(fig, outdir / "fig2a_badger_composition.png")


def fig2b_position_standardized_badger(position: dict, outdir: Path) -> None:
    fb = position["fox_badger"]
    labels = [
        "Trigger\nequal positions",
        "Trigger\nreference weights",
        "Capture\nequal positions",
        "Capture\nreference weights",
    ]
    values = [
        fb["trigger"]["equal_position_weighting"]["shift_recorded_minus_truth"],
        fb["trigger"]["reference_pass_weighting"]["shift_recorded_minus_truth"],
        fb["capture"]["equal_position_weighting"]["shift_recorded_minus_truth"],
        fb["capture"]["reference_pass_weighting"]["shift_recorded_minus_truth"],
    ]
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.axhline(0, linewidth=1)
    ax.set_ylabel("Recorded − reference badger proportion")
    ax.set_title("Species distortion after CT-position standardization")
    for i, value in enumerate(values):
        ax.text(i, value, f"{value:+.3f}", ha="center", va="bottom")
    _finish(fig, outdir / "fig2b_position_standardized_badger.png")


def fig2c_otter_context(position: dict, outdir: Path) -> None:
    otter = position["otter_wet_dry_trigger"]
    cameras = ["A", "BS", "BV"]
    equal = [otter[c]["equal_position_shift"] for c in cameras]
    ref = [otter[c]["reference_pass_weighted_shift"] for c in cameras]
    x = list(range(len(cameras)))
    width = 0.36
    fig, ax = plt.subplots()
    ax.bar([v - width / 2 for v in x], equal, width=width, label="Equal position")
    ax.bar([v + width / 2 for v in x], ref, width=width, label="Reference-pass weights")
    ax.axhline(0, linewidth=1)
    ax.set_xticks(x, cameras)
    ax.set_ylabel("Recorded − reference wet proportion")
    ax.set_title("Wet/dry selection depends on camera/position context")
    ax.legend()
    _finish(fig, outdir / "fig2c_otter_position_standardization.png")


def fig4_transport_ladder(
    transport: dict, species: dict, outdir: Path
) -> None:
    t = transport
    regimes = [
        "Otter\nmatched camera",
        "Otter\nposition within camera",
        "Otter\ncamera + position",
        "Species\ntrigger position",
        "Species\ncapture position",
    ]
    raw = [
        t["matched_context_camera_holdout"]["mean_absolute_error_raw"],
        t["position_holdout_within_camera"]["mean_absolute_error_raw"],
        t["double_holdout_camera_and_position"]["mean_absolute_error_raw"],
        species["trigger"]["mean_absolute_error_raw"],
        species["capture"]["mean_absolute_error_raw"],
    ]
    correct = [
        t["matched_context_camera_holdout"]["mean_absolute_error_correct"],
        t["position_holdout_within_camera"]["mean_absolute_error_correct"],
        t["double_holdout_camera_and_position"]["mean_absolute_error_correct"],
        species["trigger"]["mean_absolute_error_correct"],
        species["capture"]["mean_absolute_error_correct"],
    ]
    x = list(range(len(regimes)))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar([v - width / 2 for v in x], raw, width=width, label="Raw record")
    ax.bar([v + width / 2 for v in x], correct, width=width, label="Entry-aware correction")
    ax.set_xticks(x, regimes)
    ax.set_ylabel("Mean absolute composition error")
    ax.set_title("Recovery is useful in some calibration domains but not all")
    ax.legend()
    _finish(fig, outdir / "fig4_recovery_transport_ladder.png")


def fig4_sham_controls(transport: dict, species: dict, outdir: Path) -> None:
    regimes = [
        "Otter\ncamera + position",
        "Species\ntrigger position",
        "Species\ncapture position",
    ]
    raw = [
        transport["double_holdout_camera_and_position"]["mean_absolute_error_raw"],
        species["trigger"]["mean_absolute_error_raw"],
        species["capture"]["mean_absolute_error_raw"],
    ]
    correct = [
        transport["double_holdout_camera_and_position"]["mean_absolute_error_correct"],
        species["trigger"]["mean_absolute_error_correct"],
        species["capture"]["mean_absolute_error_correct"],
    ]
    sham = [
        transport["double_holdout_camera_and_position"]["mean_absolute_error_sham"],
        species["trigger"]["mean_absolute_error_sham"],
        species["capture"]["mean_absolute_error_sham"],
    ]
    x = list(range(len(regimes)))
    width = 0.25
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.bar([v - width for v in x], raw, width=width, label="Raw")
    ax.bar(x, correct, width=width, label="Correct entry model")
    ax.bar([v + width for v in x], sham, width=width, label="Swapped sham")
    ax.set_xticks(x, regimes)
    ax.set_ylabel("Mean absolute composition error")
    ax.set_title("Correct selection direction does not guarantee broad transport")
    ax.legend()
    _finish(fig, outdir / "fig4b_sham_controls.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output-dir", type=Path, default=Path("paper_figures"))
    args = parser.parse_args()

    camera = _load(args.results_dir / "findlay_camera_trap_real_data_v1.json")
    position = _load(args.results_dir / "findlay_position_standardized_distortion_summary_v1.json")
    transport = _load(args.results_dir / "findlay_h5_transport_boundary_v1.json")
    species = _load(args.results_dir / "findlay_species_position_recovery_summary_v1.json")

    fig2a_badger_composition(camera, args.output_dir)
    fig2b_position_standardized_badger(position, args.output_dir)
    fig2c_otter_context(position, args.output_dir)
    fig4_transport_ladder(transport, species, args.output_dir)
    fig4_sham_controls(transport, species, args.output_dir)

    print(f"wrote paper figures to {args.output_dir}")


if __name__ == "__main__":
    main()
