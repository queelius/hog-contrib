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


class Status(Enum):
    DEPOSITED = "deposited"
    READY = "ready"
    CANDIDATE = "candidate"


@dataclass(frozen=True)
class Record:
    """A registry record: its verification case plus what readers are told."""
    case: Case
    invariant: str
    status: Status
    certificates: str
    hog_id: int | None = None
    zenodo: str | None = None
    non_iso_minima: int | None = None
    notes: str = ""


@dataclass(frozen=True)
class Author:
    given_names: str
    family_names: str
    handle: str
    email: str
    orcid: str


@dataclass(frozen=True)
class Paper:
    key: str
    title: str
    doi: str


@dataclass(frozen=True)
class Ledger:
    title: str
    repository: str
    abstract: str
    keywords: tuple[str, ...]
    author: Author
    house_of_graphs: str
    papers: tuple[Paper, ...]
    records: tuple[Record, ...]
