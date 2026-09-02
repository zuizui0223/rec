import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "rec_shadow_identifiability",
    ROOT / "scripts" / "demonstrate_eventlog_nonidentifiability.py",
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class ShadowIdentifiabilityTests(unittest.TestCase):
    def test_same_event_log_allows_different_shadow_prevalence(self):
        result = mod.witness()
        self.assertTrue(result["same_observed_event_log"])
        q = [world["q_shadow"] for world in result["worlds"]]
        self.assertEqual(q, [0.0, 0.5, 1.0])

    def test_event_log_is_identical_across_completions(self):
        worlds = [mod.build_world(q) for q in (0.0, 0.2, 0.8, 1.0)]
        first = worlds[0]["observed_event_log"]
        for world in worlds[1:]:
            self.assertEqual(world["observed_event_log"], first)

    def test_invalid_shadow_prevalence_fails(self):
        with self.assertRaises(ValueError):
            mod.build_world(-0.1)
        with self.assertRaises(ValueError):
            mod.build_world(1.1)


if __name__ == "__main__":
    unittest.main()
