# Objetivo

Revisar y acordar la reconstrucción del TFC y el alcance simplificado con ambos integrantes. **Estado al 05/11/2026: cerrado.** El [registro de ejecución](../REGISTRO_EJECUCION.md#00--análisis-crítico-del-tfc--05112026) consigna la confirmación de ambos integrantes.

# Por qué lo hacemos

La crítica y las decisiones futuras deben ser trazables y comprendidas. Este sprint comprueba el punto de partida académico sin iniciar experimentos.

# Conceptos necesarios

Clasificación supervisada, CNN, feature engineering, etiquetas operativas, CRISP-ML(Q), comparación contextual y diferencia entre evidencia e hipótesis.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Copias locales del TFC en OneDrive y de la consigna de Descargas, identificadas por hash en [Fuentes](../FUENTES_Y_TRAZABILIDAD.md). Ambas se conservan fuera de Git.

# Tareas

- [x] Contrastar cuatro datasets, doce pruebas, arquitectura, stack y cifras con las fuentes ya localizadas.
- [x] Revisar discrepancias D01–D08, fortalezas, limitaciones y denominadores de la consulta profesional.
- [x] Documentar COVID=1 frente a normal=0, las evidencias faltantes de D4 y el carácter histórico de la CNN mientras falte equivalencia.
- [x] Documentar HOG fijo, RF como propuesta principal, SVM lineal con escalado como segundo candidato y `DummyClassifier(strategy="most_frequent")` como línea base. Selección por F1 macro medio en desarrollo, con cinco folds comunes si los datos y grupos lo permiten y test reservado.
- [x] Registrar por separado la confirmación de Juan Quirós y Andruszyszyn y las preguntas abiertas de la revisión.
- [x] Actualizar los registros existentes de ejecución e IA y dejar identificados los pendientes administrativos y de datos.
- [x] Verificar documentación, enlaces y diff. Dejar los cambios locales listos para revisión. Commit y push requieren solicitud expresa.

# Archivos a crear/modificar

Actualizar [ejecución](../REGISTRO_EJECUCION.md), [uso de IA](../REGISTRO_IA.md), este plan, el índice y los puntos afectados del README, roadmap, comparativa y fuentes.

# Pruebas

Comprobar citas/páginas, coherencia de totales y métricas documentales, enlaces y distinción entre test/validation. Confirmar que no se inventaron IDs de D4 ni resultados. Comprobar que las dos confirmaciones estén asentadas.

# Resultados esperados

Análisis crítico y alcance listos para revisión de ambos integrantes, con los pendientes de D4 identificados. Los resultados de 00-A se conservan como evidencia preliminar separada.

# Criterios de aceptación

- [x] Tablas y arquitectura históricas verificadas, con discrepancias visibles.
- [x] Registrar la confirmación de cada integrante de que revisó el análisis y puede explicar las decisiones.
- [x] Línea base y dos candidatos definidos. Matriz académica cotejada con la consigna.
- [x] Registros, checklist y documentación coherentes. Diff local verificado.

# Qué debemos saber explicar

Por qué D4 enfrenta COVID a normales, por qué 79,47 % no es un objetivo obligatorio, qué se puede reconstruir y qué permanece incierto, y por qué cambiamos representación y familia de modelos.

# Preguntas posibles de defensa

1. ¿Qué aprende la CNN y qué fijaremos mediante HOG?
2. ¿Cómo cambian las etiquetas entre D1, D2, D3 y D4?
3. ¿Por qué el mejor resultado usa test y qué límite introduce?
4. ¿Qué evidencia confirma dos pooling?
5. ¿Por qué 41/52 y 37/49 no prueban superioridad frente al médico?
6. ¿Qué no podemos afirmar sin IDs/versiones originales?

# Prompt para Codex

Material operativo interno.

```text
Ejecutá únicamente SPRINT_00_ANALISIS_TFC según su plan vigente. Leé primero README.md,
docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md,
docs/FUENTES_Y_TRAZABILIDAD.md, docs/ejecucion/README.md y el registro de ejecución
si existe; inspeccioná Git y las instrucciones aplicables. Tomá el piloto 00-A como antecedente y registrá por separado el estado de 00.
Conservá el alcance técnico documentado arriba y la selección en desarrollo.
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
