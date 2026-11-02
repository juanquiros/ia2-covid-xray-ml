"""Datos sintéticos exclusivamente para verificar software, no desempeño real."""

import csv
import json
from pathlib import Path
from zipfile import ZipFile

import joblib
import numpy as np
import pytest
from PIL import Image

from src.data import load_samples, prepare_archive, read_image
from src.features import extract_hog, preprocess
from src.models import make_random_forest, predict_image
from src.piloto import make_folds, metrics, run_pilot, main


@pytest.fixture
def dataset(tmp_path):
    root = tmp_path / "development"
    rng = np.random.default_rng(15)
    for category in ["COVID", "Normal"]:
        folder = root / category / "images"
        folder.mkdir(parents=True)
        for i in range(6):
            Image.fromarray(rng.integers(0, 256, (32, 40), dtype=np.uint8)).save(folder / f"{i}.png")
        masks = root / category / "masks"
        masks.mkdir()
        (masks / "not_an_image.png").write_text("Must never be read")
    return root


@pytest.mark.parametrize("dtype,value", [(np.uint8, 255), (np.uint16, 65535), (np.float32, 1)])
def test_preprocessing_range_and_dtype(dtype, value):
    result = preprocess(np.full((20, 30), value, dtype=dtype))
    assert result.shape == (128, 128)
    assert result.dtype == np.float32
    np.testing.assert_allclose(result, 1)


def test_rgb_and_hog_contract():
    image = np.random.default_rng(4).integers(0, 256, (64, 70, 3), dtype=np.uint8)
    processed = preprocess(image)
    assert 0 <= processed.min() <= processed.max() <= 1
    vector, drawing = extract_hog(image, visualize=True)
    assert vector.shape == (8100,) and np.isfinite(vector).all()
    assert drawing.shape == (128, 128)
    np.testing.assert_array_equal(vector, extract_hog(image))


@pytest.mark.parametrize("image", [np.zeros((0, 10)), np.ones((3, 3)) * 255,
                                   np.full((3, 3), np.nan), np.zeros((4, 4, 4)),
                                   np.full((3, 3), -1.0)])
def test_invalid_images_rejected(image):
    with pytest.raises(ValueError):
        preprocess(image)


def test_loading_labels_sampling_and_masks(dataset):
    samples, counts = load_samples(dataset, 3)
    assert len(samples) == 6 and counts == {"NORMAL": 6, "COVID": 6}
    assert [s.relative_path for s in samples] == [s.relative_path for s in load_samples(dataset, 3)[0]]
    assert {s.label for s in samples} == {0, 1}
    assert all("images" in s.relative_path and len(s.sha256) == 64 for s in samples)


def test_corrupt_image_fails(dataset):
    (dataset / "COVID/images/0.png").write_text("broken")
    with pytest.raises(ValueError, match="No se pudo leer"):
        load_samples(dataset)


def test_exact_duplicate_fails(dataset):
    (dataset / "COVID/images/1.png").write_bytes((dataset / "COVID/images/0.png").read_bytes())
    with pytest.raises(ValueError, match="Duplicado exacto"):
        load_samples(dataset)


def test_patient_csv_requires_complete_mapping(dataset, tmp_path):
    path = tmp_path / "patients.csv"
    path.write_text("path,patient_id\nCOVID/images/0.png,p0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Falta patient_id"):
        load_samples(dataset, patients_csv=path)


def test_group_folds_keep_patients_together():
    labels = np.repeat([0, 1], 20)
    groups = np.repeat(np.arange(20), 2)
    folds = make_folds(labels, groups)
    assert sorted(np.concatenate([valid for _, valid in folds]).tolist()) == list(range(40))
    for train, valid in folds:
        assert not set(groups[train]) & set(groups[valid])
        assert not set(train) & set(valid)


def test_insufficient_data_fails():
    with pytest.raises(ValueError, match="suficientes imágenes"):
        make_folds([0, 0, 1, 1], n_splits=5)
    with pytest.raises(ValueError, match="suficientes pacientes"):
        make_folds([0] * 6 + [1] * 6, groups=["a"] * 6 + ["b"] * 6)


def test_metrics_known_confusion():
    result = metrics([0, 0, 1, 1], [0, 1, 0, 1])
    assert all(value == .5 for value in result.values())
    assert metrics([0, 1], [0, 0])["precision"] == 0


def test_rf_real_hog_fit_and_predict(dataset):
    samples, _ = load_samples(dataset)
    x = np.stack([extract_hog(read_image(s.path)) for s in samples])
    model = make_random_forest().fit(x, [s.label for s in samples])
    result = predict_image(model, samples[0].path)
    assert result["label"] in [0, 1] and result["category"] in ["COVID", "NORMAL"]


def test_end_to_end_cli_outputs_are_consistent(dataset, tmp_path, capsys):
    output = tmp_path / "run"
    summary = run_pilot(dataset, output, max_per_class=6, n_splits=3)
    assert summary["used"] == {"NORMAL": 6, "COVID": 6}
    assert summary["features"] == 8100
    with (output / "predictions_oof.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 12 and len({r["path"] for r in rows}) == 12
    assert {r["fold"] for r in rows} == {"1", "2", "3"}
    assert all(sum(map(sum, cm)) == 12 for cm in summary["confusion_matrices_oof"].values())
    assert len(list(output.glob("*.png"))) == 3
    assert joblib.load(output / "random_forest.joblib").n_features_in_ == 8100
    main(["predict", "--model", str(output / "random_forest.joblib"),
          "--image", str(dataset / "COVID/images/0.png")])
    assert json.loads(capsys.readouterr().out)["category"] in ["COVID", "NORMAL"]
    with pytest.raises(ValueError, match="salida debe estar vacía"):
        run_pilot(dataset, output)


def test_prepare_archive_only_extracts_pilot(dataset, tmp_path):
    archive = tmp_path / "dataset.zip"
    with ZipFile(archive, "w") as zipped:
        for path in dataset.rglob("*.png"):
            zipped.write(path, "COVID-19_Radiography_Dataset/" + path.relative_to(dataset).as_posix())
        zipped.writestr("COVID-19_Radiography_Dataset/Normal/images/duplicate.png",
                        (dataset / "Normal/images/0.png").read_bytes())
    output = tmp_path / "pilot"
    report = prepare_archive(archive, output, 3)
    assert report["unique_counts"] == {"NORMAL": 6, "COVID": 6}
    assert len(report["exact_duplicates"]) == 1
    assert len(list(output.rglob("*.png"))) == 6
    assert report["test_created_or_evaluated"] is False
    assert not list(output.rglob("masks"))


def test_missing_directory_cli_fails_cleanly(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["train", "--data-dir", str(tmp_path / "absent")])
    assert exc.value.code == 2
    assert "No existe la carpeta" in capsys.readouterr().err
