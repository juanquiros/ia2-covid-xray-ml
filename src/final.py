"""Registra la selección de desarrollo y ejecuta el lote reservado."""

import argparse
import json
import platform
import subprocess
import warnings
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from time import perf_counter
from zipfile import BadZipFile

import joblib
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import ParameterGrid

from .baseline import file_sha256
from .comparacion import verified_inputs
from .data import csv_rows, write_csv
from .features import extract_manifest_hog
from .models import make_baseline, make_linear_svm, make_random_forest
from .tuning import candidate_grids


BATCH = ("dummy", "random_forest", "linear_svm")
THRESHOLDS = {"random_forest": 0.5, "linear_svm": 0.0}
METRICS = ("accuracy", "precision_covid", "recall_covid", "specificity", "f1_normal",
           "f1_covid", "f1_macro", "roc_auc", "average_precision")
SOURCES = ("src/final.py", "src/tuning.py", "src/features.py", "src/models.py",
           "src/baseline.py", "src/comparacion.py", "src/data.py", "src/evaluation.py",
           "src/analisis_final.py", "requirements.txt")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def versions():
    return {"python": platform.python_version(), **{
        p: version(p) for p in ("numpy", "scikit-learn", "scikit-image", "pillow", "joblib")
    }}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def check_search(tuning, folds):
    summary = read_json(tuning / "tuning.json")
    table = csv_rows(tuning / "tuning_cv.csv")
    best = {}
    pos = 0
    for name, _, grid in candidate_grids():
        expected = list(ParameterGrid(grid))
        best_score = -1.0
        for i, params in enumerate(expected, 1):
            row = table[pos]
            pos += 1
            if row["model"] != name or int(row["configuration"]) != i or json.loads(row["parameters"]) != params:
                raise ValueError("El CSV de búsqueda difiere del orden y parámetros fijados.")
            scores = np.array([float(row[f"fold_{fold}"]) for fold in range(1, folds + 1)])
            mean = float(row["mean_f1_macro"])
            if (not np.all((0 <= scores) & (scores <= 1))
                    or not np.isclose(mean, scores.mean(), atol=1e-14, rtol=0)
                    or not np.isclose(float(row["std_sample_f1_macro"]), scores.std(ddof=1),
                                      atol=1e-14, rtol=0)):
                raise ValueError("Media o desvío de búsqueda incompatible con los folds guardados.")
            if mean > best_score:
                best_score = mean
                best[name] = dict(parameters=params, configuration=i, mean_f1_macro=mean)
    selected = max(best, key=lambda name: best[name]["mean_f1_macro"])
    if pos != len(table) or summary["best"] != best or summary["selected"] != selected:
        raise ValueError("La selección difiere del recálculo de los resultados de búsqueda.")
    return summary


def final_models(best):
    return {
        "dummy": make_baseline(),
        "random_forest": make_random_forest().set_params(**best["random_forest"]["parameters"]),
        "linear_svm": make_linear_svm().set_params(**best["linear_svm"]["parameters"]),
    }


def effective_settings(models):
    svm = models["linear_svm"]
    return {"dummy": models["dummy"].get_params(),
            "random_forest": models["random_forest"].get_params(),
            "linear_svm": {"scaler": svm.named_steps["scaler"].get_params(),
                           "estimator": svm.named_steps["svm"].get_params(),
                           "solver": "liblinear primal"}}


def freeze(config_path, tuning, selection):
    config = read_json(config_path)
    _, baseline, _, labels, _, _ = verified_inputs(config)
    search = check_search(tuning, config["folds"])
    if (search["manifest_sha256"] != baseline["manifest_sha256"]
            or search["development_artifact_sha256"] != baseline["artifact_sha256"]):
        raise ValueError("La búsqueda se hizo con otros artefactos de desarrollo.")
    record = {
        "frozen_at_utc": utc_now(),
        "git_base": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "code_sha256": {path: file_sha256(path) for path in SOURCES},
        "config_sha256": file_sha256(config_path),
        "versions": versions(),
        "manifest_sha256": baseline["manifest_sha256"],
        "development_artifact_sha256": baseline["artifact_sha256"],
        "tuning_cv_sha256": file_sha256(tuning / "tuning_cv.csv"),
        "best": search["best"], "selected": search["selected"],
        "selection_metric": "mean_f1_macro",
        "tie": "linear_svm; first configuration within each grid",
        "batch": BATCH, "settings": effective_settings(final_models(search["best"])),
        "thresholds_strictly_greater_than": THRESHOLDS,
        "covid_scores": {"random_forest": "predict_proba[:, class=1]", "linear_svm": "decision_function"},
        "positive_label": 1, "zero_division": 0, "metrics": METRICS,
        "development_positive_rate": float(labels.mean()),
        "development_rows": config["development_rows"], "test_rows": config["test_rows"],
        "mcnemar": {"comparison": ["linear_svm", "random_forest"], "two_sided_alpha": 0.05,
                    "condition": "independent paired units"},
    }
    selection.parent.mkdir(parents=True, exist_ok=True)
    with selection.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def reserved_rows(config):
    rows = [row for row in csv_rows(config["development_manifest"]) if row["partition"] == "test"]
    if (len(rows) != config["test_rows"] or {row["label"] for row in rows} != {"0", "1"}
            or any(row["validation_fold"] for row in rows)):
        raise ValueError("La partición reservada difiere de lo fijado.")
    return rows


