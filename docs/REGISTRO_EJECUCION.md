# Registro de ejecución

## 00 · Análisis crítico del TFC · 05/11/2026

**Estado:** cotejo documental realizado. Cierre pendiente de registrar la revisión y confirmación individual de Juan Quirós y Andruszyszyn según el [plan de Sprint 00](ejecucion/SPRINT_00_ANALISIS_TFC.md).

**Punto de partida:** `juanquiros/ia2-covid-xray-ml`, rama `main` en `e77597b`, coincidente con el remoto verificado con `git ls-remote`. El árbol de trabajo estaba limpio. Cambios documentales locales para revisión.

**Evidencia:** se verificaron hashes y se cotejó la consigna de Descargas con la matriz de requisitos. En el TFC se contrastaron los cuatro conjuntos, las doce pruebas, los anexos de la CNN y D01–D08. Se recalcularon las métricas centrales de D4 a partir de la figura 38 y se recontaron los 52 casos de la tabla 30, separando acuerdo de aciertos frente a etiquetas. Se revisaron enlaces y coherencia documental y se ejecutó `git diff --check`. Véanse [Fuentes](FUENTES_Y_TRAZABILIDAD.md) y [Roadmap](ROADMAP_TFI.md).

**Pendientes de datos:** acreditar versión, manifiesto y particiones de D4. Si se adopta un conjunto equivalente, justificarlo y obtener autorización previa de cátedra según TFI §4. La documentación disponible acredita permiso para el piloto 00-A y deja pendiente la autorización de sustitución.

**Alcance ejecutado:** revisión documental y cálculos sobre cifras publicadas. La evidencia exploratoria de 00-A se conserva aparte.

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
