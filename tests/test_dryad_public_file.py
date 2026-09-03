import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "dryad_fetch", ROOT / "scripts" / "fetch_dryad_public_file.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class DryadResolverTests(unittest.TestCase):
    def test_select_latest_version_from_embedded_payload(self):
        payload = {
            "_embedded": {
                "stash:versions": [
                    {"id": 10, "versionNumber": 1, "publicationDate": "2024-01-01"},
                    {"id": 12, "versionNumber": 2, "publicationDate": "2025-01-01"},
                ]
            }
        }
        self.assertEqual(mod.select_latest_version(payload), 12)

    def test_select_named_file_is_exact_and_case_insensitive(self):
        payload = {
            "_embedded": {
                "stash:files": [
                    {"id": 1, "path": "README.md"},
                    {"id": 2, "path": "Nighthawk_Testing.xlsx", "size": 123},
                ]
            }
        }
        row = mod.select_named_file(payload, "nighthawk_testing.xlsx")
        self.assertEqual(row["id"], 2)

    def test_duplicate_name_fails_closed(self):
        payload = {
            "_embedded": {
                "stash:files": [
                    {"id": 1, "path": "Nighthawk_Testing.xlsx"},
                    {"id": 2, "path": "Nighthawk_Testing.xlsx"},
                ]
            }
        }
        with self.assertRaises(mod.DryadFetchError):
            mod.select_named_file(payload, "Nighthawk_Testing.xlsx")


if __name__ == "__main__":
    unittest.main()
