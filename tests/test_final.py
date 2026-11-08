import json
from hashlib import sha256
from io import BytesIO
from zipfile import ZipFile

import numpy as np
import pytest
from PIL import Image

from src.analisis_final import checked_predictions, score_test
from src.baseline import file_sha256, run as run_baseline
from src.comparacion import verified_inputs
from src.data import write_csv
from src.final import evaluate, freeze
from src.tuning import merge_candidates, search


def test_frozen_synthetic_flow_keeps_test_images_out_until_final_batch(tmp_path):
    rng = np.random.default_rng(42)
    development_zip = tmp_path / "development.zip"
    test_zip = tmp_path / "reserved.zip"
    manifest = tmp_path / "manifest.csv"
    baseline_dir = tmp_path / "baseline"
    rows, reserved = [], {}
    with ZipFile(development_zip, "w") as archive:
        for i in range(20):
            label = i % 2
            image = rng.integers(0, 60, (32, 32), dtype=np.uint8)
            if label:
                image[:, ::4] += 160
            else:
                image[::4, :] += 160
            with BytesIO() as stream:
                Image.fromarray(image).save(stream, format="PNG")
                payload = stream.getvalue()
            path = f"{i}.png"
            if i < 16:
                archive.writestr(path, payload)
            else:
                reserved[path] = payload
            rows.append(dict(id=f"image-{i}", path=path, label=label, sha256=sha256(payload).hexdigest(),
                             partition="development" if i < 16 else "test",
                             validation_fold=1 + i // 8 if i < 16 else ""))
    write_csv(manifest, list(rows[0]), rows)
    config = dict(archive=str(development_zip), development_manifest=str(manifest),
                  development_manifest_sha256=file_sha256(manifest), development_rows=16,
                  test_rows=4, image_shape=[128, 128], folds=2, sprint_02_artifacts=str(baseline_dir))
    run_baseline(config, baseline_dir)
    source, baseline, _, labels, folds, _ = verified_inputs(config)
    records, summary = search(np.load(source / "hog.npy"), labels, folds)
    assert len(records) == 11
    tuning = tmp_path / "tuning"
    tuning.mkdir()
    provenance = dict(manifest_sha256=baseline["manifest_sha256"],
                      development_artifact_sha256=baseline["artifact_sha256"])
    parts = []
    for name in ("linear_svm", "random_forest"):
        part = tmp_path / name
        part.mkdir()
        write_csv(part / "tuning_cv.csv", list(records[0]), (r for r in records if r["model"] == name))
        partial = dict(provenance, best={name: summary["best"][name]},
                       diagnostics={name: summary["diagnostics"][name]})
        (part / "tuning.json").write_text(json.dumps(partial), encoding="utf-8")
        parts.append(part)
    merged, merged_summary = merge_candidates(parts, provenance)
    assert merged_summary == summary
    write_csv(tuning / "tuning_cv.csv", list(merged[0]), merged)
    summary.update(provenance)
    (tuning / "tuning.json").write_text(json.dumps(summary), encoding="utf-8")
    config["archive"] = str(test_zip)
    config_path, selection, output = (tmp_path / name for name in ("config.json", "selection.json", "results"))
    config_path.write_text(json.dumps(config), encoding="utf-8")
    freeze(config_path, tuning, selection)
    assert not test_zip.exists()
    assert not output.exists()
    if summary["best"]["linear_svm"]["mean_f1_macro"] == summary["best"]["random_forest"]["mean_f1_macro"]:
        assert summary["selected"] == "linear_svm"
    with ZipFile(test_zip, "w") as archive:
        for path, payload in reserved.items():
            archive.writestr(path, payload)
    evaluate(config_path, selection, output)
    record, receipt, labels, predictions, scores = checked_predictions(config, selection, output)
    assert record["selected"] == receipt["selected"]
    assert len(labels) == 4 and set(scores) == {"random_forest", "linear_svm"}
    assert all(row["n"] == 4 for row in score_test(labels, predictions, scores))
    with pytest.raises(ValueError, match="salida reservada ya existe"):
        evaluate(config_path, selection, output)
