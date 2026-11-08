"""Configuraciones iniciales de la línea base y los dos candidatos."""

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

from .data import read_image
from .features import extract_hog


def make_random_forest():
    return RandomForestClassifier(n_estimators=100, max_depth=None,
                                  min_samples_leaf=1, max_features="sqrt", bootstrap=True,
                                  class_weight=None, random_state=42, n_jobs=-1)


def make_linear_svm():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("svm", LinearSVC(C=1, penalty="l2", loss="squared_hinge", dual=False,
                          class_weight=None, random_state=42, tol=1e-4, max_iter=10000)),
    ])


def make_baseline():
    return DummyClassifier(strategy="most_frequent")


def predict_image(model, path):
    vector = extract_hog(read_image(path)).reshape(1, -1)
    label = int(model.predict(vector)[0])
    if label not in (0, 1):
        raise ValueError("El modelo no utiliza etiquetas NORMAL=0, COVID=1.")
    return {"label": label, "category": "COVID" if label else "NORMAL"}
