# Handoff between research and graph deposits

Adopted 2026-10-17. `hog-contrib` maintains the deposit lifecycle and checks
the exact witness being deposited. `open-problems` maintains the supporting
mathematics, research implementation, exhaustive runs, full families, and papers.
Sequence work belongs in `oeis`. The shared
[ownership guide](../../open-problems/docs/repository-roles.md) defines these boundaries.

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
`python3 verify_witnesses.py` plus the unittest suite. Recheck the exact bytes,
property, and database identity when preparing a deposit. Maintain deposit
status here and link to the research evidence rather than copying a live
research-status ledger.

When research corrects a value, property, or attribution, inspect every affected
registry record and annotation, record the correction in `LESSONS.md`, and
verify any authorized external update separately. Correcting local metadata
does not mean a public annotation has been changed.

## Current C6 location

On 2026-10-17, branch `work/c6-contributions` in `open-problems` was checked out
at `../open-problems-c6-publication`. Discover the current path with:

```bash
git -C ../open-problems worktree list
```

Read `docs/graph-contributions-progress.md`,
`discoveries/extremal-graph-theory/saturation/REPRODUCE.md`, and
`discoveries/extremal-graph-theory/saturation/PRIOR-ART-2026-10-17.md` on that
branch before restarting computations or claiming publication. The branch
records newer evidence and unresolved final-literature checks; this registry
does not replace them. Its integration into the main research checkout is a
separate action, not a prerequisite to keeping the deposit ledger accurate.
