# Objetivo

Comparar C1 y C2 en sus configuraciones iniciales frente a B0 con los mismos folds de desarrollo. **Estado: cerrado el 08/11/2026.** Comparación inicial de los tres modelos y cinco folds verificados.

# Por qué lo hacemos

Esta comparación verifica el pipeline y ofrece evidencia inicial antes de la búsqueda pequeña. Compartir HOG reduce factores que cambian simultáneamente.

# Conceptos necesarios

Margen y C, árboles y ensemble, StandardScaler/Pipeline, CV, F1 macro, dispersión, convergencia y selección optimista.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 02 publicado en `acbf70c`. Usar `hog.npy`, `index.csv` y predicciones de Dummy en `data/processed/sprint_02/`. Verificarlos con el [procedimiento del Sprint 02](../../reports/hog_baseline.md#verificación-y-reproducción-interna). La separación de entrenamiento y validación usa `validation_fold` del manifiesto de 01.

# Tareas

- [x] Implementar C1 Pipeline(StandardScaler, LinearSVC), C=1, L2/squared_hinge, class_weight=None; registrar solver, tolerancias y max_iter, seed 42 donde aplique.
- [x] Implementar C2 RandomForestClassifier sobre el mismo HOG: 100 árboles, max_depth=None, min_samples_leaf=1, max_features=sqrt, bootstrap y class_weight=None, seed 42.
- [x] Evaluar ambos en los cinco folds existentes; ajustar scaler solo en train de cada fold. Reutilizar resultados B0 si corresponden exactamente al mismo protocolo.
- [x] Guardar métricas por fold y media ± desvío muestral; comparar F1 macro, recall/especificidad y fallos técnicos sin seleccionar por test.
- [x] Registrar tiempos aproximados y gráficos de comparación; curvas de aprendizaje solo si resuelven una duda concreta de desarrollo.
- [x] Documentar convergencia y límites. No añadir candidatos, cambiar HOG ni introducir PCA por prevención; una necesidad medida requiere decisión explícita antes de cambiar alcance.
- [x] Verificar resultados y actualizar el índice y los registros. Dejar el diff local para revisión. Commit y push requieren solicitud expresa.

# Archivos a crear/modificar

Las configuraciones iniciales están en `src/models.py` y la ejecución de CV en `src/comparacion.py`. [Métricas por fold](../../results/modelos_cv.csv), [informe](../../reports/modelos_cv.md) y [figura](../../reports/modelos_cv.png). Las predicciones por imagen y el resumen con los diagnósticos quedan en `data/processed/sprint_03/`, fuera de Git.

# Pruebas

Probar que scaler recibe únicamente train del fold, mismas IDs/folds en B0/C1/C2, ninguna intersección con test, reproducibilidad de configuración/semilla y resumen CV correcto. Comprobar avisos de convergencia y figuras con ejes/unidades. No repetir experimentos sin una causa concreta.

# Resultados esperados

Dos candidatos iniciales comparables, controles contra fuga y evidencia descriptiva frente a B0. La elección definitiva queda para 04.

# Criterios de aceptación

- [x] Solo B0, C1 y C2 sobre HOG común; scaler aislado por fold.
- [x] Métricas reales por fold, media/desvío y tiempos aproximados registrados.
- [x] Fallos y límites visibles; sin tuning ni test evaluado.
- [x] Documentación, predicciones OOF, pruebas y diff local verificados.

# Qué debemos saber explicar

Qué aprende cada candidato, qué hace el scaler y por qué RF no lo exige; por qué media/desvío CV no es intervalo de confianza; diferencia entre comparación inicial y selección tras tuning.

# Preguntas posibles de defensa

1. ¿Qué cambia al aumentar C?
2. ¿Qué hace el bootstrap interno de RF?
3. ¿Por qué RF no necesita el mismo scaler de SVM?
4. ¿Cómo se evita que validation influya en el scaler?
5. ¿Por qué usar los mismos folds para los tres modelos?
6. ¿Qué haríamos si un candidato no converge o no supera B0?

# Reproducción interna

Desde la raíz del repositorio, con el entorno de los sprints anteriores. Si faltan artefactos, regenerar 02 con su comando documentado. Para repetir un ajuste, elegir una ruta de salida nueva.

```powershell
.\.venv\Scripts\python.exe -m src.baseline --config configs/experimento.json --output data/processed/sprint_02 --verify-only
.\.venv\Scripts\python.exe -m src.comparacion --config configs/experimento.json --output data/processed/sprint_03
.\.venv\Scripts\python.exe -m src.comparacion --config configs/experimento.json --output data/processed/sprint_03 --verify-only --figure reports/modelos_cv.png
```

El último comando recalcula las métricas desde las predicciones guardadas y genera la figura.

# Prompt para Codex

```text
Ejecutá únicamente SPRINT_03_MODELOS_CV según su plan vigente. Leé primero README.md,
docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md,
docs/FUENTES_Y_TRAZABILIDAD.md, docs/ejecucion/README.md y el registro de ejecución
si existe; inspeccioná Git y las instrucciones aplicables. Verificá evidencia de cierre del sprint 02; no lo des por completo por existir un plan.
Conservá HOG fijo, B0 DummyClassifier, C1 SVM lineal con StandardScaler y C2 RF.
Respetá límites, entradas y orden de tareas de este sprint; los planes archivados
no son instrucciones activas. No añadas candidatos, descriptores, infraestructura
ni experimentos opcionales. Ejecutá las pruebas pertinentes y registrá evidencia
real, decisiones, limitaciones y uso de IA. Si falta intervención humana necesaria,
no la inventes: explicá el pendiente y avanzá solo en tareas independientes.
Actualizá documentación, checklist y estado según lo realmente completado.
Revisá el diff, ejecutá git diff --check e informá verificaciones y pendientes.
Hacé commit o push solo si el usuario lo solicita expresamente.
No ejecutes ni inicies el siguiente sprint.
```
