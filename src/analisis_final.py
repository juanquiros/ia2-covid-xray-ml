"""Reconstruye resultados reservados desde las predicciones guardadas."""

import argparse
from datetime import datetime
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (average_precision_score, confusion_matrix, f1_score,
                             precision_recall_curve, roc_auc_score, roc_curve)

from .baseline import file_sha256
from .data import csv_rows, write_csv
from .evaluation import metrics
from .final import BATCH, THRESHOLDS, read_json, reserved_rows


DISPLAY = {"dummy": "Dummy", "random_forest": "Random Forest", "linear_svm": "SVM lineal"}
COLORS = {"random_forest": "#216469", "linear_svm": "#a84e2f"}


def checked_predictions(config, selection, evaluation):
    record, receipt = read_json(selection), read_json(evaluation / "ejecucion.json")
    table = evaluation / "predicciones_test.csv"
    if (file_sha256(config["development_manifest"]) != record["manifest_sha256"]
            or file_sha256(selection) != receipt["selection_sha256"]
            or file_sha256(table) != receipt["prediction_sha256"]
            or record["selected"] != receipt["selected"]
            or datetime.fromisoformat(record["frozen_at_utc"]) >= datetime.fromisoformat(receipt["test_started_utc"])):
        raise ValueError("La evidencia reservada difiere del registro previo o del manifiesto.")
    rows = csv_rows(table)
    expected = [(row["id"], row["label"]) for row in reserved_rows(config)]
    if [(row["id"], row["label"]) for row in rows] != expected or len(rows) != receipt["n_test"]:
        raise ValueError("Los IDs o etiquetas reservados no coinciden con el manifiesto.")
    labels = np.array([int(row["label"]) for row in rows])
    predictions = {name: np.array([int(row[name]) for row in rows]) for name in BATCH}
    if any(not np.isin(pred, (0, 1)).all() for pred in predictions.values()):
        raise ValueError("Se encontraron predicciones fuera de las dos clases.")
    scores = {name: np.array([float(row[f"{name}_score"]) for row in rows]) for name in THRESHOLDS}
    for name, score in scores.items():
        if not np.isfinite(score).all() or not np.array_equal(score > THRESHOLDS[name], predictions[name]):
            raise ValueError(f"El score de {name} difiere del umbral fijado.")
    if not ((0 <= scores["random_forest"]) & (scores["random_forest"] <= 1)).all():
        raise ValueError("Probabilidad de Random Forest fuera de [0, 1].")
    return record, receipt, labels, predictions, scores


def score_test(labels, predictions, scores):
    results = []
    for name in BATCH:
        pred = predictions[name]
        tn, fp, fn, tp = (int(value) for value in confusion_matrix(labels, pred, labels=[0, 1]).ravel())
        basic = metrics(labels, pred)
        results.append(dict(
            model=name, n=len(labels), tn=tn, fp=fp, fn=fn, tp=tp,
            accuracy=basic["accuracy"], precision_covid=basic["precision"], recall_covid=basic["recall"],
            specificity=tn / (tn + fp), f1_normal=float(f1_score(labels, pred, pos_label=0, zero_division=0)),
            f1_covid=basic["f1"], f1_macro=basic["f1_macro"],
            roc_auc=float(roc_auc_score(labels, scores[name])) if name in scores else "",
            average_precision=float(average_precision_score(labels, scores[name])) if name in scores else "",
        ))
    return results


def confusion_figure(results, path):
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.25), layout="constrained")
    vmax = max(row[k] for row in results for k in ("tn", "fp", "fn", "tp"))
    for ax, row in zip(axes, results, strict=True):
        matrix = [[row["tn"], row["fp"]], [row["fn"], row["tp"]]]
        rendered = ax.imshow(matrix, cmap="Blues", vmin=0, vmax=vmax)
        for (i, j), value in np.ndenumerate(matrix):
            ax.text(j, i, str(value), ha="center", va="center",
                    color="white" if value > vmax / 2 else "black")
        ax.set(xticks=[0, 1], yticks=[0, 1], xticklabels=["Normal", "COVID"], yticklabels=["Normal", "COVID"],
               xlabel="Predicción", ylabel="Etiqueta real", title=DISPLAY[row["model"]])
    fig.colorbar(rendered, ax=axes, shrink=.75, label="Radiografías")
    fig.suptitle("Figura 1. Matrices de confusión en prueba reservada")
    fig.savefig(path, dpi=150)
    plt.close(fig)


