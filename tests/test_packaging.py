"""Package metadata must agree with the ledger it ships with."""

from pathlib import Path
import tomllib
import unittest

from hogledger import registry

ROOT = Path(__file__).resolve().parent.parent


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
        self.ledger = registry.load_ledger(ROOT)

    def test_code_license_matches_the_ledger(self):
        self.assertEqual(self.project["license"], self.ledger.code_license)

    def test_version_matches_the_ledger(self):
        self.assertEqual(self.project["version"], self.ledger.version)

    def test_license_files_exist(self):
        for name in ("LICENSE", "LICENSE-DATA"):
            self.assertTrue((ROOT / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
