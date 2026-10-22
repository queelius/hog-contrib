"""The verification gate: every registered witness must pass every checker."""

from pathlib import Path

from . import crosscheck, primary
from .model import Case, Result

# Every checker must pass. crosscheck shares no code with primary.
CHECKERS = {"pure-python": primary.check, "networkx": crosscheck.check}


def verify_case(case: Case, root: Path, checkers=CHECKERS) -> Result:
    """Verify the exact file mirrors the registry, then require every checker to pass."""
    try:
        graph6 = (Path(root) / case.path).read_text().strip()
    except (OSError, UnicodeError) as error:
        return Result(False, str(error))
    if graph6 != case.graph6:
        return Result(False, "graph6 file differs from registry")
    results = {name: check(case, graph6) for name, check in checkers.items()}
    detail = "; ".join(f"{name}: {result.detail}" for name, result in results.items())
    return Result(all(result.ok for result in results.values()), detail)
