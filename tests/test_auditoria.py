"""Controles estructurales sintéticos de Sprint 01."""

from collections import Counter
from io import BytesIO
from zipfile import ZipFile

import numpy as np
from PIL import Image

from src.auditoria import Record, audit_archive, make_partition


def png(value):
    with BytesIO() as stream:
        Image.fromarray(np.full((5, 5), value, dtype=np.uint8)).save(stream, format="PNG")
        return stream.getvalue()


def test_audit_exclusions_and_group_inheritance(tmp_path):
    path = tmp_path / "archive.zip"
    prefix = "source/COVID/images/"
    with ZipFile(path, "w") as zipped:
        for name, content in [("a.png", png(1)), ("b.png", png(1)),
                              ("conflict.png", png(2)), ("bad.png", b"not a png")]:
            zipped.writestr(prefix + name, content)
        zipped.writestr("source/Normal/images/conflict.png", png(2))
        zipped.writestr("source/Normal/masks/excluded.png", b"outside scope")

    with ZipFile(path) as zipped:
        records = audit_archive(zipped, "source@1", {(prefix + "a.png").casefold(): "example.org"},
                                {prefix + "b.png": "verified-patient"})

    assert Counter(row.status for row in records) == {
        "retained": 1, "exact_duplicate": 1, "label_conflict": 2, "unreadable": 1
    }
    first, duplicate = records[:2]
    assert first.origin == "example.org"
    assert first.patient_id == "verified-patient"
    assert duplicate.retained_id == first.id
    assert first.sha256 == duplicate.sha256
    assert all(row.sha256 for row in records)


def test_partition_excludes_pilot_hash_and_group_and_preserves_group_folds():
    rows = []
    for label in (0, 1):
        for i in range(80):
            key = f"{label}-{i}"
            group = f"{label}-{i // 2}" if i < 70 else ""
            rows.append(Record(key, key, label, "source", "", sha256=key, patient_id=group))
    settings = dict(seed=42, fraction=.2, folds=5)
    pilot_hashes, pilot_groups = {"0-0", "1-79"}, {"1-3"}
    development, test, assigned = make_partition(rows, pilot_hashes, pilot_groups, **settings)
    assert (development, test, assigned) == make_partition(rows, pilot_hashes, pilot_groups, **settings)
    assert {row.sha256 for row in test}.isdisjoint({"0-0", "0-1", "1-6", "1-7", "1-79"})
    assert abs(len(test) / len(rows) - .2) <= .02
    assert len(development) == len(assigned) == len(rows) - len(test)
    assert set(assigned.values()) == set(range(1, 6))
    grouped = {}
    for row in development:
        if row.patient_id:
            assert grouped.setdefault(row.patient_id, assigned[row.id]) == assigned[row.id]
