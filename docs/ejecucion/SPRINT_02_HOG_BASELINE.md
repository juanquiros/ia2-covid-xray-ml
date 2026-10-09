# Objetivo

Implementar el preprocesamiento único, HOG fijo y B0 sobre desarrollo. **Estado: no iniciado.**

# Por qué lo hacemos

Ambos candidatos compartirán una representación verificable. La baseline ofrece una referencia mínima antes de entrenar modelos capaces de usar imágenes.

# Conceptos necesarios

Gradiente, celda, bloque, L2-Hys, longitud del vector, transformación por imagen, DummyClassifier y métricas por clase.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 01: entorno, datos autorizados, manifiesto/folds y contrato de preprocesamiento.

# Tareas

- [ ] Implementar grises y resize 128×128 según contrato de 01 en una función común.
- [ ] Implementar HOG con orientations=9, pixels_per_cell=(8,8), cells_per_block=(2,2), block_norm=L2-Hys y transform_sqrt=False. Sin búsqueda de parámetros.
- [ ] Extraer únicamente desarrollo, conservando correspondencia exacta ID/etiqueta/vector; verificar 8100 atributos finitos.
- [ ] Implementar B0 DummyClassifier(strategy="most_frequent") y evaluarlo sobre los cinco folds acordados.
- [ ] Guardar métricas por fold, media/desvío muestral, distribución de predicciones y convención de divisiones por cero; explicar resultado trivial.
- [ ] Registrar tiempo aproximado de extracción y dimensión; no crear profiling ni infraestructura de cache compleja.
- [ ] Verificar, documentar y actualizar checklist/registros; commit y push. No entrenar C1/C2 ni iniciar 03.

# Archivos a crear/modificar

Crear `src/features.py` y baseline mínima en `src/models.py`; función de métricas compartida en `src/evaluation.py` si se necesita. Actualizar configuración; guardar `results/baseline_cv.csv`, `reports/hog_baseline.md` y pruebas de contratos en `tests/`. No crear infraestructura vacía.

# Pruebas

Comprobar forma/rango del preprocesamiento, HOG de 8100 atributos finitos/deterministas, igualdad de función de extracción para futuras rutas e IDs alineados. Probar métricas sobre una matriz pequeña calculable a mano y comportamiento de B0 cuando predice una sola clase. Verificar uso exclusivo de desarrollo.

# Resultados esperados

Representación HOG funcional, trazable y documentada; primera baseline CV real, sin candidatos ni test evaluados.

# Criterios de aceptación

- [ ] HOG exacto y sin descriptores alternativos ni PCA.
- [ ] B0 guarda cinco resultados y resumen descriptivo, con convención de métricas definida.
- [ ] Contratos e IDs probados; evidencia de que test no se evaluó.
- [ ] Resultados reales distinguidos de ejemplos didácticos; commit y push confirmados.

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
Revisá el diff, hacé un commit coherente y push al remoto/rama del proyecto,
confirmá el resultado y reportá SHA, verificaciones y pendientes.
No ejecutes ni inicies el siguiente sprint.
```
