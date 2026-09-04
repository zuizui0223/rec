from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "findlay_h5_double", ROOT / "scripts" / "analyze_findlay_h5_double_holdout.py"
)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def _row(position: str, camera: str, condition: str, trigger: str) -> dict[str, str]:
    return {
        "CT.POS": position,
        "CAMERA.ID": camera,
        "wet.dry": condition,
        "TRIGGER": trigger,
    }


def _synthetic_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    cameras = ["A", "BS", "BV"]
    positions = ["P1", "P2", "P3"]
    # Dry passes trigger more often than wet passes in every camera/position.
    for position in positions:
        for camera in cameras:
            rows += [_row(position, camera, "dry", "1") for _ in range(8)]
            rows += [_row(position, camera, "dry", "0") for _ in range(2)]
            rows += [_row(position, camera, "wet", "1") for _ in range(4)]
            rows += [_row(position, camera, "wet", "0") for _ in range(6)]
    return rows


def test_double_holdout_excludes_camera_and_position() -> None:
    rows = _synthetic_rows()
    cell = MOD._evaluate_cell(rows, "A", "P1")
    assert cell is not None
    assert cell["heldout_camera"] == "A"
    assert cell["heldout_position"] == "P1"
    # Training has 2 cameras x 2 positions x 20 rows.
    assert cell["training_rows"] == 80
    assert cell["test_rows"] == 20


def test_correct_direction_beats_raw_and_swapped_sham() -> None:
    rows = _synthetic_rows()
    result = MOD.analyze(rows)
    assert result["aggregate"]["mean_absolute_error_correct"] < result["aggregate"]["mean_absolute_error_raw"]
    assert result["aggregate"]["mean_absolute_error_correct"] < result["aggregate"]["mean_absolute_error_sham"]
    assert result["promotion_rule"]["aggregate_correct_lt_raw"] is True
    assert result["promotion_rule"]["aggregate_correct_lt_sham"] is True


def test_uniform_weighting_identity_is_enforced() -> None:
    assert MOD._weighted_wet(4, 8, 1.0, 1.0) == 4 / 12


def test_unresolved_training_is_bounded_not_failed() -> None:
    rows = _synthetic_rows()
    # Add unresolved dry trigger outside the held-out camera and position.
    rows.append(_row("P2", "BS", "dry", "NA"))
    cell = MOD._evaluate_cell(rows, "A", "P1")
    assert cell is not None
    bounds = cell["correct_ipw_unresolved_training_bounds"]
    assert bounds["lower"] is not None
    assert bounds["upper"] is not None
    assert bounds["lower"] <= cell["correct_ipw_wet_proportion"] <= bounds["upper"]
