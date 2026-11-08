"""Contrato único de preprocesamiento y HOG, sin ajuste estadístico global."""

from hashlib import sha256
from io import BytesIO
from zipfile import ZipFile

import numpy as np
from skimage.color import rgb2gray
from skimage.feature import hog
from skimage.transform import resize

from .data import read_image

IMAGE_SHAPE = (128, 128)
N_FEATURES = 8100
HOG_CONFIG = dict(orientations=9, pixels_per_cell=(8, 8),
                  cells_per_block=(2, 2), block_norm="L2-Hys",
                  transform_sqrt=False, feature_vector=True, channel_axis=None)


def preprocess(image):
    """RGB/grises uint8/uint16 o flotantes [0,1] -> grises float32 [0,1].

    Resize directo bilineal con antialiasing: no recorta ni preserva la relación
    de aspecto de imágenes no cuadradas. No usa normalización min-max por caso.
    """
    image = np.asarray(image)
    if image.size == 0 or image.ndim not in (2, 3):
        raise ValueError("Se requiere una imagen no vacía en grises o RGB.")
    if image.ndim == 3 and image.shape[2] != 3:
        raise ValueError("Solo se admiten tres canales RGB; no máscaras/alpha.")
    if image.dtype.kind == "u" and image.dtype.itemsize in (1, 2):
        image = image.astype(np.float32) / np.iinfo(image.dtype).max
    elif image.dtype.kind == "f":
        image = image.astype(np.float32)
    else:
        raise ValueError("Tipo admitido: uint8, uint16 o flotante en [0,1].")
    if not np.isfinite(image).all() or image.min() < 0 or image.max() > 1:
        raise ValueError("Las intensidades deben ser finitas y estar en [0,1].")
    if image.ndim == 3:
        image = rgb2gray(image)
    return resize(image, IMAGE_SHAPE, order=1, mode="reflect",
                  anti_aliasing=True, preserve_range=True).astype(np.float32)


def extract_hog(image, *, visualize=False):
    """Extrae siempre la misma representación; opcionalmente devuelve su dibujo."""
    result = hog(preprocess(image), visualize=visualize, **HOG_CONFIG)
    vector = result[0] if visualize else result
    if vector.shape != (N_FEATURES,) or not np.isfinite(vector).all():
        raise ValueError("HOG debe producir 8100 características finitas.")
    vector = vector.astype(np.float32)
    return (vector, result[1]) if visualize else vector


def extract_manifest_hog(archive, rows):
    """Lee únicamente las rutas suministradas, en el orden del manifiesto."""
    matrix = np.empty((len(rows), N_FEATURES), dtype=np.float32)
    with ZipFile(archive) as zipped:
        for i, row in enumerate(rows):
            content = zipped.read(row["path"])
            if sha256(content).hexdigest() != row["sha256"]:
                raise ValueError(f"El contenido difiere del manifiesto: {row['id']}.")
            matrix[i] = extract_hog(read_image(BytesIO(content)))
    return matrix
