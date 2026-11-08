"""Validación cruzada común para el piloto y el protocolo académico."""

import numpy as np
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold


def make_folds(labels, groups=None, n_splits=5, *, seed=42):
    labels = np.asarray(labels)
    if n_splits < 2 or set(labels.tolist()) != {0, 1}:
        raise ValueError("CV requiere dos clases y al menos dos folds.")
    if min(np.bincount(labels)) < n_splits:
        raise ValueError("No hay suficientes imágenes por clase para los folds solicitados.")
    if groups is not None:
        groups = np.asarray(groups)
        if len(groups) != len(labels) or any(not str(g) for g in groups):
            raise ValueError("Todos los ejemplos necesitan un grupo válido.")
        for label in (0, 1):
            if len(set(groups[labels == label])) < n_splits:
                raise ValueError("No hay suficientes pacientes por clase para esta CV.")
        cv = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    else:
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    folds = list(cv.split(np.zeros(len(labels)), labels, groups))
    for train, valid in folds:
        if set(labels[train]) != {0, 1} or set(labels[valid]) != {0, 1}:
            raise ValueError("Un fold carece de alguna clase; revisar datos/agrupación.")
        if groups is not None and set(groups[train]) & set(groups[valid]):
            raise ValueError("Hay pacientes compartidos entre train y validation.")
    return folds