def predict(name, model, features):
    if not np.array_equal(model.classes_, [0, 1]):
        raise ValueError(f"Orden de clases incompatible en {name}.")
    if name == "dummy":
        return model.predict(np.zeros((len(features), 1), dtype=np.uint8)), None
    if name == "random_forest":
        score = model.predict_proba(features)[:, 1]
    else:
        score = model.decision_function(features)
    if not np.isfinite(score).all():
        raise ValueError(f"Scores no finitos en {name}.")
    return (score > THRESHOLDS[name]).astype(int), score


def fit_models(models, features, labels):
    timings = {}
    sample = np.r_[np.flatnonzero(labels == 0)[:4], np.flatnonzero(labels == 1)[:4]]
    for name, model in models.items():
        train = np.zeros((len(labels), 1), dtype=np.uint8) if name == "dummy" else features
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            start = perf_counter()
            model.fit(train, labels)
            elapsed = perf_counter() - start
        predicted, _ = predict(name, model, train[sample])
        if not np.array_equal(predicted, model.predict(train[sample])):
            raise ValueError(f"El umbral fijado difiere de la predicción de {name}.")
        timings[name] = {"fit_seconds": elapsed, "warnings": [
            f"{item.category.__name__}: {item.message}" for item in caught
        ]}
    scaler = models["linear_svm"].named_steps["scaler"]
    if (not np.all(scaler.n_samples_seen_ == len(features))
            or not np.allclose(scaler.mean_, features.mean(axis=0, dtype=np.float64), rtol=0, atol=1e-10)):
        raise ValueError("El escalador final difiere de desarrollo completo.")
    timings["linear_svm"]["n_iter"] = int(models["linear_svm"].named_steps["svm"].n_iter_)
    return timings, sample


def evaluate(config_path, selection, output):
    if output.exists():
        raise ValueError("La salida reservada ya existe. Analizar las predicciones guardadas.")
    config = read_json(config_path)
    selection_hash = file_sha256(selection)
    record = read_json(selection)
    source, baseline, _, labels, _, _ = verified_inputs(config)
    if (record["code_sha256"] != {path: file_sha256(path) for path in SOURCES}
            or record["config_sha256"] != file_sha256(config_path)
            or record["versions"] != versions()
            or record["manifest_sha256"] != baseline["manifest_sha256"]
            or record["development_artifact_sha256"] != baseline["artifact_sha256"]
            or record["batch"] != list(BATCH)
            or record["thresholds_strictly_greater_than"] != THRESHOLDS
            or record["metrics"] != list(METRICS)):
        raise ValueError("La ejecución difiere del registro previo a prueba.")
    rows = reserved_rows(config)
    models = final_models(record["best"])
    if record["settings"] != effective_settings(models):
        raise ValueError("Los parámetros efectivos difieren del registro previo.")
    features = np.load(source / "hog.npy", mmap_mode="r", allow_pickle=False)
    timings, sample = fit_models(models, features, labels)
    output.mkdir(parents=True, exist_ok=False)
    selected = record["selected"]
    model_file = output / "modelo_elegido.joblib"
    joblib.dump(models[selected], model_file, compress=3)
    restored = joblib.load(model_file)
    if not np.array_equal(restored.predict(features[sample]), models[selected].predict(features[sample])):
        raise ValueError("El modelo guardado no reproduce su predicción en desarrollo.")
    if file_sha256(selection) != selection_hash:
        raise ValueError("El registro previo cambió durante el reajuste.")
    # La primera lectura de imágenes reservadas ocurre después del registro y de los reajustes.
    started = utc_now()
    start = perf_counter()
    test = extract_manifest_hog(config["archive"], rows)
    extraction_seconds = perf_counter() - start
    predictions = {}
    for name, model in models.items():
        start = perf_counter()
        predictions[name], scores = predict(name, model, test)
        timings[name]["predict_seconds"] = perf_counter() - start
        if scores is not None:
            predictions[f"{name}_score"] = scores
    table = output / "predicciones_test.csv"
    write_csv(table, ["id", "label", *predictions],
              (dict(id=row["id"], label=row["label"],
                    **{key: values[i].item() for key, values in predictions.items()})
               for i, row in enumerate(rows)))
    receipt = {"test_started_utc": started, "completed_utc": utc_now(),
               "selection_sha256": selection_hash, "prediction_sha256": file_sha256(table),
               "n_test": len(rows), "extraction_seconds": extraction_seconds,
               "timings": timings, "selected": selected,
               "model_sha256": file_sha256(model_file), "model_bytes": model_file.stat().st_size}
    (output / "ejecucion.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    stage = parser.add_mutually_exclusive_group(required=True)
    stage.add_argument("--freeze-from", type=Path, metavar="TUNING_DIR")
    stage.add_argument("--evaluate-to", type=Path, metavar="OUTPUT_DIR")
    args = parser.parse_args()
    try:
        if args.freeze_from:
            freeze(args.config, args.freeze_from, args.selection)
        else:
            evaluate(args.config, args.selection, args.evaluate_to)
    except (ValueError, OSError, KeyError, IndexError, BadZipFile) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
