"""The primary property checker: a pure-Python graph6 codec and brute force.

The codec and the cycle, path and K4 checks were copied from the research
repository's hog/hog_verify.py. They decode the exact deposited graph6 string
(n <= 62) rather than a stored description. crosscheck.py is the separate
implementation the gate requires to agree.
"""

import itertools

from .model import Case, Family, Result


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


def num_edges(n, adj):
    return len(edge_set(n, adj))


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


def max_common_neighbours(adj, side, other, subset_size):
    """Maximum common neighbours of a fixed-size subset of one part."""
    return max(
        (sum(all(adj[u][v] for u in subset) for v in other)
         for subset in itertools.combinations(side, subset_size)),
        default=0,
    )


def check(case: Case, graph6: str) -> Result:
    """Check counts, round trip, and the defining property."""
    try:
        n, adj = decode_graph6(graph6)
        m = num_edges(n, adj)
        if (n, m) != (case.n, case.edges) or encode_graph6(n, adj) != graph6 or not roundtrip_ok(n, adj):
            return Result(False, f"count or roundtrip mismatch: n={n} m={m}")
        if case.family is Family.CYCLE:
            ok = is_ck_free(n, adj, case.order) and is_ck_saturated(n, adj, case.order)
            detail = f"C{case.order}-saturated={ok}"
        elif case.family is Family.PATH:
            ok = is_pk_free(n, adj, case.order) and is_pk_saturated(n, adj, case.order)
            detail = f"P{case.order}-saturated={ok}"
        elif case.family is Family.CLIQUE:
            ok = is_k4_free(n, adj) and is_k4_saturated(n, adj)
            detail = f"K4-saturated={ok}"
        else:
            partition = is_bipartite(n, adj)
            if partition is None:
                return Result(False, "graph is not bipartite")
            a, b = partition
            s, t = case.forbidden_parts
            ab = max_common_neighbours(adj, a, b, s)
            ba = max_common_neighbours(adj, b, a, s)
            orientations = [(a, b, ab), (b, a, ba)]
            clean = any((len(rows), len(cols)) == case.parts and common < t
                        for rows, cols, common in orientations)
            abstract_free = ab < t and ba < t
            ok = clean and (case.abstract_free is None or case.abstract_free == abstract_free)
            detail = f"parts=({len(a)},{len(b)}) ordered-clean={clean} abstract-free={abstract_free}"
        return Result(ok, f"n={n} m={m} roundtrip=True {detail}")
    except (ValueError, IndexError) as error:
        return Result(False, str(error))
