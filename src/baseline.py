"""Extrae HOG y evalúa Dummy en los folds ya fijados de desarrollo."""

import argparse
import json
import platform
from hashlib import file_digest
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from zipfile import BadZipFile

import numpy as np

from .data import csv_rows, write_csv
from .evaluation import score_oof
from .features import HOG_CONFIG, IMAGE_SHAPE, N_FEATURES, extract_manifest_hog
from .models import make_baseline


def file_sha256(path):
    with Path(path).open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def development_inputs(config):
    manifest = Path(config["development_manifest"])
    if file_sha256(manifest) != config["development_manifest_sha256"]:
        raise ValueError("El SHA-256 del manifiesto difiere del cierre de Sprint 01.")
    if tuple(config["image_shape"]) != IMAGE_SHAPE:
        raise ValueError("La configuración de entrada difiere del contrato de HOG.")
    rows = csv_rows(manifest)
    for key in ("id", "path", "sha256"):
        values = {row[key] for row in rows}
        if "" in values or len(values) != len(rows):
            raise ValueError(f"{key} vacío o repetido en el manifiesto.")
    if {row["partition"] for row in rows} != {"development", "test"}:
        raise ValueError("El manifiesto debe contener desarrollo y test.")
    development = [row for row in rows if row["partition"] == "development"]
    index = [{"row": str(i), "id": row["id"], "label": row["label"],
              "validation_fold": row["validation_fold"]} for i, row in enumerate(development)]
    if len(index) != config["development_rows"]:
        raise ValueError("La cantidad de imágenes difiere del cierre de Sprint 01.")
    if {row["label"] for row in index} != {"0", "1"}:
        raise ValueError("Desarrollo debe contener las dos clases.")
    labels = np.array([int(row["label"]) for row in index])
    folds = np.array([int(row["validation_fold"]) for row in index])
    if set(folds) != set(range(1, config["folds"] + 1)):
        raise ValueError("Los folds de desarrollo difieren de la configuración.")
    for fold in range(1, config["folds"] + 1):
        if set(labels[folds == fold]) != {0, 1} or set(labels[folds != fold]) != {0, 1}:
            raise ValueError(f"Falta alguna clase en entrenamiento o validación del fold {fold}.")
    return development, index, labels, folds


def predict_oof(labels, folds):
    predictions = np.empty_like(labels)
    # Dummy necesita el número de filas, pero su predicción depende solo de y_train.
    placeholders = np.zeros((len(labels), 1), dtype=np.uint8)
    for fold in np.unique(folds):
        valid = folds == fold
        model = make_baseline().fit(placeholders[~valid], labels[~valid])
        predictions[valid] = model.predict(placeholders[valid])
    return predictions


def verify(config, output):
    _, index, labels, folds = development_inputs(config)
    if csv_rows(output / "index.csv") != index:
        raise ValueError("El índice HOG no coincide con las filas de desarrollo del manifiesto.")
    matrix = np.load(output / "hog.npy", mmap_mode="r", allow_pickle=False)
    if matrix.shape != (len(index), N_FEATURES) or matrix.dtype != np.float32 or not np.isfinite(matrix).all():
        raise ValueError("La matriz HOG tiene forma, tipo o valores inválidos.")
    del matrix
    predictions = csv_rows(output / "predictions_oof.csv")
    saved_index = [{key: row[key] for key in index[0]} for row in predictions]
    if saved_index != index or {row["prediction"] for row in predictions} - {"0", "1"}:
        raise ValueError("Las predicciones OOF no coinciden con el índice de desarrollo.")
    pred = np.array([int(row["prediction"]) for row in predictions])
    records, summary = score_oof(labels, folds, pred)
    if csv_rows(output / "baseline_cv.csv") != [{k: str(v) for k, v in row.items()} for row in records]:
        raise ValueError("Las métricas por fold difieren del recálculo desde OOF.")
    saved = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    if saved["metrics"] != summary or saved["manifest_sha256"] != config["development_manifest_sha256"]:
        raise ValueError("El resumen difiere del recálculo o del manifiesto.")
    for name, expected_hash in saved["artifact_sha256"].items():
        if file_sha256(output / name) != expected_hash:
            raise ValueError(f"El SHA-256 de {name} difiere del resumen.")
    return saved


def run(config, output):
    if output.exists():
        raise ValueError("La carpeta de salida ya existe. Elegir otra ruta para preservar la ejecución.")
    development, index, labels, folds = development_inputs(config)
    start = perf_counter()
    matrix = extract_manifest_hog(config["archive"], development)
    elapsed = perf_counter() - start
    predictions = predict_oof(labels, folds)
    records, summary = score_oof(labels, folds, predictions)
    metadata = {
        "manifest_sha256": config["development_manifest_sha256"],
        "shape": list(matrix.shape), "dtype": str(matrix.dtype), "image_shape": IMAGE_SHAPE,
        "hog": HOG_CONFIG, "extraction_seconds": elapsed,
        "strategy": "most_frequent", "positive_label": 1, "zero_division": 0,
        "prediction_counts": np.bincount(predictions, minlength=2).tolist(),
        "metrics": summary, "python": platform.python_version(),
        "versions": {p: version(p) for p in ("numpy", "scikit-image", "scikit-learn", "pillow")},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as temp:
        stage = Path(temp) / "stage"
        stage.mkdir()
        np.save(stage / "hog.npy", matrix, allow_pickle=False)
        del matrix
        write_csv(stage / "index.csv", list(index[0]), index)
        write_csv(stage / "predictions_oof.csv", [*index[0], "prediction"],
                  (dict(row, prediction=int(pred)) for row, pred in zip(index, predictions, strict=True)))
        write_csv(stage / "baseline_cv.csv", list(records[0]), records)
        metadata["artifact_sha256"] = {name: file_sha256(stage / name) for name in
                                      ("hog.npy", "index.csv", "predictions_oof.csv", "baseline_cv.csv")}
        (stage / "summary.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")
        verify(config, stage)
        stage.rename(output.resolve())
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true", help="Verifica artefactos sin abrir el ZIP.")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8-sig"))
        result = (verify if args.verify_only else run)(config, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, BadZipFile) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
