"""Métricas de clasificación con COVID como clase positiva."""

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def metrics(y, prediction):
    return dict(accuracy=float(accuracy_score(y, prediction)),
                precision=float(precision_score(y, prediction, pos_label=1, zero_division=0)),
                recall=float(recall_score(y, prediction, pos_label=1, zero_division=0)),
                f1=float(f1_score(y, prediction, pos_label=1, zero_division=0)),
                f1_macro=float(f1_score(y, prediction, average="macro", zero_division=0)))
