# Repository guidelines

Purpose: a citable ledger of Alexander Richard Towell's House of Graphs (HoG)
witnesses, each verifiable from its exact graph6, honestly described, and
easy to build on. The ledger grows by systematic sweeps across invariant
families; C6 is one family among several.

## Research ownership

This repo owns the deposit registry, witness files, receipts for external
actions, and independent graph-property checks. Proofs, exhaustive searches,
complete minimum families and manuscripts remain in `../open-problems`;
sequence work is in `../oeis`. Read `docs/research-handoff.md` and
`../open-problems/docs/repository-roles.md`.

C6 evidence is on open-problems `master` (the `work/c6-contributions` worktree
was merged and retired 2026-10-21). C6 research is paused, maintenance only;
start from `docs/history/2026-10-21-c6-maintenance.md` for branch pointers and
the review boundary, and `../open-problems/docs/c6-current-status.md` before
any C6 research. Do not resume historical sessions or searches from old logs.

## Commands

Dependencies (PyYAML, networkx) are declared in `pyproject.toml`; the system
`python3` may not have them. Install with `python3 -m pip install -e '.[dev]'`,
or prefix any command with `uv run --with pyyaml --with networkx --with coverage`.
From the repository root:

```
python3 -m hogledger verify                    # the gate: exit 0 iff every witness passes
python3 -m hogledger verify sat-c6-n15         # only the named record ids
python3 -m hogledger render                    # regenerate docs/graphs/, README table, CITATION.cff, .zenodo.json
python3 -m hogledger render --check            # list stale generated files; exit 1 if any
python3 -m unittest discover -s tests -v
python3 -m unittest tests.test_registry_verification.RegistryVerificationTests.test_deposited_requires_confirmed_id
python3 -m coverage run -m unittest discover -s tests && python3 -m coverage report
```

Run the gate and the tests before adding, editing or depositing any graph;
both must pass before graph data is committed. After any registry, witness or
receipt change, run `python3 -m hogledger render`; the suite fails on stale
output.

## Architecture

