"""Regression checks for registry-driven witness verification."""

import json
from pathlib import Path
import tempfile
import unittest

import verify_witnesses as verifier


class RegistryVerificationTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        (self.root / "graphs").mkdir()
        (self.root / "graphs" / "witness.g6").write_text("FbSko\n")
        self.record = {
            "graph_file": "graphs/witness.g6", "graph6": "FbSko", "n": 7,
            "edges": 10, "status": "ready", "hog_id": None,
            "verification": {"family": "cycle_saturation", "order": 6},
        }

    def write_registry(self, records=None):
        path = self.root / "contributions.yaml"
        path.write_text(json.dumps({"graphs": records or [self.record]}))
        return path

    def test_registry_witness_is_actually_verified(self):
        load = getattr(verifier, "load_cases", None)
        self.assertTrue(callable(load), "registry loader is missing")
        cases = load(self.write_registry())
        self.assertEqual(len(cases), 1)
        self.assertTrue(verifier.verify_case(cases[0], self.root).ok)

    def test_registry_graph6_mismatch_fails(self):
        self.record["graph6"] = "F????"
        load = getattr(verifier, "load_cases", None)
        self.assertTrue(callable(load), "registry loader is missing")
        case = load(self.write_registry())[0]
        self.assertFalse(verifier.verify_case(case, self.root).ok)

    def test_noncanonical_graph6_length_fails_even_when_mirrored(self):
        self.record["graph6"] = "FbSko?"
        (self.root / "graphs" / "witness.g6").write_text("FbSko?\n")
        case = verifier.load_cases(self.write_registry())[0]
        self.assertFalse(verifier.verify_case(case, self.root).ok)

    def test_unregistered_file_cannot_escape_verification(self):
        (self.root / "graphs" / "omitted.g6").write_text("FbSko\n")
        load = getattr(verifier, "load_cases", None)
        self.assertTrue(callable(load), "registry loader is missing")
        with self.assertRaisesRegex(ValueError, "unregistered"):
            load(self.write_registry())

    def test_duplicate_registry_path_is_rejected(self):
        load = getattr(verifier, "load_cases", None)
        self.assertTrue(callable(load), "registry loader is missing")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            load(self.write_registry([self.record, self.record]))

    def test_deposited_requires_confirmed_id(self):
        self.record["status"] = "deposited"
        load = getattr(verifier, "load_cases", None)
        self.assertTrue(callable(load), "registry loader is missing")
        with self.assertRaisesRegex(ValueError, "HoG"):
            load(self.write_registry())


if __name__ == "__main__":
    unittest.main()
