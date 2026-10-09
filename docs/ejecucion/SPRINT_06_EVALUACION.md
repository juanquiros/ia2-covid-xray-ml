# Sprint 06 · Test final y comparación

**Estado:** no iniciado. Depende del cierre 05 y protocolo congelado.

# Objetivo

Evaluar una sola vez el final y los comparadores predefinidos en test, documentar incertidumbre/costo y contrastar con el TFC al nivel de equivalencia disponible.

# Por qué existe este sprint

Se necesita una evaluación independiente de selección y tuning. La elección ya se realizó en 05: aquí se confirma su registro y se estima desempeño, aunque otro comparador obtenga mejor test.

# Conocimientos previos necesarios

Matriz/métricas, scores, umbrales, intervalos, McNemar, dependencia entre grupos, comparabilidad y benchmark. Teoría §§16–19,21.

# Entradas

Cierre 05, hashes de pipelines/configuración/test, protocolo final, versión de datos, comparadores y referencias originales. Predicciones CNN individuales solo si existen y son válidas para el mismo test con entrenamiento independiente.

# Tareas

- [ ] Verificar cierre 05, hashes, selección previa, test sin evaluación y supuestos estadísticos predefinidos.
- [ ] Probar el evaluador sobre fixtures, no sobre test, antes de habilitar el acceso final.
- [ ] Abrir test para un único lote de predicción del final, B0, C1/C2 y B1 si está incluido; registrar momento y configuración.
- [ ] Guardar predicciones/scores por ID y modelo de forma inmutable con hash, sin reajustar transformaciones.
- [ ] Calcular matriz, accuracy, precision/recall/F1 por clase, F1 macro, especificidad, ROC-AUC y AP según scores/clases disponibles.
- [ ] Aplicar intervalos y contraste primario únicamente si el protocolo y supuestos lo permiten; justificar omisiones.
- [ ] Medir costo completo, extracción, ajuste/búsqueda provenientes de logs, RAM y artefacto; registrar hardware/hilos y condiciones de latencia.
- [ ] Comparar con 79,47 % y demás métricas históricas sin afirmar equivalencia inexistente; no calcular prueba pareada con valores agregados.
- [ ] Documentar resultados positivos o negativos y cerrar test para decisiones futuras; no sustituir ganador por otro con mejor test.

# Archivos futuros involucrados

Crear `src/evaluation/evaluar_final.py`, `src/evaluation/estadistica.py`, `src/evaluation/recursos.py`, `tests/test_evaluacion_final.py`, `results/metrics/test_predicciones.csv`, `results/metrics/test_metricas.csv`, `results/metrics/recursos.csv`, figuras de evaluación y `results/reports/evaluacion_final.md`. Los CSV por imagen solo se publican con IDs no personales autorizados; si no, hash/resumen y acceso local. Modificar documentos con resultados etiquetados como reales sin borrar la historia de propuestas.

# Implementación esperada

Evaluador idempotente que detecta registro previo y reutiliza predicciones para tablas/figuras en vez de ejecutar nuevas evaluaciones adaptativas. El primer lote no hace fit. Si falla técnicamente, conservar incidencia y salidas parciales; reanudar bajo protocolo idéntico, sin elegir umbrales/modelos por datos ya vistos. No fingir un nuevo test intacto.

McNemar usa b/c de dos modelos fijos en los mismos IDs independientes; versión exacta cuando corresponda. Sin CNN comparable, contraste primario final frente a B0 y comparación CNN descriptiva. Bootstrap pareado/grupal según protocolo de 05, no cinco folds tratados como muestras independientes. Latencias repetidas sobre lote de benchmark predefinido de desarrollo no abren nuevas decisiones de test.

# Pruebas

Matrices manuales, signo de score COVID, orden de labels, unidades de tiempo, control de división por cero y AUC indefinida. Ejemplos pareados con discordancias conocidas para McNemar; verificar remuestreo por grupos y seeds, tablas suman N y hashes permanecen. Asegurar que una segunda invocación reutiliza archivo y no permite nuevos modelos/thresholds bajo mismo protocolo.

