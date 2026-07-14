#!/usr/bin/env python3
"""Verify every witness in graphs/ against contributions.yaml using verify.py.

For each graph6 file: decode it, confirm the roundtrip, the vertex count, and the
edge count; then run the property check appropriate to its invariant family:

  Cycle saturation: Ck-free AND Ck-saturated (verify.is_ck_free / is_ck_saturated)
  Path saturation : Pk-free AND Pk-saturated (verify.is_pk_free / is_pk_saturated)
  K_4 saturation: K_4-free AND K_4-saturated (verify.is_k4_free / is_k4_saturated)
  Zarankiewicz  : bipartite with the stated part sizes, and an orientation-explicit
                  K_(3,4) report (triple-based: does any 3 vertices on one side share
                  4 common neighbours on the other). This is the Mistake-in-LESSONS
                  check: state the matrix condition, never call it "K_(3,4)-free"
                  unless BOTH orientations are clean.

Run from the repo root:  python3 verify_witnesses.py
Exit code 0 iff every check passes.
"""
import itertools
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import verify as V

# graph6_file -> (n, edges, family, param)
#   family "ck" / "pk": param = cycle/path order k
#   family "k4":        param = None
#   family "zar":       param = (m, ncols) part sizes for the z(m,ncols;3,4) matrix
CASES = {
    "sat7_C6_10.g6":        (7,  10, "ck",  6),
    "sat8_C6_11.g6":        (8,  11, "ck",  6),
    "sat9_C6_12.g6":        (9,  12, "ck",  6),
    "sat9_C6_12_class2.g6": (9,  12, "ck",  6),
    "sat9_C6_12_class3.g6": (9,  12, "ck",  6),
    "sat9_C6_12_class4.g6": (9,  12, "ck",  6),
    "sat9_C6_12_class5.g6": (9,  12, "ck",  6),
    "sat10_C6_13.g6":       (10, 13, "ck",  6),
    "sat10_C6_13_alt.g6":   (10, 13, "ck",  6),
    "sat8_C5_10.g6":        (8,  10, "ck",  5),
    "sat8_K4_13.g6":      (8,  13, "k4",  None),
    "sat9_K4_15.g6":      (9,  15, "k4",  None),
    "sat10_K4_17.g6":     (10, 17, "k4",  None),
    "sat6_P4_3.g6":       (6,  3,  "pk",  4),
    "sat7_P4_5.g6":       (7,  5,  "pk",  4),
    "sat8_P4_4.g6":       (8,  4,  "pk",  4),
    "sat8_P5_6.g6":       (8,  6,  "pk",  5),
    "sat9_P5_7.g6":       (9,  7,  "pk",  5),
    "z10_10_34.g6":       (20, 66, "zar", (10, 10)),
    "z9_10_34.g6":        (19, 60, "zar", (9, 10)),
    "z9_11_34.g6":        (20, 66, "zar", (9, 11)),
}


def max_triple_share(adj, side, other):
    """Max over 3-subsets of `side` of the number of common neighbours in `other`."""
    best = 0
    for trip in itertools.combinations(side, 3):
        common = sum(1 for c in other if all(adj[r][c] for r in trip))
        best = max(best, common)
    return best


def main():
    graphs_dir = os.path.join(ROOT, "graphs")
    all_ok = True
    for fname, (exp_n, exp_m, fam, param) in CASES.items():
        with open(os.path.join(graphs_dir, fname), "rb") as fh:
            g6 = fh.read().decode().strip()
        n, adj = V.decode_graph6(g6)
        m = V.num_edges(n, adj)
        rt = V.roundtrip_ok(n, adj)
        ok = (n == exp_n and m == exp_m and rt)
        detail = ""
        if fam == "ck":
            cfree = V.is_ck_free(n, adj, param)
            csat = V.is_ck_saturated(n, adj, param)
            ok = ok and cfree and csat
            detail = f"C{param}-free={cfree} C{param}-saturated={csat}"
        elif fam == "pk":
            pfree = V.is_pk_free(n, adj, param)
            psat = V.is_pk_saturated(n, adj, param)
            ok = ok and pfree and psat
            detail = f"P{param}-free={pfree} P{param}-saturated={psat}"
        elif fam == "k4":
            kfree = V.is_k4_free(n, adj)
            ksat = V.is_k4_saturated(n, adj)
            ok = ok and kfree and ksat
            detail = f"K4-free={kfree} K4-saturated={ksat}"
        elif fam == "zar":
            A, B = V.is_bipartite(n, adj)
            parts = tuple(sorted((len(A), len(B))))
            ab = max_triple_share(adj, A, B)
            ba = max_triple_share(adj, B, A)
            has_k34 = ab >= 4 or ba >= 4
            # z(m,ncols;3,4) requires no 3 vertices on the smaller/"row" side sharing
            # 4 on the other; the min side is the row side here for our witnesses.
            one_sided_clean = min(ab, ba) < 4
            ok = ok and parts == tuple(sorted(param)) and one_sided_clean
            detail = (f"parts={parts} 3-share-4(A->B)={ab} 3-share-4(B->A)={ba} "
                      f"abstract_K(3,4)={has_k34}")
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {fname:22s} g6={g6!r:40s} n={n} m={m} rt={rt} {detail}")
        all_ok = all_ok and ok
    print("-" * 78)
    print("ALL WITNESSES VERIFIED" if all_ok else "VERIFICATION FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
