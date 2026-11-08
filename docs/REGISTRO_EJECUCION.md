# Registro de ejecución

## 04 · Ajuste y evaluación final · 08/11/2026

**Registro previo a prueba:** a las 17:20:25 (UTC−3) se fijó SVM lineal con C=0,1 por su F1 macro medio de 0,875984 en desarrollo. El bosque del lote quedó fijado en 200 árboles, profundidad sin límite y hoja mínima 1, con F1 macro medio de 0,798345. El lote incluye Dummy y ambos candidatos. El [registro previo](../results/seleccion_pretest.json) conserva los parámetros, umbrales, métricas, SHA-256 del manifiesto, versión del entorno y hashes del código local sobre la base `f315c05`. SHA-256 del registro `421de5533435017599ea06bcbda7b1071283ea641650fefe05243e4a49a42437`. Las imágenes reservadas aún no se habían abierto.

**Búsqueda:** se verificó el cierre de 03 y se ejecutó GridSearchCV con los cinco folds de desarrollo. Una primera ejecución se interrumpió por el costo observado en SVM con C=0,1. El diagnóstico sobre desarrollo confirmó que ese ajuste requería más iteraciones que C=1. La búsqueda completa se ejecutó por candidato con la misma grilla, datos, tolerancia y solver. Se consolidaron las 11 configuraciones y se recalcularon media y desvío muestral. Los 55 ajustes válidos no registraron avisos. Pasaron las 25 pruebas antes de abrir el conjunto reservado, incluido un lote completo con datos sintéticos.

**Estado:** cerrado el 08/11/2026. El lote reservado comenzó a las 17:31:52 y se guardó a las 17:32:14 (UTC−3), después del registro de selección. Los tres modelos se reajustaron con desarrollo completo. El SVM seleccionado terminó en 788 iteraciones, sin avisos. Se comprobó la carga del modelo con ejemplos de desarrollo antes de abrir las imágenes de prueba. SHA-256 del modelo local `8f603704aa8bdb6b81cf4c1bc1510f2d91d4a57e8ce688ed06dbc366498aa4c5` (247554 bytes).

**Evaluación y verificación:** una predicción por cada uno de los 2.752 IDs reservados y por modelo. SVM lineal obtuvo F1 macro 0,871946, exactitud 0,899346, ROC-AUC 0,951055 y AP 0,890350. No se cambió la selección. Se omitió McNemar por falta de identificadores fiables de pacientes. Las matrices y el recálculo independiente de métricas, incluidos ROC-AUC y AP, se hicieron desde las predicciones guardadas, sin volver a abrir el ZIP. Se verificaron las tres figuras, enlaces, hashes y `git diff --check`. [Informe de evaluación](../reports/evaluacion.md)

