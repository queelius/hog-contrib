# House of Graphs witness ledger

Alexander Richard Towell's extremal and saturated graphs on
[House of Graphs](https://houseofgraphs.org) (HoG). Each graph is stored as a
byte-exact graph6 witness and counts as checked only when two separate
implementations verify its defining property. Each record states what is
claimed, what prior art was checked, and which archived evidence backs it.

The witnesses come from a private research repository, `open-problems`,
which holds the proofs, exhaustive lower-bound searches and manuscripts; the
public evidence for each value is the archived Zenodo version cited on its
record page. This ledger curates the witnesses, tracks their HoG status and
re-checks each one.

## Records

Every record has a permanent id and a page under [`docs/graphs/`](docs/graphs/)
with its claim, prior art, witness hash, verify command and citation. A claim
is one of: *known value* (already published, reproduced here), *new value*,
*new classification* (value known, complete minimum family new),
*correction* (contradicts a specific published value), or *unassessed*
(prior art not yet checked; no novelty claimed).

<!-- BEGIN GENERATED: deposits -->
26 records: 26 deposited. Claims: 10 known value, 6 new value, 1 new classification, 1 correction, 8 unassessed.

| Record | Invariant | n | Edges | Claim | House of Graphs | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [sat-c6-n7](docs/graphs/sat-c6-n7.md) | sat(7,C6)=10 | 7 | 10 | unassessed | [868](https://houseofgraphs.org/graphs/868) | deposited |
| [sat-c6-n8](docs/graphs/sat-c6-n8.md) | sat(8,C6)=11 | 8 | 11 | unassessed | [57145](https://houseofgraphs.org/graphs/57145) | deposited |
| [sat-c6-n9](docs/graphs/sat-c6-n9.md) | sat(9,C6)=12 | 9 | 12 | known value | [21054](https://houseofgraphs.org/graphs/21054) | deposited |
| [sat-c6-n9-class2](docs/graphs/sat-c6-n9-class2.md) | sat(9,C6)=12 | 9 | 12 | known value | [57168](https://houseofgraphs.org/graphs/57168) | deposited |
| [sat-c6-n9-class3](docs/graphs/sat-c6-n9-class3.md) | sat(9,C6)=12 | 9 | 12 | known value | [57169](https://houseofgraphs.org/graphs/57169) | deposited |
| [sat-c6-n9-class4](docs/graphs/sat-c6-n9-class4.md) | sat(9,C6)=12 | 9 | 12 | known value | [57170](https://houseofgraphs.org/graphs/57170) | deposited |
| [sat-c6-n9-class5](docs/graphs/sat-c6-n9-class5.md) | sat(9,C6)=12 | 9 | 12 | known value | [57171](https://houseofgraphs.org/graphs/57171) | deposited |
| [sat-c6-n10](docs/graphs/sat-c6-n10.md) | sat(10,C6)=13 | 10 | 13 | known value | [57167](https://houseofgraphs.org/graphs/57167) | deposited |
| [sat-c6-n10-alt](docs/graphs/sat-c6-n10-alt.md) | sat(10,C6)=13 | 10 | 13 | known value | [57166](https://houseofgraphs.org/graphs/57166) | deposited |
| [sat-c6-n11](docs/graphs/sat-c6-n11.md) | sat(11,C6)=14 | 11 | 14 | correction | [58088](https://houseofgraphs.org/graphs/58088) | deposited |
| [sat-c6-n12](docs/graphs/sat-c6-n12.md) | sat(12,C6)=16 | 12 | 16 | new classification | [58089](https://houseofgraphs.org/graphs/58089) | deposited |
| [sat-c6-n13](docs/graphs/sat-c6-n13.md) | sat(13,C6)=17 | 13 | 17 | new value | [58090](https://houseofgraphs.org/graphs/58090) | deposited |
| [sat-c6-n15](docs/graphs/sat-c6-n15.md) | sat(15,C6)=20 | 15 | 20 | new value | [58092](https://houseofgraphs.org/graphs/58092) | deposited |
| [sat-c6-n14](docs/graphs/sat-c6-n14.md) | sat(14,C6)=19 | 14 | 19 | new value | [58091](https://houseofgraphs.org/graphs/58091) | deposited |
| [sat-c5-n8](docs/graphs/sat-c5-n8.md) | sat(8,C5)=10 | 8 | 10 | unassessed | [57172](https://houseofgraphs.org/graphs/57172) | deposited |
| [sat-k4-n8](docs/graphs/sat-k4-n8.md) | sat(8,K\_4)=13 | 8 | 13 | known value | [664](https://houseofgraphs.org/graphs/664) | deposited |
| [sat-k4-n9](docs/graphs/sat-k4-n9.md) | sat(9,K\_4)=15 | 9 | 15 | known value | [182](https://houseofgraphs.org/graphs/182) | deposited |
| [sat-k4-n10](docs/graphs/sat-k4-n10.md) | sat(10,K\_4)=17 | 10 | 17 | known value | [250](https://houseofgraphs.org/graphs/250) | deposited |
| [sat-p4-n6](docs/graphs/sat-p4-n6.md) | sat(6,P\_4)=3 | 6 | 3 | unassessed | [484](https://houseofgraphs.org/graphs/484) | deposited |
| [sat-p4-n7](docs/graphs/sat-p4-n7.md) | sat(7,P\_4)=5 | 7 | 5 | unassessed | [56649](https://houseofgraphs.org/graphs/56649) | deposited |
| [sat-p4-n8](docs/graphs/sat-p4-n8.md) | sat(8,P\_4)=4 | 8 | 4 | unassessed | [684](https://houseofgraphs.org/graphs/684) | deposited |
| [sat-p5-n8](docs/graphs/sat-p5-n8.md) | sat(8,P\_5)=6 | 8 | 6 | unassessed | [57173](https://houseofgraphs.org/graphs/57173) | deposited |
| [sat-p5-n9](docs/graphs/sat-p5-n9.md) | sat(9,P\_5)=7 | 9 | 7 | unassessed | [57174](https://houseofgraphs.org/graphs/57174) | deposited |
| [z-10-10-3-4](docs/graphs/z-10-10-3-4.md) | z(10,10;3,4)=66 | 20 | 66 | new value | [56650](https://houseofgraphs.org/graphs/56650) | deposited |
| [z-9-10-3-4](docs/graphs/z-9-10-3-4.md) | z(9,10;3,4)=60 | 19 | 60 | new value | [56652](https://houseofgraphs.org/graphs/56652) | deposited |
| [z-9-11-3-4](docs/graphs/z-9-11-3-4.md) | z(9,11;3,4)=66 | 20 | 66 | new value | [56651](https://houseofgraphs.org/graphs/56651) | deposited |
<!-- END GENERATED: deposits -->

Some witnesses were submitted as new graphs; others matched existing
canonical forms and were annotated with their saturation interpretation.
External actions have dated receipts in [`receipts/`](receipts/), listed on
each record page, for example the
[order-15 v6 publication](receipts/2026-10-21-c6-v6-publication.json).
Background and publication history by family:
[C6 saturation](docs/families/c6-saturation.md).

## Verify

```
python3 -m pip install .                    # PyYAML and networkx
python3 -m hogledger verify                 # every witness
python3 -m hogledger verify sat-c6-n15      # named records only
python3 -m unittest discover -s tests -v
```

`hogledger/primary.py`, a pure-Python checker inherited from the research
repository, and `hogledger/crosscheck.py`, built on networkx with its own
graph6 codec and algorithms, share no code; the gate passes a witness only
when both accept it. Loading the registry also rejects unregistered or missing
graph files, graph6 files that differ from the registry, deposited records
without a HoG id, and assessed claims without dated prior art.

## Cite

- **One graph:** cite its House of Graphs entry and the archived evidence
  listed on its record page, which also gives a ready-made citation.
- **The ledger:** see [`CITATION.cff`](CITATION.cff). Each tagged release is
  archived on Zenodo; cite the version you used.
- **Papers:** A. R. Towell, "Small-order C6 saturation: exact values, minimum
  graphs, and a correction", Zenodo v6
  [10.5281/zenodo.23527267](https://doi.org/10.5281/zenodo.23527267);
  A. R. Towell, "Three new Zarankiewicz numbers z(m,n;3,4)", Zenodo
  [10.5281/zenodo.19985042](https://doi.org/10.5281/zenodo.19985042). The
  Zarankiewicz values are also on OEIS (A006615, A006622, A006625).

## Layout

- `contributions.yaml`: the single source of truth, one record per graph.
- `graphs/`: byte-exact graph6 witnesses. Some contain a literal backtick
  (ASCII 96); they are written from byte values, not prose.
- `hogledger/`: the registry loader, the gate and its two property checkers,
  the receipt loader, the renderer and the `python3 -m hogledger` command.
- `receipts/`: dated JSON receipts for external actions (HoG submissions and
  annotations, Zenodo publications).
- `docs/graphs/`, `CITATION.cff`, `.zenodo.json` and the table above are
  generated by `python3 -m hogledger render`; a test fails when any is stale.
- `docs/families/`: family histories. `docs/history/`: dated operations notes.
- `provenance/`: the original deposit-preparation JSON.
- `LESSONS.md`: dated lessons. Read before preparing a deposit.

## Research boundary

Deposits, annotations, registry metadata and independent witness checks
belong here; proofs, exhaustive computations, complete minimum families and
manuscripts stay in `open-problems`. See the
[research handoff](docs/research-handoff.md). A verified witness establishes
attainment only; an exact value also needs the lower-bound evidence in the
archived version cited on its record page.

## Status vocabulary

`deposited`: live on House of Graphs with a confirmed id. `ready`: verified,
both certificates in hand, not yet deposited. `candidate`: worth a deposit,
pending a HoG duplicate-check.

## License

Data (the registry, witnesses, receipts and documentation) is licensed under
[CC-BY-4.0](LICENSE-DATA); the code in `hogledger/` and `tests/` under the
[MIT license](LICENSE).
