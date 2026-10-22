"""Load contributions.yaml into typed records and ledger metadata, fail-closed."""

import datetime
from pathlib import Path
import re

import yaml

from . import receipts
from .model import Author, Case, Claim, ClaimKind, Family, Ledger, Paper, PriorArt, Record, Status

REGISTRY = "contributions.yaml"
RECORD_ID = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"invalid {name}: {value!r}")
    return value


def _pair(value, name):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{name} must contain two positive integers")
    return tuple(_integer(x, name, 1) for x in value)


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")
    return value


def _prior_art(entry):
    if not isinstance(entry, dict):
        raise ValueError("each prior art entry must be a mapping")
    checked = entry.get("checked")
    if type(checked) is not datetime.date:
        raise ValueError(f"prior art checked must be a date, not {checked!r}")
    locator = entry.get("locator")
    return PriorArt(_text(entry.get("source"), "prior art source"), checked,
                    _text(entry.get("finding"), "prior art finding"),
                    None if locator is None else _text(locator, "prior art locator"))


def _claim(specification):
    """Parse a claim; every assessed kind must cite dated, checked prior art."""
    if not isinstance(specification, dict):
        raise ValueError("missing structured claim")
    kind = ClaimKind(specification.get("kind"))
    entries = specification.get("prior_art") or []
    if not isinstance(entries, list):
        raise ValueError("prior_art must be a list")
    prior_art = tuple(map(_prior_art, entries))
    if kind is not ClaimKind.UNASSESSED and not prior_art:
        raise ValueError(f"a {kind.value} claim requires prior art")
    return Claim(kind, _text(specification.get("statement"), "claim statement"), prior_art)


def _optional(value, parse, *args):
    return None if value is None else parse(value, *args)


def _read(root):
    data = yaml.safe_load((Path(root) / REGISTRY).read_text())
    if not isinstance(data, dict) or not isinstance(data.get("graphs"), list):
        raise ValueError("registry must contain a graphs list")
    return data


def load_records(root: Path) -> list[Record]:
    """Load typed records and reject omitted files or inconsistent metadata."""
    return _records(_read(root), Path(root).resolve())


def load_cases(root: Path) -> list[Case]:
    return [record.case for record in load_records(root)]


def load_ledger(root: Path) -> Ledger:
    """Load the records with the ledger metadata and receipts used for documentation."""
    root = Path(root).resolve()
    data = _read(root)
    author, ledger = data["author"], data["ledger"]
    keywords = ledger.get("keywords", [])
    if not isinstance(keywords, list):
        raise ValueError("ledger keywords must be a list")
    licenses = ledger["license"]
    records = tuple(_records(data, root))
    return Ledger(
        _text(ledger["title"], "ledger title"), _text(ledger["repository"], "ledger repository"),
        _text(ledger["abstract"], "ledger abstract"), tuple(_text(k, "keyword") for k in keywords),
        _text(ledger["version"], "ledger version"),
        _text(licenses["data"], "data license"), _text(licenses["code"], "code license"),
        Author(*(_text(author[field], f"author {field}")
                 for field in ("given_names", "family_names", "handle", "email", "orcid"))),
        _text(data["house_of_graphs"], "house_of_graphs"),
        tuple(Paper(key, _text(paper["title"], "paper title"), _text(paper["zenodo"], "paper zenodo"))
              for key, paper in data.get("papers", {}).items()),
        records,
        receipts.load(root, records),
        _optional(ledger.get("doi"), _text, "ledger doi"),
    )


def _records(data, root):
    records = []
    paths = set()
    ids = set()
    for record in data["graphs"]:
        if not isinstance(record, dict):
            raise ValueError("each graph record must be a mapping")
        path = Path(record["graph_file"])
        if path.is_absolute() or not (root / path).resolve().is_relative_to(root / "graphs"):
            raise ValueError("graph_file must remain within graphs/")
        if path in paths:
            raise ValueError(f"duplicate graph_file: {path}")
        paths.add(path)
        record_id = record.get("id")
        if not isinstance(record_id, str) or not RECORD_ID.fullmatch(record_id):
            raise ValueError(f"record id must be a lowercase slug: {record_id!r}")
        if record_id in ids:
            raise ValueError(f"duplicate id: {record_id}")
        ids.add(record_id)
        claim = _claim(record.get("claim"))
        status = Status(record.get("status"))
        if status is Status.DEPOSITED:
            _integer(record.get("hog_id"), "confirmed HoG ID", 1)
        n = _integer(record["n"], "vertex count")
        edges = _integer(record["edges"], "edge count")
        if edges > n * (n - 1) // 2:
            raise ValueError("edge count exceeds a simple graph's capacity")
        graph6 = record["graph6"]
        if not isinstance(graph6, str) or not graph6:
            raise ValueError("graph6 must be a nonempty string")
        specification = record.get("verification")
        if not isinstance(specification, dict):
            raise ValueError(f"missing structured verification for {path}")
        family = Family(specification["family"])
        order = parts = forbidden = None
        if family in (Family.CYCLE, Family.PATH, Family.CLIQUE):
            order = _integer(specification["order"], "forbidden graph order", 2)
            if family is Family.CLIQUE and order != 4:
                raise ValueError("only K4 clique saturation is supported")
            if family is Family.CYCLE and order < 3:
                raise ValueError("a cycle must have at least three vertices")
        else:
            parts = _pair(record["parts"], "parts")
            forbidden = _pair(specification["forbidden_parts"], "forbidden_parts")
            if sum(parts) != n:
                raise ValueError("part sizes do not sum to the graph order")
        abstract_free = record.get("k34_free")
        if abstract_free is not None and type(abstract_free) is not bool:
            raise ValueError("abstract freeness flag must be boolean")
        case = Case(path, graph6, n, edges, family, order, parts, forbidden, abstract_free,
                    record_id, claim)
        records.append(Record(
            case, _text(record.get("invariant"), "invariant"), status,
            _text(record.get("certificates"), "certificates"),
            _optional(record.get("hog_id"), _integer, "HoG ID", 1),
            _optional(record.get("zenodo"), _text, "zenodo"),
            _optional(record.get("non_iso_minima"), _integer, "non_iso_minima", 1),
            _optional(record.get("notes"), _text, "notes") or "",
        ))
    files = {path.relative_to(root) for path in (root / "graphs").rglob("*.g6")}
    if files - paths:
        raise ValueError(f"unregistered graph files: {sorted(map(str, files - paths))}")
    if paths - files:
        raise ValueError(f"missing graph files: {sorted(map(str, paths - files))}")
    return records
