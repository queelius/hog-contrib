#!/usr/bin/env python3
"""Verify every graph6 witness using the structured contributions registry."""

import datetime
import itertools
from pathlib import Path
import re
import sys

import yaml

from cases import Case, Claim, ClaimKind, Family, PriorArt, Result
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


def load_cases(registry: Path = ROOT / "contributions.yaml") -> list[Case]:
    """Load typed cases and reject omitted files or inconsistent metadata."""
    registry = Path(registry)
    root = registry.parent.resolve()
    data = yaml.safe_load(registry.read_text())
    if not isinstance(data, dict) or not isinstance(data.get("graphs"), list):
        raise ValueError("registry must contain a graphs list")
    cases = []
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
        if record.get("status") == "deposited":
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
        cases.append(Case(path, graph6, n, edges, family, order, parts, forbidden, abstract_free,
                          record_id, claim))
    files = {path.relative_to(root) for path in (root / "graphs").rglob("*.g6")}
    if files - paths:
        raise ValueError(f"unregistered graph files: {sorted(map(str, files - paths))}")
    if paths - files:
        raise ValueError(f"missing graph files: {sorted(map(str, paths - files))}")
    return cases


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


def main():
    try:
        cases = load_cases()
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"REGISTRY ERROR: {error}", file=sys.stderr)
        return 1
    results = [(case, verify_case(case)) for case in cases]
    for case, result in results:
        print(f"[{'OK' if result.ok else 'FAIL'}] {case.path.name}: {result.detail}")
    ok = all(result.ok for _, result in results)
    print("ALL WITNESSES VERIFIED" if ok else "VERIFICATION FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
