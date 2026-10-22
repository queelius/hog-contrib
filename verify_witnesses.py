#!/usr/bin/env python3
"""Verify every graph6 witness using the structured contributions registry."""

import datetime
import itertools
from pathlib import Path
import re
import sys

import yaml

from cases import Author, Case, Claim, ClaimKind, Family, Ledger, Paper, PriorArt, Record, Result, Status
import crosscheck
import verify as V

ROOT = Path(__file__).resolve().parent
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


def _read(registry):
    data = yaml.safe_load(Path(registry).read_text())
    if not isinstance(data, dict) or not isinstance(data.get("graphs"), list):
        raise ValueError("registry must contain a graphs list")
    return data


def load_records(registry: Path = ROOT / "contributions.yaml") -> list[Record]:
    """Load typed records and reject omitted files or inconsistent metadata."""
    registry = Path(registry)
    return _records(_read(registry), registry.parent.resolve())


def load_cases(registry: Path = ROOT / "contributions.yaml") -> list[Case]:
    return [record.case for record in load_records(registry)]


def load_ledger(registry: Path = ROOT / "contributions.yaml") -> Ledger:
    """Load the registry with the ledger metadata used for documentation."""
    registry = Path(registry)
    data = _read(registry)
    author, ledger = data["author"], data["ledger"]
    keywords = ledger.get("keywords", [])
    if not isinstance(keywords, list):
        raise ValueError("ledger keywords must be a list")
    return Ledger(
        _text(ledger["title"], "ledger title"), _text(ledger["repository"], "ledger repository"),
        _text(ledger["abstract"], "ledger abstract"), tuple(_text(k, "keyword") for k in keywords),
        Author(*(_text(author[field], f"author {field}")
                 for field in ("given_names", "family_names", "handle", "email", "orcid"))),
        _text(data["house_of_graphs"], "house_of_graphs"),
        tuple(Paper(key, _text(paper["title"], "paper title"), _text(paper["zenodo"], "paper zenodo"))
              for key, paper in data.get("papers", {}).items()),
        tuple(_records(data, registry.parent.resolve())),
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


def max_common_neighbours(adj, side, other, subset_size):
    """Maximum common neighbours of a fixed-size subset of one part."""
    return max(
        (sum(all(adj[u][v] for u in subset) for v in other)
         for subset in itertools.combinations(side, subset_size)),
        default=0,
    )


def primary_check(case: Case, graph6: str) -> Result:
    """Check counts, round trip, and the defining property with verify.py."""
    try:
        n, adj = V.decode_graph6(graph6)
        m = V.num_edges(n, adj)
        if (n, m) != (case.n, case.edges) or V.encode_graph6(n, adj) != graph6 or not V.roundtrip_ok(n, adj):
            return Result(False, f"count or roundtrip mismatch: n={n} m={m}")
        if case.family is Family.CYCLE:
            ok = V.is_ck_free(n, adj, case.order) and V.is_ck_saturated(n, adj, case.order)
            detail = f"C{case.order}-saturated={ok}"
        elif case.family is Family.PATH:
            ok = V.is_pk_free(n, adj, case.order) and V.is_pk_saturated(n, adj, case.order)
            detail = f"P{case.order}-saturated={ok}"
        elif case.family is Family.CLIQUE:
            ok = V.is_k4_free(n, adj) and V.is_k4_saturated(n, adj)
            detail = f"K4-saturated={ok}"
        else:
            partition = V.is_bipartite(n, adj)
            if partition is None:
                return Result(False, "graph is not bipartite")
            a, b = partition
            s, t = case.forbidden_parts
            ab = max_common_neighbours(adj, a, b, s)
            ba = max_common_neighbours(adj, b, a, s)
            orientations = [(a, b, ab), (b, a, ba)]
            clean = any((len(rows), len(cols)) == case.parts and common < t
                        for rows, cols, common in orientations)
            abstract_free = ab < t and ba < t
            ok = clean and (case.abstract_free is None or case.abstract_free == abstract_free)
            detail = f"parts=({len(a)},{len(b)}) ordered-clean={clean} abstract-free={abstract_free}"
        return Result(ok, f"n={n} m={m} roundtrip=True {detail}")
    except (ValueError, IndexError) as error:
        return Result(False, str(error))


# Every checker must pass. crosscheck shares no code with verify.py.
CHECKERS = {"verify.py": primary_check, "networkx": crosscheck.check}


def verify_case(case: Case, root: Path = ROOT, checkers=CHECKERS) -> Result:
    """Verify the exact file mirrors the registry, then require every checker to pass."""
    try:
        graph6 = (Path(root) / case.path).read_text().strip()
    except (OSError, UnicodeError) as error:
        return Result(False, str(error))
    if graph6 != case.graph6:
        return Result(False, "graph6 file differs from registry")
    results = {name: check(case, graph6) for name, check in checkers.items()}
    detail = "; ".join(f"{name}: {result.detail}" for name, result in results.items())
    return Result(all(result.ok for result in results.values()), detail)


def main(argv=None):
    """Verify every witness, or only the records whose ids are given."""
    ids = set(sys.argv[1:] if argv is None else argv)
    try:
        cases = load_cases()
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"REGISTRY ERROR: {error}", file=sys.stderr)
        return 1
    unknown = ids - {case.id for case in cases}
    if unknown:
        print(f"UNKNOWN RECORD ID: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 1
    cases = [case for case in cases if not ids or case.id in ids]
    results = [(case, verify_case(case)) for case in cases]
    for case, result in results:
        print(f"[{'OK' if result.ok else 'FAIL'}] {case.id}: {result.detail}")
    ok = all(result.ok for _, result in results)
    print("ALL WITNESSES VERIFIED" if ok else "VERIFICATION FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
