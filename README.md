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

These graphs realize exact values of extremal invariants with no known closed
form (C6 saturation) or newly computed values of classical ones (Zarankiewicz
z(m,n;3,4), K_4 and P_4 saturation). Each was computed by SAT solving or
exhaustive enumeration, checked against published prior art, and re-verified from
its graph6 string before it was called ready. The two headline results are
`sat(9,C6)=12` and `sat(10,C6)=13`: new exact values, each with both
certificates, that continue the observed `n+3` pattern and sit at the top of the
Lan-Shi window valid for `n >= 9`.

## Layout

- `contributions.yaml` : single source of truth. One record per graph deposit or
  candidate (invariant, n, edges, graph6, hog_id, status, certificates,
  non_iso_minima, zenodo, verified).
- `graphs/` : byte-exact graph6 witness files, one per record. Some contain a
  literal backtick (ASCII 96); they are written from byte values, not prose.
- `verify.py` : the graph6 toolkit and property checkers (decode/encode, edge
  count, roundtrip, C6-free/saturated, K_4-free/saturated, bipartite report).
- `verify_witnesses.py` : the verification gate. Re-decodes every witness in
  `graphs/`, checks n, edges, roundtrip, and the defining property.
- `manifests/` : `saturation-graphs.json` and `zarankiewicz-graphs.json`, the
  original deposit-prep records (edge lists, matrices, descriptions) for
  provenance.
- `LESSONS.md` : dated lessons-learned log. Read before preparing a deposit.
- `CLAUDE.md` : repo instructions.

## Verify

```
python3 verify_witnesses.py     # re-decode and re-check every witness in graphs/
```

Latest run (2026-07-03): all 14 witnesses verified. The C6 headline checks:
`sat(9,C6)=12` is C6-free and C6-saturated at 12 edges; `sat(10,C6)=13` is
C6-free and C6-saturated at 13 edges (primary and near-cubic alternate minima).

## Status vocabulary

`candidate` (worth a deposit, pending a HoG duplicate-check), `ready` (verified,
both certificates, not yet deposited), `deposited` (live on House of Graphs with a
confirmed id). Registration, the duplicate-check, and the final submit are Alex's
own step.

## Deposits and candidates

| Invariant | n | edges | HoG id | status |
|-----------|---|-------|--------|--------|
| sat(7,C6)=10 | 7 | 10 | -- | candidate |
| sat(8,C6)=11 | 8 | 11 | [57145](https://houseofgraphs.org/graphs/57145) | deposited |
| sat(9,C6)=12 | 9 | 12 | -- | ready |
| sat(10,C6)=13 (primary) | 10 | 13 | -- | ready |
| sat(10,C6)=13 (alternate) | 10 | 13 | -- | ready |
| sat(8,K_4)=13 | 8 | 13 | -- | ready |
| sat(9,K_4)=15 | 9 | 15 | -- | ready |
| sat(10,K_4)=17 | 10 | 17 | -- | ready |
| sat(6,P_4)=3 | 6 | 3 | -- | ready |
| sat(7,P_4)=5 | 7 | 5 | -- | ready |
| sat(8,P_4)=4 | 8 | 4 | -- | ready |
| z(10,10;3,4)=66 | 20 | 66 | [56650](https://houseofgraphs.org/graphs/56650) | deposited |
| z(9,10;3,4)=60 | 19 | 60 | [56652](https://houseofgraphs.org/graphs/56652) | deposited |
| z(9,11;3,4)=66 | 20 | 66 | [56651](https://houseofgraphs.org/graphs/56651) | deposited |

Four graphs are live on House of Graphs; ten are verified and ready or candidate.

## Papers

- Saturation: A. Towell, "Graph saturation for C_k, P_k, K_4, K_{2,3}", Zenodo
  [10.5281/zenodo.19985046](https://doi.org/10.5281/zenodo.19985046).
- Zarankiewicz: A. Towell, "Three new Zarankiewicz numbers z(m,n;3,4)", Zenodo
  [10.5281/zenodo.19985042](https://doi.org/10.5281/zenodo.19985042).

The Zarankiewicz values are also on OEIS (A006615, A006622, A006625).

---

House of Graphs is a shared database of graphs with computed invariants. Adding a
concrete extremal witness makes a value citable and checkable by anyone: a graph
that realized a bound is now stored, named, and searchable.
