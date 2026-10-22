# C6 saturation: background and publication history

Moved from the README on 2026-10-21. Per-record claims, prior art and
evidence are generated in [the record pages](../graphs/); this page keeps
the narrative and publication history.

These graphs provide concrete, independently checkable witnesses for cycle,
path, clique, and ordered bipartite extremal problems. Known values are useful
validation cases and are distinguished from new results. In particular,
`sat(9,C6)=12`, `sat(10,C6)=13`, and their minimum families already appear in
Remark 1 of the Zhang-Luo-Shigeno preprint (2012); our earlier novelty claims
for those cases were incorrect.

The October 2026 release publishes `sat(11,C6)=14` (a unique minimum class),
the complete minimum classification for `sat(12,C6)=16`,
`sat(13,C6)=17`, and `sat(14,C6)=19`. The n=12 value breaks
the `n+3` pattern. See the sibling research repository for exhaustive count
logs and independent witness checks. Publication status is recorded below.

The final Zhang-Luo-Shigeno paper (2015), Remark 1, page 1089, also already
records `sat(12,C6)=16`. The contribution at order 12 is the complete
35-class classification. Its reported order-11 value 15 is contradicted
by our byte-verified 14-edge witness.

The complete minimum families at orders 12 and 13 have 35 and four classes.
All family witnesses and independent verification logs are preserved in the
research repository; this deposit ledger tracks one representative per new
order rather than treating additional representatives as separate contributions.

Published v5 classifies all **205** order-14 minima, with two
complete census implementations and independent checks of every witness.
The live HoG annotation links the complete archive;
the full family remains in `open-problems`. The existing HoG 58091 witness
is class 55 in the archived family order. No duplicate deposit is needed.

Published v5 proves `sat(15,C6)=20`: both complete checkers reject all
784,526,109 graphs through 19 edges, and a 20-edge witness passes independent
checks. The witness is live as
[HoG 58092](https://houseofgraphs.org/graphs/58092), backed by
[Zenodo v5](https://doi.org/10.5281/zenodo.23447722).

[Zenodo v6](https://doi.org/10.5281/zenodo.23527267) completes the order-15
minimum classification: **24 classes, 12 with leaves and 12 leaf-free**.
The archive retains the full family, complete census, leaf attachments,
weighted-kernel recovery, rejection certificates, code and verification logs.
The existing HoG 58092 annotation now links this classification; its source
witness is class 4 in the archived order. Detailed research remains in
`open-problems`; the public source is in Zenodo because the development
repositories are private. The curated public index is
[research-records](https://github.com/queelius/research-records/tree/main/records/small-order-c6-saturation).

For the canonical checkout, branch pointers and paused research boundary, read
the [C6 maintenance handoff](../c6-maintenance-2026-10-21.md).