def curve_figure(labels, scores, path):
    fig, (roc_ax, pr_ax) = plt.subplots(1, 2, figsize=(9, 4), layout="constrained")
    roc_ax.plot([0, 1], [0, 1], "--", color="#737b87", linewidth=1, label="Azar")
    pr_ax.axhline(labels.mean(), linestyle="--", color="#737b87", linewidth=1, label="Prevalencia COVID")
    for name, score in scores.items():
        fpr, tpr, _ = roc_curve(labels, score, pos_label=1)
        precision, recall, _ = precision_recall_curve(labels, score, pos_label=1)
        auc, ap = roc_auc_score(labels, score), average_precision_score(labels, score)
        roc_ax.plot(fpr, tpr, color=COLORS[name], label=f"{DISPLAY[name]} · AUC {auc:.3f}".replace(".", ","))
        pr_ax.plot(recall, precision, color=COLORS[name], label=f"{DISPLAY[name]} · AP {ap:.3f}".replace(".", ","))
    roc_ax.set(xlabel="Tasa de falsos positivos", ylabel="Recall de COVID", title="Curva ROC")
    pr_ax.set(xlabel="Recall de COVID", ylabel="Precisión de COVID", title="Curva precisión–recall")
    for ax in (roc_ax, pr_ax):
        ax.set(xlim=(0, 1), ylim=(0, 1.03))
        ax.legend(loc="lower right", fontsize=8, frameon=False)
    fig.suptitle("Figura 2. Discriminación por puntaje en prueba reservada")
    fig.savefig(path, dpi=150)
    plt.close(fig)


def interpretation_figure(evaluation, receipt, path):
    model_file = evaluation / "modelo_elegido.joblib"
    if file_sha256(model_file) != receipt["model_sha256"]:
        raise ValueError("El archivo del modelo difiere de la ejecución reservada.")
    model = joblib.load(model_file)
    if receipt["selected"] == "linear_svm":
        weights = model.named_steps["svm"].coef_[0].reshape(15, 15, 2, 2, 9)
        blocks = np.sqrt(np.square(weights).sum(axis=(2, 3, 4)))
        measure = "Norma L2 de coeficientes estandarizados"
    else:
        weights = model.feature_importances_.reshape(15, 15, 2, 2, 9)
        blocks = weights.sum(axis=(2, 3, 4))
        measure = "Suma de importancia por impureza"
    fig, ax = plt.subplots(figsize=(6.5, 5), layout="constrained")
    image = ax.imshow(blocks, cmap="viridis", extent=(4, 124, 124, 4))
    ax.set(xlabel="Columna del centro del bloque (píxeles)", ylabel="Fila del centro del bloque (píxeles)",
           title=f"Figura 3. Pesos HOG de {DISPLAY[receipt['selected']]}")
    fig.colorbar(image, ax=ax, label=measure)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    row, col = np.unravel_index(int(blocks.argmax()), blocks.shape)
    return 8 + 8 * int(row), 8 + 8 * int(col)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--evaluation", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--figures", type=Path, required=True)
    args = parser.parse_args()
    try:
        _, receipt, labels, predictions, scores = checked_predictions(
            read_json(args.config), args.selection, args.evaluation)
        results = score_test(labels, predictions, scores)
        args.results.parent.mkdir(parents=True, exist_ok=True)
        write_csv(args.results, list(results[0]), results)
        args.figures.mkdir(parents=True, exist_ok=True)
        confusion_figure(results, args.figures / "01_matrices.png")
        curve_figure(labels, scores, args.figures / "02_curvas.png")
        row, col = interpretation_figure(args.evaluation, receipt, args.figures / "03_hog.png")
        print(f"Máximo de interpretación HOG en fila {row}, columna {col}.")
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
