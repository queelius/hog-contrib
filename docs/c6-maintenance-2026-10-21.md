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
  maintenance commit `cf3452b`, advanced by normal fast-forward. The archive
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

## Shared public index: reconciliation applied

After user confirmation, shared `research-records/main` was reconciled at
`97289ce`, including public state through pinned commit `17af4a9`. It is
clean and no longer divergent from that remote state: eight local commits
ahead, zero behind at verification. Its C6 record tree is byte-identical to
the public remote. All 24 catalog IDs are present without duplicates, all
preexisting remote record files are byte-preserved, and local-only codec
records remain unpublished. No public-index push was made.

A local safety commit `4bf1b0d` preserves the original shared HEAD,
README/catalog edits and untracked sandpile files at
`safety/c6-index-before-reconciliation-20261021`. All six saved files were
checked byte-for-byte before adopting that existing commit by fast-forward.
The checkout then fast-forwarded to the separately validated reconciliation;
one additional pinned remote update was merged without rewriting history.
`audit/c6-shared-index-20261021` and `/tmp/c6-index-publication-20261021` retain
the final reconciliation. Neither safety/audit branch was pushed. Review the
local-only codec record with its owning session before any shared-main push;
do not force-push or treat public indexing as approval to publish local work.

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
