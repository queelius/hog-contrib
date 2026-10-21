"""A separate implementation of every family's defining property.

This module shares no code with verify.py, which was copied from the research
repository. It decodes and re-encodes graph6 with networkx and uses different
algorithms: bounded simple-path search instead of permutation enumeration,
maximal-clique enumeration instead of fixed-size subsets, and neighbourhood
set intersection for ordered bipartite conditions. The gate requires both
implementations to agree before a witness counts as independently checked.
"""

import itertools

import networkx as nx

from cases import Case, Family, Result


def _has_path_with_edges(graph, u, v, length):
    """A u-v simple path with exactly `length` edges exists in `graph`."""
    return any(len(path) == length + 1 for path in nx.all_simple_paths(graph, u, v, cutoff=length))


def _contains_cycle(graph, k):
    # A simple cycle through edge uv is that edge plus a u-v path of k-1 >= 2
    # edges, and such a path never reuses the edge uv itself.
    return any(_has_path_with_edges(graph, u, v, k - 1) for u, v in graph.edges)


def _cycle_saturated(graph, k):
    if _contains_cycle(graph, k):
        return False
    return all(_has_path_with_edges(graph, u, v, k - 1) for u, v in nx.non_edges(graph))


def _contains_path(graph, k):
    """A simple path on exactly k vertices exists."""
    if k == 1:
        return graph.number_of_nodes() > 0
    return any(_has_path_with_edges(graph, u, v, k - 1) for u, v in itertools.combinations(graph, 2))


def _path_saturated(graph, k):
    if _contains_path(graph, k):
        return False
    for u, v in nx.non_edges(graph):
        graph.add_edge(u, v)
        created = _contains_path(graph, k)
        graph.remove_edge(u, v)
        if not created:
            return False
    return True


def _clique_number(graph):
    return max((len(clique) for clique in nx.find_cliques(graph)), default=0)


def _clique_saturated(graph, r):
    # Adding uv creates a K_r exactly when the common neighbourhood of u and v
    # contains a K_(r-2).
    if _clique_number(graph) >= r:
        return False
    return all(
        _clique_number(graph.subgraph(set(graph[u]) & set(graph[v]))) >= r - 2
        for u, v in nx.non_edges(graph)
    )


def _max_shared(graph, side, size):
    """Largest common neighbourhood over all `size`-subsets of `side`."""
    return max(
        (len(set.intersection(*(set(graph[x]) for x in subset)))
         for subset in itertools.combinations(side, size)),
        default=0,
    )


def _ordered_bipartite(graph, case):
    if not nx.is_bipartite(graph):
        return False, "not bipartite"
    if not nx.is_connected(graph):
        return False, "disconnected: the bipartition is ambiguous"
    left, right = nx.bipartite.sets(graph)
    s, t = case.forbidden_parts
    # A list, not a dict keyed by part sizes: equal parts must keep both orientations.
    orientations = [((len(rows), len(cols)), _max_shared(graph, rows, s))
                    for rows, cols in ((left, right), (right, left))]
    clean = any(sizes == case.parts and shared < t for sizes, shared in orientations)
    abstract_free = all(shared < t for _, shared in orientations)
    ok = clean and case.abstract_free in (None, abstract_free)
    return ok, f"ordered-clean={clean} abstract-free={abstract_free}"


def check(case: Case, graph6: str) -> Result:
    """Check counts, canonical encoding, and the defining property with networkx."""
    try:
        data = graph6.encode("ascii")
        graph = nx.from_graph6_bytes(data)
        n, m = graph.number_of_nodes(), graph.number_of_edges()
        if (n, m) != (case.n, case.edges):
            return Result(False, f"count mismatch: n={n} m={m}")
        if nx.to_graph6_bytes(graph, header=False).strip() != data:
            return Result(False, "graph6 is not the canonical encoding of its graph")
        if case.family is Family.CYCLE:
            ok = _cycle_saturated(graph, case.order)
            detail = f"C{case.order}-saturated={ok}"
        elif case.family is Family.PATH:
            ok = _path_saturated(graph, case.order)
            detail = f"P{case.order}-saturated={ok}"
        elif case.family is Family.CLIQUE:
            ok = _clique_saturated(graph, case.order)
            detail = f"K{case.order}-saturated={ok}"
        else:
            ok, detail = _ordered_bipartite(graph, case)
        return Result(ok, detail)
    except (ValueError, UnicodeError, nx.NetworkXError) as error:
        return Result(False, str(error))
