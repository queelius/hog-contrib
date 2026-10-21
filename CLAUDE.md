# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# hog-contrib -- repo instructions

Purpose: track Alex Towell's House of Graphs (HoG) deposits and the certificates
and lessons behind them, so each deposited graph is verifiable, honestly
described, and easy to build on.

## Research ownership (2026-10-17)

This repo maintains the deposit registry, witness files, annotations, and
independent graph-property checks. Mathematical proofs, exhaustive searches,
complete minimum families, and manuscripts remain in `../open-problems`;
sequence work is maintained in `../oeis`. Read `docs/research-handoff.md` and
`../open-problems/docs/repository-roles.md`.

Locate current C6 evidence with `git -C ../open-problems worktree list`:
branch `work/c6-contributions` is in a separate research worktree. The older
main-checkout reports are not a current work queue. As of 2026-10-21 C6
research is paused (maintenance only); start from
`docs/c6-maintenance-2026-10-21.md` for branch pointers and the review boundary.
Do not resume historical sessions or searches from old logs.

## Commands

Dependencies are PyYAML and networkx (`requirements.txt`), and the system
`python3` may not have them. Use one of:

```
python3 -m pip install -r requirements.txt     # or a venv
uv run --no-project --with-requirements requirements.txt python3 verify_witnesses.py
```

Then, from the repo root:

```
python3 verify_witnesses.py                    # the gate: exit 0 iff every witness passes
python3 -m unittest discover -s tests -v       # registry/gate regression tests
python3 -m unittest tests.test_registry_verification.RegistryVerificationTests.test_deposited_requires_confirmed_id
python3 -m coverage run -m unittest discover -s tests && python3 -m coverage report
```

Run the gate and the tests before adding, editing, or preparing to deposit any
graph. Both must pass before graph data is committed.

## Architecture

- `contributions.yaml` is the single source of truth. It has top-level `author`,
  `papers` (current DOIs), and a `graphs` list. Each record carries invariant,
  n, edges, `graph6`, `graph_file`, `hog_id`/`hog_url`, status, certificates,
  `non_iso_minima`, a per-record `zenodo` (the archive version backing *that*
  record), and notes.
- Each record's structured `verification:` block drives the gate. There is no
  parallel witness table in code, and none should be added. Families
  (`verify_witnesses.Family`):
  - `cycle_saturation` / `path_saturation`: `{family, order}`
  - `clique_saturation`: `{family, order: 4}` (only K4 is supported)
  - `ordered_bipartite`: `{family, forbidden_parts: [s, t]}` plus record-level
    `parts: [a, b]` and optional `k34_free` (whether the *unlabeled* graph is
    also abstractly free). The check passes if some orientation has the stated
    part sizes with fewer than t common neighbours for every s-subset.
- `verify_witnesses.load_cases()` builds typed `Case` objects. It rejects:
  unregistered `.g6` files, missing files, duplicate paths, paths outside
  `graphs/`, inconsistent counts, and `status: deposited` without a positive
  `hog_id`.
- `verify_case()` re-reads the file and requires its bytes to equal the registry
  `graph6`. It then runs every checker in `verify_witnesses.CHECKERS` and passes
  only if all agree. Each checker independently decodes, checks n and edges,
  requires the canonical encoding, and tests the family's property:
  - `primary_check` uses `verify.py`: a pure-Python codec (n <= 62) with
    brute-force checkers copied from open-problems `hog/hog_verify.py`.
  - `crosscheck.check` uses networkx (its own codec, path search, clique
    enumeration) and shares no code with `verify.py`. It rejects disconnected
    ordered-bipartite witnesses, whose bipartition is ambiguous.
  "Independently checked" means both pass; never weaken this to one checker.
- Shared types (`Family`, `Case`, `Result`) live in `cases.py`.
- Adding a witness is a data-only change: one registry record plus the exact `.g6`
  file. A new invariant family needs: a `Family` value, a branch in *both*
  checkers, and accept/reject fixtures in `tests/test_property_checkers.py`.
  That table runs every case against every checker. Include a near miss that
  only the freeness check rejects (e.g. a complete graph: no non-edges, so
  saturation holds vacuously).
- `manifests/` holds the original deposit-prep JSON (`saturation-graphs.json`,
  `zarankiewicz-graphs.json`) and dated publication and maintenance receipts
  (`c6-*.json`, `c6-v6-annotation.md`) recording live HoG checks.
- `README.md` carries the human-facing deposit table and the "Latest run" line.
  Keep both aligned with any status change.

## Status vocabulary

- `deposited` : live on House of Graphs with a confirmed graph id (`hog_id` set).
- `ready` : witness verified from scratch, both certificates in hand, not deposited.
- `candidate` : worth a deposit, pending a HoG duplicate-check.

Live status and the HoG id mapping, including canonical matches to pre-existing
graphs, are in `contributions.yaml`. Do not copy counts into this file.

## Conventions

- Identity: Alexander Richard Towell, handle `queelius`, email `lex@metafunctor.com`,
  ORCID 0000-0001-6443-9897. Use these for any author or citation field.
- Verify then claim. Do not mark a graph `deposited` without a confirmed live HoG
  id. Do not assert a value or a graph6 that has not been re-decoded and
  re-checked by `verify_witnesses.py`. A witness establishes attainment (the
  upper bound) only. An exact value also needs the lower-bound evidence from
  open-problems. Absence from HoG does not make a value new: check prior art
  (see LESSONS.md 2026-10-17).
- graph6 strings can contain a literal backtick (ASCII 96). Store each as a
  byte-exact file and re-decode it; never rely on a graph6 typed into prose.
  Record byte values in a comment when a string contains a backtick.
- Never call a Zarankiewicz witness "K_(s,t)-free". State the matrix condition
  ("no s-by-t all-ones submatrix") or the one-sided neighbour-sharing condition.
  House of Graphs stores graphs unlabeled, so the abstract claim is false for the
  transposed orientation of z(10,10) and z(9,10). Only z(9,11) is genuinely
  K_(3,4)-free (`k34_free: true`). See LESSONS.md.
- Cite the exact archived version that backs each claim. The current releases
  are in `contributions.yaml` `papers:`: saturation v6 10.5281/zenodo.23527267
  and Zarankiewicz 10.5281/zenodo.19985042. Per-record `zenodo` fields keep
  earlier versions (e.g. 21350167) as historical evidence; do not rewrite them.
- House of Graphs submissions and annotations (decided 2026-10-21): once the
  gate and tests pass and the canonical-form duplicate-check is done, the agent
  may submit and annotate. Alex handles login only. Record a receipt in
  `manifests/` for every external action, and confirm the live id before
  setting `deposited`.
- When a deposit is corrected or a value is found wrong, add a dated entry to
  LESSONS.md: what happened, why, and the rule going forward. Correcting local
  metadata does not update a public HoG annotation; verify that separately.
