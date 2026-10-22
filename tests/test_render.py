"""Generated documentation must follow the registry and stay current."""

import datetime
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import yaml

from hogledger import render

ROOT = Path(__file__).resolve().parent.parent
MARKERS = f"intro\n{render.BEGIN}\nold table\n{render.END}\noutro\n"


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        (self.root / "graphs").mkdir()
        (self.root / "graphs" / "witness.g6").write_text("FbSko\n")
        (self.root / "README.md").write_text(MARKERS)
        self.ledger_fields = {}
        self.record = {
            "id": "sat-c6-n7", "invariant": "sat(7,C6)=10", "n": 7, "edges": 10,
            "graph6": "FbSko", "graph_file": "graphs/witness.g6",
            "verification": {"family": "cycle_saturation", "order": 6},
            "hog_id": 868, "status": "deposited", "certificates": "both",
            "non_iso_minima": None, "zenodo": "10.5281/zenodo.21350167",
            "notes": "Extends L???C@_ECKI`i` by one vertex.",
            "claim": {"kind": "known_value", "statement": "sat(7,C6) = 10.", "prior_art": [{
                "source": "doi:10.1007/s00373-014-1422-4", "locator": "Remark 1",
                "checked": datetime.date(2026, 10, 17), "finding": "Records the value."}]},
        }

    def write_registry(self, records=None):
        data = {
            "author": {"given_names": "Alexander Richard", "family_names": "Towell",
                       "handle": "queelius", "email": "lex@metafunctor.com",
                       "orcid": "0000-0001-6443-9897"},
            "ledger": {"title": "House of Graphs witness ledger",
                       "repository": "https://github.com/queelius/hog-contrib",
                       "abstract": "Witness graphs.", "keywords": ["House of Graphs"],
                       "version": "1.0.0", "license": {"data": "CC-BY-4.0", "code": "MIT"},
                       **self.ledger_fields},
            "house_of_graphs": "https://houseofgraphs.org",
            "papers": {"saturation": {"title": "C6 saturation", "zenodo": "10.5281/zenodo.23527267"}},
            "graphs": records or [self.record],
        }
        (self.root / "contributions.yaml").write_text(yaml.safe_dump(data))

    def outputs(self):
        self.write_registry()
        return render.outputs(self.root)

    def page(self):
        return self.outputs()[Path("docs/graphs/sat-c6-n7.md")]

    def test_page_states_the_claim_and_its_prior_art(self):
        page = self.page()
        self.assertIn("sat(7,C6) = 10.", page)
        self.assertIn("known value", page)
        self.assertIn("https://doi.org/10.1007/s00373-014-1422-4", page)
        self.assertIn("Remark 1", page)
        self.assertIn("2026-10-17", page)
        self.assertIn("Records the value.", page)

    def test_page_links_the_live_graph_and_evidence(self):
        page = self.page()
        self.assertIn("https://houseofgraphs.org/graphs/868", page)
        self.assertIn("https://doi.org/10.5281/zenodo.21350167", page)

    def test_page_hash_is_derived_from_the_witness_file(self):
        digest = hashlib.sha256((self.root / "graphs" / "witness.g6").read_bytes()).hexdigest()
        self.assertIn(digest, self.page())

    def test_page_gives_a_single_record_verify_command(self):
        self.assertIn("python3 -m hogledger verify sat-c6-n7", self.page())

    def test_notes_are_escaped_so_backticks_stay_literal(self):
        self.assertIn(r"L???C@\_ECKI\`i\`", self.page())

    def test_fence_is_longer_than_any_backtick_run(self):
        self.assertEqual(render.fence("FbSko"), "```")
        self.assertEqual(render.fence("a```b"), "````")

    def test_readme_table_replaces_only_the_marked_block(self):
        readme = self.outputs()[Path("README.md")]
        self.assertTrue(readme.startswith("intro\n") and readme.endswith("outro\n"))
        self.assertNotIn("old table", readme)
        self.assertIn("[sat-c6-n7](docs/graphs/sat-c6-n7.md)", readme)
        self.assertIn("1 records: 1 deposited", readme)

    def test_readme_without_markers_is_rejected(self):
        (self.root / "README.md").write_text("no markers\n")
        with self.assertRaisesRegex(ValueError, "marker"):
            self.outputs()

    def test_citation_names_the_author_and_backing_papers(self):
        citation = yaml.safe_load(self.outputs()[Path("CITATION.cff")])
        self.assertEqual(citation["type"], "dataset")
        (author,) = citation["authors"]
        self.assertEqual((author["given-names"], author["family-names"]), ("Alexander Richard", "Towell"))
        self.assertEqual(author["orcid"], "https://orcid.org/0000-0001-6443-9897")
        self.assertEqual([r["doi"] for r in citation["references"]], ["10.5281/zenodo.23527267"])

    def test_citation_states_version_and_licenses(self):
        citation = yaml.safe_load(self.outputs()[Path("CITATION.cff")])
        self.assertEqual(citation["version"], "1.0.0")
        self.assertEqual(citation["license"], ["CC-BY-4.0", "MIT"])
        self.assertNotIn("doi", citation)

    def test_ledger_doi_reaches_the_citation_and_every_page(self):
        self.ledger_fields = {"doi": "10.5281/zenodo.1"}
        self.assertEqual(yaml.safe_load(self.outputs()[Path("CITATION.cff")])["doi"], "10.5281/zenodo.1")
        self.assertIn("doi:10.5281/zenodo.1", self.page())

    def test_zenodo_metadata_describes_the_dataset(self):
        metadata = json.loads(self.outputs()[Path(".zenodo.json")])
        self.assertEqual(metadata["upload_type"], "dataset")
        self.assertEqual(metadata["version"], "1.0.0")
        self.assertEqual(metadata["license"], "cc-by-4.0")
        self.assertEqual(metadata["creators"], [{"name": "Towell, Alexander Richard",
                                                 "orcid": "0000-0001-6443-9897"}])
        self.assertEqual(metadata["related_identifiers"], [
            {"identifier": "https://github.com/queelius/hog-contrib/tree/v1.0.0",
             "relation": "isSupplementTo", "scheme": "url"},
            {"identifier": "10.5281/zenodo.23527267", "relation": "references",
             "scheme": "doi", "resource_type": "publication"}])

    def test_page_lists_the_receipts_for_its_record(self):
        (self.root / "receipts").mkdir()
        (self.root / "receipts" / "2026-10-17-annotate.json").write_text(json.dumps({
            "schema_version": 2, "date": "2026-10-17", "action": "annotate",
            "records": ["sat-c6-n7"], "summary": "Annotated the live graph."}))
        page = self.page()
        self.assertIn("[2026-10-17-annotate](../../receipts/2026-10-17-annotate.json)", page)
        self.assertIn("Annotated the live graph.", page)

    def test_stale_reports_changed_missing_and_orphaned_files(self):
        self.write_registry()
        render.write(self.root)
        self.assertEqual(render.stale(self.root), [])
        (self.root / "CITATION.cff").write_text("edited\n")
        (self.root / "docs" / "graphs" / "sat-c6-n7.md").unlink()
        (self.root / "docs" / "graphs" / "removed-record.md").write_text("orphan\n")
        self.assertEqual(sorted(map(str, render.stale(self.root))),
                         ["CITATION.cff", "docs/graphs/removed-record.md", "docs/graphs/sat-c6-n7.md"])

    def test_write_removes_orphaned_pages(self):
        self.write_registry()
        (self.root / "docs" / "graphs").mkdir(parents=True)
        (self.root / "docs" / "graphs" / "removed-record.md").write_text("orphan\n")
        render.write(self.root)
        self.assertFalse((self.root / "docs" / "graphs" / "removed-record.md").exists())


class RepositoryDocsTests(unittest.TestCase):
    def test_generated_files_are_current(self):
        self.assertEqual(render.stale(ROOT), [], "run: python3 -m hogledger render")


if __name__ == "__main__":
    unittest.main()
