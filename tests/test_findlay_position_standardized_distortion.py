from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "findlay_std",
    ROOT / "scripts" / "analyze_findlay_position_standardized_distortion.py",
)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def row(pos, group, trigger):
    return {"CT.POS": pos, "group": group, "TRIGGER": trigger}


class PositionStandardizationTests(unittest.TestCase):
    def test_common_position_weights_preserve_direction(self):
        rows = []
        for pos in ["P1", "P2"]:
            rows += [row(pos, "wet", "1") for _ in range(2)]
            rows += [row(pos, "wet", "0") for _ in range(8)]
            rows += [row(pos, "dry", "1") for _ in range(8)]
            rows += [row(pos, "dry", "0") for _ in range(2)]
        cells = {}
        for pos in ["P1", "P2"]:
            pr = [r for r in rows if r["CT.POS"] == pos]
            cells[pos] = MOD._position_composition(
                pr,
                group_fn=lambda r: r["group"],
                focal_group="wet",
                other_group="dry",
                entry_fn=lambda r: MOD._optional_binary(r["TRIGGER"], "TRIGGER"),
            )
        std = MOD._standardize(cells)
        self.assertLess(std["equal_position_weighting"]["shift_recorded_minus_truth"], 0)
        self.assertLess(std["reference_pass_weighting"]["shift_recorded_minus_truth"], 0)

    def test_nontrigger_is_final_nonentry(self):
        self.assertFalse(MOD._final_entry({"TRIGGER": "0", "CAPTURE": "NA"}))


if __name__ == "__main__":
    unittest.main()
