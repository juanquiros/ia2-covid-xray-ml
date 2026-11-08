"""Auditoría estructural de Kaggle, split reproducible y EDA de desarrollo."""

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from hashlib import file_digest, sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
from zipfile import BadZipFile, ZipFile

import numpy as np
from openpyxl import load_workbook

from .data import archive_images, csv_rows, read_image, write_csv
from .features import IMAGE_SHAPE, preprocess
from .particiones import make_folds


@dataclass
class Record:
    id: str
    path: str
    label: int
    source: str
    origin: str
    sha256: str = ""
    patient_id: str = ""
    status: str = "retained"
    retained_id: str = ""


def archive_origins(zipped):
    """Asocia cada nombre con el dominio de su URL en el XLSX de su clase."""
    origins = {}
    for category in ("COVID", "Normal"):
        name = f"COVID-19_Radiography_Dataset/{category}.metadata.xlsx"
        with BytesIO(zipped.read(name)) as stream:
            book = load_workbook(stream, read_only=True, data_only=True)
            try:
                rows = book.active.values
                header = next(rows)
                name_index, url_index = header.index("FILE NAME"), header.index("URL")
                for row in rows:
                    if row[name_index] is None:
                        continue
                    path = f"COVID-19_Radiography_Dataset/{category}/images/{row[name_index]}.png".casefold()
                    if path in origins:
                        raise ValueError(f"Ruta de origen repetida en metadatos: {path}")
                    origins[path] = urlsplit(str(row[url_index])).hostname or ""
            finally:
                book.close()
    return origins


def audit_archive(zipped, source, origins, patients):
    records, by_hash, seen_paths = [], defaultdict(list), set()
    for entry, label in archive_images(zipped):
        path = entry.filename
        if path in seen_paths:
            raise ValueError(f"Ruta repetida en el ZIP: {path}")
        seen_paths.add(path)
        record = Record(sha256(f"{source}/{path}".encode()).hexdigest(), path, label,
                        source, origins.get(path.casefold(), ""), patient_id=patients.get(path, ""))
        records.append(record)
        try:
            content = zipped.read(entry)
            record.sha256 = sha256(content).hexdigest()
            read_image(BytesIO(content))
        except (ValueError, OSError, BadZipFile):
            record.status = "unreadable"
            continue
        by_hash[record.sha256].append(record)
    if patients.keys() - seen_paths:
        raise ValueError("El CSV de pacientes contiene rutas ajenas al inventario.")

    for copies in by_hash.values():
        if len({row.label for row in copies}) > 1:
            for row in copies:
                row.status = "label_conflict"
            continue
        known = {row.patient_id for row in copies if row.patient_id}
        if len(known) > 1:
            raise ValueError("Una imagen exacta tiene pacientes incompatibles. Revisar metadatos antes del split.")
        canonical = copies[0]
        if known:
            canonical.patient_id = known.pop()
        for row in copies[1:]:
            row.status = "exact_duplicate"
            row.retained_id = canonical.id
    return records


def patient_mapping(path):
    patients = {}
    if path is not None:
        for row in csv_rows(path):
            key = row["path"].replace("\\", "/").strip()
            group = row["patient_id"].strip()
            if key in patients or not key or not group:
                raise ValueError("El CSV de pacientes requiere rutas únicas e IDs no vacíos.")
            patients[key] = group
    return patients


def pilot_data(config):
    source_rows = csv_rows(config["pilot_manifest"])
    local_rows = csv_rows(config["pilot_groups"])
    source = {row["sha256"]: row["label"] for row in source_rows}
    local = {row["sha256"]: row["label"] for row in local_rows}
    if source != local or len(source) != len(source_rows) or len(local) != len(local_rows):
        raise ValueError("Los manifiestos del piloto divergen en etiquetas o hashes.")
    return source, {row["patient_id"] for row in local_rows if row["patient_id"]}


def grouping_keys(rows):
    if any(row.patient_id for row in rows):
        return [f"patient:{row.patient_id}" if row.patient_id else f"image:{row.id}" for row in rows]
    return None


