# Objetivo

Integrar resultados existentes en informe académico y defensa completa. **Estado: no iniciado.** No agregar experimentos.

# Por qué lo hacemos

El aporte del TFI se sostiene con evidencia, discusión y comprensión de ambos integrantes; no depende de alcanzar un umbral de accuracy.

# Conceptos necesarios

Comparación contextual/controlada, límites, ética, comunicación científica, citas, uso declarado de IA y despliegue conceptual.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 04 y resultados guardados, fuentes primarias, registros de IA, consigna y rúbrica. Datos administrativos y modalidad confirmados por equipo/cátedra.

# Tareas

- [ ] Redactar análisis del TFC, fundamentos, datos, pipeline, CV/tuning, resultados, errores, interpretación, discusión, límites, conclusiones y trabajos futuros sin programar nuevas pruebas.
- [ ] Comparar con CNN solo al nivel de equivalencia demostrado; conservar referencia 79,47 %, precision 0,7912, recall 0,8008 y F1 0,7960 como cifras históricas.
- [ ] Discutir privacidad/licencia, sesgo, FP/FN y límites académicos. Describir integración, costo/latencia, monitoreo, drift y reentrenamiento solo conceptualmente.
- [ ] Preparar PDF A4, márgenes 2,5 cm, Arial/Times 11–12, interlineado 1,15–1,5, numeración y 20–30 páginas orientativas sin anexos; nombre TFI_IA2_Quiros_Andruszyszyn.
- [ ] Completar carátula, resumen ≤250 palabras y palabras clave en español e inglés, índices general/figuras/tablas, referencias IEEE uniformes y anexo obligatorio de IA con propósito/verificación/versiones conocidas.
- [ ] Verificar cada figura/tabla numerada, ejes/unidades, citas y explicación en texto; no inventar campos administrativos ni resultados faltantes.
- [ ] Dejar repositorio accesible o ZIP según consigna e instrucciones reproducibles. Ensayar comandos en entorno limpio con pruebas/ejemplos de desarrollo y tablas desde predicciones guardadas, sin volver a evaluar test ni entrenar nuevas alternativas.
- [ ] Preparar presentación y ensayo de ambos integrantes; confirmar [15] minutos de exposición y [10] preguntas, fecha y plataforma. Revisar toda rúbrica y comprensión individual.
- [ ] Actualizar checklist/registros y estado final; commit y push. Informar pendientes humanos reales sin simular defensa realizada.

# Archivos a crear/modificar

Crear fuente editable de informe y PDF en `reports/`, presentación/material de defensa y guía de reproducción. Actualizar README, comparativa con resultados reales identificados, registros de ejecución/IA e índice. Usar resultados existentes; no cambiar módulos ML para ampliar experimentos.

# Pruebas

Revisar formato/renderizado de PDF, enlaces/citas, cálculos contra archivos guardados, cobertura de §§5.1–5.8 y §7, anexo IA y rúbrica. Comprobar guía en entorno limpio sin nuevo test. Ensayo humano real de explicación y preguntas; registrar lo pendiente si aún no ocurrió.

# Resultados esperados

Entrega legible y trazable, comparación honesta, límites y despliegue conceptual, repositorio accesible y preparación de defensa. Ninguna métrica nueva se genera en este sprint.

# Criterios de aceptación

- [ ] Informe y anexos cubren consigna, formato y fuentes; campos administrativos confirmados o pendientes visibles.
- [ ] Resultados coinciden con 04; no hay experimentos añadidos ni nueva selección.
- [ ] Despliegue/monitoreo solo conceptuales; IA declarada y figuras verificadas.
- [ ] Ambos integrantes prepararon defensa y revisaron rúbrica; no declarar ensayo sin evidencia humana.
- [ ] Entregables, guía, checklist y commit/push comprobados.

# Qué debemos saber explicar

Todo el proyecto: crítica del original, fundamentos, decisiones, código y resultados; errores y límites; reproducibilidad; qué requeriría un uso real y por qué el prototipo no lo valida.

# Preguntas posibles de defensa

1. ¿Cuál es el aporte concreto aunque no superemos a la CNN?
2. ¿Qué permite afirmar la comparación y qué no?
3. ¿Cuál fue el error o límite más relevante?
4. ¿Cómo se regeneran tablas sin repetir selección por test?
5. ¿Qué se implementó de CRISP-ML(Q) y qué quedó conceptual?
6. ¿Qué falta para un uso clínico real?
7. ¿Cómo verificaron y declararon la asistencia de IA?
8. ¿Puede cada integrante defender todas las decisiones?

# Prompt para Codex

```text
Ejecutá únicamente SPRINT_05_INFORME_DEFENSA según su plan vigente. Leé primero README.md,
docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md,
docs/FUENTES_Y_TRAZABILIDAD.md, docs/ejecucion/README.md y el registro de ejecución
si existe; inspeccioná Git y las instrucciones aplicables. Verificá evidencia de cierre del sprint 04; no lo des por completo por existir un plan.
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
