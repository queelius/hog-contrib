# Repository Guidelines

## Project Structure & Module Organization

`contributions.yaml` is the source of truth for every House of Graphs deposit or candidate. Byte-exact graph6 witnesses live in `graphs/`, while `manifests/` preserves the original JSON deposit-preparation records. `verify.py` contains the pure-Python graph6 codec and graph-property checks; `verify_witnesses.py` is the repository-wide verification gate. Read `LESSONS.md` before preparing deposits, and keep the human-facing summary in `README.md` aligned with material status changes.

## Research Ownership

This repository owns graph deposits and their independent witness checks.
Proofs, exhaustive lower-bound research, complete extremal families, and papers
remain in `../open-problems`; sequence work belongs in `../oeis`. Read
`docs/research-handoff.md` and the shared `../open-problems/docs/repository-roles.md`.
Before starting C6 research, read `../open-problems/docs/c6-current-status.md`;
the C6 line was merged into open-problems `master` on 2026-10-21.

## Build, Test, and Development Commands

There is no build step. PyYAML parses the structured registry. Every witness
must pass two separate property checkers: pure-Python `verify.py` and
networkx-based `crosscheck.py`, which share no code. Run from the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 verify_witnesses.py
python3 -m unittest discover -s tests -v
python3 -m py_compile verify.py verify_witnesses.py
```

The witness gate decodes every registered graph, checks counts and round trips,
and applies its defining property checks. Both the gate and the registry tests
must pass before graph data is committed; compilation is only a syntax check.

## Coding Style & Naming Conventions

Use four-space indentation, `snake_case` functions and variables, typed records
and enums, and concise docstrings. Derive verification cases from structured
registry data; do not maintain a parallel `CASES` table. Keep checks explicit
and deterministic. Name witnesses after their invariant and parameters, for
example `graphs/sat9_C6_12.g6`. Preserve graph6 files byte-for-byte; strings may
contain a literal backtick.

## Testing Guidelines

The unittest suite in `tests/` checks registry and verification failures. There
is no numeric coverage threshold; inspect coverage when changing logic. Add a
witness through its registry metadata and exact `.g6` file, then run the full
witness gate. New invariant families need focused property tests and independent
cross-checks. A witness establishes attainment, not the lower bound for exactness. Every record
needs a permanent `id` and a structured `claim`; any kind other than `unassessed`
must cite dated prior art that was actually read.

## Commit & Pull Request Guidelines

Use short, imperative subjects identifying the affected graph or verification
rule. Pull requests should explain the invariant or status change, cite the
backing evidence and its version, and include verification output. Never mark
an entry `deposited` without a confirmed live HoG ID; add a dated `LESSONS.md`
entry for corrected claims.