def make_partition(records, pilot_hashes, pilot_groups, *, seed, fraction, folds):
    retained = [row for row in records if row.status == "retained"]
    known_pilot = pilot_groups | {row.patient_id for row in records
                                  if row.sha256 in pilot_hashes and row.patient_id}
    eligible = [row for row in retained
                if row.sha256 not in pilot_hashes and row.patient_id not in known_pilot]
    total = Counter(row.label for row in retained)
    target = {label: round(total[label] * fraction) for label in (0, 1)}
    groups = grouping_keys(eligible)
    if groups is None:
        rng = np.random.default_rng(seed)
        test_ids = set()
        for label, count in target.items():
            candidates = [row.id for row in eligible if row.label == label]
            if count < 1 or len(candidates) < count:
                raise ValueError("La reserva del piloto impide alcanzar un test con ambas clases.")
            test_ids.update(rng.choice(candidates, count, replace=False).tolist())
    else:
        candidates = make_folds([row.label for row in eligible], groups, round(1 / fraction), seed=seed)
        # Con grupos indivisibles, elegir el candidato más cercano a los tamaños por clase.
        def distance(candidate):
            counts = Counter(eligible[i].label for i in candidate[1])
            return sum(abs(counts[label] - target[label]) / total[label] for label in (0, 1))

        _, test_index = min(candidates, key=distance)
        test_ids = {eligible[i].id for i in test_index}
    development = [row for row in retained if row.id not in test_ids]
    test = [row for row in retained if row.id in test_ids]
    if not test or abs(len(test) / len(retained) - fraction) > .02:
        raise ValueError("No se pudo reservar un test dentro de dos puntos del porcentaje previsto.")
    splits = make_folds([row.label for row in development], grouping_keys(development), folds, seed=seed)
    assigned = {}
    for fold, (_, valid) in enumerate(splits, 1):
        for index in valid:
            image_id = development[index].id
            if image_id in assigned:
                raise ValueError("Imagen de desarrollo repetida en validación.")
            assigned[image_id] = fold
    if set(assigned) != {row.id for row in development}:
        raise ValueError("Hay imágenes de desarrollo sin fold.")
    verify_partition(development, test, assigned, pilot_hashes, known_pilot, folds)
    return development, test, assigned


def verify_partition(development, test, assigned, pilot_hashes, pilot_groups, folds):
    def verify_pair(train, valid):
        for rows in (train, valid):
            if {row.label for row in rows} != {0, 1}:
                raise ValueError("Una partición o fold carece de alguna clase.")
        for key in ("id", "sha256", "patient_id"):
            overlap = {getattr(row, key) for row in train} & {getattr(row, key) for row in valid}
            if overlap - {""}:
                raise ValueError(f"Cruce de {key} entre particiones.")

    for key in ("id", "sha256"):
        values = {getattr(row, key) for row in development + test}
        if "" in values or len(values) != len(development) + len(test):
            raise ValueError(f"{key} vacío o repetido entre imágenes retenidas.")
    if set(assigned) != {row.id for row in development} or set(assigned.values()) != set(range(1, folds + 1)):
        raise ValueError("Las asignaciones de validación no cubren exactamente desarrollo y sus folds.")
    verify_pair(development, test)
    if any(row.sha256 in pilot_hashes or row.patient_id in pilot_groups for row in test):
        raise ValueError("El test contiene imágenes o grupos del piloto.")
    for fold in range(1, folds + 1):
        verify_pair([row for row in development if assigned[row.id] != fold],
                    [row for row in development if assigned[row.id] == fold])


