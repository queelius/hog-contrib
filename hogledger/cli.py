"""Command line: `hogledger verify [ID ...]` and `hogledger render [--check]`."""

import argparse
from pathlib import Path
import sys

import yaml

from . import gate, registry, render

LOAD_ERRORS = (OSError, ValueError, KeyError, TypeError, yaml.YAMLError)


def verify(root: Path, ids: list[str]) -> int:
    """Verify every witness, or only the records whose ids are given."""
    try:
        cases = registry.load_cases(root)
    except LOAD_ERRORS as error:
        print(f"REGISTRY ERROR: {error}", file=sys.stderr)
        return 1
    unknown = set(ids) - {case.id for case in cases}
    if unknown:
        print(f"UNKNOWN RECORD ID: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 1
    results = [(case, gate.verify_case(case, root)) for case in cases if not ids or case.id in ids]
    for case, result in results:
        print(f"[{'OK' if result.ok else 'FAIL'}] {case.id}: {result.detail}")
    ok = all(result.ok for _, result in results)
    print("ALL WITNESSES VERIFIED" if ok else "VERIFICATION FAILED")
    return 0 if ok else 1


def render_outputs(root: Path, check: bool) -> int:
    """Rewrite the generated files, or with check list the stale ones."""
    try:
        if not check:
            render.write(root)
            return 0
        paths = render.stale(root)
    except LOAD_ERRORS as error:
        print(f"REGISTRY ERROR: {error}", file=sys.stderr)
        return 1
    for path in paths:
        print(f"STALE: {path}")
    return 1 if paths else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="hogledger", description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="ledger directory holding contributions.yaml (default: current)")
    commands = parser.add_subparsers(dest="command", required=True)
    verify_parser = commands.add_parser("verify", help="check witnesses with every checker")
    verify_parser.add_argument("ids", nargs="*", metavar="ID", help="record ids (default: all)")
    render_parser = commands.add_parser("render", help="regenerate pages, README table, citation files")
    render_parser.add_argument("--check", action="store_true", help="list stale files; exit 1 if any")
    args = parser.parse_args(argv)
    if args.command == "verify":
        return verify(args.root, args.ids)
    return render_outputs(args.root, args.check)
