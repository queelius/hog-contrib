"""Regression checks for registry-driven witness verification."""

import datetime
from pathlib import Path
import tempfile
import unittest

import yaml

from cases import ClaimKind
import verify_witnesses as verifier

CHECKED = datetime.date(2026, 10, 17)


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
            "invariant": "sat(7,C6)=10", "certificates": "both",
            "verification": {"family": "cycle_saturation", "order": 6},
            "id": "sat-c6-n7",
            "claim": {"kind": "unassessed", "statement": "A 10-edge C6-saturated graph on 7 vertices."},
        }

    def write_registry(self, records=None):
        path = self.root / "contributions.yaml"
        path.write_text(yaml.safe_dump({"graphs": records or [self.record]}))
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


    def prior_art(self, **fields):
        entry = {"source": "doi:10.1007/s00373-014-1422-4", "checked": CHECKED,
                 "finding": "Remark 1 records the value."}
        entry.update(fields)
        return entry

    def claim(self, kind, prior_art=()):
        self.record["claim"] = {"kind": kind, "statement": "A claim.", "prior_art": list(prior_art)}

    def test_record_without_id_is_rejected(self):
        del self.record["id"]
        with self.assertRaisesRegex(ValueError, "id"):
            verifier.load_cases(self.write_registry())

    def test_id_must_be_a_lowercase_slug(self):
        self.record["id"] = "Sat C6 n7"
        with self.assertRaisesRegex(ValueError, "id"):
            verifier.load_cases(self.write_registry())

    def test_duplicate_id_is_rejected(self):
        (self.root / "graphs" / "other.g6").write_text("FbSko\n")
        other = dict(self.record, graph_file="graphs/other.g6")
        with self.assertRaisesRegex(ValueError, "duplicate id"):
            verifier.load_cases(self.write_registry([self.record, other]))

    def test_record_without_claim_is_rejected(self):
        del self.record["claim"]
        with self.assertRaisesRegex(ValueError, "claim"):
            verifier.load_cases(self.write_registry())

    def test_unknown_claim_kind_is_rejected(self):
        self.claim("probably_new")
        with self.assertRaises(ValueError):
            verifier.load_cases(self.write_registry())

    def test_claim_needs_a_statement(self):
        self.record["claim"]["statement"] = ""
        with self.assertRaisesRegex(ValueError, "statement"):
            verifier.load_cases(self.write_registry())

    def test_every_assessed_kind_requires_prior_art(self):
        for kind in ClaimKind:
            if kind is ClaimKind.UNASSESSED:
                continue
            with self.subTest(kind=kind):
                self.claim(kind.value)
                with self.assertRaisesRegex(ValueError, "prior art"):
                    verifier.load_cases(self.write_registry())

    def test_prior_art_needs_a_checked_date(self):
        for checked in (None, "2026-10-17", "recently"):
            with self.subTest(checked=checked):
                self.claim("known_value", [self.prior_art(checked=checked)])
                with self.assertRaisesRegex(ValueError, "checked"):
                    verifier.load_cases(self.write_registry())

    def test_prior_art_needs_source_and_finding(self):
        for field in ("source", "finding"):
            with self.subTest(field=field):
                self.claim("known_value", [self.prior_art(**{field: ""})])
                with self.assertRaisesRegex(ValueError, field):
                    verifier.load_cases(self.write_registry())

    def test_unassessed_needs_no_prior_art(self):
        case = verifier.load_cases(self.write_registry())[0]
        self.assertIs(case.claim.kind, ClaimKind.UNASSESSED)
        self.assertEqual(case.claim.prior_art, ())

    def test_assessed_claim_is_loaded_with_its_prior_art(self):
        self.claim("new_value", [self.prior_art(locator="Remark 1, p. 1089")])
        case = verifier.load_cases(self.write_registry())[0]
        self.assertEqual(case.id, "sat-c6-n7")
        self.assertIs(case.claim.kind, ClaimKind.NEW_VALUE)
        (entry,) = case.claim.prior_art
        self.assertEqual((entry.checked, entry.locator), (CHECKED, "Remark 1, p. 1089"))


if __name__ == "__main__":
    unittest.main()
