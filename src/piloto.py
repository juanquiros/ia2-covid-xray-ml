"""CLI del piloto: python -m src.piloto --help. No usa un test final."""

import argparse
import csv
import json
import platform
from importlib.metadata import version
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.base import clone
from sklearn.metrics import confusion_matrix

from .data import load_samples, read_image, save_manifest
from .evaluation import metrics
from .features import extract_hog, preprocess, HOG_CONFIG
from .models import make_baseline, make_random_forest, predict_image
from .particiones import make_folds


def evaluate_cv(features, labels, folds):
    """Predicciones fuera de fold; ambos modelos usan exactamente los mismos folds."""
    records, predictions = [], {}
    for name, estimator in [("dummy", make_baseline()), ("random_forest", make_random_forest())]:
        oof = np.full(len(labels), -1, dtype=int)
        for number, (train, valid) in enumerate(folds, start=1):
            model = clone(estimator).fit(features[train], labels[train])
            prediction = model.predict(features[valid])
            oof[valid] = prediction
            records.append(dict(model=name, fold=number, **metrics(labels[valid], prediction)))
        if (oof == -1).any():
            raise ValueError("CV no cubrió todas las imágenes.")
        predictions[name] = oof
    return records, predictions


def plot_figures(samples, labels, predictions, records, output):
    original = read_image(samples[0].path)
    _, drawing = extract_hog(original, visualize=True)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
    for ax, image, title in zip(axes, [original, preprocess(original), drawing],
                                ["Original", "Grises / 128×128", "HOG (descriptor, no lesión)"]):
        ax.imshow(image, cmap="gray")
        ax.set_title(title)
        ax.set_xlabel("Columna (píxel)")
        ax.set_ylabel("Fila (píxel)")
    fig.suptitle("Figura 1. Ejemplo de desarrollo y representación HOG")
    fig.tight_layout()
    fig.savefig(output / "01_preprocesamiento_hog.png", dpi=150)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    for ax, (name, pred) in zip(axes, predictions.items()):
        matrix = confusion_matrix(labels, pred, labels=[0, 1])
        ax.imshow(matrix, cmap="Blues")
        for (row, col), value in np.ndenumerate(matrix):
            ax.text(col, row, str(value), ha="center", va="center",
                    color="white" if value > matrix.max() / 2 else "black")
        ax.set(xticks=[0, 1], yticks=[0, 1], xticklabels=["Normal", "COVID"],
               yticklabels=["Normal", "COVID"], xlabel="Predicción", ylabel="Etiqueta real", title=name)
    fig.suptitle("Figura 2. Matrices OOF del piloto (conteos; no test final)")
    fig.tight_layout()
    fig.savefig(output / "02_matrices_cv.png", dpi=150)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4))
    names = ["accuracy", "precision", "recall", "f1", "f1_macro"]
    x = np.arange(len(names))
    for offset, model in [(-0.18, "dummy"), (0.18, "random_forest")]:
        values = np.array([[r[k] for k in names] for r in records if r["model"] == model])
        ax.bar(x + offset, values.mean(axis=0), width=.36, yerr=values.std(axis=0, ddof=1),
               capsize=3, label=model)
    ax.set(xticks=x, xticklabels=names, ylim=(0, 1.15), ylabel="Valor de métrica [0,1]",
           title="Figura 3. Piloto: media ± desvío muestral de CV")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / "03_metricas_cv.png", dpi=150)
    plt.close(fig)


def run_pilot(data_dir, output, *, max_per_class=100, n_splits=5, patients_csv=None):
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("La carpeta de salida debe estar vacía para preservar ejecuciones previas.")
    samples, available = load_samples(data_dir, max_per_class, patients_csv=patients_csv)
    labels = np.array([s.label for s in samples])
    groups = [s.patient_id for s in samples] if patients_csv else None
    folds = make_folds(labels, groups, n_splits)
    features = np.stack([extract_hog(read_image(s.path)) for s in samples])
    records, predictions = evaluate_cv(features, labels, folds)
    output.mkdir(parents=True, exist_ok=True)
    save_manifest(samples, output / "manifest.csv")
    with (output / "metrics_cv.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    fold_ids = np.zeros(len(samples), dtype=int)
    for number, (_, valid) in enumerate(folds, start=1):
        fold_ids[valid] = number
    with (output / "predictions_oof.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["path", "label", "fold", "dummy", "random_forest"])
        for i, sample in enumerate(samples):
            writer.writerow([sample.relative_path, sample.label, fold_ids[i],
                             predictions["dummy"][i], predictions["random_forest"][i]])
    summary = {
        "status": "piloto_preliminar_desarrollo_no_test_final",
        "available": available, "used": {k: int((labels == v).sum()) for k, v in [("NORMAL", 0), ("COVID", 1)]},
        "features": int(features.shape[1]), "seed": 42, "n_splits": n_splits,
        "example_path": samples[0].relative_path,
        "patient_groups": groups is not None,
        "limitation": "Sin IDs de pacientes no puede garantizarse independencia entre imágenes." if groups is None else "Grupos proporcionados por el usuario; su calidad depende de los metadatos.",
        "hog": HOG_CONFIG, "rf": make_random_forest().get_params(),
        "python": platform.python_version(),
        "versions": {p: version(p) for p in ["numpy", "scikit-image", "scikit-learn", "matplotlib", "pillow", "joblib"]},
        "metrics": {}, "confusion_matrices_oof": {},
    }
    for name, prediction in predictions.items():
        summary["metrics"][name] = {metric: {
            "mean": float(np.mean([r[metric] for r in records if r["model"] == name])),
            "std": float(np.std([r[metric] for r in records if r["model"] == name], ddof=1)),
        } for metric in metrics(labels, prediction)}
        summary["confusion_matrices_oof"][name] = confusion_matrix(labels, prediction, labels=[0, 1]).tolist()
    final_model = make_random_forest().fit(features, labels)
    joblib.dump(final_model, output / "random_forest.joblib")
    plot_figures(samples, labels, predictions, records, output)
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description="Piloto HOG + RF; usar solo imágenes autorizadas de desarrollo.")
    commands = parser.add_subparsers(dest="command", required=True)
    train = commands.add_parser("train", help="CV RF/Dummy y ajuste del RF piloto, sin tuning ni test.")
    train.add_argument("--data-dir", type=Path, required=True, help="Carpeta de DESARROLLO con COVID/ y NORMAL/.")
    train.add_argument("--output", type=Path, default=Path("output/piloto"))
    train.add_argument("--max-per-class", type=int, default=100)
    train.add_argument("--folds", type=int, default=5)
    train.add_argument("--patients-csv", type=Path)
    predict = commands.add_parser("predict", help="Clasificar una imagen con el RF piloto guardado.")
    predict.add_argument("--model", type=Path, required=True, help="Archivo joblib propio/de confianza.")
    predict.add_argument("--image", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "train":
            summary = run_pilot(args.data_dir, args.output, max_per_class=args.max_per_class,
                                n_splits=args.folds, patients_csv=args.patients_csv)
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(predict_image(joblib.load(args.model), args.image), ensure_ascii=False))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
