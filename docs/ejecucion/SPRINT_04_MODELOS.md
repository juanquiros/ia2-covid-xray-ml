# Sprint 04 · Candidatos con configuración fija

**Estado:** no iniciado. Depende del cierre 03.

# Objetivo

Comparar C1=HOG+scaler+SVM lineal y C2=LBP+Random Forest, además de B0 y referencia B1=HOG+scaler+logística L2, con configuraciones iniciales fijadas y CV común.

# Por qué existe este sprint

La consigna exige dos candidatos además de baseline. Antes de una búsqueda debemos comprobar contratos, convergencia, variabilidad y costo sin elegir un ganador por intuición.

# Conocimientos previos necesarios

SVM, RF, logística, Pipeline, CV, costo, media/desvío y distinción comparación de pipelines frente a comparación de clasificadores. Teoría §§12–18.

# Entradas

Cierre 03, descriptores, baseline, folds guardados y entorno probado. Test intacto. La configuración inicial se registra antes de obtener resultados.

# Tareas

- [ ] Verificar aceptación 03 y resultados B0.
- [ ] Crear pipelines C1, C2 y B1 con parámetros explícitos, semilla y condiciones de convergencia.
- [ ] Fijar C1 C=1, sin PCA; C2 200 árboles, max_features=sqrt, min_samples_leaf=1 y max_depth=None; B1 C=1 L2, salvo incompatibilidad técnica justificada antes de evaluar.
- [ ] Ajustar scaler exclusivamente dentro de train de cada fold y evaluar todos con mismas listas de IDs.
- [ ] Guardar métricas train/validation por fold, scores fuera de fold, tiempos y avisos/errores.
- [ ] Reportar media ± desvío muestral para B0/B1/C1/C2 y comparar F1 macro, recall y especificidad.
- [ ] Analizar brechas train/CV y capacidad/costo; no llamarlas automáticamente overfitting sin auditoría.
- [ ] Estimar presupuesto de tuning con medidas de desarrollo; justificar opcionales KNN/RBF si se proponen, sin incorporarlos automáticamente.

# Archivos futuros involucrados

Crear `src/models/candidatos.py`, `src/models/comparacion_cv.py`, `configs/modelos.json`, `tests/test_pipelines.py`, `results/metrics/modelos_cv.csv`, `results/metrics/modelos_oof.csv`, figuras comparativas y `results/reports/modelos.md`. Modificar README, decisiones, uso de IA y planes si hay cambios justificados; binarios en models ignorado.

# Implementación esperada

Fábricas de estimadores clonables y runner que consume folds persistidos. Los scores se alinean por ID y signo de clase positiva. RF no necesita scaler; modelos lineales sí lo incluyen como parte del fit. El benchmark de comparación incluye extracción por separado y costo completo pertinente; B0 no requiere features. No realizar grillas ni cambios repetidos buscando mejor media en este sprint.

# Pruebas

Verificar que scaler ve solo IDs de train; no hay cruce de grupos; cada observación tiene una predicción OOF por repetición; forma/finito/signo de scores correcto; serialización de pipeline conserva predicciones en una muestra de desarrollo. Pruebas de humo usan datos sintéticos; la comparación real debe poder regenerarse con datos de desarrollo. No exigir una accuracy arbitraria para que pase un test de software.

# Resultados esperados

Comparación real inicial de baseline y candidatos con dispersión y costos, sin ganador final ni resultados test. Hipótesis de mejora/costo aún sujetas a evaluación final.

# Criterios de aceptación

B0 más dos candidatos y B1 evaluados en mismos folds; parámetros/configuración identificados; transformaciones aprendidas dentro del pipeline; advertencias de convergencia resueltas o fallo reportado sin ocultamiento; métricas y tiempos trazables; test intacto.

# Evidencias a conservar

Config/commit/entorno, IDs por fold, scores OOF publicables, tablas completas, avisos, hardware/hilos, tiempos y resultados de pruebas. No conservar únicamente la fila mejor.

# Riesgos

Costo RF alto, descriptores espurios, fallo de convergencia, sobreinterpretación de pocos folds y atribuir efecto de descriptor al clasificador.

# Errores frecuentes

Escalar toda matriz antes de CV, evaluar métodos con folds distintos, usar test “para ver cómo va”, esconder corridas malas y empezar tuning en este sprint.

# Qué debemos comprender antes de cerrarlo

Qué aprende cada familia, qué función/coste optimiza, qué mide CV y por qué comparar HOG-SVM con LBP-RF no aísla el clasificador.

# Preguntas posibles de defensa

1. ¿Qué controla C de la SVM?
2. ¿Qué aporta aleatoriedad en RF?
3. ¿Por qué logística es clasificación?
4. ¿Qué comparación aísla el efecto de un descriptor?
5. ¿Por qué reportar dispersión además de media?
6. ¿Cómo se detecta un scaler mal ajustado?
7. ¿Qué significa un fallo de convergencia?

# Definition of Done

Comparación inicial reproducible, todos los criterios/pruebas documentados, test intacto, checklist actualizado, commit y push. 05 no comienza automáticamente.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá solo SPRINT_04_MODELOS en juanquiros/ia2-covid-xray-ml/main.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/ejecucion/README.md y docs/ejecucion/SPRINT_04_MODELOS.md; verificá aceptación y cierre 03, contratos/features/baseline y folds. Revisá raíz/remoto/rama/status/diff y preservá cambios.
Objetivo: comparación inicial reproducible de C1 HOG-scaler-SVM lineal, C2 LBP-RF y B1 HOG-scaler-logística L2 frente a B0. Creá src/models/candidatos.py, src/models/comparacion_cv.py, configs/modelos.json, tests/test_pipelines.py y resultados modelos_cv.csv, modelos_oof.csv y modelos.md con figuras pertinentes.
Fijá las configuraciones iniciales indicadas en el sprint antes de evaluar; ajustá cada Pipeline dentro de sus folds y conservá IDs, scores, métricas train/validation, media/desvío y tiempos. Documentá costo y avisos de convergencia sin ocultar fallos.
Restricciones: test prohibido, sin tuning/grillas, sin elegir ganador final, sin CNN y sin ampliar modelos opcionales por defecto. No ejecutes 05 o posteriores.
Probá aislamiento de fit, grupos, alineación de OOF/scores, clase positiva y serialización en desarrollo. Regenerá la comparación real y cumplí aceptación/DoD sin umbrales ficticios de rendimiento. Actualizá documentos afectados, decisiones, uso de IA, README, índice y checklist con resultados reales.
Revisá diff y git diff --check, stage explícito, commit 'feat: compare classical candidates on development folds' y push origin/main. Informá SHA, archivos, pruebas, resultados de desarrollo, límites y estado Git. No continúes a otro sprint.
```