# Resultados esperados

Métricas finales reales con tamaños de muestra, intervalos cuando válidos, costos y comparación honesta. Pueden ser inferiores a baseline o CNN; no hay resultado numérico obligatorio.

# Criterios de aceptación

Protocolo preexistente e inalterado, una apertura evaluativa registrada, ausencia de fit/test y de reselección; predicciones y métricas alineadas; pruebas correctas; estadística justificada; nivel de comparación CNN explícito; figuras/tablas interpretadas y resultados reproducibles desde predicciones congeladas.

# Evidencias a conservar

Protocolo, SHA de configuración/modelos/datos, registro de apertura, predicciones y su hash, métricas completas, tablas discordantes, método de intervalo, benchmark y limitaciones. No descartar casos problemáticos después de medir.

# Riesgos

Test históricamente usado por CNN, muestra pequeña/no independiente, comparaciones múltiples, métricas calculadas sobre clase incorrecta y costo medido en condiciones distintas.

# Errores frecuentes

Elegir ganador en test, retocar threshold, aplicar Wilcoxon ingenuo a folds, afirmar igualdad por p>0,05, comparar tiempos sin extracción o llamar cero a métricas no disponibles.

# Qué debemos comprender antes de cerrarlo

Qué inferencia permite cada comparación, qué no se puede concluir y por qué conservar resultados desfavorables. Diferenciar precisión estadística, desempeño y utilidad clínica.

# Preguntas posibles de defensa

1. ¿Cuándo se eligió el modelo final?
2. ¿Cuántas veces se abrió test y para qué?
3. ¿Por qué no cambiar de ganador si otro tiene mejor test?
4. ¿Qué necesita una comparación pareada con CNN?
5. ¿Qué significa un intervalo amplio?
6. ¿Cómo medimos costo de extremo a extremo?
7. ¿Qué supuestos impidieron alguna prueba estadística?

# Definition of Done

Evaluación completa sin reselección, controles y criterios satisfechos, datos derivados congelados, documentos/checklist actualizados, commit y push. No iniciar 07 automáticamente ni volver a optimización.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá solo SPRINT_06_EVALUACION de juanquiros/ia2-covid-xray-ml/main.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/ejecucion/README.md y docs/ejecucion/SPRINT_06_EVALUACION.md; comprobá cierre/aceptación 05, protocolo_congelado, selección, hashes y test sin evaluación previa. Revisá root/remote/branch/status/diff y preservá cambios.
Objetivo: evaluación final única, no selección. Creá src/evaluation/evaluar_final.py, estadistica.py, recursos.py, tests/test_evaluacion_final.py y resultados test_predicciones.csv, test_metricas.csv, recursos.csv, figuras e informe evaluacion_final.md.
Primero validá evaluador con fixtures y todos los supuestos; luego evaluá en un único lote solo final y comparadores congelados, sin fit. Guardá predicciones/scores por ID con hash; generá métricas e intervalos desde ese archivo. Aplicá McNemar u otra prueba solo si protocolo y supuestos lo permiten; no usar folds dependientes como experimentos independientes. CNN histórica solo descriptiva salvo evidencia de equivalencia y pares individuales válidos. Medí costo completo según protocolo.
Restricciones: no tuning, no nuevos modelos/thresholds, no exclusiones guiadas por test, no cambiar ganador ni entrenar CNN; no ejecutar 07 o posteriores. Si hay ejecución previa, reutilizá predicciones; si hay fallo, conservá incidencia y no reinicies pretendiendo independencia.
Ejecutá pruebas de matrices/labels/scores, métricas indefinidas, discordancias, remuestreo por grupos, unidades y prevención de reevaluación. Cumplí criterios/DoD y documentá resultados reales aunque sean desfavorables, con incertidumbre y límites.
Actualizá documentación afectada, comparativa, uso de IA, README, índice y checklist. Revisá diff/check, stage de datos derivados publicables, commit 'evaluation: report frozen test results and valid comparisons' y push origin/main. Informá SHA, pruebas, métricas reales, archivos y estado Git. No continúes a otro sprint.
```
