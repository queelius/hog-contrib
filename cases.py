"""Typed verification cases shared by the gate and every property checker."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Family(Enum):
    CYCLE = "cycle_saturation"
    PATH = "path_saturation"
    CLIQUE = "clique_saturation"
    ORDERED_BIPARTITE = "ordered_bipartite"


@dataclass(frozen=True)
class Case:
    path: Path
    graph6: str
    n: int
    edges: int
    family: Family
    order: int | None = None
    parts: tuple[int, int] | None = None
    forbidden_parts: tuple[int, int] | None = None
    abstract_free: bool | None = None


@dataclass(frozen=True)
class Result:
    ok: bool
    detail: str
