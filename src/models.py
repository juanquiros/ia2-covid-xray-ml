"""Modelos del piloto. SVM y tuning quedan para la comparación posterior."""

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier

from .data import read_image
from .features import extract_hog


def make_random_forest():
    return RandomForestClassifier(n_estimators=100, max_depth=None,
                                  min_samples_leaf=1, random_state=42, n_jobs=-1)


def make_baseline():
    return DummyClassifier(strategy="most_frequent")


def predict_image(model, path):
    vector = extract_hog(read_image(path)).reshape(1, -1)
    label = int(model.predict(vector)[0])
    if label not in (0, 1):
        raise ValueError("El modelo no utiliza etiquetas NORMAL=0, COVID=1.")
    return {"label": label, "category": "COVID" if label else "NORMAL"}
