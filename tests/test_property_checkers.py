"""Each property checker must accept true witnesses and reject near misses.

Every case runs against every checker in hogledger.gate.CHECKERS, so the
primary (pure-Python) and separate (networkx) implementations face one table.
"""

from pathlib import Path
import unittest

import networkx as nx

from hogledger import gate, registry
from hogledger.model import Case, Family, Result

ROOT = Path(__file__).resolve().parent.parent


def g6(graph):
    return nx.to_graph6_bytes(graph, header=False).decode().strip()


def stored(name):
    return (ROOT / "graphs" / name).read_text().strip()


def case(graph6, family, n, edges, **fields):
    return Case(Path("graphs/fixture.g6"), graph6, n, edges, family, **fields)


def without_edge(graph6):
    graph = nx.from_graph6_bytes(graph6.encode())
    graph.remove_edge(*next(iter(graph.edges)))
    return g6(graph)


C6_SAT_7 = stored("sat7_C6_10.g6")
Z10_10 = stored("z10_10_34.g6")
Z9_11 = stored("z9_11_34.g6")
ZARANKIEWICZ = {"family": Family.ORDERED_BIPARTITE, "forbidden_parts": (3, 4)}

ACCEPT = {
    "C6-saturated sat(7,C6)=10": case(C6_SAT_7, Family.CYCLE, 7, 10, order=6),
    "P4-saturated sat(6,P4)=3": case(stored("sat6_P4_3.g6"), Family.PATH, 6, 3, order=4),
    "P5-saturated sat(8,P5)=6": case(stored("sat8_P5_6.g6"), Family.PATH, 8, 6, order=5),
    "K4-saturated sat(8,K4)=13": case(stored("sat8_K4_13.g6"), Family.CLIQUE, 8, 13, order=4),
    "z(10,10) ordered only": case(Z10_10, n=20, edges=66, parts=(10, 10), abstract_free=False, **ZARANKIEWICZ),
    "z(9,11) abstractly free": case(Z9_11, n=20, edges=66, parts=(9, 11), abstract_free=True, **ZARANKIEWICZ),
    "z(9,11) freeness unstated": case(Z9_11, n=20, edges=66, parts=(9, 11), **ZARANKIEWICZ),
}

REJECT = {
    "contains C6": case(g6(nx.cycle_graph(6)), Family.CYCLE, 6, 6, order=6),
    # Complete graphs have no non-edges, so only the freeness check rejects them.
    "contains C6, vacuously saturated": case(g6(nx.complete_graph(6)), Family.CYCLE, 6, 15, order=6),
    # "FbSko" with a nonzero padding bit: same graph, non-canonical bytes.
    "non-canonical graph6": case("FbSkp", Family.CYCLE, 7, 10, order=6),
    # sat(7,C6)=10, so no 9-edge graph on 7 vertices is C6-saturated.
    "C6-free, not saturated": case(without_edge(C6_SAT_7), Family.CYCLE, 7, 9, order=6),
    "wrong edge count": case(C6_SAT_7, Family.CYCLE, 7, 11, order=6),
    "wrong vertex count": case(C6_SAT_7, Family.CYCLE, 8, 10, order=6),
    "contains P4": case(g6(nx.path_graph(4)), Family.PATH, 4, 3, order=4),
    "contains P4, vacuously saturated": case(g6(nx.complete_graph(4)), Family.PATH, 4, 6, order=4),
    "P4-free, not saturated": case(g6(nx.empty_graph(6)), Family.PATH, 6, 0, order=4),
    "contains K4": case(g6(nx.complete_graph(4)), Family.CLIQUE, 4, 6, order=4),
    "K4-free, not saturated": case(g6(nx.empty_graph(5)), Family.CLIQUE, 5, 0, order=4),
    "not bipartite": case(g6(nx.cycle_graph(5)), n=5, edges=5, parts=(2, 3), **ZARANKIEWICZ),
    "3x4 all-ones block": case(g6(nx.complete_bipartite_graph(3, 4)), n=7, edges=12, parts=(3, 4), **ZARANKIEWICZ),
    "wrong part sizes": case(Z9_11, n=20, edges=66, parts=(10, 10), **ZARANKIEWICZ),
    "z(10,10) falsely abstractly free": case(Z10_10, n=20, edges=66, parts=(10, 10), abstract_free=True, **ZARANKIEWICZ),
    "z(9,11) falsely not abstractly free": case(Z9_11, n=20, edges=66, parts=(9, 11), abstract_free=False, **ZARANKIEWICZ),
}


class PropertyCheckerTests(unittest.TestCase):
    def test_gate_has_a_separate_implementation(self):
        self.assertGreaterEqual(len(gate.CHECKERS), 2)

    def test_checkers_accept_true_witnesses(self):
        for checker, check in gate.CHECKERS.items():
            for label, witness in ACCEPT.items():
                with self.subTest(checker=checker, case=label):
                    result = check(witness, witness.graph6)
                    self.assertTrue(result.ok, result.detail)

    def test_checkers_reject_near_misses(self):
        for checker, check in gate.CHECKERS.items():
            for label, witness in REJECT.items():
                with self.subTest(checker=checker, case=label):
                    self.assertFalse(check(witness, witness.graph6).ok)

    def test_crosscheck_rejects_disconnected_bipartite_claims(self):
        graph = nx.disjoint_union(nx.complete_bipartite_graph(2, 2), nx.complete_bipartite_graph(2, 2))
        witness = case(g6(graph), n=8, edges=8, parts=(4, 4), **ZARANKIEWICZ)
        result = gate.CHECKERS["networkx"](witness, witness.graph6)
        self.assertFalse(result.ok)
        self.assertIn("disconnected", result.detail)


class GateCompositionTests(unittest.TestCase):
    def test_every_registered_witness_passes_every_checker(self):
        for witness in registry.load_cases(ROOT):
            result = gate.verify_case(witness, ROOT)
            with self.subTest(witness=witness.path.name):
                self.assertTrue(result.ok, result.detail)
                for checker in gate.CHECKERS:
                    self.assertIn(checker, result.detail)

    def test_one_dissenting_checker_fails_the_gate(self):
        witness = next(c for c in registry.load_cases(ROOT) if c.path.name == "sat7_C6_10.g6")
        dissent = dict(gate.CHECKERS, dissent=lambda case, graph6: Result(False, "disagrees"))
        result = gate.verify_case(witness, ROOT, checkers=dissent)
        self.assertFalse(result.ok)
        self.assertIn("disagrees", result.detail)


if __name__ == "__main__":
    unittest.main()
