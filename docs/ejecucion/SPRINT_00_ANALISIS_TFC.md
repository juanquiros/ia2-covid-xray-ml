# Objetivo

Revisar y acordar la reconstrucción del TFC y el alcance simplificado con ambos integrantes. **Estado: no iniciado.** La lectura documental previa no constituye este cierre operativo.

# Por qué lo hacemos

La crítica y las decisiones futuras deben ser trazables y comprendidas. Este sprint comprueba el punto de partida académico sin iniciar experimentos.

# Conceptos necesarios

Clasificación supervisada, CNN, feature engineering, etiquetas operativas, CRISP-ML(Q), comparación contextual y diferencia entre evidencia e hipótesis.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Copias locales TFC-2023.pdf y consigna DOCX con hashes registrados; no copiar esos documentos al repositorio.

# Tareas

- [ ] Contrastar cuatro datasets, doce pruebas, arquitectura, stack y cifras con las fuentes ya localizadas.
- [ ] Revisar discrepancias D01–D08, fortalezas, limitaciones y denominadores de la consulta profesional.
- [ ] Confirmar tarea COVID=1 frente a normal=0 y comparación contextual si no se recupera D4 exacto.
- [ ] Acordar núcleo HOG fijo, B0 DummyClassifier, C1 SVM lineal y C2 RF; cinco folds y test reservado.
- [ ] Registrar comprensión/revisión real de ambos integrantes y preguntas abiertas; no atribuirles una aprobación que no dieron.
- [ ] Iniciar registro breve de ejecución y uso de IA, y listar datos administrativos pendientes.
- [ ] Verificar documentación, actualizar checklist y estado; commit y push del sprint. No iniciar 01.

# Archivos a crear/modificar

Crear `docs/REGISTRO_EJECUCION.md` y `docs/REGISTRO_IA.md`; corregir documentos existentes solo si aparece evidencia; actualizar este plan y el índice. No crear código ML.

# Pruebas

Comprobar citas/páginas, coherencia de totales y métricas documentales, enlaces y distinción entre test/validation. Confirmar que no se inventaron IDs de D4 ni resultados. Revisar evidencia de la intervención humana pendiente.

# Resultados esperados

Base conceptual aceptada por el equipo, críticas sustentadas, alcance único y dudas localizadas. No hay resultados experimentales ni datos descargados.

# Criterios de aceptación

- [ ] Tablas y arquitectura históricas verificadas, con discrepancias visibles.
- [ ] Los dos integrantes revisaron y pueden explicar las decisiones; si falta su revisión, informar cierre pendiente.
- [ ] Baseline y dos candidatos sin rutas adicionales; matriz académica cubierta.
- [ ] Registros, checklist y documentación coherentes; commit y push confirmados.

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

```text
Ejecutá únicamente SPRINT_00_ANALISIS_TFC según su plan vigente. Leé primero README.md,
docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md,
docs/FUENTES_Y_TRAZABILIDAD.md, docs/ejecucion/README.md y el registro de ejecución
si existe; inspeccioná Git y las instrucciones aplicables. No hay cierre previo de ejecución: la planificación documental no lo reemplaza.
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
