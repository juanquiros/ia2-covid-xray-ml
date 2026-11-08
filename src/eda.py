"""Genera las figuras de desarrollo a partir del resumen de Sprint 01."""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np


CLASSES = [("0", "Normal", "#216469"), ("1", "COVID", "#ab502d")]


def plot_development(report, output):
    output.mkdir(parents=True, exist_ok=True)
    sizes = {(str(row["label"]), row["width"], row["height"]): row["images"]
             for row in report["development_sizes"]}
    dimensions = sorted({(width, height) for _, width, height in sizes})
    x = np.arange(len(dimensions))
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    for offset, (label, category, color) in zip((-.19, .19), CLASSES):
        counts = [sizes.get((label, width, height), 0) for width, height in dimensions]
        bars = ax.bar(x + offset, counts, .36, color=color, label=category)
        ax.bar_label(bars, padding=4)
    ax.set(xticks=x, xticklabels=[f"{width} × {height}" for width, height in dimensions],
           xlabel="Tamaño original (ancho × alto, píxeles)", ylabel="Radiografías (n)",
           title="Figura 1. Tamaños originales en desarrollo")
    ax.margins(y=.17)
    ax.legend(frameon=False)
    fig.savefig(output / "01_tamanos.png", dpi=150)
    plt.close(fig)

    quality = report["development_quality"]
    indicators = [("constant", "Intensidad\nconstante"),
                  ("range_at_most_0.05", "Rango\n≤ 0,05"),
                  ("over_25_percent_at_limits", ">25 % de píxeles\ncerca de 0 o 1")]
    x = np.arange(len(indicators))
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    for offset, (label, category, color) in zip((-.19, .19), CLASSES):
        counts = [quality[label][key] for key, _ in indicators]
        rates = [count / quality[label]["images"] for count in counts]
        bars = ax.bar(x + offset, rates, .36, color=color, label=category)
        ax.bar_label(bars, labels=[str(count) for count in counts], padding=4)
    ax.set(xticks=x, xticklabels=[name for _, name in indicators],
           ylabel="Porcentaje de radiografías de la clase",
           title="Figura 2. Indicadores de intensidad en desarrollo")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.margins(y=.24)
    ax.legend(frameon=False)
    fig.savefig(output / "02_calidad.png", dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    plot_development(json.loads(args.summary.read_text(encoding="utf-8")), args.output)


if __name__ == "__main__":
    main()
