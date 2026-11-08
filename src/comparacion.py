"""Compara las configuraciones iniciales en los folds de desarrollo."""

import argparse
import json
import platform
import warnings
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

import numpy as np
from sklearn.exceptions import ConvergenceWarning

from .baseline import development_inputs, verify as verify_baseline
from .data import csv_rows, write_csv
from .evaluation import score_oof
from .models import make_baseline, make_linear_svm, make_random_forest


MODEL_NAMES = ("dummy", "random_forest", "linear_svm")


def fit_oof(features, labels, folds, factory, *, check_scaler=False, progress=None):
    predictions = np.full(len(labels), -1, dtype=int)
    diagnostics = []
    for fold in np.unique(folds):
        valid = folds == fold
        x_train, x_valid = features[~valid], features[valid]
        model = factory()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            start = perf_counter()
            model.fit(x_train, labels[~valid])
            fit_seconds = perf_counter() - start
        start = perf_counter()
        predictions[valid] = model.predict(x_valid)
        predict_seconds = perf_counter() - start
        record = dict(fold=int(fold), n_train=len(x_train), fit_seconds=fit_seconds,
                      predict_seconds=predict_seconds,
                      warnings=[f"{item.category.__name__}: {item.message}" for item in caught])
        if check_scaler:
            scaler = model.named_steps["scaler"]
            expected_mean = x_train.mean(axis=0, dtype=np.float64)
            if (not np.all(scaler.n_samples_seen_ == len(x_train))
                    or not np.allclose(scaler.mean_, expected_mean, rtol=0, atol=1e-10)):
                raise ValueError(f"Scaler incompatible con las filas de entrenamiento del fold {fold}.")
            record.update(scaler_train_only=True, n_iter=int(model.named_steps["svm"].n_iter_))
        diagnostics.append(record)
        if progress:
            progress(record)
    if not np.isin(predictions, (0, 1)).all():
        raise ValueError("La predicción OOF no cubre exactamente las etiquetas binarias.")
    return predictions, diagnostics


def comparison_scores(labels, folds, predictions, diagnostics):
    records, summaries = [], {}
    for name in MODEL_NAMES:
        per_fold, summary = score_oof(labels, folds, predictions[name])
        for metrics, details in zip(per_fold, diagnostics[name], strict=True):
            if metrics["fold"] != details["fold"]:
                raise ValueError(f"El diagnóstico de {name} no coincide con su fold.")
            records.append(dict(model=name, **metrics, n_train=details["n_train"],
                                fit_seconds=details["fit_seconds"],
                                predict_seconds=details["predict_seconds"]))
        for key in ("fit_seconds", "predict_seconds"):
            values = [row[key] for row in diagnostics[name]]
            summary[key] = {"mean": float(np.mean(values)), "std": float(np.std(values, ddof=1))}
        summaries[name] = summary
    return records, summaries


def verified_inputs(config):
    source = Path(config["sprint_02_artifacts"])
    baseline = verify_baseline(config, source)
    _, index, labels, folds = development_inputs(config)
    dummy = np.array([int(row["prediction"]) for row in csv_rows(source / "predictions_oof.csv")])
    return source, baseline, index, labels, folds, dummy


def verify_output(output, baseline, index, labels, folds, dummy):
    rows = csv_rows(output / "predictions_oof.csv")
    saved_index = [{key: row[key] for key in index[0]} for row in rows]
    if saved_index != index or any(row[name] not in {"0", "1"} for row in rows for name in MODEL_NAMES):
        raise ValueError("Las predicciones no cubren exactamente el índice de desarrollo.")
    predictions = {name: np.array([int(row[name]) for row in rows]) for name in MODEL_NAMES}
    if not np.array_equal(predictions["dummy"], dummy):
        raise ValueError("Las predicciones de Dummy difieren del Sprint 02.")
    metadata = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    if (metadata["baseline_artifact_sha256"] != baseline["artifact_sha256"]
            or metadata["manifest_sha256"] != baseline["manifest_sha256"]):
        raise ValueError("Los artefactos de entrada difieren de los de la ejecución.")
    records, summaries = comparison_scores(labels, folds, predictions, metadata["diagnostics"])
    if (csv_rows(output / "modelos_cv.csv") != [{k: str(v) for k, v in row.items()} for row in records]
            or metadata["metrics"] != summaries):
        raise ValueError("Las métricas guardadas difieren del recálculo desde OOF.")
    return metadata