def development_eda(zipped, development):
    sizes, quality = Counter(), defaultdict(Counter)
    for row in development:
        image = read_image(BytesIO(zipped.read(row.path)))
        height, width = image.shape[:2]
        sizes[row.label, width, height] += 1
        prepared = preprocess(image)
        if prepared.shape != IMAGE_SHAPE or prepared.dtype != np.float32 or not np.isfinite(prepared).all():
            raise ValueError(f"Salida de preprocesamiento inválida para {row.id}.")
        quality[row.label]["images"] += 1
        quality[row.label]["non_square"] += width != height
        quality[row.label]["constant"] += np.ptp(prepared) == 0
        quality[row.label]["range_at_most_0.05"] += np.ptp(prepared) <= .05
        quality[row.label]["over_25_percent_at_limits"] += np.mean((prepared <= .01) | (prepared >= .99)) > .25
    return sizes, {label: {key: int(value) for key, value in counts.items()}
                   for label, counts in quality.items()}


def run(config, output, patients_csv=None):
    output = Path(output)
    if output.exists():
        raise ValueError("La carpeta de salida ya existe. Usar una nueva para preservar la evidencia.")
    with Path(config["archive"]).open("rb") as stream:
        archive_hash = file_digest(stream, "sha256").hexdigest()
    if archive_hash != config["archive_sha256"]:
        raise ValueError("El SHA-256 del ZIP difiere de la versión documentada.")
    if tuple(config["image_shape"]) != IMAGE_SHAPE:
        raise ValueError("La configuración difiere del contrato de preprocesamiento vigente.")
    pilot_hashes, pilot_groups = pilot_data(config)
    source = f'{config["dataset"]}@{config["version"]}'
    with ZipFile(config["archive"]) as zipped:
        origins = archive_origins(zipped)
        records = audit_archive(zipped, source, origins, patient_mapping(patients_csv))
        present = {row.sha256 for row in records} & pilot_hashes.keys()
        for row in records:
            if (row.status == "retained" and row.sha256 in pilot_hashes
                    and row.label != int(pilot_hashes[row.sha256])):
                raise ValueError("Una imagen del piloto cambió de etiqueta en la fuente definitiva.")
        development, test, assigned = make_partition(
            records, present, pilot_groups, seed=config["seed"], fraction=config["test_fraction"],
            folds=config["folds"])
        sizes, quality = development_eda(zipped, development)

    columns = [field.name for field in fields(Record)]
    report = {
        "source": source, "archive_sha256": archive_hash,
        "inventory_by_class": dict(Counter(row.label for row in records)),
        "exclusions_by_class": {status: dict(Counter(row.label for row in records if row.status == status))
                                for status in ("unreadable", "exact_duplicate", "label_conflict")},
        "origin_available": sum(bool(row.origin) for row in records),
        "known_patient_images": sum(bool(row.patient_id) for row in records),
        "known_patient_retained_images": sum(bool(row.patient_id) for row in development + test),
        "pilot_hashes": len(pilot_hashes), "pilot_hashes_present": len(present),
        "pilot_hashes_in_development": sum(row.sha256 in present for row in development),
        "pilot_hashes_in_test": sum(row.sha256 in present for row in test),
        "split_by_class": {"development": dict(Counter(row.label for row in development)),
                           "test": dict(Counter(row.label for row in test))},
        "validation_by_fold": {fold: dict(Counter(row.label for row in development if assigned[row.id] == fold))
                               for fold in range(1, config["folds"] + 1)},
        "development_sizes": [{"label": label, "width": width, "height": height, "images": count}
                              for (label, width, height), count in sorted(sizes.items())],
        "development_quality": quality,
        "development_origins": {
            label: dict(sorted(Counter(row.origin for row in development if row.label == label).items()))
            for label in (0, 1)
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as temp:
        stage = Path(temp) / "stage"
        stage.mkdir()
        write_csv(stage / "inventario.csv", columns, (asdict(row) for row in records))
        manifest = (dict(asdict(row), partition=partition, validation_fold=assigned.get(row.id, ""))
                    for partition, rows in (("development", development), ("test", test)) for row in rows)
        write_csv(stage / "manifiesto.csv", columns + ["partition", "validation_fold"], manifest)
        (stage / "resumen.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
        stage.rename(output.resolve())
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--patients-csv", type=Path, help="CSV local con path,patient_id verificables.")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8-sig"))
        run(config, args.output, args.patients_csv)
    except (ValueError, OSError, KeyError, BadZipFile) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
