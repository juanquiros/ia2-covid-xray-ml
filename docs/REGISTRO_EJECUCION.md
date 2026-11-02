# Registro de ejecución

## 00-A · Primer prototipo funcional · 02/11/2026

**Solicitud:** sprint 00-A adjunto y autorización posterior para usar la misma base pública del TFC. Esta solicitud habilita el avance técnico preliminar antes del cierre académico 00–05. No se eliminó documentación ni se marcaron esos sprints como completos.

**Implementado:** carga/auditoría de imágenes, muestreo, preprocesamiento, HOG, RF y Dummy, CV exploratoria, predicción individual, serialización, figuras y pruebas. No se implementaron SVM, tuning, interfaces ni evaluación de test.

**Datos:** Kaggle versión 5. Se identificaron 47 copias exactas entre 13808 imágenes COVID/Normal; se conservaron 13761 contenidos únicos y se extrajeron 100 por clase. Metadatos sin patient_id explícito. Manifiestos y procedencia en [evidencia del piloto](../reports/piloto_2026-11-02/README.md). Los 200 hashes quedan asignados a desarrollo, excluidos del futuro test; resto sin asignar. No existía test final del proyecto.

**Resultados reales:** cinco folds comunes, RF accuracy media 0,75 ± 0,0919 y F1 macro 0,7488 ± 0,0930; Dummy accuracy 0,50. Limitaciones de muestra e independencia explícitas en el [avance](AVANCE_2026-11-02.md). No se utilizó la CV para elegir hiperparámetros ni se modificó RF para mejorar el resultado.

**Comandos ejecutados** (Python del entorno `.venv`; creación inicial con Python 3.12.14):

```text
python -m venv .venv
python -m pip install numpy scikit-image scikit-learn matplotlib pillow joblib pytest
python -m pip freeze
python -m pip check
python -m pytest -q
python -m src.data --archive data/raw/covid19-radiography-database.zip --output data/raw/pilot_development --max-per-class 100
python -m src.piloto train --data-dir data/raw/pilot_development --max-per-class 100 --folds 5 --output output/piloto_2026-11-02
python -m src.piloto --help
python -m src.piloto predict --model output/piloto_2026-11-02/random_forest.joblib --image data/raw/pilot_development/NORMAL/Normal-1224.png
```

La descarga se realizó con urllib desde la API pública de Kaggle; no requirió credenciales. Las versiones instaladas quedaron fijadas en requirements.txt. Se ajustó el contraste de las etiquetas de la matriz y se regeneraron figuras desde predicciones guardadas, sin repetir el experimento real.

**Criterios técnicos de 00-A:**

- [x] Código importable y CLI ejecutable.
- [x] Preprocesamiento probado; HOG finito de 8100 atributos.
- [x] RF entrenado y capaz de predecir; Dummy comparado con mismos folds.
- [x] Pruebas automatizadas relevantes aprobadas y dependencias verificadas.
- [x] Evidencia sintética separada de resultados reales.
- [x] Manifiestos, figuras e informe breve creados; datos y modelo fuera de Git.

**Pendientes académicos:** revisión de ambos integrantes, metadatos y auditoría integral de pacientes, split definitivo, comparación con SVM, tuning acotado y evaluación final. Son trabajo posterior, no bloqueos del prototipo funcional. El cierre Git se identifica por el commit de este registro; su SHA y resultado del push se informan al entregar, sin un segundo commit circular.
