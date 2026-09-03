#!/usr/bin/env python3
"""Generate an annotation-naive BirdVox continuous score stream from band-energy contrast.

This is an optional real-data runner and intentionally depends on numpy + soundfile.
It never reads BirdVox annotations. The output can therefore be used as a provenance-safe
pre-gate score source for the REC external replication.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path


DEV_SENSORS = {"01", "03", "07"}
HELDOUT_SENSORS = {"02", "05", "10"}


class BirdVoxScoreError(ValueError):
    pass


def _sensor_from_path(path: Path) -> str:
    match = re.search(r"unit(\d+)", path.name, flags=re.IGNORECASE)
    if not match:
        raise BirdVoxScoreError(
            f"cannot infer sensor from {path.name!r}; expected filename containing unitNN"
        )
    sensor = match.group(1).zfill(2)
    if sensor not in DEV_SENSORS | HELDOUT_SENSORS:
        raise BirdVoxScoreError(f"unexpected BirdVox sensor {sensor!r}")
    return sensor


def _split(sensor: str) -> str:
    return "development" if sensor in DEV_SENSORS else "heldout"


def score_audio(
    path: Path,
    *,
    window_seconds: float = 1.0,
    target_low_hz: float = 2000.0,
    target_high_hz: float = 10000.0,
    reference_low_hz: float = 200.0,
    reference_high_hz: float = 2000.0,
) -> tuple[list[dict[str, str]], dict[str, str]]:
    try:
        import numpy as np
        import soundfile as sf
    except ImportError as exc:
        raise BirdVoxScoreError(
            "score_birdvox_band_energy.py requires numpy and soundfile"
        ) from exc

    if not math.isfinite(window_seconds) or window_seconds <= 0:
        raise BirdVoxScoreError("window_seconds must be finite and >0")

    sensor = _sensor_from_path(path)
    with sf.SoundFile(path) as audio:
        sr = int(audio.samplerate)
        if audio.channels != 1:
            raise BirdVoxScoreError(
                f"{path.name}: expected mono audio, got {audio.channels} channels"
            )
        if sr <= 2 * target_high_hz:
            raise BirdVoxScoreError(
                f"{path.name}: sample rate {sr} is too low for target_high_hz={target_high_hz}"
            )
        blocksize = int(round(sr * window_seconds))
        if blocksize <= 0:
            raise BirdVoxScoreError("window_seconds produces zero-length blocks")

        raw_rows: list[tuple[float, float]] = []
        window_index = 0
        total_frames = len(audio)

        while True:
            block = audio.read(blocksize, dtype="float32", always_2d=False)
            if len(block) == 0:
                break
            x = np.asarray(block, dtype=np.float64)
            if x.ndim != 1:
                raise BirdVoxScoreError(f"{path.name}: expected mono vector")
            if len(x) < 2:
                break

            window = np.hanning(len(x))
            spectrum = np.fft.rfft(x * window)
            power = np.abs(spectrum) ** 2
            freqs = np.fft.rfftfreq(len(x), d=1.0 / sr)
            target_mask = (freqs >= target_low_hz) & (freqs < target_high_hz)
            ref_mask = (freqs >= reference_low_hz) & (freqs < reference_high_hz)
            target_power = float(power[target_mask].sum())
            reference_power = float(power[ref_mask].sum())
            eps = max(1e-18, 1e-12 * float(power.sum() + 1e-18))
            raw_db = 10.0 * math.log10((target_power + eps) / (reference_power + eps))
            midpoint = (window_index * blocksize + len(x) / 2.0) / sr
            raw_rows.append((midpoint, raw_db))
            window_index += 1

    if not raw_rows:
        raise BirdVoxScoreError(f"{path.name}: no score windows produced")

    raw = np.asarray([v for _, v in raw_rows], dtype=float)
    median = float(np.median(raw))
    mad = float(np.median(np.abs(raw - median)))
    scale = 1.4826 * mad
    if not math.isfinite(scale) or scale <= 0:
        scale = float(np.std(raw))
    if not math.isfinite(scale) or scale <= 0:
        scale = 1.0

    rows = [
        {
            "sensor_id": sensor,
            "time_seconds": f"{t:.6f}",
            "score": f"{((raw_db - median) / scale):.12g}",
            "raw_band_contrast_db": f"{raw_db:.12g}",
            "score_source": "annotation-naive-band-energy-v1",
        }
        for t, raw_db in raw_rows
    ]
    duration_seconds = total_frames / sr
    manifest = {
        "sensor_id": sensor,
        "duration_seconds": f"{duration_seconds:.9f}",
        "split": _split(sensor),
    }
    return rows, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file", nargs="+", type=Path)
    parser.add_argument("--window-seconds", type=float, default=1.0)
    parser.add_argument("--scores-output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    args = parser.parse_args()

    all_scores: list[dict[str, str]] = []
    manifests: list[dict[str, str]] = []
    seen: set[str] = set()

    try:
        for path in args.audio_file:
            rows, manifest = score_audio(path, window_seconds=args.window_seconds)
            sensor = manifest["sensor_id"]
            if sensor in seen:
                raise BirdVoxScoreError(f"duplicate audio for sensor {sensor}")
            seen.add(sensor)
            all_scores.extend(rows)
            manifests.append(manifest)
    except BirdVoxScoreError as exc:
        raise SystemExit(f"BirdVox band-energy scoring failed: {exc}") from exc

    args.scores_output.parent.mkdir(parents=True, exist_ok=True)
    with args.scores_output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "sensor_id",
                "time_seconds",
                "score",
                "raw_band_contrast_db",
                "score_source",
            ],
        )
        writer.writeheader()
        writer.writerows(all_scores)

    args.manifest_output.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest_output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["sensor_id", "duration_seconds", "split"]
        )
        writer.writeheader()
        writer.writerows(sorted(manifests, key=lambda r: r["sensor_id"]))

    print(
        f"wrote {len(all_scores)} continuous score windows across {len(manifests)} sensors"
    )


if __name__ == "__main__":
    main()