The package `hogledger/` takes a ledger root (the directory holding
`contributions.yaml`; the CLI's `--root`, default the current directory).

- `contributions.yaml` is the single source of truth: top-level `author`,
  `ledger` (title, abstract, keywords, version, `license: {data, code}`, and
  `doi` once a release is archived), `papers` (current DOIs) and a `graphs`
  list. Each record carries `id`, `claim`, invariant, n, edges, `graph6`,
  `graph_file`, `hog_id`, status, certificates, `non_iso_minima`, a
  per-record `zenodo` (the archive version backing *that* record), notes, and
  a structured `verification:` block.
- `model.py`: the typed vocabulary (`Family`, `ClaimKind`, `Case`, `Claim`,
  `PriorArt`, `Record`, `Receipt`, `Ledger`, ...).
- `registry.py`: `load_records`/`load_cases`/`load_ledger`, fail-closed. It
  rejects unregistered, missing, duplicate or out-of-tree `.g6` files,
  inconsistent counts, malformed ids or claims, and `status: deposited`
  without a positive `hog_id`.
- `gate.py`: `verify_case()` requires the file's bytes to equal the registry
  `graph6`, then runs every checker in `CHECKERS` and passes only if all
  agree. Each checker independently decodes, checks n and edges, requires the
  canonical encoding, and tests the family's property:
  - `primary.py`: pure-Python codec (n <= 62) and brute-force checks copied
    from open-problems `hog/hog_verify.py`.
  - `crosscheck.py`: networkx (its own codec, path search, clique enumeration),
    sharing no code with `primary.py`. It rejects disconnected
    ordered-bipartite witnesses, whose bipartition is ambiguous.
  "Independently checked" means both pass; never weaken this to one checker.
- Verification families (`model.Family`): `cycle_saturation` /
  `path_saturation`: `{family, order}`; `clique_saturation`: `{family, order: 4}`
  (only K4); `ordered_bipartite`: `{family, forbidden_parts: [s, t]}` plus
  record-level `parts: [a, b]` and optional `k34_free` (whether the
  *unlabeled* graph is also abstractly free).
- Claims (`model.ClaimKind`): `known_value`, `new_value`,
  `new_classification`, `correction`, or `unassessed`. Every kind except
  `unassessed` needs prior-art entries with `source`, `finding` and a
  YAML-date `checked`. `unassessed` records are prior-art sweep targets.
- `receipts.py`: `receipts/YYYY-MM-DD-<slug>.json`, one per external action
  (HoG submission or annotation, Zenodo publication). Schema version 2 is
  documented in the module docstring: `date`, `action`, `records` (ids),
  `summary`, optional `attachments` and free-form `details`. Legacy
  `schema_version: "1.0"` receipts are kept byte for byte; their records
  derive from HoG ids. Every other file in `receipts/` must be attached by
  some receipt.
- `render.py` generates `docs/graphs/<id>.md` (claim, prior art, witness
  SHA-256 computed from the file, verify command, citation, receipts), the
  README block between the `BEGIN/END GENERATED: deposits` markers,
  `CITATION.cff` and `.zenodo.json`. Never hand-edit these; change the
  registry and re-render. Family narratives in `docs/families/` are
  hand-written.
- `provenance/` holds the original deposit-prep JSON; `docs/history/` holds
  dated operations notes. Neither is a receipt.

Adding a witness is a data-only change: one registry record plus the exact
`.g6` file. A new invariant family needs a `Family` value, a branch in *both*
checkers, and accept/reject fixtures in `tests/test_property_checkers.py`,
whose table runs every case against every checker. Include a near miss that
only the freeness check rejects (e.g. a complete graph: no non-edges, so
saturation holds vacuously).

## Status vocabulary

- `deposited`: live on House of Graphs with a confirmed graph id (`hog_id` set).
- `ready`: witness verified from scratch, both certificates in hand, not deposited.
- `candidate`: worth a deposit, pending a HoG duplicate-check.

Live status and counts are in `contributions.yaml` and the generated README
table; do not copy them into instruction files.

## Conventions

- Identity: Alexander Richard Towell, handle `queelius`, email
  `lex@metafunctor.com`, ORCID 0000-0001-6443-9897.
- Verify then claim. Do not mark a graph `deposited` without a confirmed live
  HoG id, or assert a value or graph6 the gate has not re-checked. A witness
  establishes attainment (the upper bound) only; an exact value also needs the
  lower-bound evidence from open-problems. Absence from HoG does not make a
  value new: record the checked prior art in the record's `claim` (LESSONS.md
  2026-10-17). Enter a source only after reading it; never cite from memory.
- graph6 strings can contain a literal backtick (ASCII 96). Store each as a
  byte-exact file and re-decode it; record byte values in a comment when a
  string contains a backtick.
- Never call a Zarankiewicz witness "K_(s,t)-free". State the matrix condition
  ("no s-by-t all-ones submatrix") or the one-sided neighbour-sharing
  condition. HoG stores graphs unlabeled, so the abstract claim is false for
  the transposed orientation of z(10,10) and z(9,10). Only z(9,11) is
  genuinely K_(3,4)-free (`k34_free: true`). See LESSONS.md.
- Cite the exact archived version that backs each claim. Current releases are
  in `contributions.yaml` `papers:`. Per-record `zenodo` fields keep earlier
  versions (e.g. 21350167) as historical evidence; do not rewrite them.
- House of Graphs submissions and annotations (decided 2026-10-21): once the
  gate and tests pass and the canonical-form duplicate-check is done, the
  agent may submit and annotate; Alex handles login only. Write a receipt for
  every external action and confirm the live id before setting `deposited`.
- Releases: bump `ledger.version` and `pyproject.toml` together (a test checks
  they agree), render, tag `v<version>`, and archive as a new version of the
  ledger's Zenodo concept record; never create a second concept.
- When a deposit is corrected or a value is found wrong, add a dated entry to
  LESSONS.md. Correcting local metadata does not update a public HoG
  annotation; verify that separately.
- Licensing: data (registry, witnesses, receipts, docs) is CC-BY-4.0
  (`LICENSE-DATA`); code (`hogledger/`, `tests/`) is MIT (`LICENSE`).
- Style: four-space indentation, typed records and enums, concise docstrings.
  Derive behaviour from registry structure; no parallel tables in code.
  Commits use short imperative subjects naming the affected graph or rule.
- The design behind ids, claims, generated docs, citation and this layout is
  `docs/superpowers/specs/2026-10-21-ledger-structure-design.md`.
