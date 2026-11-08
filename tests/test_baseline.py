"""Verificaciones sintéticas del contrato de Sprint 02."""

from hashlib import sha256
from io import BytesIO
from zipfile import ZipFile

import numpy as np
import pytest
from PIL import Image

from src.baseline import file_sha256, run, verify
from src.data import csv_rows, write_csv
from src.features import extract_hog


def test_baseline_uses_fixed_folds_and_only_opens_development(tmp_path):
    archive = tmp_path / "images.zip"
    manifest = tmp_path / "manifest.csv"
    output = tmp_path / "results"
    records, expected_hog = [], []
    rng = np.random.default_rng(42)
    with ZipFile(archive, "w") as zipped:
        for fold, labels in enumerate(([1, 1, 1, 0], [1, 0, 0], [1, 0, 0]), 1):
            for label in labels:
                name = str(len(records))
                image = rng.integers(0, 256, (32, 40), dtype=np.uint8)
                with BytesIO() as stream:
                    Image.fromarray(image).save(stream, format="PNG")
                    payload = stream.getvalue()
                zipped.writestr(f"{name}.png", payload)
                records.append(dict(id=name, path=f"{name}.png", label=label,
                                    sha256=sha256(payload).hexdigest(),
                                    partition="development", validation_fold=fold))
                expected_hog.append(extract_hog(image))
    # La entrada de test no existe en el ZIP. Cualquier lectura de ella fallaría.
    records.insert(2, dict(id="reserved", path="absent.png", label=1,
                          sha256="f" * 64, partition="test", validation_fold=""))
    write_csv(manifest, list(records[0]), records)
    config = dict(archive=archive, development_manifest=manifest,
                  development_manifest_sha256=file_sha256(manifest), development_rows=10,
                  image_shape=[128, 128], folds=3)
    run(config, output)
    np.testing.assert_array_equal(np.load(output / "hog.npy"), expected_hog)
    predictions = csv_rows(output / "predictions_oof.csv")
    assert [row["id"] for row in predictions] == [str(i) for i in range(10)]
    assert [row["prediction"] for row in predictions] == ["0"] * 4 + ["1"] * 6
    first = csv_rows(output / "baseline_cv.csv")[0]
    assert float(first["accuracy"]) == .25
    assert float(first["specificity"]) == 1
    assert float(first["f1"]) == float(first["recall"]) == float(first["precision"]) == 0
    assert float(first["f1_macro"]) == .2
    verify(config, output)

    with pytest.raises(ValueError, match="SHA-256 del manifiesto"):
        verify(dict(config, development_manifest_sha256="0" * 64), output)
    index = csv_rows(output / "index.csv")
    index[0]["id"] = "reserved"
    write_csv(output / "index.csv", list(index[0]), index)
    with pytest.raises(ValueError, match="índice HOG"):
        verify(config, output)
