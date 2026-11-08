"""Reconstruye tablas y figuras académicas desde evidencia tabular guardada."""

import argparse
import json
from pathlib import Path

import numpy as np

from .analisis_final import DISPLAY, plt, score_test
from .baseline import file_sha256
from .data import csv_rows, write_csv
from .evaluation import score_oof
from .final import BATCH, THRESHOLDS
from sklearn.metrics import precision_recall_curve, roc_curve


COLORS = ("#737b87", "#216469", "#a84e2f")


def read_evidence(root):
    integrity = json.loads((root / "sha256.json").read_text(encoding="utf-8"))
    for name in ("prueba.csv", "desarrollo_oof.csv", "eda.json", "pesos_hog.csv"):
        if file_sha256(root / name) != integrity[name]:
            raise ValueError(f"SHA-256 incorrecto para {name}.")
    return csv_rows(root / "prueba.csv"), csv_rows(root / "desarrollo_oof.csv")


def arrays(rows):
    if len({row["sample"] for row in rows}) != len(rows):
        raise ValueError("Hay muestras repetidas.")
    labels = np.array([int(row["label"]) for row in rows])
    predictions = {name: np.array([int(row[name]) for row in rows]) for name in BATCH}
    if set(labels) != {0, 1} or any(not np.isin(value, (0, 1)).all() for value in predictions.values()):
        raise ValueError("Las etiquetas o predicciones no son binarias.")
    return labels, predictions


def save(fig, path):
    fig.savefig(path, dpi=170)
    plt.close(fig)


def development_figure(eda, path):
    normal, covid = (eda["development_quality"][label] for label in ("0", "1"))
    fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3.15), layout="constrained")
    bars = a.bar(["Normal", "COVID"], [row["images"] for row in (normal, covid)], color=COLORS[1:])
    a.bar_label(bars, padding=3)
    a.set(ylabel="Radiografías", title="Imágenes originales de 299 × 299 píxeles", ylim=(0, 9200))
    rates = [100 * row["over_25_percent_at_limits"] / row["images"] for row in (normal, covid)]
    bars = b.bar(["Normal", "COVID"], rates, color=COLORS[1:])
    b.bar_label(bars, labels=[f"{r:.2f}".replace(".", ",") for r in rates], padding=3)
    b.set(ylabel="Radiografías de la clase (%)", title="Píxeles extremos en más del 25 %",
          ylim=(0, 2.3))
    save(fig, path)


def cv_figure(summary, path):
    fig, ax = plt.subplots(figsize=(8, 3.4), layout="constrained")
    keys = ("f1_macro", "recall", "specificity")
    x = np.arange(len(keys))
    for i, name in enumerate(BATCH):
        means = [summary[name][key]["mean"] for key in keys]
        deviations = [summary[name][key]["std"] for key in keys]
        bars = ax.bar(x + (i - 1) * .24, means, .22, yerr=deviations, capsize=3,
                      color=COLORS[i], label=DISPLAY[name])
        ax.bar_label(bars, labels=[f"{v:.3f}".replace(".", ",") for v in means], padding=4)
    ax.set(xticks=x, xticklabels=("F1 macro", "Recall COVID", "Especificidad"),
           ylim=(0, 1.15), ylabel="Valor de la métrica (0 a 1)")
    ax.legend(ncols=3, frameon=False, loc="lower center", bbox_to_anchor=(.5, -.23))
    save(fig, path)


def confusion_figure(results, path):
    fig, axes = plt.subplots(1, 3, figsize=(8, 3.05), layout="constrained")
    vmax = max(row[key] for row in results for key in ("tn", "fp", "fn", "tp"))
    for ax, row in zip(axes, results, strict=True):
        values = [[row["tn"], row["fp"]], [row["fn"], row["tp"]]]
        image = ax.imshow(values, cmap="Blues", vmin=0, vmax=vmax)
        for (i, j), value in np.ndenumerate(values):
            ax.text(j, i, str(value), ha="center", va="center",
                    color="white" if value > vmax / 2 else "black")
        ax.set(xticks=(0, 1), yticks=(0, 1), xticklabels=("Normal", "COVID"),
               yticklabels=("Normal", "COVID"), xlabel="Predicción", title=DISPLAY[row["model"]])
    axes[0].set_ylabel("Etiqueta real")
    fig.colorbar(image, ax=axes, shrink=.78, label="Radiografías")
    save(fig, path)


