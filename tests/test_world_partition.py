import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "world_partition", ROOT / "scripts" / "analyze_world_partition.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class WorldPartitionTests(unittest.TestCase):
    def test_example_partition_distinguishes_record_and_reference_state(self):
        result = mod.analyze(
            ROOT / "examples" / "exposure_ledger.csv",
            ROOT / "examples" / "chapter2_windows.csv",
        )
        raw = result["raw_partition_counts"]
        self.assertEqual(raw["shadow__resolved"], 3)
        self.assertEqual(raw["shadow__not_sampled"], 1)
        self.assertEqual(raw["entered__resolved"], 1)
        self.assertAlmostEqual(result["shadow_reference_resolved_event_rate"], 0.75)
        self.assertAlmostEqual(result["shadow_reference_unresolved_fraction"], 0.0)

    def test_sampled_unresolved_shadow_is_dark_mass_not_negative(self):
        source = ROOT / "examples" / "chapter2_windows.csv"
        with source.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
            fields = list(rows[0].keys())

        for row in rows:
            if row["window_id"] == "w4":
                row["target_truth"] = "unresolved"
                break

        tmp = tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))

        result = mod.analyze(ROOT / "examples" / "exposure_ledger.csv", path)
        raw = result["raw_partition_counts"]
        self.assertEqual(raw["shadow__resolved"], 2)
        self.assertEqual(raw["shadow__unresolved"], 1)
        self.assertAlmostEqual(result["shadow_reference_unresolved_fraction"], 0.25)
        # The unresolved row is not added to resolved negatives, so the resolved-only
        # event rate among shadow truth becomes 1.0 rather than 0.75.
        self.assertAlmostEqual(result["shadow_reference_resolved_event_rate"], 1.0)

    def test_missing_truth_row_is_not_audited_not_negative(self):
        source = ROOT / "examples" / "chapter2_windows.csv"
        with source.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
            fields = list(rows[0].keys())
        rows = [row for row in rows if row["window_id"] != "w2"]

        tmp = tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        path = Path(tmp.name)
        self.addCleanup(lambda: path.unlink(missing_ok=True))

        result = mod.analyze(ROOT / "examples" / "exposure_ledger.csv", path)
        self.assertEqual(result["raw_partition_counts"]["shadow__not_audited"], 1)


if __name__ == "__main__":
    unittest.main()