def run(config, output):
    if output.exists():
        raise ValueError("La carpeta de salida ya existe. Elegir otra para preservar la ejecución.")
    source, baseline, index, labels, folds, dummy = verified_inputs(config)
    features = np.load(source / "hog.npy", mmap_mode="r", allow_pickle=False)
    svm = make_linear_svm()
    settings = {
        "dummy": make_baseline().get_params(),
        "random_forest": make_random_forest().get_params(),
        "linear_svm": {"scaler": svm.named_steps["scaler"].get_params(),
                       "estimator": svm.named_steps["svm"].get_params(),
                       "solver": "liblinear primal"},
    }
    predictions, diagnostics = {}, {}
    for name, x, factory in (
            ("dummy", np.zeros((len(index), 1), dtype=np.uint8), make_baseline),
            ("random_forest", features, make_random_forest),
            ("linear_svm", features, make_linear_svm)):
        def progress(record):
            print(f"{name}, fold {record['fold']}: ajuste {record['fit_seconds']:.2f} s, "
                  f"predicción {record['predict_seconds']:.3f} s", flush=True)
            for warning in record["warnings"]:
                print(warning, flush=True)

        predictions[name], diagnostics[name] = fit_oof(
            x, labels, folds, factory, check_scaler=name == "linear_svm", progress=progress)
        if name == "dummy":
            if not np.array_equal(predictions[name], dummy):
                raise ValueError("La réplica cronometrada de Dummy difiere del Sprint 02.")
            predictions[name] = dummy

    records, summaries = comparison_scores(labels, folds, predictions, diagnostics)
    metadata = {
        "manifest_sha256": baseline["manifest_sha256"],
        "baseline_artifact_sha256": baseline["artifact_sha256"],
        "settings": settings, "diagnostics": diagnostics, "metrics": summaries,
        "python": platform.python_version(),
        "versions": {p: version(p) for p in ("numpy", "scikit-learn", "matplotlib")},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as temp:
        stage = Path(temp) / "stage"
        stage.mkdir()
        write_csv(stage / "predictions_oof.csv", [*index[0], *MODEL_NAMES],
                  (dict(row, **{name: int(predictions[name][i]) for name in MODEL_NAMES})
                   for i, row in enumerate(index)))
        write_csv(stage / "modelos_cv.csv", list(records[0]), records)
        (stage / "summary.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")
        verify_output(stage, baseline, index, labels, folds, dummy)
        stage.rename(output.resolve())
    return metadata


def plot_comparison(metrics, path):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    keys = ("f1_macro", "recall", "specificity")
    ticks = ("F1 macro", "Recall COVID", "Especificidad")
    names = ("Dummy", "Random Forest", "SVM lineal")
    colors = ("#737b87", "#216469", "#a84e2f")
    positions = np.arange(len(keys))
    fig, ax = plt.subplots(figsize=(8, 4.7), layout="constrained")
    for i, name in enumerate(MODEL_NAMES):
        means = [metrics[name][key]["mean"] for key in keys]
        deviations = [metrics[name][key]["std"] for key in keys]
        bars = ax.bar(positions + (i - 1) * .24, means, width=.22, yerr=deviations, capsize=3,
                      label=names[i], color=colors[i])
        ax.bar_label(bars, labels=[f"{value:.3f}".replace(".", ",") for value in means], padding=4)
    ax.set(xticks=positions, xticklabels=ticks, ylim=(0, 1.14), ylabel="Valor de la métrica (0 a 1)",
           title="Figura 1. Comparación inicial en cinco folds de desarrollo")
    ax.legend(loc="lower center", bbox_to_anchor=(.5, -.23), ncols=3, frameon=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true", help="Recalcula métricas sin ajustar modelos.")
    parser.add_argument("--figure", type=Path, help="Guarda la figura comparativa en la ruta indicada.")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8-sig"))
        if args.verify_only:
            _, *inputs = verified_inputs(config)
            metadata = verify_output(args.output, *inputs)
            print("Comparación OOF verificada.")
        else:
            metadata = run(config, args.output)
        if args.figure:
            plot_comparison(metadata["metrics"], args.figure)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
