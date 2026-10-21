"""Typed verification cases shared by the gate and every property checker."""

from dataclasses import dataclass
import datetime
from enum import Enum
from pathlib import Path


class Family(Enum):
    CYCLE = "cycle_saturation"
    PATH = "path_saturation"
    CLIQUE = "clique_saturation"
    ORDERED_BIPARTITE = "ordered_bipartite"


class ClaimKind(Enum):
    KNOWN_VALUE = "known_value"
    NEW_VALUE = "new_value"
    NEW_CLASSIFICATION = "new_classification"
    CORRECTION = "correction"
    UNASSESSED = "unassessed"


@dataclass(frozen=True)
class PriorArt:
    source: str
    checked: datetime.date
    finding: str
    locator: str | None = None


@dataclass(frozen=True)
class Claim:
    kind: ClaimKind
    statement: str
    prior_art: tuple[PriorArt, ...] = ()


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
    id: str | None = None
    claim: Claim | None = None


@dataclass(frozen=True)
class Result:
    ok: bool
    detail: str
