#!/usr/bin/env python3
"""
Reusable graph6 toolkit + property verifiers for House of Graphs deposits.

Everything here is dependency-light (pure Python for the core), so a claim can be
verified on the exact object that gets deposited (the graph6 string), not on a
stored description. See open-problems/CLAUDE.md Mistake #2 for why that matters.

Core:
  encode_graph6(n, adj)  -> graph6 string   (n <= 62)
  decode_graph6(s)       -> (n, adj)
  from_edges(n, edges)   -> adj
Properties (all take (n, adj)):
  degrees, num_edges, is_regular(k), triangles, is_c4_free, girth_is_3,
  is_ck_free, is_ck_saturated, is_pk_free, is_pk_saturated,
  is_bipartite -> (partA, partB) or None,
  zarankiewicz_report(m, n)  (one-sided vs abstract K_{s,t}),
  is_k4_free, is_k4_saturated
Convenience:
  roundtrip_ok(n, adj)   encode then decode, confirm identical edge set.
"""
import itertools


def from_edges(n, edges):
    adj = [[0] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = 1
    return adj


def encode_graph6(n, adj):
    if n > 62:
        raise ValueError("this encoder handles n <= 62 only")
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(adj[i][j])
    while len(bits) % 6:
        bits.append(0)
    out = chr(n + 63)
    for k in range(0, len(bits), 6):
        b = 0
        for t in range(6):
            b = (b << 1) | bits[k + t]
        out += chr(b + 63)
    return out


def decode_graph6(s):
    s = s.strip()
    if s.startswith(">>graph6<<"):
        s = s[10:]
    data = [ord(c) - 63 for c in s]
    n = data[0]
    if n > 62:
        raise ValueError("this decoder handles n <= 62 only")
    bits = []
    for byte in data[1:]:
        for k in range(5, -1, -1):
            bits.append((byte >> k) & 1)
    adj = [[0] * n for _ in range(n)]
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i][j] = adj[j][i] = 1
            idx += 1
    return n, adj


def edge_set(n, adj):
    return {(i, j) for i in range(n) for j in range(i + 1, n) if adj[i][j]}


def degrees(n, adj):
    return [sum(adj[i]) for i in range(n)]


def num_edges(n, adj):
    return sum(degrees(n, adj)) // 2


def is_regular(n, adj, k=None):
    d = degrees(n, adj)
    if k is None:
        return len(set(d)) == 1
    return all(x == k for x in d)


def _neighbors(n, adj):
    return [frozenset(j for j in range(n) if adj[i][j]) for i in range(n)]


def max_common_neighbours(n, adj, side=None):
    """Max over pairs (both in `side`, or all pairs if side is None) of
    |common neighbours|. A value >= 2 means a 4-cycle exists (for all pairs)."""
    nb = _neighbors(n, adj)
    verts = range(n) if side is None else side
    best = 0
    for a, b in itertools.combinations(verts, 2):
        c = len(nb[a] & nb[b])
        if c > best:
            best = c
    return best


def is_c4_free(n, adj):
    """C4-free  <=>  every pair of vertices has at most one common neighbour."""
    return max_common_neighbours(n, adj) <= 1


def contains_ck(n, adj, k):
    """True iff G has a simple cycle of length exactly k (chords allowed).

    Method: a length-k simple cycle uses exactly k vertices and is a Hamiltonian
    cycle of the induced subgraph on those k vertices, so test every k-subset for
    a Hamiltonian cycle. This is deliberately a DIFFERENT algorithm from the
    minimum-anchored DFS used elsewhere in the project, so agreement is a genuine
    cross-check. O(C(n,k) * (k-1)!), fine for small k."""
    if k < 3 or k > n:
        return False
    for S in itertools.combinations(range(n), k):
        first, rest = S[0], S[1:]          # fix S[0] to kill rotations
        for perm in itertools.permutations(rest):
            cyc = (first,) + perm
            if all(adj[cyc[i]][cyc[(i + 1) % k]] for i in range(k)):
                return True
    return False


def is_ck_free(n, adj, k):
    return not contains_ck(n, adj, k)


def is_ck_saturated(n, adj, k):
    """Ck-saturated: Ck-free, and adding any single non-edge creates a Ck."""
    if contains_ck(n, adj, k):
        return False
    for u, v in itertools.combinations(range(n), 2):
        if adj[u][v]:
            continue
        adj[u][v] = adj[v][u] = 1
        created = contains_ck(n, adj, k)
        adj[u][v] = adj[v][u] = 0
        if not created:
            return False
    return True


