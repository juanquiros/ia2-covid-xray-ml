# Objetivo

Comparar C1 y C2 en sus configuraciones iniciales frente a B0 con los mismos folds de desarrollo. **Estado: no iniciado.**

# Por qué lo hacemos

Esta comparación verifica el pipeline y ofrece evidencia inicial antes de la búsqueda pequeña. Compartir HOG reduce factores que cambian simultáneamente.

# Conceptos necesarios

Margen y C, árboles y ensemble, StandardScaler/Pipeline, CV, F1 macro, dispersión, convergencia y selección optimista.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 02: HOG/IDs de desarrollo, baseline y funciones probadas; configuración y folds de 01.

# Tareas

- [ ] Implementar C1 Pipeline(StandardScaler, LinearSVC), C=1, L2/squared_hinge, class_weight=None; registrar solver, tolerancias y max_iter, seed 42 donde aplique.
- [ ] Implementar C2 RandomForestClassifier sobre el mismo HOG: 100 árboles, max_depth=None, min_samples_leaf=1, max_features=sqrt, bootstrap y class_weight=None, seed 42.
- [ ] Evaluar ambos en los cinco folds existentes; ajustar scaler solo en train de cada fold. Reutilizar resultados B0 si corresponden exactamente al mismo protocolo.
- [ ] Guardar métricas por fold y media ± desvío muestral; comparar F1 macro, recall/especificidad y fallos técnicos sin seleccionar por test.
- [ ] Registrar tiempos aproximados y gráficos de comparación; curvas de aprendizaje solo si resuelven una duda concreta de desarrollo.
- [ ] Documentar convergencia y límites. No añadir candidatos, cambiar HOG ni introducir PCA por prevención; una necesidad medida requiere decisión explícita antes de cambiar alcance.
- [ ] Verificar, actualizar checklist y registros; commit y push. No ejecutar tuning, test ni iniciar 04.

# Archivos a crear/modificar

Completar `src/models.py` y evaluación CV en `src/evaluation.py`; actualizar `configs/experimento.json`; guardar `results/modelos_cv.csv`, `reports/modelos_cv.md` y figura comparativa. Añadir pruebas de aislamiento y ajuste donde aporten evidencia.

# Pruebas

Probar que scaler recibe únicamente train del fold, mismas IDs/folds en B0/C1/C2, ninguna intersección con test, reproducibilidad de configuración/semilla y resumen CV correcto. Comprobar avisos de convergencia y figuras con ejes/unidades. No repetir experimentos sin una causa concreta.

# Resultados esperados

Dos candidatos iniciales comparables, controles contra fuga y evidencia descriptiva frente a B0. La elección definitiva queda para 04.

# Criterios de aceptación

- [ ] Solo B0, C1 y C2 sobre HOG común; scaler aislado por fold.
- [ ] Métricas reales por fold, media/desvío y tiempos aproximados registrados.
- [ ] Fallos y límites visibles; sin tuning ni test evaluado.
- [ ] Documentación y pruebas al día; commit y push confirmados.

# Qué debemos saber explicar

Qué aprende cada candidato, qué hace el scaler y por qué RF no lo exige; por qué media/desvío CV no es intervalo de confianza; diferencia entre comparación inicial y selección tras tuning.

# Preguntas posibles de defensa

1. ¿Qué cambia al aumentar C?
2. ¿Qué hace el bootstrap interno de RF?
3. ¿Por qué RF no necesita el mismo scaler de SVM?
4. ¿Cómo se evita que validation influya en el scaler?
5. ¿Por qué usar los mismos folds para los tres modelos?
6. ¿Qué haríamos si un candidato no converge o no supera B0?

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
Revisá el diff, hacé un commit coherente y push al remoto/rama del proyecto,
confirmá el resultado y reportá SHA, verificaciones y pendientes.
No ejecutes ni inicies el siguiente sprint.
```
