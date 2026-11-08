"""Controles tabulares de la entrega, sin ajuste de modelos."""

import json

import numpy as np
import pytest

from src.analisis_final import score_test
from src.baseline import file_sha256
from src.reproducir_entrega import arrays, read_evidence


def test_metrics_are_recomputed_from_tabular_predictions():
    rows = [
        dict(sample="T1", label="0", dummy="0", random_forest="0", linear_svm="0"),
        dict(sample="T2", label="0", dummy="0", random_forest="0", linear_svm="1"),
        dict(sample="T3", label="1", dummy="0", random_forest="1", linear_svm="1"),
        dict(sample="T4", label="1", dummy="0", random_forest="1", linear_svm="1"),
    ]
    y, predictions = arrays(rows)
    scores = {"random_forest": np.array([.1, .3, .7, .9]), "linear_svm": np.array([-.5, .2, .6, .8])}
    dummy, forest, svm = score_test(y, predictions, scores)
    assert dummy["recall_covid"] == 0 and dummy["roc_auc"] == ""
    assert forest["accuracy"] == forest["roc_auc"] == 1
    assert svm["fp"] == 1 and svm["recall_covid"] == 1 and svm["specificity"] == .5
    with pytest.raises(ValueError, match="repetidas"):
        arrays(rows + rows[:1])


def test_evidence_integrity_fails_before_loading_predictions(tmp_path):
    names = ("prueba.csv", "desarrollo_oof.csv", "eda.json", "pesos_hog.csv")
    for name in names:
        (tmp_path / name).write_text("sample,label\nT1,0\n", encoding="utf-8")
    hashes = {name: file_sha256(tmp_path / name) for name in names}
    (tmp_path / "sha256.json").write_text(json.dumps(hashes), encoding="utf-8")
    test, dev = read_evidence(tmp_path)
    assert test == dev == [{"sample": "T1", "label": "0"}]
    (tmp_path / "prueba.csv").write_text("alterado", encoding="utf-8")
    with pytest.raises(ValueError, match="SHA-256 incorrecto"):
        read_evidence(tmp_path)
