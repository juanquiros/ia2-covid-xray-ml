"""Búsqueda de Sprint 04 sobre los folds de desarrollo ya asignados."""

import argparse
import json
import warnings
from itertools import product
from pathlib import Path
from time import perf_counter

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import GridSearchCV

from .comparacion import verified_inputs
from .data import csv_rows, write_csv
from .models import make_linear_svm, make_random_forest


def candidate_grids():
    return (
        ("linear_svm", make_linear_svm(), [{"svm__C": [c]} for c in (.1, 1, 10)]),
        ("random_forest", make_random_forest(), [
            {"n_estimators": [trees], "max_depth": [depth], "min_samples_leaf": [leaf]}
            for trees, depth, leaf in product((100, 200), (None, 20), (1, 3))
        ]),
    )


def search(features, labels, folds, *, candidate=None, verbose=0):
    splits = [(np.flatnonzero(folds != fold), np.flatnonzero(folds == fold))
              for fold in np.unique(folds)]
    scoring = make_scorer(f1_score, average="macro", labels=[0, 1], zero_division=0)
    records, best, diagnostics = [], {}, {}
    for name, estimator, grid in candidate_grids():
        if candidate is not None and candidate != name:
            continue
        searcher = GridSearchCV(estimator, grid, scoring=scoring, cv=splits,
                                refit=False, n_jobs=1, error_score="raise", verbose=verbose)
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always", ConvergenceWarning)
            start = perf_counter()
            searcher.fit(features, labels)
            elapsed = perf_counter() - start
        results = searcher.cv_results_
        diagnostics[name] = {"seconds": elapsed, "warnings": [
            f"{item.category.__name__}: {item.message}" for item in captured
        ]}
        for i, params in enumerate(results["params"]):
            scores = [float(results[f"split{j}_test_score"][i]) for j in range(len(splits))]
            records.append(dict(model=name, configuration=i + 1, parameters=json.dumps(params),
                                **{f"fold_{j}": score for j, score in enumerate(scores, 1)},
                                mean_f1_macro=float(results["mean_test_score"][i]),
                                std_sample_f1_macro=float(np.std(scores, ddof=1)),
                                mean_fit_seconds=float(results["mean_fit_time"][i])))
        best[name] = dict(parameters=searcher.best_params_,
                          configuration=int(searcher.best_index_) + 1,
                          mean_f1_macro=float(searcher.best_score_))
        if verbose:
            print(f"{name}: {elapsed:.1f} s, avisos={len(captured)}", flush=True)
    # El orden de best conserva SVM en un empate exacto entre candidatos.
    selected = max(best, key=lambda name: best[name]["mean_f1_macro"])
    return records, {"best": best, "selected": selected, "diagnostics": diagnostics}


def merge_candidates(paths, provenance):
    records, best, diagnostics = [], {}, {}
    for name, path in zip(("linear_svm", "random_forest"), paths, strict=True):
        summary = json.loads((path / "tuning.json").read_text(encoding="utf-8"))
        if set(summary["best"]) != {name} or any(summary[key] != value for key, value in provenance.items()):
            raise ValueError("La búsqueda parcial no corresponde al candidato o al desarrollo fijado.")
        records.extend(csv_rows(path / "tuning_cv.csv"))
        best.update(summary["best"])
        diagnostics.update(summary["diagnostics"])
    return records, {"best": best, "selected": max(best, key=lambda name: best[name]["mean_f1_macro"]),
                     "diagnostics": diagnostics}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--candidate", choices=("linear_svm", "random_forest"))
    mode.add_argument("--merge-from", type=Path, nargs=2, metavar=("SVM_DIR", "RF_DIR"))
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError("La carpeta de búsqueda ya existe.")
        config = json.loads(args.config.read_text(encoding="utf-8-sig"))
        source, baseline, _, labels, folds, _ = verified_inputs(config)
        provenance = dict(manifest_sha256=baseline["manifest_sha256"],
                          development_artifact_sha256=baseline["artifact_sha256"])
        if args.merge_from:
            records, summary = merge_candidates(args.merge_from, provenance)
        else:
            features = np.load(source / "hog.npy", mmap_mode="r", allow_pickle=False)
            records, summary = search(features, labels, folds, candidate=args.candidate, verbose=3)
        summary.update(provenance)
        args.output.mkdir(parents=True, exist_ok=False)
        write_csv(args.output / "tuning_cv.csv", list(records[0]), records)
        (args.output / "tuning.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                                encoding="utf-8")
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
