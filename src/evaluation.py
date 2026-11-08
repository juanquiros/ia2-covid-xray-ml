"""Métricas de clasificación con COVID como clase positiva."""

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def metrics(y, prediction):
    return dict(accuracy=float(accuracy_score(y, prediction)),
                precision=float(precision_score(y, prediction, pos_label=1, zero_division=0)),
                recall=float(recall_score(y, prediction, pos_label=1, zero_division=0)),
                f1=float(f1_score(y, prediction, pos_label=1, zero_division=0)),
                f1_macro=float(f1_score(y, prediction, average="macro", zero_division=0)))


def score_oof(labels, folds, predictions):
    records = []
    for fold in np.unique(folds):
        valid = folds == fold
        y, pred = labels[valid], predictions[valid]
        records.append(dict(fold=int(fold), n_validation=len(y), n_covid=int(y.sum()),
                            n_predicted_covid=int(pred.sum()), **metrics(y, pred),
                            specificity=float(recall_score(y, pred, pos_label=0, zero_division=0))))
    summary = {}
    for key in ("accuracy", "precision", "recall", "f1", "specificity", "f1_macro"):
        values = [row[key] for row in records]
        summary[key] = {"mean": float(np.mean(values)), "std": float(np.std(values, ddof=1))}
    return records, summary
