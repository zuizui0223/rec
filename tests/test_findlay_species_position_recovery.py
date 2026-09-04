from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "findlay_species_recovery",
    ROOT / "scripts" / "analyze_findlay_species_position_recovery.py",
)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def row(position: str, species: str, trigger: str, capture: str) -> dict[str, str]:
    return {
        "CT.POS": position,
        "SPECIES": species,
        "TRIGGER": trigger,
        "CAPTURE": capture,
    }


class SpeciesRecoveryTests(unittest.TestCase):
    def synthetic(self) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        for pos in ["P1", "P2", "P3", "P4"]:
            # Equal truth composition; fox has higher entry probability.
            rows += [row(pos, "BADGER", "1", "1") for _ in range(4)]
            rows += [row(pos, "BADGER", "0", "NA") for _ in range(6)]
            rows += [row(pos, "FOX", "1", "1") for _ in range(8)]
            rows += [row(pos, "FOX", "0", "NA") for _ in range(2)]
        return rows

    def test_trigger_correction_moves_to_truth(self) -> None:
        result = MOD.analyze(self.synthetic())
        agg = result["stages"]["trigger"]["aggregate"]
        self.assertLess(agg["mean_absolute_error_correct"], agg["mean_absolute_error_raw"])
        self.assertLess(agg["mean_absolute_error_correct"], agg["mean_absolute_error_sham"])

    def test_capture_correction_moves_to_truth(self) -> None:
        result = MOD.analyze(self.synthetic())
        agg = result["stages"]["capture"]["aggregate"]
        self.assertLess(agg["mean_absolute_error_correct"], agg["mean_absolute_error_raw"])
        self.assertLess(agg["mean_absolute_error_correct"], agg["mean_absolute_error_sham"])

    def test_nontrigger_defines_final_nonentry_not_capture_unresolved(self) -> None:
        r, k = MOD._states(row("P1", "FOX", "0", "NA"))
        self.assertFalse(r)
        self.assertFalse(k)


if __name__ == "__main__":
    unittest.main()
