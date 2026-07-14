# hog-contrib -- repo instructions

Purpose: track Alex Towell's House of Graphs (HoG) deposits and the certificates
and lessons behind them, so each deposited graph is verifiable, honestly
described, and easy to build on. Private for now (no remote).

## Files

- `contributions.yaml` -- source of truth. One record per graph deposit or
  candidate: invariant, n, edges, graph6, hog_id, status, certificates,
  non_iso_minima, zenodo, verified, notes.
- `graphs/<name>.g6` -- byte-exact graph6 witness files, one per record.
- `verify.py` -- graph6 toolkit and property checkers (copied from the
  open-problems `hog/hog_verify.py`).
- `verify_witnesses.py` -- the verification gate; re-decodes and re-checks every
  witness in `graphs/`.
- `manifests/` -- original deposit-prep JSON (edge lists, matrices) for provenance.
- `LESSONS.md` -- dated lessons-learned log. Read before preparing a deposit.
- `README.md` -- human-facing overview.

## Status vocabulary

- `deposited` : live on House of Graphs with a confirmed graph id (`hog_id` set).
- `ready` : witness verified from scratch, both certificates in hand, not deposited.
- `candidate` : worth a deposit, pending a HoG duplicate-check.

Confirmed live records as of 2026-07-14: all 21 tracked witnesses have HoG ids.
The five non-isomorphic sat(9,C6)=12 minima are #21054 and #57168–#57171; the
two sat(10,C6)=13 minima are #57166 and #57167. See `contributions.yaml` for
the complete id mapping, including canonical matches to pre-existing graphs.

## Conventions

- Identity: Alexander Towell, handle `queelius`, email `lex@metafunctor.com`,
  ORCID 0000-0001-6443-9897. Use these for any author or citation field.
- Verify then claim. Do not mark a graph `deposited` without a confirmed live HoG
  id. Do not assert a value or a graph6 that has not been re-decoded and
  re-checked by `verify_witnesses.py`.
- graph6 strings can contain a literal backtick (ASCII 96). Store each as a
  byte-exact file and re-decode it; never rely on a graph6 typed into prose.
  Record byte values in a comment when a string contains a backtick.
- Never call a Zarankiewicz witness "K_(s,t)-free". State the matrix condition
  ("no s-by-t all-ones submatrix") or the one-sided neighbour-sharing condition.
  House of Graphs stores graphs unlabeled, so the abstract claim is false for the
  transposed orientation of z(10,10) and z(9,10). Only z(9,11) is genuinely
  K_(3,4)-free. See LESSONS.md.
- Cite the backing paper by its current Zenodo DOI on each deposit: saturation
  10.5281/zenodo.21350167, Zarankiewicz 10.5281/zenodo.19985042.
- Registration, the duplicate-check, and the final submit on House of Graphs are
  Alex's own step. Automation prepares and verifies; it does not deposit.
- When a deposit is corrected or a value is found wrong, add a dated entry to
  LESSONS.md: what happened, why, and the rule going forward.

## Verify

```
python3 verify_witnesses.py
```

Exit 0 iff every witness re-decodes and passes its property check. Run it before
adding, editing, or preparing to deposit any graph.
