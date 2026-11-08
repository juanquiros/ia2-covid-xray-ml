"""Lectura de un subconjunto de DESARROLLO; nunca descubre datos de test."""

import csv
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path, PurePosixPath

import numpy as np
from PIL import Image

LABELS = {"NORMAL": 0, "COVID": 1}
EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


@dataclass(frozen=True)
class Sample:
    path: Path
    relative_path: str
    label: int
    sha256: str
    patient_id: str = ""


def read_image(path):
    """Decodifica totalmente la imagen; rechaza formatos ambiguos."""
    try:
        with Image.open(path) as image:
            if image.mode == "P":
                image = image.convert("RGB")
            if image.mode not in {"L", "RGB", "I;16", "I;16L", "I;16B"}:
                raise ValueError(f"Modo no admitido: {image.mode}")
            return np.array(image)
    except (OSError, ValueError) as exc:
        raise ValueError(f"No se pudo leer {path}: {exc}") from exc


def load_samples(data_dir, max_per_class=100, *, seed=42, patients_csv=None):
    """Muestrea sin reemplazo; acepta CLASS/*.png o CLASS/images/*.png.

    data_dir debe contener únicamente desarrollo autorizado. No se buscan
    subcarpetas recursivamente (evita cargar masks/ o test/). IDs de pacientes
    solo proceden de un CSV explícito path,patient_id; no se adivinan del nombre.
    """
    root = Path(data_dir).resolve()
    if not root.is_dir():
        raise ValueError(f"No existe la carpeta de desarrollo: {root}")
    if max_per_class < 1:
        raise ValueError("max_per_class debe ser positivo.")
    patient_map = {}
    if patients_csv:
        with Path(patients_csv).open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not {"path", "patient_id"} <= set(reader.fieldnames or []):
                raise ValueError("CSV de pacientes requiere path,patient_id.")
            for row in reader:
                key = row["path"].replace("\\", "/").strip()
                if key in patient_map or not row["patient_id"].strip():
                    raise ValueError("Paciente vacío o ruta repetida en CSV.")
                patient_map[key] = row["patient_id"].strip()
    rng = np.random.default_rng(seed)
    samples, seen_hashes, available = [], {}, {}
    for name, label in LABELS.items():
        matches = [p for p in root.iterdir() if p.is_dir() and p.name.upper() == name]
        if len(matches) != 1:
            raise ValueError(f"Se requiere una única carpeta {name} en {root}.")
        folder = matches[0]
        if (folder / "images").is_dir():
            folder = folder / "images"
        paths = sorted(p for p in folder.iterdir() if p.suffix.lower() in EXTENSIONS and p.is_file())
        available[name] = len(paths)
        if not paths:
            raise ValueError(f"No hay imágenes en {folder}.")
        indices = sorted(rng.choice(len(paths), min(max_per_class, len(paths)), replace=False))
        for index in indices:
            path = paths[index]
            digest = sha256(path.read_bytes()).hexdigest()
            if digest in seen_hashes:
                raise ValueError(f"Duplicado exacto: {path.name} y {seen_hashes[digest]}. Resolver antes de CV.")
            seen_hashes[digest] = path.name
            read_image(path)  # No ocultar imágenes corruptas cambiando la muestra.
            relative = path.relative_to(root).as_posix()
            if patients_csv and relative not in patient_map:
                raise ValueError(f"Falta patient_id para {relative}.")
            samples.append(Sample(path, relative, label, digest, patient_map.get(relative, "")))
    return samples, available


def save_manifest(samples, path):
    with Path(path).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["path", "label", "sha256", "patient_id", "partition"])
        for sample in samples:
            writer.writerow([sample.relative_path, sample.label, sample.sha256,
                             sample.patient_id, "development_pilot"])


def archive_images(zipped):
    """Recorre solo PNG de COVID/Normal en la estructura de Kaggle."""
    for entry in sorted(zipped.infolist(), key=lambda item: item.filename):
        path = PurePosixPath(entry.filename)
        parts = path.parts
        if (not entry.is_dir() and len(parts) == 4 and parts[2] == "images"
                and parts[1].upper() in LABELS and path.suffix.lower() == ".png"):
            yield entry, LABELS[parts[1].upper()]


def prepare_archive(archive, output, max_per_class=100):
    """Audita hashes de COVID/Normal del ZIP y extrae solo el piloto.

    Útil ANTES de definir un test: no sustituye un split académico ni una
    auditoría por paciente. Los hashes seleccionados pasan a desarrollo.
    """
    from zipfile import ZipFile
    import json
    output = Path(output)
    if max_per_class < 1 or (output.exists() and any(output.iterdir())):
        raise ValueError("Cantidad positiva y carpeta de salida vacía requeridas.")
    rng = np.random.default_rng(42)
    unique, seen, duplicates, counts = {0: [], 1: []}, {}, [], {0: 0, 1: 0}
    with ZipFile(archive) as zipped:
        for entry, label in archive_images(zipped):
            member = entry.filename
            counts[label] += 1
            digest = sha256(zipped.read(member)).hexdigest()
            if digest in seen:
                previous, previous_label = seen[digest]
                if previous_label != label:
                    raise ValueError(f"Duplicado con etiquetas contradictorias: {previous}, {member}")
                duplicates.append({"excluded": member, "retained": previous})
                continue
            seen[digest] = (member, label)
            unique[label].append((member, digest))
        if any(len(rows) < max_per_class for rows in unique.values()):
            raise ValueError("El ZIP no tiene suficientes imágenes COVID/Normal únicas.")
        output.mkdir(parents=True, exist_ok=True)
        selected = []
        for category, label in LABELS.items():
            folder = output / category
            folder.mkdir()
            indices = sorted(rng.choice(len(unique[label]), max_per_class, replace=False))
            for index in indices:
                member, digest = unique[label][index]
                target = folder / Path(member).name
                target.write_bytes(zipped.read(member))
                selected.append({"path": target.relative_to(output).as_posix(), "source_path": member,
                                 "label": label, "sha256": digest, "partition": "development_pilot"})
    with (output / "source_manifest.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(selected[0]))
        writer.writeheader()
        writer.writerows(selected)
    with Path(archive).open("rb") as stream:
        import hashlib
        archive_hash = hashlib.file_digest(stream, "sha256").hexdigest()
    report = {"archive_sha256": archive_hash, "seed": 42,
              "source_counts": {name: counts[label] for name, label in LABELS.items()},
              "unique_counts": {name: len(unique[label]) for name, label in LABELS.items()},
              "selected_per_class": max_per_class, "exact_duplicates": duplicates,
              "test_created_or_evaluated": False,
              "note": "Excluir los hashes del piloto del futuro test; resto del ZIP no asignado."}
    (output / "preparation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description="Preparar piloto del ZIP Kaggle antes de definir test.")
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-per-class", type=int, default=100)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare_archive(args.archive, args.output, args.max_per_class), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")