**Artefactos locales:** `data/processed/sprint_04_test/` contiene las predicciones por ID, el registro temporal del lote y el modelo elegido. SHA-256 de las predicciones `2e9d2ecfb4e63e1528360f507760fd583654fabf0dbf9c018b72977d99ad0a50`. Los resultados agregados, el registro previo y la búsqueda se conservan en `results/`. [Guía interna](ejecucion/SPRINT_04_TUNING_EVALUACION.md#reproducción-interna)

## 03 · Random Forest y SVM lineal en validación cruzada · 08/11/2026

**Estado:** cerrado con los cinco folds de los tres modelos verificados. El punto de partida fue `main` en `acbf70c`, coincidente con `origin/main`. Pasó `src.baseline --verify-only` para HOG, índice, métricas y predicciones de Dummy. Se conservaron las 11.009 imágenes de desarrollo, los 8.100 atributos y el fold de cada imagen.

**Ajuste:** se usó una instancia nueva de cada candidato por fold. Se comprobó el número de filas y las medias del escalador contra el entrenamiento de cada fold. SVM usó liblinear primal (`dual=False`), tolerancia `1e-4` y máximo de 10.000 iteraciones. Terminó en 20, 19, 19, 24 y 19 iteraciones, sin avisos de convergencia.

**Resultados:** F1 macro medio y desvío muestral de 0,425478 ± 0,000065 para Dummy, 0,795500 ± 0,009817 para Random Forest y 0,870162 ± 0,004566 para SVM lineal. Se reutilizaron las predicciones de Dummy del Sprint 02 y se hizo una réplica idéntica para medir tiempos. El [informe del Sprint 03](../reports/modelos_cv.md) registra métricas, tiempos y límites. La independencia por paciente queda sin verificar porque faltan identificadores fiables. La selección final corresponde al Sprint 04.

**Verificación:** se cotejaron 33.027 predicciones OOF y se recalcularon los 15 resultados desde las confusiones por fold. Los IDs y folds coinciden con el manifiesto y no contienen IDs de test. Pasaron las 24 pruebas, `pip check` y `git diff --check`. Los artefactos por imagen y el resumen quedaron en `data/processed/sprint_03/`. [Comandos internos](ejecucion/SPRINT_03_MODELOS_CV.md#reproducción-interna)

## 02 · HOG y línea base en desarrollo · 08/11/2026

**Estado:** cerrado con matriz, índice y cinco resultados de Dummy verificados. Se partió de `main` en `55315df`, coincidente con `origin/main`. El SHA-256 del manifiesto de 01 coincide con el registrado y se conservaron las imágenes y sus folds.

**Extracción:** se verificaron los hashes de las 11.009 imágenes de desarrollo y se reutilizó el contrato 128 × 128 con HOG fijo. El proceso tardó 80,5 s y produjo una matriz `float32` de 11.009 × 8.100, con valores finitos. La matriz, el índice y las predicciones por imagen quedaron en `data/processed/sprint_02/`. SHA-256 de `hog.npy` `f808c8c28bf59fc6b71cbc2ec9139280e3f5a78920d2bcac11970e3e4998df1b`.

**Dummy:** 11.009 predicciones fuera de fold, todas Normal. Exactitud media 0,740576 ± 0,000197 y F1 macro 0,425478 ± 0,000065, con desvío estándar muestral. Recall de COVID igual a cero en los cinco folds. Los resultados completos y comandos internos están en el [informe del Sprint 02](../reports/hog_baseline.md).

**Verificación:** se cotejaron todos los IDs, etiquetas y folds, se comprobó la ausencia de IDs de test, se reextrajeron diez vectores y se recalcularon las métricas desde las predicciones guardadas. Pasaron `pip check`, 21 pruebas pertinentes y `git diff --check`. Las dos pruebas sintéticas que entrenan RF quedaron fuera de la ejecución.

## 01 · Auditoría de datos y partición definitiva · 08/11/2026

**Estado:** cerrado con manifiesto, cinco folds y [análisis de desarrollo](../reports/sprint_01/README.md) verificados. El punto de partida fue `main` en `837bf35` con los cambios locales del cierre de 00.

**Fuente y aprobación:** el equipo había comunicado aprobación y acceso el 05/11. Al consultar por la versión, aclaró el 08/11 que la aprobación cubre «el uso de todos los datos». Se usó el conjunto completo disponible en el ZIP local de Kaggle, identificado por metadatos y SHA-256 como versión 5. Se conservaron todas las imágenes elegibles de COVID y Normal, con exclusión estructural de copias exactas. Los manifiestos y particiones originales de D4 no estaban disponibles.

**Evidencia:** 13.808 rutas inventariadas, 47 copias exactas excluidas, cero ilegibles, cero conflictos de etiqueta y cero imágenes con paciente verificable. Se fijaron 11.009 imágenes de desarrollo y 2.752 de test. Los 200 hashes de 00-A quedaron en desarrollo. Se comprobaron ambas clases, unicidad y separación por ID y hash y cobertura de validación una sola vez por imagen. Sin IDs de pacientes, la independencia por paciente queda sin verificar.

**Verificación:** Python 3.12.14, `pip check` sin conflictos, 19 pruebas pertinentes aprobadas y tres pruebas de HOG o entrenamiento excluidas de la ejecución. Dos regeneraciones con semilla 42 produjeron inventario, manifiesto y resumen idénticos. SHA-256 del manifiesto `262e251fcfbe4c370a613f987725306d6fb4f5e735a15bcce49cdb2fb352707d`. Se verificaron las figuras, una muestra visual de ocho casos de desarrollo y `git diff --check`. Los comandos están en el [plan del Sprint 01](ejecucion/SPRINT_01_DATOS_EDA.md).

## 00 · Análisis crítico del TFC · 05/11/2026

**Estado:** cerrado el 05/11/2026. Cotejo documental realizado y revisión de ambos integrantes confirmada según el [plan de Sprint 00](ejecucion/SPRINT_00_ANALISIS_TFC.md).

**Punto de partida:** `juanquiros/ia2-covid-xray-ml`, rama `main` en `e77597b`, coincidente con el remoto verificado con `git ls-remote`. El árbol de trabajo estaba limpio. Cambios documentales locales para revisión.

**Evidencia:** se verificaron hashes y se cotejó la consigna de Descargas con la matriz de requisitos. En el TFC se contrastaron los cuatro conjuntos, las doce pruebas, los anexos de la CNN y D01–D08. Se recalcularon las métricas centrales de D4 a partir de la figura 38 y se recontaron los 52 casos de la tabla 30, separando acuerdo de aciertos frente a etiquetas. Se revisaron enlaces y coherencia documental y se ejecutó `git diff --check`. Véanse [Fuentes](FUENTES_Y_TRAZABILIDAD.md) y [Roadmap](ROADMAP_TFI.md).

**Revisión del equipo:** el 05/11/2026 se comunicaron las dos confirmaciones en este chat.

- **Juan Quirós:** confirmó que revisó el análisis y puede explicar las decisiones.
- **Andruszyszyn:** el equipo transmitió su confirmación de que revisó el análisis y puede explicar las decisiones.

**Datos:** el equipo informó el 05/11/2026 que la cátedra aprobó los datos y que el acceso está confirmado. En 01 se registrarán el conjunto y la versión aprobados y el respaldo de esa aprobación. También se verificará qué se puede acreditar sobre el manifiesto y las particiones de D4. Si se usa un conjunto equivalente, se justificará su correspondencia según TFI §4.

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
