import numpy as np
from sklearn.preprocessing import StandardScaler

from src.comparacion import fit_oof
from src.models import make_linear_svm


def test_svm_scaler_fits_only_on_training_rows_of_each_fold():
    folds = np.repeat([1, 2, 3], 4)
    labels = np.tile([0, 1, 0, 1], 3)
    features = np.column_stack((folds * 100, labels * 10, np.arange(12))).astype(np.float32)
    seen, fitted = [], []

    class RecordingScaler(StandardScaler):
        def fit(self, X, y=None, sample_weight=None):
            seen.append(X.copy())
            return super().fit(X, y, sample_weight)

    def factory():
        model = make_linear_svm().set_params(scaler=RecordingScaler())
        fitted.append(model)
        return model

    predictions, diagnostics = fit_oof(features, labels, folds, factory, check_scaler=True)
    np.testing.assert_array_equal(predictions, labels)
    assert len({id(model) for model in fitted}) == 3
    assert [row["fold"] for row in diagnostics] == [1, 2, 3]
    for fold, scaler_input, row in zip((1, 2, 3), seen, diagnostics, strict=True):
        np.testing.assert_array_equal(scaler_input, features[folds != fold])
        assert row["scaler_train_only"] and row["n_train"] == 8
