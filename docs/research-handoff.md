# Handoff between research and graph deposits

Adopted 2026-10-17. `hog-contrib` maintains the deposit lifecycle and checks
the exact witness being deposited. `open-problems` maintains the supporting
mathematics, research implementation, exhaustive runs, full families, and papers.
Sequence work belongs in `oeis`. The shared
[ownership guide](../../open-problems/docs/repository-roles.md) defines these boundaries.

The ledger's central index record is `hog-witness-ledger` in
[research-records](https://github.com/queelius/research-records/tree/main/records/hog-witness-ledger).
After each archived release, update that record to the new version DOI and
public-file hashes; the concept DOI stays 10.5281/zenodo.23550687.

## Evidence supplied by the research repository

- A precise invariant and convention, including ordered bipartite conditions
  where applicable.
- The byte-exact witness and an independent property check.
- A separate lower-bound argument when claiming an exact extremal value.
  Record whether this is a checked certificate, exhaustive enumeration, a
  theorem, or only a solver report; agreement alone does not make them equivalent.
- A source commit or archive version and reproducible evidence paths.
- The scope of any complete minimum-family classification and the actual
  prior-art checks, including unresolved questions.

Retain the full research artifacts at their source even when this registry
stores only selected graph representatives. A deposition candidate is not a
new mathematical result merely because its graph6 is absent from a database.

## Work maintained here

Use the existing `contributions.yaml` and its structured `verification` fields;
do not introduce a second witness table in code. Add exact `.g6` files and run
`python3 -m hogledger verify` plus the unittest suite. Recheck the exact bytes,
property, and database identity when preparing a deposit. Maintain deposit
status here and link to the research evidence rather than copying a live
research-status ledger.

When research corrects a value, property, or attribution, inspect every affected
registry record and annotation, record the correction in `LESSONS.md`, and
verify any authorized external update separately. Correcting local metadata
does not mean a public annotation has been changed.

## Current C6 location

The C6 line, checked out at `../open-problems-c6-publication` from 2026-10-17,
was merged into open-problems `master` on 2026-10-21 and the worktree retired.
Read `docs/graph-contributions-progress.md`,
`discoveries/extremal-graph-theory/saturation/REPRODUCE.md`, and
`discoveries/extremal-graph-theory/saturation/PRIOR-ART-2026-10-17.md` there
before restarting computations or claiming publication. They record the evidence and final-literature checks; this registry does not
replace them.
