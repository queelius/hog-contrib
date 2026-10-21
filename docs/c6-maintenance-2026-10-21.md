# C6 branch and session checkpoint

Alexander Richard Towell. 2026-10-21. Maintenance only; research is paused.

## Start here

The exact public evidence is [Zenodo v6](https://doi.org/10.5281/zenodo.23527267).
The [public index](https://github.com/queelius/research-records/tree/main/records/small-order-c6-saturation)
and [HoG58092](https://houseofgraphs.org/graphs/58092) describe the 24-class
order-15 minimum family. This repository owns deposit status and witness
verification; detailed research remains in `open-problems`.

The canonical local research handoff is
[`c6-current-status.md`](../../open-problems-c6-publication/docs/c6-current-status.md),
with an [independent-review brief](../../open-problems-c6-publication/docs/c6-review-brief.md).
Locate that checkout using `git -C ../open-problems worktree list` from this
repository root. Do not resume historical sessions or searches from old logs.

## Branch reconciliation

- `open-problems` remote `master` and `work/c6-contributions` now both contain
  maintenance commit `e585398`, advanced by normal fast-forward. The archive
  source pin remains `47002aacd10733ed784ce054c8ae8c39cd19a178`.
- `hog-contrib/main` is advanced only by fast-forward from the verified
  `work/c6-contributions` branch. Its local `main` can likewise advance
  without switching the dirty active worktree.
- The original local `open-problems/master` is divergent and heavily dirty.
  It is not the current C6 checkout. Its branch and files were not reset,
  rebased, stashed, bulk-staged or merged. Its old ownership guide's C6
  checkpoint predates v6; follow the current handoff above instead.
- Older research branches remain historical. No branches were deleted,
  histories rewritten, visibility changed or frozen archives replaced.

## Shared public index: preserved, not switched

The shared `research-records/main` contains other sessions' work. Its C6
record tree is byte-identical to the public remote; no C6 change is missing.
The apparent divergence includes equivalent cherry-picked C6 and coprime
changes, a local-only codec record, and remote-only records from other projects.
The four untracked sandpile files already match the remote byte-for-byte.

A local safety commit `4bf1b0d` preserves the shared HEAD, README/catalog edits
and untracked sandpile files at
`safety/c6-index-before-reconciliation-20261021`. A clean reconciliation is
available at `audit/c6-shared-index-20261021`, commit `b9db93a`, and in
`/tmp/c6-index-publication-20261021`. It combines all 20 catalog IDs from both
parents, with no duplicates; every preexisting remote record is byte-preserved.
Neither branch was pushed. The shared checkout remains untouched, pending
confirmation that another session is not using it. Do not force-push its
divergent `main`, publish unrelated records, or apply the candidate blindly
after further remote/local changes.

## Review and verification boundary

The review brief separates minimality, graph-generation coverage, leaf
attachments, kernel coverage and final witness checks. Human review remains
pending; no one was contacted. No new experiment, census, publication version,
submission or email was initiated.

All 61 focused research tests passed for this maintenance revision. The audit
checks new documentation links and source/archive pins; one inherited broken
`../erdos/` link in the research README was left out of scope. No verification
logic changed, so no new code-coverage measurement is claimed. The structured
[audit receipt](../manifests/c6-maintenance-2026-10-21.json) records the final
registry checks and the limited branch-tip exclusion scan; it does not claim
an exhaustive historical secret scan.
