"""Load receipts/: dated JSON records of external actions, tied to ledger records.

A receipt is named YYYY-MM-DD-<slug>.json. Schema version 2 is the current
format; every other file in receipts/ must be an attachment a receipt names.

    {"schema_version": 2, "date": "YYYY-MM-DD", "action": "submit|annotate|publish",
     "records": [record ids], "summary": "...", "attachments": [file names],
     "details": {...free-form evidence...}}

Legacy receipts (schema_version "1.0") predate this format and are kept byte
for byte. Their records derive from graphs[].hog_id and their attachments
from graphs[].annotation_file.
"""

import datetime
import json
from pathlib import Path

from .model import Receipt, ReceiptAction, Record

DIRECTORY = Path("receipts")
LEGACY = "1.0"
CURRENT = 2


def _date(text: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(text)
    except (TypeError, ValueError):
        raise ValueError(f"not a YYYY-MM-DD date: {text!r}") from None


def _current(body, path, date, known):
    if body.get("date") != date.isoformat():
        raise ValueError(f"{path.name}: date {body.get('date')!r} differs from the file name")
    records = body.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{path.name}: records must be a nonempty list of record ids")
    unknown = sorted(set(records) - known)
    if unknown:
        raise ValueError(f"{path.name}: unknown records {unknown}")
    summary = body.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError(f"{path.name}: summary must be nonempty text")
    return (ReceiptAction(body.get("action")), tuple(records), summary,
            tuple(body.get("attachments", [])))


def _legacy(body, path, by_hog_id):
    graphs = body.get("graphs", [])
    unknown = sorted(g["hog_id"] for g in graphs if g["hog_id"] not in by_hog_id)
    if unknown:
        raise ValueError(f"{path.name}: HoG ids {unknown} match no record")
    records = tuple(dict.fromkeys(by_hog_id[g["hog_id"]] for g in graphs))
    attachments = tuple(g["annotation_file"] for g in graphs if g.get("annotation_file"))
    return None, records, None, attachments


def load(root: Path, records: tuple[Record, ...]) -> tuple[Receipt, ...]:
    """Every receipt under root/receipts, validated against the records."""
    directory = Path(root) / DIRECTORY
    if not directory.is_dir():
        return ()
    known = {record.case.id for record in records}
    by_hog_id = {record.hog_id: record.case.id for record in records if record.hog_id is not None}
    receipts, attached = [], set()
    for path in sorted(directory.glob("*.json")):
        date = _date(path.name[:10])
        body = json.loads(path.read_text())
        version = body.get("schema_version")
        if version == CURRENT:
            action, ids, summary, names = _current(body, path, date, known)
        elif version == LEGACY:
            action, ids, summary, names = _legacy(body, path, by_hog_id)
        else:
            raise ValueError(f"{path.name}: unsupported schema_version {version!r}")
        missing = [name for name in names if not (directory / name).is_file()]
        if missing:
            raise ValueError(f"{path.name}: missing attachments {missing}")
        attached.update(names)
        receipts.append(Receipt(path.relative_to(root), date, action, ids, summary,
                                tuple(DIRECTORY / name for name in names)))
    stray = sorted(p.name for p in directory.iterdir() if p.suffix != ".json" and p.name not in attached)
    if stray:
        raise ValueError(f"files in receipts/ that no receipt attaches: {stray}")
    return tuple(receipts)
