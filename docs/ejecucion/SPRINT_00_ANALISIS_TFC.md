# Sprint 00 · Análisis estructurado del TFC

**Estado:** no iniciado. Este archivo es un plan; la lectura realizada durante la planificación sirve como entrada, no como cierre del sprint.

# Objetivo

Convertir el análisis preliminar en una base de evidencia auditable y comprendida por ambos integrantes, con requisitos y decisiones pendientes explícitos.

# Por qué existe este sprint

Las cantidades, etiquetas y fragmentos de código del TFC presentan diferencias que no deben propagarse como certezas. Antes de implementar necesitamos saber qué replicar, qué cambiar y qué no podemos verificar.

# Conocimientos previos necesarios

Clasificación supervisada, matriz de confusión, train/validation/test, arquitectura CNN y distinción [A]/[B]/[C]/[D]. Estudiar secciones 1–7 de teoría y la reconstrucción del roadmap.

# Entradas

Los dos documentos primarios y hashes en `docs/FUENTES_Y_TRAZABILIDAD.md`; roadmap, teoría, comparativa y este índice. Verificar fuente completa de 103 páginas y consigna, no solo artículo CACIC.

# Tareas

- [ ] Verificar repositorio, rama, cambios previos y acceso a ambas fuentes.
- [ ] Contrastar las afirmaciones del roadmap con páginas, tablas y anexos; mantener discrepancias D01–D08.
- [ ] Crear matriz de cuatro datasets y doce pruebas con clase/métrica/partición inequívocas.
- [ ] Registrar arquitectura de tres convoluciones y dos pooling, escala de inferencia y límites de reproducción.
- [ ] Consolidar requisitos de consigna y pendientes administrativos/de datos.
- [ ] Clasificar hechos, decisiones e hipótesis, sin considerar demostrada una fuga entre pacientes.
- [ ] Registrar decisión preliminar B0/B1/C1/C2, estrategia de partición y condiciones para dataset equivalente.
- [ ] Preparar preguntas para obtener IDs/versión/splits originales y autorización de cátedra si corresponde; no contactar a terceros sin instrucción.
- [ ] Registrar uso de IA y revisión/comprensión de los dos estudiantes; actualizar documentación y checklist con evidencia real.

# Archivos futuros involucrados

Crear `results/reports/analisis_tfc.md`, `results/reports/matriz_requisitos.md`, `docs/DECISIONES.md` y `docs/USO_IA.md`. Modificar, si hay correcciones verificadas, roadmap, teoría, comparativa, fuentes, README raíz, índice y este sprint. No copiar fuentes completas a Git sin permiso ni crear carpetas de código vacías.

# Implementación esperada

Proceso documental, sin ML: matriz afirmación→fuente/localizador→tipo→grado de certeza→decisión afectada. Tablas derivadas deben indicar operaciones y datos de origen. Documentar cómo los integrantes pueden explicar etiquetas, particiones y la diferencia entre validation y test. Conservar incógnitas cuando no hay manifiestos, sin inventar conteos exactos.

# Pruebas

Verificar hashes y paginación; contrastar las 12 filas con tabla 17; comprobar 197+49+52+194=492 en prueba 10 y denominadores 52/49 de validación profesional. Revisar enlaces Markdown y requisitos contra consigna. No escribir ni ejecutar entrenamiento para “confirmar” el PDF.

# Resultados esperados

Una auditoría documental reproducible y un registro de decisiones; ninguna métrica experimental propia. Solicitudes pendientes identificadas con responsable, condición de cierre e impacto.

# Criterios de aceptación

Fuentes presentes y verificadas; las 12 pruebas y 4 datasets trazables; inconsistencias y limitaciones conservadas; matriz de requisitos completa; tarea futura definida con baseline y dos candidatos; estudiantes cuentan con explicación registrada. Una duda de IDs puede permanecer abierta y bloquear solo la ruta exacta de datos, no falsearse para cerrar el análisis.

# Evidencias a conservar

Hashes, citas por página/sección, tablas de auditoría, preguntas pendientes, decisiones razonadas, registro de IA y resultados de verificación documental. Fuentes y extracciones completas permanecen locales.

# Riesgos

Confundir lectura preliminar con aceptación, transcribir porcentajes sin clase/partición, asumir que todas las bibliotecas tienen versiones conocidas o atribuir causalidad a la limpieza.

# Errores frecuentes

Declarar D1 perfectamente balanceado; usar 90,34 % como test; añadir un tercer pooling; comparar 41/52 con 37/49 como prueba de superioridad; llamar a un problema de escala “leakage confirmado”.

# Qué debemos comprender antes de cerrarlo

Qué tarea cambia entre D1/D2 y D4, qué prueba sirve como referencia histórica y qué información falta para comparación controlada. Ambos integrantes deben poder ubicar la evidencia y explicar sus límites.

# Preguntas posibles de defensa

1. ¿Cuáles son los cuatro datasets y qué significa cada etiqueta?
2. ¿Qué diferencia existe entre resultado reportado y reproducido?
3. ¿Por qué no puede reconstruirse exactamente D4 solo con 2462 por clase?
4. ¿Qué contradicción hay entre validation y test de prueba 9?
5. ¿Qué evidencia aporta el código anexado sobre normalización?
6. ¿Qué significa el 75 % de concordancia con el médico?
7. ¿Qué requiere la consigna además de entrenar un modelo?

# Definition of Done

Tareas y criterios anteriores satisfechos con enlaces a evidencias; documentos coherentes; sin datos descargados ni ML implementado; revisión documental registrada; checklist e índice actualizados; un commit del sprint y push confirmado. No comenzar 01 automáticamente.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá exclusivamente SPRINT_00_ANALISIS_TFC en juanquiros/ia2-covid-xray-ml.
Objetivo: auditar documentalmente el TFC y la consigna, consolidar requisitos y decisiones sin implementar ML.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/FUENTES_Y_TRAZABILIDAD.md, docs/ejecucion/README.md y docs/ejecucion/SPRINT_00_ANALISIS_TFC.md; localizá las dos fuentes primarias y comprobá hashes.
Revisá git root, remote -v, branch --show-current, status y diferencias existentes; trabajá solo en el repositorio oficial y main, preservando trabajo previo.
Creá results/reports/analisis_tfc.md, results/reports/matriz_requisitos.md, docs/DECISIONES.md y docs/USO_IA.md. Aplicá el proceso de trazabilidad afirmación/fuente/tipo/certeza; verificá cuatro datasets, doce pruebas, arquitectura, denominadores y discrepancias documentadas.
Restricciones: no descargar dataset, no entrenar, no producir métricas propias, no contactar terceros, no ejecutar sprint 01 o posteriores. Si falta una fuente, detené lo dependiente y reportá el faltante. Conservá incógnitas en lugar de inventar exactitud.
Pruebas: hashes, referencias, sumas de tablas, diferencias validation/test, enlaces y cobertura de consigna. Cumplí todos los criterios de aceptación y Definition of Done del sprint; documentá los resultados reales de esa revisión y la comprensión pendiente del equipo.
Actualizá los documentos afectados, README raíz, índice operativo y checklist; agregá Cierre real solo con evidencias efectivas. El resultado esperado es una auditoría, no un modelo.
Revisá diff y git diff --check; agregá solo archivos del sprint; realizá un commit 'docs: audit TFC evidence and TFI requirements' y push a origin/main. Informá SHA, archivos, verificaciones, pendientes y estado Git. No inicies otro sprint.
```
