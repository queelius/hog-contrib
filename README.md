# hog-contrib

A tracker and portfolio for Alexander Towell's House of Graphs (HoG) deposits:
the concrete extremal graphs, their deposit status, the certificate behind each
value, and the lessons that shape how they get deposited.

Each graph gets a record in `contributions.yaml` (the invariant it realizes, its
graph6 string, its House of Graphs id if live, the certificate, and whether it
has been re-verified), a byte-exact witness file in `graphs/`, and a place in the
verification gate. The witnesses come from the sibling research repo
([open-problems](https://github.com/queelius/open-problems)); this repo curates
them, tracks their HoG status, and re-checks each one from its graph6 string. Over
time this becomes a base to grow from: new extremal families, new deposits, a
record of what was verified and when.

## Why these

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

## Layout

- `contributions.yaml` : single source of truth. One record per graph deposit or
  candidate (invariant, n, edges, graph6, hog_id, status, certificates,
  non_iso_minima, zenodo, verified).
- `graphs/` : byte-exact graph6 witness files, one per record. Some contain a
  literal backtick (ASCII 96); they are written from byte values, not prose.
- `verify.py` : the graph6 toolkit and property checkers (decode/encode, edge
  count, roundtrip, cycle/path/K_4 saturation, bipartite report).
- `verify_witnesses.py` : the verification gate. Re-decodes every witness in
  `graphs/`, checks n, edges, roundtrip, and the defining property.
- `manifests/` : `saturation-graphs.json` and `zarankiewicz-graphs.json`, the
  original deposit-prep records (edge lists, matrices, descriptions) for
  provenance.
- `LESSONS.md` : dated lessons-learned log. Read before preparing a deposit.
- `CLAUDE.md` : repo instructions.

## Verify

```
python3 -m pip install -r requirements.txt
python3 verify_witnesses.py     # re-decode and re-check every witness in graphs/
python3 -m unittest discover -s tests -v
```

The verification gate reads structured `verification` fields directly from
`contributions.yaml`; no separate per-file lookup table is maintained. It
rejects missing or unregistered graph files, mismatched graph6 mirrors, and
deposited records without a positive HoG ID. PyYAML is the only runtime
dependency and is used to parse the registry safely; graph-property checks
remain pure Python.

Latest run (2026-10-21): all 26 stored witnesses verified, including the
15-vertex, 20-edge C6-saturated witness. All six registry tests pass.

## Status vocabulary

`candidate` (worth a deposit, pending a HoG duplicate-check), `ready` (verified,
both certificates, not yet deposited), `deposited` (live on House of Graphs with a
confirmed id). The current contribution goal authorizes publication and deposit
after verification; login is a user handoff when needed.

## Deposits and canonical matches

| Invariant | n | edges | HoG id | status |
|-----------|---|-------|--------|--------|
| sat(7,C6)=10 | 7 | 10 | [868](https://houseofgraphs.org/graphs/868) | deposited |
| sat(8,C6)=11 | 8 | 11 | [57145](https://houseofgraphs.org/graphs/57145) | deposited |
| sat(9,C6)=12 (classes 1–5) | 9 | 12 | [21054](https://houseofgraphs.org/graphs/21054), [57168](https://houseofgraphs.org/graphs/57168)–[57171](https://houseofgraphs.org/graphs/57171) | deposited |
| sat(10,C6)=13 (near-cubic) | 10 | 13 | [57166](https://houseofgraphs.org/graphs/57166) | deposited |
| sat(10,C6)=13 (cut-vertex) | 10 | 13 | [57167](https://houseofgraphs.org/graphs/57167) | deposited |
| sat(11,C6)=14 | 11 | 14 | [58088](https://houseofgraphs.org/graphs/58088) | deposited |
| sat(12,C6)=16 | 12 | 16 | [58089](https://houseofgraphs.org/graphs/58089) | deposited |
| sat(13,C6)=17 | 13 | 17 | [58090](https://houseofgraphs.org/graphs/58090) | deposited |
| sat(14,C6)=19 | 14 | 19 | [58091](https://houseofgraphs.org/graphs/58091) | deposited |
| sat(15,C6)=20 | 15 | 20 | [58092](https://houseofgraphs.org/graphs/58092) | deposited |
| sat(8,C5)=10 | 8 | 10 | [57172](https://houseofgraphs.org/graphs/57172) | deposited |
| sat(8,K_4)=13 | 8 | 13 | [664](https://houseofgraphs.org/graphs/664) | deposited |
| sat(9,K_4)=15 | 9 | 15 | [182](https://houseofgraphs.org/graphs/182) | deposited |
| sat(10,K_4)=17 | 10 | 17 | [250](https://houseofgraphs.org/graphs/250) | deposited |
| sat(6,P_4)=3 | 6 | 3 | [484](https://houseofgraphs.org/graphs/484) | deposited |
| sat(7,P_4)=5 | 7 | 5 | [56649](https://houseofgraphs.org/graphs/56649) | deposited |
| sat(8,P_4)=4 | 8 | 4 | [684](https://houseofgraphs.org/graphs/684) | deposited |
| sat(8,P_5)=6 | 8 | 6 | [57173](https://houseofgraphs.org/graphs/57173) | deposited |
| sat(9,P_5)=7 | 9 | 7 | [57174](https://houseofgraphs.org/graphs/57174) | deposited |
| z(10,10;3,4)=66 | 20 | 66 | [56650](https://houseofgraphs.org/graphs/56650) | deposited |
| z(9,10;3,4)=60 | 19 | 60 | [56652](https://houseofgraphs.org/graphs/56652) | deposited |
| z(9,11;3,4)=66 | 20 | 66 | [56651](https://houseofgraphs.org/graphs/56651) | deposited |

All 26 tracked witnesses are live on House of Graphs. The four earlier October 18
deposits and their downloaded canonical graphs were checked against the source
witnesses; see [publication verification](manifests/c6-publication-2026-10-18.json).
The v5 classification annotation and order-15 deposit have separate
[live verification evidence](manifests/c6-v5-publication.json).
The order-15 classification update has its own
[v6 publication receipt](manifests/c6-v6-publication.json).
Some live witnesses were submitted as new graphs;
others matched existing canonical forms and were annotated with their
saturation interpretation where useful.

## Papers

- Saturation: Alexander Richard Towell, "Small-order C6 saturation: exact
  values, minimum graphs, and a correction", Zenodo v6
  [10.5281/zenodo.23527267](https://doi.org/10.5281/zenodo.23527267).
- Zarankiewicz: A. Towell, "Three new Zarankiewicz numbers z(m,n;3,4)", Zenodo
  [10.5281/zenodo.19985042](https://doi.org/10.5281/zenodo.19985042).

The Zarankiewicz values are also on OEIS (A006615, A006622, A006625).

---

House of Graphs is a shared database of graphs with computed invariants. Adding a
concrete extremal witness makes a value citable and checkable by anyone: a graph
that realized a bound is now stored, named, and searchable.
