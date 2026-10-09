# Sprint 07 · Interpretación y análisis de errores

**Estado:** no iniciado. Depende del cierre 06.

# Objetivo

Explicar el comportamiento del modelo congelado, caracterizar errores y comunicar límites sin corregir el pipeline a partir del test.

# Por qué existe este sprint

Una métrica global no explica qué casos fallan ni qué señales utiliza el modelo. La consigna exige interpretación fundada y análisis de errores, con cautela sobre causalidad.

# Conocimientos previos necesarios

Coeficientes, importancia por impureza/permutación, correlación, PCA, FP/FN, sesgo de procedencia y límites clínicos. Teoría §19.

# Entradas

Cierre 06, predicciones congeladas, modelos/configuración, diccionario de features y metadatos publicables. Para importancia retenida en desarrollo usar estimadores de folds de la configuración congelada guardados en 05; un modelo ajustado en todo desarrollo no tiene holdout de desarrollo propio.

# Tareas

- [ ] Verificar aceptación 06 y hashes de predicciones/pipeline.
- [ ] Definir muestra reproducible de FP/FN y aciertos, con distribución por clase/fuente/calidad disponible.
- [ ] Reutilizar predicciones finales sin recalcular elección ni entrenar otro final.
- [ ] Para modelo lineal, mapear coeficientes a grupos HOG considerando scaler y PCA si existe.
- [ ] Para RF, contrastar importancia por impureza con permutaciones agrupadas y repetidas en validation de modelos de fold congelados.
- [ ] Documentar cuando no existe holdout apropiado para importancia: evitar llamarla evidencia independiente si se calcula sobre train.
- [ ] Relacionar errores con metadatos disponibles sin inferir diagnósticos o atributos sensibles por apariencia.
- [ ] Separar observación, hipótesis y futura mejora; justificar SHAP solo si aporta una respuesta nueva.
- [ ] Elaborar límites, ética y monitoreo conceptual; dejar mejoras de modelos para otro protocolo futuro.

# Archivos futuros involucrados

Crear `src/evaluation/interpretacion.py`, `tests/test_interpretacion.py`, `results/reports/errores_interpretabilidad.md`, `results/metrics/errores_por_grupo.csv`, `results/metrics/importancias.csv` y figuras autorizadas. Modificar discusión, comparativa, teoría cuando corresponda y documentos operativos. No modificar modelo final ni predicciones de test.

# Implementación esperada

Análisis descriptivo sobre resultados existentes con denominadores explícitos. Permutar grupos HOG/regiones LBP, registrar métrica, repeticiones y variación. La explicación global en desarrollo retenido se calcula con sus estimadores de fold, no fingiendo independencia del modelo ajustado a todo desarrollo. Coeficientes pueden describir el final directamente, con límites por correlación y escala. SHAP opcional no debe disparar un nuevo proyecto.

# Pruebas

Verificar identidad de hashes finales antes/después; todos los casos de error coinciden con predicciones almacenadas; conteos por grupo suman sus denominadores; correspondencia feature↔región y retroproyección PCA controlada con ejemplo sintético; permutaciones reproducibles y sin fit nuevo del final. Revisar visualmente figuras y ausencia de datos personales.

# Resultados esperados

Explicaciones técnicas con evidencia y límites, taxonomía de errores y propuestas de mejora futuras. No nuevos resultados de selección ni afirmaciones de mecanismos clínicos demostrados.

# Criterios de aceptación

Modelo/test intactos, casos seleccionados por protocolo reproducible, denominadores claros, técnica adecuada al modelo y representación, incertidumbre/correlación reconocidas, explicación de datos usada sin afirmar causalidad médica y riesgos éticos documentados.

# Evidencias a conservar

IDs autorizados de casos, reglas de muestreo, tablas por grupo, pesos/importancias, estimadores de folds identificados, seeds y figuras con leyendas. No divulgar radiografías si permisos no están claros; reemplazar por resúmenes no identificatorios.

# Riesgos

Explicaciones inestables, importancia repartida entre variables correlacionadas, sesgo de selección de ejemplos y confundir un borde de texto con signo patológico.

# Errores frecuentes

Usar mapas HOG como “atención del modelo”, permutar train y llamarlo generalización, olvidar escalado al leer coeficientes, ajustar modelo para corregir FN de test y exigir SHAP sin objetivo.

# Qué debemos comprender antes de cerrarlo

Qué explica realmente cada método, cómo la representación limita interpretación y qué mejoras requieren una nueva evaluación independiente.

# Preguntas posibles de defensa

1. ¿Importancia de una feature implica causalidad?
2. ¿Por qué importa la correlación al permutar?
3. ¿Cómo se interpreta un coeficiente después de PCA?
4. ¿Cómo elegimos FP/FN sin sesgar ejemplos?
5. ¿Qué información falta para evaluar equidad?
6. ¿Por qué no corregimos ahora los errores observados en test?
7. ¿Cuándo aportaría SHAP algo útil?

# Definition of Done

Errores e interpretación sustentados, pruebas/criterios completos, artefactos finales sin cambios, documentación/checklist actualizados, commit y push. No iniciar 08 automáticamente.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá únicamente SPRINT_07_INTERPRETABILIDAD en juanquiros/ia2-covid-xray-ml/main.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/ejecucion/README.md y docs/ejecucion/SPRINT_07_INTERPRETABILIDAD.md; verificá cierre/criterios 06, resultados congelados, modelos y diccionario de features. Revisá raíz/remoto/rama/status/diff y preservá trabajo previo.
Objetivo: interpretación y errores sin cambiar decisiones finales. Creá src/evaluation/interpretacion.py, tests/test_interpretacion.py, errores_interpretabilidad.md, errores_por_grupo.csv, importancias.csv y figuras autorizadas.
Reutilizá predicciones de 06 para FP/FN/aciertos y estratos conocidos, con muestreo reproducible y denominadores. Aplicá coeficientes de modelos lineales con escalas/PCA correctas o permutación agrupada en validation de estimadores de fold congelados. No confundas importancia en train con evidencia retenida. Separá observaciones, hipótesis y mejoras futuras; SHAP solo con necesidad específica justificada.
Restricciones: no modificar final, no reentrenar para corregir test, no elegir nuevos umbrales, no diagnosticar ni publicar imágenes/metadatos personales sin permiso. No ejecutar 08 o posteriores.
Probá hashes intactos, correspondencia casos-predicciones, sumas, mapa feature/región, retroproyección y reproducibilidad de permutaciones; revisá figuras y privacidad. Cumplí aceptación/DoD y documentá hallazgos reales con límites y ética.
Actualizá comparativa, discusión, uso de IA, README, índice y checklist. Revisá diff/check, agregá solo artefactos publicables, commit 'analysis: explain frozen model behavior and errors' y push origin/main. Informá SHA, pruebas, archivos, limitaciones y estado Git. Finalizá sin avanzar a otro sprint.
```
