# Citable ledger: structure, documentation and citation

Alexander Richard Towell. Drafted 2026-10-21 with Claude Code.

## Intent

hog-contrib is an ongoing ledger of House of Graphs (HoG) witnesses, fed by
systematic sweeps, read by people (referees, other researchers) and by agents.
Its payoffs are an academic record and service to the field. A reader who
lands on any graph should find the exact claim and its scope, the prior art
behind it, the archived evidence, how to verify it, and how to cite it,
without reading prose history.

## Problems today

1. Nothing in the repo can be cited. The repo is private, has no LICENSE,
   no CITATION.cff and no stable per-graph identifier. Only HoG ids and the
   two Zenodo papers are citable. The sibling `oeis` repo is public, MIT,
   with a `type: dataset` CITATION.cff.
2. Documentation is hand-maintained and drifts. Most of README is C6
   history; its deposit table and counts are copied from the registry.
   CLAUDE.md, AGENTS.md and README overlap.
3. Claims live in prose. New/known/correction status and prior art sit in
   free-text `notes`, so the gate cannot enforce them.

## Goals

- Every record has a permanent `id` and a structured `claim`.
- The gate refuses a novelty-bearing claim without dated prior-art entries.
- Documentation that restates registry facts is generated and test-checked.
- The ledger has a citation path: CITATION.cff, a license and, if made
  public, a Zenodo concept DOI with one version per tagged release.

## Non-goals

- No change to the property checkers or the two-implementation rule.
- No new invariant families in this work (K_r, Turan, Ramsey come after).
- No rewrite of historical `notes`, receipts or per-record `zenodo` fields.

## Anti-goals

- A `kind: new_value` that rests on search absence alone, stated as novelty.
- Any fact stored twice (e.g. a witness hash typed into YAML that can be
  computed from the file).
- Prior-art entries written from memory. A source is entered only when its
  content was checked; otherwise the record is `unassessed`.

## Design

### Step 1: identifiers and structured claims (this change)

Each `graphs:` record gains:

```yaml
id: sat-c6-n15              # permanent, unique, lowercase slug; never reused
claim:
  kind: new_value           # see below
  statement: "One sentence: the exact claim and its scope."
  prior_art:                # list; required unless kind is unassessed
    - source: doi:10.1007/s00373-014-1422-4   # or a URL
      locator: "Remark 1, p. 1089"            # optional
      checked: 2026-10-17                     # YAML date, not a string
      finding: "What the source does and does not establish."
```

`kind` values (enum `ClaimKind`):

| kind | meaning |
| --- | --- |
| `known_value` | value already published; the deposit reproduces or illustrates it |
| `new_value` | exact value not located in the checked prior art |
| `new_classification` | value known; the complete minimum family is the contribution |
| `correction` | contradicts a specific published value |
| `unassessed` | prior-art status not yet recorded; a sweep target |

Gate rules, enforced in `load_cases` and fail-closed:

- `id` present, unique, matching `^[a-z0-9]+(-[a-z0-9]+)*$`.
- `claim` present with a known `kind` and a nonempty `statement`.
- Every kind except `unassessed` needs at least one prior-art entry, each
  with a `source`, a `finding` and a `checked` date.

`evidence` is the existing per-record `zenodo` field; the witness SHA-256 is
derived from the file at render time, never stored.

Initial classification, from the 2026-10-17 audit
(`open-problems/discoveries/extremal-graph-theory/saturation/PRIOR-ART-2026-10-17.md`),
the OEIS registry, and Crossref-verified metadata:

- C6 n=9, 10: `known_value` (Zhang-Luo-Shigeno 2012 preprint, Remark 1).
- C6 n=11: `correction` (2012 and 2015 Remark 1 report 15).
- C6 n=12: `new_classification` (2015 Remark 1 records 16).
- C6 n=13, 14, 15: `new_value` (bounded audit of 2015 and Lan et al. 2025,
  which give bounds only); n=14, 15 also classified.
- K4 n=8, 9, 10: `known_value` (Erdos-Hajnal-Moon 1964).
- Zarankiewicz: `new_value` (OEIS terms credited to the author's extension).
- C6 n=7, 8; C5 n=8; P4; P5: `unassessed`. Their notes assert known or new
  status without a recorded, checked source.

### Step 2: generated documentation

A `render` command writes `docs/graphs/<id>.md` (graph6, HoG link, claim,
prior art, evidence DOI, witness SHA-256, verify command, citation), the
README deposit table, and CITATION.cff. A test fails when any generated file
differs from a fresh render. The README keeps purpose, verify, table, cite;
C6 history moves to `docs/families/c6-saturation.md`. CLAUDE.md imports
AGENTS.md instead of repeating it.

### Step 3: citation (decided 2026-10-21)

Data is CC-BY-4.0 (`LICENSE-DATA`) and code MIT (`LICENSE`), recorded in the
registry's `ledger.license` and checked against `pyproject.toml`. The repo is
made public after a whole-history audit. Each tagged release is archived as a
version of one Zenodo concept record; its metadata is the generated
`.zenodo.json`, and the concept DOI is `ledger.doi`, which reaches
CITATION.cff and every page's citation. A `hog-witness-ledger` record in
research-records indexes it. Editing live HoG annotations to cite the ledger
is a separate decision, taken after the DOI exists.

### Step 4: layout (done 2026-10-21)

Package `hogledger/` with a pyproject entry point and `python3 -m hogledger
{verify,render}`; every function takes the ledger root instead of a module
constant. Modules: `model` (types), `registry` (loading), `primary` and
`crosscheck` (the two checkers), `gate`, `receipts`, `render`, `cli`. The
unused `verify.zarankiewicz_report` (pair-based, so wrong for 3x4) and the
other helpers the gate never called were removed. Dependencies live only in
`pyproject.toml`.

Receipts are `receipts/YYYY-MM-DD-<slug>.json` with schema version 2 (date,
action, record ids, summary, attachments, free-form details). The three
earlier publication receipts keep their bytes as legacy `schema_version
"1.0"`; their records derive from HoG ids. Record pages list their receipts.
Deposit-prep JSON is in `provenance/`; the branch-maintenance note and its
JSON are operations history in `docs/history/`, not receipts.

## Left to the builder

Module boundaries within the package, renderer formatting, and the receipt
schema's exact fields, provided each derives from registry structure.
