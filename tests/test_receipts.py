"""Receipts for external actions must be dated, typed and tied to records."""

import datetime
import json
from pathlib import Path
import tempfile
import unittest

import yaml

from hogledger import registry
from hogledger.model import ReceiptAction

ROOT = Path(__file__).resolve().parent.parent


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        (self.root / "graphs").mkdir()
        (self.root / "graphs" / "witness.g6").write_text("FbSko\n")
        (self.root / "receipts").mkdir()
        (self.root / "contributions.yaml").write_text(yaml.safe_dump({
            "author": {"given_names": "Alexander Richard", "family_names": "Towell",
                       "handle": "queelius", "email": "lex@metafunctor.com",
                       "orcid": "0000-0001-6443-9897"},
            "ledger": {"title": "Ledger", "repository": "https://example.org", "abstract": "A.",
                       "version": "1.0.0", "license": {"data": "CC-BY-4.0", "code": "MIT"}},
            "house_of_graphs": "https://houseofgraphs.org",
            "graphs": [{
                "id": "sat-c6-n7", "invariant": "sat(7,C6)=10", "n": 7, "edges": 10,
                "graph6": "FbSko", "graph_file": "graphs/witness.g6",
                "verification": {"family": "cycle_saturation", "order": 6},
                "hog_id": 868, "status": "deposited", "certificates": "both",
                "claim": {"kind": "unassessed", "statement": "A claim."}}],
        }))
        self.receipt = {"schema_version": 2, "date": "2026-10-17", "action": "annotate",
                        "records": ["sat-c6-n7"], "summary": "Annotated the live graph."}

    def write(self, name="2026-10-17-annotate.json", body=None):
        (self.root / "receipts" / name).write_text(json.dumps(self.receipt if body is None else body))

    def receipts(self):
        return registry.load_ledger(self.root).receipts

    def test_receipt_is_loaded_with_its_records(self):
        self.write()
        (receipt,) = self.receipts()
        self.assertEqual(receipt.path, Path("receipts/2026-10-17-annotate.json"))
        self.assertEqual(receipt.date, datetime.date(2026, 10, 17))
        self.assertIs(receipt.action, ReceiptAction.ANNOTATE)
        self.assertEqual(receipt.records, ("sat-c6-n7",))
        self.assertEqual(receipt.summary, "Annotated the live graph.")

    def test_ledger_without_receipts_directory_has_none(self):
        (self.root / "receipts").rmdir()
        self.assertEqual(self.receipts(), ())

    def test_file_name_must_start_with_a_date(self):
        self.write("annotate.json")
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            self.receipts()

    def test_body_date_must_match_file_name(self):
        self.receipt["date"] = "2026-10-18"
        self.write()
        with self.assertRaisesRegex(ValueError, "date"):
            self.receipts()

    def test_unknown_action_is_rejected(self):
        self.receipt["action"] = "tweak"
        self.write()
        with self.assertRaises(ValueError):
            self.receipts()

    def test_unknown_record_is_rejected(self):
        self.receipt["records"] = ["no-such-record"]
        self.write()
        with self.assertRaisesRegex(ValueError, "no-such-record"):
            self.receipts()

    def test_receipt_needs_a_summary(self):
        del self.receipt["summary"]
        self.write()
        with self.assertRaisesRegex(ValueError, "summary"):
            self.receipts()

    def test_unsupported_schema_version_is_rejected(self):
        self.receipt["schema_version"] = 3
        self.write()
        with self.assertRaisesRegex(ValueError, "schema"):
            self.receipts()

    def test_attachments_must_exist(self):
        self.receipt["attachments"] = ["annotation.md"]
        self.write()
        with self.assertRaisesRegex(ValueError, "annotation.md"):
            self.receipts()

    def test_unreferenced_files_are_rejected(self):
        self.write()
        (self.root / "receipts" / "stray.md").write_text("text\n")
        with self.assertRaisesRegex(ValueError, "stray.md"):
            self.receipts()

    def test_attached_file_is_accepted(self):
        self.receipt["attachments"] = ["annotation.md"]
        self.write()
        (self.root / "receipts" / "annotation.md").write_text("text\n")
        (receipt,) = self.receipts()
        self.assertEqual(receipt.attachments, (Path("receipts/annotation.md"),))

    def legacy(self, **graph):
        return {"schema_version": "1.0", "verified_date": "2026-10-18",
                "graphs": [{"hog_id": 868, **graph}]}

    def test_legacy_receipt_records_derive_from_hog_ids(self):
        self.write("2026-10-18-c6-v5-publication.json", self.legacy())
        (receipt,) = self.receipts()
        self.assertIsNone(receipt.action)
        self.assertEqual(receipt.records, ("sat-c6-n7",))
        self.assertEqual(receipt.date, datetime.date(2026, 10, 18))

    def test_legacy_receipt_with_unknown_hog_id_is_rejected(self):
        body = self.legacy()
        body["graphs"][0]["hog_id"] = 1
        self.write("2026-10-18-c6-v5-publication.json", body)
        with self.assertRaisesRegex(ValueError, "HoG"):
            self.receipts()

    def test_legacy_annotation_file_is_an_attachment(self):
        self.write("2026-10-18-c6-v5-publication.json", self.legacy(annotation_file="note.md"))
        (self.root / "receipts" / "note.md").write_text("text\n")
        (receipt,) = self.receipts()
        self.assertEqual(receipt.attachments, (Path("receipts/note.md"),))


class RepositoryReceiptTests(unittest.TestCase):
    def test_every_receipt_loads_and_names_a_record(self):
        receipts = registry.load_ledger(ROOT).receipts
        self.assertTrue(receipts)
        for receipt in receipts:
            with self.subTest(receipt=receipt.path.name):
                self.assertTrue(receipt.records)


if __name__ == "__main__":
    unittest.main()
