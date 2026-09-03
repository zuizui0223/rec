#!/usr/bin/env python3
"""Build a gate-independent BirdVox REC exposure grid from frozen durations, truth and scores."""
from __future__ import annotations

import argparse
import csv
import math
import re
from collections import defaultdict
from pathlib import Path


class BirdVoxGridError(ValueError):
    pass


TIME_COLUMNS = ("time_seconds", "Time (s)", "Center Time (s)", "Time")
SCORE_TIME_COLUMNS = ("time_seconds", "Time (s)", "Center Time (s)", "Time")
SCORE_COLUMNS = ("score", "confidence", "Detection confidence (%)")


def _pick(fieldnames: list[str] | None, candidates: tuple[str, ...], label: str) -> str:
    if not fieldnames:
        raise BirdVoxGridError(f"{label} table has no header")
    for candidate in candidates:
        if candidate in fieldnames:
            return candidate
    raise BirdVoxGridError(
        f"{label} table requires one of {', '.join(candidates)}; got {', '.join(fieldnames)}"
    )


def _float(value: str, field: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise BirdVoxGridError(f"{field} must be numeric, got {value!r}") from exc
    if not math.isfinite(out):
        raise BirdVoxGridError(f"{field} must be finite, got {value!r}")
    return out


def _sensor_from_path(path: Path) -> str:
    match = re.search(r"unit(\d+)", path.name, flags=re.IGNORECASE)
    if not match:
        raise BirdVoxGridError(
            f"cannot infer sensor from {path.name!r}; expected filename containing unitNN"
        )
    return match.group(1).zfill(2)


def load_manifest(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise BirdVoxGridError("manifest has no header")
        required = {"sensor_id", "duration_seconds", "split"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise BirdVoxGridError(f"manifest missing: {', '.join(sorted(missing))}")
        out: dict[str, dict[str, str]] = {}
        for row in reader:
            sensor = row["sensor_id"].strip().zfill(2)
            if not sensor:
                raise BirdVoxGridError("blank sensor_id")
            if sensor in out:
                raise BirdVoxGridError(f"duplicate sensor_id {sensor!r}")
            duration = _float(row["duration_seconds"], "duration_seconds")
            if duration <= 0:
                raise BirdVoxGridError("duration_seconds must be >0")
            split = row["split"].strip().lower()
            if split not in {"development", "heldout"}:
                raise BirdVoxGridError(
                    f"sensor {sensor}: split must be development or heldout"
                )
            out[sensor] = {
                "sensor_id": sensor,
                "duration_seconds": str(duration),
                "split": split,
            }
    if not out:
        raise BirdVoxGridError("manifest is empty")
    return out


def load_annotations(paths: list[Path]) -> dict[str, list[float]]:
    out: dict[str, list[float]] = defaultdict(list)
    for path in paths:
        sensor = _sensor_from_path(path)
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            time_col = _pick(reader.fieldnames, TIME_COLUMNS, "annotation")
            label_col = None
            if reader.fieldnames:
                for candidate in ("label", "event_type", "Annotation"):
                    if candidate in reader.fieldnames:
                        label_col = candidate
                        break
            for row in reader:
                if label_col and row[label_col].strip().lower() in {"alarm", "beep"}:
                    continue
                t = _float(row[time_col], f"{path.name}.{time_col}")
                if t < 0:
                    raise BirdVoxGridError(f"{path.name}: negative annotation time {t}")
                out[sensor].append(t)
    return out


def load_scores(path: Path) -> dict[str, list[tuple[float, float]]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise BirdVoxGridError("score table has no header")
        required = {"sensor_id"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise BirdVoxGridError(f"score table missing: {', '.join(sorted(missing))}")
        time_col = _pick(reader.fieldnames, SCORE_TIME_COLUMNS, "score")
        score_col = _pick(reader.fieldnames, SCORE_COLUMNS, "score")
        out: dict[str, list[tuple[float, float]]] = defaultdict(list)
        for row in reader:
            sensor = row["sensor_id"].strip().zfill(2)
            t = _float(row[time_col], time_col)
            score = _float(row[score_col].rstrip("%"), score_col)
            if t < 0:
                raise BirdVoxGridError(f"sensor {sensor}: negative score time {t}")
            out[sensor].append((t, score))
    return out


def build_grid(
    manifest: dict[str, dict[str, str]],
    annotations: dict[str, list[float]],
    scores: dict[str, list[tuple[float, float]]],
    *,
    window_seconds: float,
) -> list[dict[str, str]]:
    if not math.isfinite(window_seconds) or window_seconds <= 0:
        raise BirdVoxGridError("window_seconds must be finite and >0")
    rows: list[dict[str, str]] = []
    for sensor in sorted(manifest):
        duration = float(manifest[sensor]["duration_seconds"])
        n_windows = int(math.ceil(duration / window_seconds))
        call_counts = [0] * n_windows
        score_max: list[float | None] = [None] * n_windows

        for t in annotations.get(sensor, []):
            if t >= duration:
                raise BirdVoxGridError(
                    f"sensor {sensor}: annotation time {t} is outside duration {duration}"
                )
            idx = min(int(t // window_seconds), n_windows - 1)
            call_counts[idx] += 1

        for t, score in scores.get(sensor, []):
            if t >= duration:
                raise BirdVoxGridError(
                    f"sensor {sensor}: score time {t} is outside duration {duration}"
                )
            idx = min(int(t // window_seconds), n_windows - 1)
            current = score_max[idx]
            score_max[idx] = score if current is None else max(current, score)

        for idx in range(n_windows):
            start = idx * window_seconds
            end = min((idx + 1) * window_seconds, duration)
            max_score = score_max[idx]
            rows.append(
                {
                    "sensor_id": sensor,
                    "split": manifest[sensor]["split"],
                    "window_id": f"birdvox-{sensor}-{idx:06d}",
                    "window_index": str(idx),
                    "window_start_seconds": f"{start:.6f}",
                    "window_end_seconds": f"{end:.6f}",
                    "window_seconds": f"{end-start:.6f}",
                    "truth_call_count": str(call_counts[idx]),
                    "truth_positive": "true" if call_counts[idx] > 0 else "false",
                    "gate_evaluable": "true" if max_score is not None else "false",
                    "max_score": "" if max_score is None else f"{max_score:.12g}",
                }
            )
    return rows


def write_grid(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "sensor_id",
        "split",
        "window_id",
        "window_index",
        "window_start_seconds",
        "window_end_seconds",
        "window_seconds",
        "truth_call_count",
        "truth_positive",
        "gate_evaluable",
        "max_score",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest_csv", type=Path)
    parser.add_argument("scores_csv", type=Path)
    parser.add_argument("annotation_csv", nargs="+", type=Path)
    parser.add_argument("--window-seconds", type=float, default=1.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        rows = build_grid(
            load_manifest(args.manifest_csv),
            load_annotations(args.annotation_csv),
            load_scores(args.scores_csv),
            window_seconds=args.window_seconds,
        )
    except BirdVoxGridError as exc:
        raise SystemExit(f"BirdVox REC grid build failed: {exc}") from exc
    write_grid(args.output, rows)
    print(f"wrote {len(rows)} exposure windows to {args.output}")


if __name__ == "__main__":
    main()