def curves_figure(labels, scores, results, path):
    fig, (roc, pr) = plt.subplots(1, 2, figsize=(8.2, 3.55), layout="constrained")
    roc.plot([0, 1], [0, 1], "--", color=COLORS[0], label="Azar")
    pr.axhline(labels.mean(), linestyle="--", color=COLORS[0], label="Proporción COVID")
    for color, row in zip(COLORS[1:], results[1:], strict=True):
        name = row["model"]
        fpr, tpr, _ = roc_curve(labels, scores[name])
        precision, recall, _ = precision_recall_curve(labels, scores[name])
        roc.plot(fpr, tpr, color=color, label=f"{DISPLAY[name]} · AUC {row['roc_auc']:.3f}".replace(".", ","))
        pr.plot(recall, precision, color=color,
                label=f"{DISPLAY[name]} · AP {row['average_precision']:.3f}".replace(".", ","))
    roc.set(xlabel="Tasa de falsos positivos", ylabel="Recall COVID", title="Curva ROC")
    pr.set(xlabel="Recall COVID", ylabel="Precisión COVID", title="Curva precisión–recall")
    for ax in (roc, pr):
        ax.set(xlim=(0, 1), ylim=(0, 1.03))
        ax.legend(frameon=False, loc="lower right", fontsize=8)
    save(fig, path)


def weights_figure(root, path):
    values = np.loadtxt(root / "pesos_hog.csv", delimiter=",")
    if values.shape != (15, 15) or not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("Pesos HOG inválidos.")
    fig, ax = plt.subplots(figsize=(5.6, 4.3), layout="constrained")
    image = ax.imshow(values, cmap="viridis", extent=(4, 124, 124, 4))
    ax.set(xlabel="Columna del centro del bloque (píxeles)", ylabel="Fila del centro del bloque (píxeles)")
    fig.colorbar(image, ax=ax, label="Norma L2 de coeficientes estandarizados")
    save(fig, path)


def run(evidence, output):
    test, dev = read_evidence(evidence)
    y, predictions = arrays(test)
    y_dev, predictions_dev = arrays(dev)
    if len(y) != 2752 or len(y_dev) != 11009:
        raise ValueError("El tamaño de las particiones difiere del estudio.")
    folds = np.array([int(row["validation_fold"]) for row in dev])
    if set(folds) != {1, 2, 3, 4, 5}:
        raise ValueError("Folds de desarrollo incompletos.")
    scores = {name: np.array([float(row[f"{name}_score"]) for row in test]) for name in THRESHOLDS}
    if any(not np.isfinite(value).all() or not np.array_equal(value > THRESHOLDS[name], predictions[name])
           for name, value in scores.items()):
        raise ValueError("Los puntajes difieren de las predicciones fijadas.")
    if not ((0 <= scores["random_forest"]) & (scores["random_forest"] <= 1)).all():
        raise ValueError("Probabilidad de Random Forest fuera de rango.")
    results = score_test(y, predictions, scores)
    dev_table, summary = [], {}
    for name in BATCH:
        records, summary[name] = score_oof(y_dev, folds, predictions_dev[name])
        dev_table.extend(dict(model=name, **row) for row in records)
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "metricas_test.csv", list(results[0]), results)
    write_csv(output / "metricas_desarrollo.csv", list(dev_table[0]), dev_table)
    eda = json.loads((evidence / "eda.json").read_text(encoding="utf-8"))
    development_figure(eda, output / "01_desarrollo.png")
    cv_figure(summary, output / "02_cv.png")
    confusion_figure(results, output / "03_matrices.png")
    curves_figure(y, scores, results, output / "04_curvas.png")
    weights_figure(evidence, output / "05_pesos_hog.png")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidencia", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    run(args.evidencia, args.salida)


if __name__ == "__main__":
    main()
