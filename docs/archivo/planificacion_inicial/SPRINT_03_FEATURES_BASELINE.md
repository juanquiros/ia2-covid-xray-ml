# Sprint 03 · Descriptores y baseline

**Estado:** no iniciado. Depende del cierre 02.

# Objetivo

Implementar preprocesamiento común, HOG/LBP reproducibles y baseline B0 en validación cruzada de desarrollo.

# Por qué existe este sprint

La representación debe estar verificada antes de comparar clasificadores. B0 establece una referencia mínima que ignora las imágenes y revela si las métricas están correctamente definidas.

# Conocimientos previos necesarios

HOG, LBP, vectores, histogramas, scaling, Pipeline, baseline y métricas con clase positiva. Teoría §§5–6, 8–10, 15–16.

# Entradas

Cierre 02, configuración de preprocesamiento, manifiestos de desarrollo/folds, entorno y contrato de etiquetas. Test sellado sin acceso.

# Tareas

- [ ] Verificar aceptación 02 y configuración; implementar una única ruta de carga/preprocesamiento.
- [ ] Implementar HOG explícito: 9 orientaciones, celdas 8×8, bloques 2×2, L2-Hys, sobre 128×128.
- [ ] Implementar LBP uniform P=8 R=1 e histogramas normalizados en grilla 4×4.
- [ ] Validar dimensiones esperadas 8100 y 160, rango, finitud y manejo de entradas inválidas.
- [ ] Diseñar cache de descriptores fijos por hash de imagen y configuración; nunca cachear transformaciones aprendidas globalmente.
- [ ] Construir contratos de Pipeline para escaladores futuros, sin ajustar PCA ni entrenar candidatos.
- [ ] Evaluar B0=DummyClassifier most_frequent en mismos folds de desarrollo, ajustando clase mayoritaria solo en train.
- [ ] Guardar métricas por fold, media ± desvío y ejemplos visuales de descriptores de desarrollo con advertencia de que no son explicaciones del clasificador.

# Archivos futuros involucrados

Crear `src/features/preprocesamiento.py`, `src/features/descriptores.py`, `src/features/cache.py`, `src/models/baseline.py`, `src/evaluation/metricas.py`, `configs/features.json`, `tests/test_features.py`, `tests/test_metricas.py`, `results/metrics/baseline_cv.csv` y `results/reports/features_baseline.md`. Features cacheados locales en `data/processed/`; no versionar grandes matrices. Modificar README, configuración/dependencias solo si justificadas y documentos operativos.

# Implementación esperada

Funciones deterministas con etiquetas/IDs alineados y estimadores clonables cuando corresponda. El módulo de métricas fija labels=[0,1], positivo=COVID=1, tratamiento de ceros y scores. B0 no necesita HOG para predecir; no cobrar extracción innecesaria como costo de baseline. La extracción futura de test se hará solo dentro de evaluación 06, usando configuración congelada.

# Pruebas

Imágenes sintéticas pequeñas con intensidades conocidas: consistencia de grises/resize/rango y repetición, forma de vectores, histogramas normalizados, NaN/corrupción rechazados y cache invalidado al cambiar configuración. Matrices manuales verifican VP/VN/FP/FN, F1 macro y especificidad; verificar que B0 solo recibe train de cada fold. Tests no deben usar imágenes de test reservado.

# Resultados esperados

Representaciones verificadas y métricas reales de baseline en desarrollo; ninguna métrica de candidatos ni test. Un resultado trivial pobre no es fallo de implementación por sí mismo.

# Criterios de aceptación

Contratos/dimensiones pasan pruebas; IDs de features y etiquetas coinciden; cache trazable; B0 tiene cinco folds o k previamente aprobado, media/desvío y resultados regenerables; no se ajustó scaler/PCA global para CV; test intacto.

# Evidencias a conservar

Configuración, pruebas, hash/cache, conteo de features, tiempos de extracción en desarrollo, métricas B0, muestras HOG/LBP autorizadas, comandos y versiones.

# Riesgos

Rango incompatible, doble normalización, LBP sensible a ruido, dimensión inesperada por defaults, orden incorrecto de clases/archivos y cache obsoleto.

# Errores frecuentes

Presentar HOG como mapa diagnóstico, entrenar SVM en este sprint, ajustar PCA antes de CV, asignar 0,5 a todas las métricas de baseline y almacenar vectores sin ID.

# Qué debemos comprender antes de cerrarlo

Cómo se forma cada vector, qué información se pierde, qué aprende B0 y qué cálculos dependen de la clase positiva. Poder explicar las dimensiones sin consultar el código.

# Preguntas posibles de defensa

1. ¿Cómo obtenemos 8100 features HOG?
2. ¿Por qué LBP tiene 160 valores en este diseño?
3. ¿Extraer HOG requiere aprender etiquetas?
4. ¿Qué garantiza y qué no garantiza el cache?
5. ¿Por qué B0 ignora la imagen?
6. ¿Por qué accuracy y F1 macro de B0 pueden ser distintos?
7. ¿Cómo verificamos que no se intercambiaron etiquetas?

# Definition of Done

Features/B0 reproducibles, pruebas y criterios completos, resultados reales documentados, test sin acceso, checklist e índice actualizados, commit y push confirmado. No iniciar candidatos de 04.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá exclusivamente SPRINT_03_FEATURES_BASELINE en juanquiros/ia2-covid-xray-ml/main.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/ejecucion/README.md y docs/ejecucion/SPRINT_03_FEATURES_BASELINE.md; verificá cierre/criterios de 02, EDA, configuración y manifiestos. Revisá repo, remote, rama, status/diff; preservá trabajo existente.
Objetivo: descriptores confiables y baseline B0 sobre desarrollo. Creá módulos preprocesamiento/descriptores/cache en src/features, src/models/baseline.py, src/evaluation/metricas.py, configs/features.json, tests/test_features.py, tests/test_metricas.py y resultados baseline_cv.csv/features_baseline.md.
Implementá HOG 128x128, 9 bins, celda 8x8, bloque 2x2 y L2-Hys; LBP uniform P8 R1 con histogramas 4x4; mantené IDs y contrato de rango. Cacheá solo operaciones fijas por imagen/configuración. Evaluá DummyClassifier most_frequent en folds existentes, sin usar test, y guardá media/desvío y métricas por clase/fold.
Restricciones: no entrenar SVM/RF/KNN/logística, no ajustar PCA, no tuning ni test, no generar resultados ficticios ni publicar matrices pesadas. No implementar 04 o posteriores.
Probá dimensiones 8100/160, normalización, finitud, reproducibilidad, cache, IDs, errores de entrada y métricas con matrices manuales. Comprobá que baseline aprende solo de train de cada fold. Cumplí aceptación/DoD y documentá resultados reales y límites.
Actualizá documentación, uso de IA, README, índice y checklist; agregá Cierre real con evidencias. Revisá git diff --check/diff, agregá solo archivos pertinentes, commit 'feat: add image descriptors and development baseline' y push origin/main. Informá SHA, pruebas, métricas reales de desarrollo, archivos y estado Git. Detenete aquí.
```
