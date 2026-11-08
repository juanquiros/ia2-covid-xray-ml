# Objetivo

Implementar el preprocesamiento único, HOG fijo y B0 sobre desarrollo. **Estado: cerrado el 08/11/2026.** Matriz HOG, índice y cinco resultados de Dummy verificados en desarrollo.

# Por qué lo hacemos

Ambos candidatos compartirán una representación verificable. La baseline ofrece una referencia mínima antes de entrenar modelos capaces de usar imágenes.

# Conceptos necesarios

Gradiente, celda, bloque, L2-Hys, longitud del vector, transformación por imagen, DummyClassifier y métricas por clase.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 01 publicado en `55315df`. Usar `data/processed/sprint_01/manifiesto.csv` con el SHA-256 del [registro de ejecución](../REGISTRO_EJECUCION.md). Si falta, seguir la [reproducción de 01](SPRINT_01_DATOS_EDA.md#reproducción-local) antes de extraer HOG.

# Tareas

- [x] Reutilizar grises y resize a 128 × 128 según el contrato de 01.
- [x] Reutilizar HOG con `orientations=9`, `pixels_per_cell=(8,8)`, `cells_per_block=(2,2)`, `block_norm="L2-Hys"` y `transform_sqrt=False`.
- [x] Extraer únicamente desarrollo, conservando correspondencia exacta ID/etiqueta/vector; verificar 8100 atributos finitos.
- [x] Reutilizar `DummyClassifier(strategy="most_frequent")` y evaluarlo sobre los cinco folds del manifiesto.
- [x] Guardar métricas por fold, media/desvío muestral, distribución de predicciones y convención de divisiones por cero; explicar resultado trivial.
- [x] Registrar tiempo aproximado de extracción y dimensión; no crear profiling ni infraestructura de cache compleja.
- [x] Verificar resultados, actualizar el índice y los registros y dejar el diff local para revisión. Commit y push requieren solicitud expresa.

# Archivos a crear/modificar

La ejecución de `src/baseline.py` reutiliza `src/features.py`, `src/models.py` y las métricas compartidas en `src/evaluation.py`. La configuración fija el manifiesto de 01 y su SHA-256. Los resultados agregados están en [baseline_cv.csv](../../results/baseline_cv.csv) y el [informe del Sprint 02](../../reports/hog_baseline.md) incluye los comandos internos. La matriz, el índice y las predicciones por imagen quedan en `data/processed/sprint_02/`, fuera de Git.

# Pruebas

Comprobar forma/rango del preprocesamiento, HOG de 8100 atributos finitos/deterministas, igualdad de función de extracción para futuras rutas e IDs alineados. Probar métricas sobre una matriz pequeña calculable a mano y comportamiento de B0 cuando predice una sola clase. Verificar uso exclusivo de desarrollo.

# Resultados esperados

Representación HOG funcional, trazable y documentada; primera baseline CV real, sin candidatos ni test evaluados.

# Criterios de aceptación

- [x] HOG exacto y sin descriptores alternativos ni PCA.
- [x] B0 guarda cinco resultados y resumen descriptivo, con convención de métricas definida.
- [x] Contratos e IDs probados; evidencia de que test no se evaluó.
- [x] Resultados reales documentados, con pruebas pertinentes y diff verificado.

# Qué debemos saber explicar

Cómo 15×15 bloques por 2×2 celdas por 9 bins dan 8100 features; por qué HOG no aprende etiquetas; por qué la baseline puede tener accuracy aceptable y F1 macro bajo.

# Preguntas posibles de defensa

1. ¿Qué representan las orientaciones del gradiente?
2. ¿Por qué se normalizan bloques y no solo la imagen?
3. ¿Cómo obtenemos exactamente 8100 features?
4. ¿DummyClassifier utiliza los valores de HOG?
5. ¿Por qué no todas las métricas de B0 valen 0,5 en datos balanceados?
6. ¿Una visualización HOG indica enfermedad o importancia predictiva?

# Prompt para Codex

```text
Ejecutá únicamente SPRINT_02_HOG_BASELINE según su plan vigente. Leé primero README.md,
docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md,
docs/FUENTES_Y_TRAZABILIDAD.md, docs/ejecucion/README.md y el registro de ejecución
si existe; inspeccioná Git y las instrucciones aplicables. Verificá evidencia de cierre del sprint 01; no lo des por completo por existir un plan.
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