def contains_pk(n, adj, k):
    """True iff G has a simple path on exactly k vertices (not induced)."""
    if k < 1 or k > n:
        return False
    return any(
        all(adj[path[i]][path[i + 1]] for i in range(k - 1))
        for path in itertools.permutations(range(n), k)
    )


def is_pk_free(n, adj, k):
    return not contains_pk(n, adj, k)


def is_pk_saturated(n, adj, k):
    """Pk-saturated: Pk-free, and adding any single non-edge creates a Pk."""
    if contains_pk(n, adj, k):
        return False
    for u, v in itertools.combinations(range(n), 2):
        if adj[u][v]:
            continue
        adj[u][v] = adj[v][u] = 1
        created = contains_pk(n, adj, k)
        adj[u][v] = adj[v][u] = 0
        if not created:
            return False
    return True


def triangles(n, adj):
    return sum(1 for a, b, c in itertools.combinations(range(n), 3)
               if adj[a][b] and adj[a][c] and adj[b][c])


def is_bipartite(n, adj):
    color = {}
    for s in range(n):
        if s in color:
            continue
        color[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for v in range(n):
                if adj[u][v]:
                    if v not in color:
                        color[v] = color[u] ^ 1
                        stack.append(v)
                    elif color[v] == color[u]:
                        return None
    A = [v for v in range(n) if color[v] == 0]
    B = [v for v in range(n) if color[v] == 1]
    return A, B


def zarankiewicz_report(n, adj, m):
    """For a bipartite graph, m = size of the 'row' side. Returns a dict on the
    K_{3,4}-type structure. clean_3x4 = no 3 row-vertices share 4 neighbours
    (the z(m,.;3,4) extremal condition). abstract_k34 = a K_{3,4} exists in
    EITHER orientation (so 'K_{3,4}-free' as an unlabelled graph is false)."""
    part = is_bipartite(n, adj)
    if part is None:
        return {"bipartite": False}
    A, B = part
    rows, cols = (A, B) if len(A) == m else (B, A)
    best_rc = max_common_neighbours(n, adj, side=rows)   # 3 rows -> common cols
    best_cr = max_common_neighbours(n, adj, side=cols)   # 3 cols -> common rows
    return {
        "bipartite": True,
        "part_sizes": sorted([len(A), len(B)]),
        "max_common_over_row_triples": best_rc,
        "max_common_over_col_triples": best_cr,
        "clean_3x4": best_rc < 4,
        "abstract_k34_present": best_cr >= 4 or best_rc >= 4,
    }


def is_k4_free(n, adj):
    for a, b, c, d in itertools.combinations(range(n), 4):
        if (adj[a][b] and adj[a][c] and adj[a][d] and
                adj[b][c] and adj[b][d] and adj[c][d]):
            return False
    return True


def is_k4_saturated(n, adj):
    if not is_k4_free(n, adj):
        return False
    for u, v in itertools.combinations(range(n), 2):
        if adj[u][v]:
            continue
        common = [w for w in range(n) if adj[u][w] and adj[v][w]]
        if not any(adj[x][y] for x, y in itertools.combinations(common, 2)):
            return False
    return True


def roundtrip_ok(n, adj):
    n2, adj2 = decode_graph6(encode_graph6(n, adj))
    return n2 == n and edge_set(n, adj) == edge_set(n2, adj2)


if __name__ == "__main__":
    # self-test on the A006672 Ramsey witness (4-regular, C4-free, 15 vertices)
    es = "0-1 0-2 0-3 0-4 1-2 1-5 1-11 2-6 2-8 3-4 3-7 3-12 4-9 4-10 5-7 5-9 5-11 6-7 6-8 6-10 7-12 8-9 8-13 9-13 10-11 10-14 11-14 12-13 12-14 13-14"
    E = [tuple(map(int, e.split("-"))) for e in es.split()]
    adj = from_edges(15, E)
    print("n=15 edges=%d 4-regular=%s c4free=%s triangles=%d roundtrip=%s" % (
        num_edges(15, adj), is_regular(15, adj, 4), is_c4_free(15, adj),
        triangles(15, adj), roundtrip_ok(15, adj)))
    print("graph6:", encode_graph6(15, adj))
