# Sprint 08 · Informe y defensa

**Estado:** no iniciado. Depende del cierre 07 y evidencia experimental real.

# Objetivo

Consolidar un informe técnico conforme a consigna, una presentación y un ensayo de defensa en el que ambos integrantes dominen la totalidad del trabajo.

# Por qué existe este sprint

El proyecto debe comunicar problema, fundamento, evaluación y límites de forma defendible. Un repositorio que ejecuta código no sustituye discusión crítica ni comprensión individual.

# Conocimientos previos necesarios

Todo el material de teoría; interpretación de resultados reales, normas de citación y requisitos de consigna. Distinguir hipótesis inicial de conclusión sustentada.

# Entradas

Cierre 07 y anteriores, datos/entorno autorizados, resultados/figuras/predicciones congelados, fuentes originales, registro de IA y matriz de requisitos. Nombre completo, legajos, institución, fecha/plataforma de entrega y tiempos de defensa confirmados para la carátula/entrega definitiva.

# Tareas

- [ ] Verificar cumplimiento de todos los sprints y de cada punto de rúbrica.
- [ ] Crear informe con carátula, resumen ≤250 palabras y palabras clave en español e inglés; índices general/figuras/tablas.
- [ ] Redactar introducción, análisis TFC, alternativa/fundamento, implementación, resultados, errores/interpretación, ética/despliegue, discusión/conclusiones, referencias y anexos.
- [ ] Aplicar IEEE de forma consistente, distinguiendo cifras del TFC y resultados propios; citar código/figuras reutilizados.
- [ ] Respetar PDF A4, márgenes 2,5 cm, Arial/Times 11–12 pt, interlineado 1,15–1,5, páginas numeradas y extensión orientativa 20–30 páginas sin anexos.
- [ ] Crear anexo de uso IA con herramienta/versión conocida, etapa, finalidad y verificación; no inventar versiones.
- [ ] Preparar presentación y guion para ambos integrantes, inicialmente 15 minutos + 10 de preguntas, sujetos a confirmación de valores entre corchetes de consigna.
- [ ] Ensayar regeneración en entorno limpio y explicación de cualquier parte del pipeline; usar predicciones congeladas para validar tablas test sin nueva selección.
- [ ] Revisar visualmente PDF/presentación y comprobar cada cifra, figura, enlace y referencia.
- [ ] Preparar entrega `TFI_IA2_Quiros_Andruszyszyn`, acceso a cátedra y registro final; no enviar a terceros sin instrucción.

# Archivos futuros involucrados

Crear `docs/informe/TFI_IA2_Quiros_Andruszyszyn.md` (fuente o formato fuente alternativo justificado), `results/reports/TFI_IA2_Quiros_Andruszyszyn.pdf`, `docs/defensa/GUION.md`, `docs/defensa/PREGUNTAS_Y_RESPUESTAS.md`, presentación editable/PDF según herramienta y `results/reports/reproduccion_final.md`. Modificar README con instrucciones reales, registro IA, matriz de requisitos y documentos de cierre. Versionar fuentes y PDF pequeño pertinente; entregar binarios grandes por mecanismo acordado, no subir datasets.

# Implementación esperada

Redacción basada solo en evidencia, figuras numeradas con epígrafes, ejes/unidades y lectura en texto. Discusión multidimensional: no declarar superioridad por diferencia mínima de accuracy ni omitir limitaciones de datos. Consultar las habilidades de documentos/PDF/presentaciones al crear esos formatos y renderizar para revisar. No agregar experimentos para embellecer conclusiones.

# Pruebas

Auditoría cifra→archivo→ejecución→configuración; reproducción desde entorno limpio del pipeline de desarrollo y de métricas/gráficos de test desde predicciones congeladas; validación de referencias y enlaces; render de cada página/slide para detectar cortes; ensayo cronometrado, intercambio de preguntas entre integrantes y registro de conceptos a reforzar.

# Resultados esperados

Informe/presentación finales con conclusiones reales y límites, instrucciones de reproducción y defensa practicada. La aprobación académica la determina la cátedra, no este sprint.

# Criterios de aceptación

Formato/secciones de consigna cumplidos; ninguna cifra sin trazabilidad; figuras legibles e interpretadas; IA declarada; ambos integrantes pueden explicar todo; reproducción documentada; datos privados fuera de publicación; metadatos de carátula completos. Si falta fecha/plataforma o identidad, distinguir borrador revisable de entrega definitiva.

# Evidencias a conservar

Fuente editable, PDF/presentación finales, matriz de verificación, logs/comandos/entorno de reproducción, guion cronometrado, preguntas contestadas, registro IA y SHA de entrega. No afirmar envío a cátedra si no ocurrió.

# Riesgos

Confundir conclusión con hipótesis, presentación demasiado extensa, tablas ilegibles, pérdidas de trazabilidad, estudiantes especializados solo en una parte y metadatos administrativos incompletos.

# Errores frecuentes

Copiar porcentajes sin denominador, llamar diagnóstico al clasificador, ocultar resultados negativos, usar estilos bibliográficos mezclados, nuevas pruebas de test para ajustar narrativa y no declarar IA.

# Qué debemos comprender antes de cerrarlo

Explicar el proyecto completo en lenguaje técnico y sencillo, fundamentar cada decisión y distinguir alcance evaluado de mejoras futuras. Ambos deben poder reproducir y defender el trabajo completo.

# Preguntas posibles de defensa

1. ¿Qué problema resolvimos exactamente y para qué población?
2. ¿Por qué la solución es distinta de la CNN original?
3. ¿Qué evidencia sostiene la selección final?
4. ¿Qué significa “mejor” con desempeño y costos observados?
5. ¿Qué no permiten concluir nuestros datos?
6. ¿Cómo regeneraría otro estudiante los resultados?
7. ¿Dónde se usó IA y cómo se verificó?
8. ¿Qué necesitaría una evaluación clínica real fuera del TFI?

# Definition of Done

Informe y defensa cumplen criterios, reproducción y revisión visual verificadas, metadatos pendientes resueltos para entrega definitiva, checklist actualizado, commit y push confirmado. No enviar el trabajo ni iniciar mejoras adicionales sin instrucción.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá exclusivamente SPRINT_08_INFORME_DEFENSA en juanquiros/ia2-covid-xray-ml/main.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/ejecucion/README.md y docs/ejecucion/SPRINT_08_INFORME_DEFENSA.md, consigna, fuentes, cierres previos y todos los resultados reales. Verificá criterios/DoD de 07 y matriz de requisitos. Revisá raíz/remoto/rama/status/diff y preservá trabajo previo.
Objetivo: informe y defensa sustentados. Creá fuente editable y PDF TFI_IA2_Quiros_Andruszyszyn, docs/defensa/GUION.md, PREGUNTAS_Y_RESPUESTAS.md, presentación y results/reports/reproduccion_final.md. Usá habilidades pertinentes para formatos y renderizado.
Aplicá secciones, formato A4/márgenes/tipografía/longitud de consigna, resumen y palabras clave español/inglés, figuras numeradas e interpretadas, IEEE consistente y anexo IA con formato requerido. No inventes carátula, fecha, resultados ni versiones. Prepará guion para ambos y ensayo de 15 minutos más preguntas con tiempos de consigna a confirmar.
Restricciones: no nuevos experimentos/tuning/selección por test, no conclusiones clínicas, no publicar datos privados ni enviar a cátedra sin instrucción. No iniciar mejoras o sprints nuevos.
Verificá cada cifra contra artefactos y reproducí en entorno limpio desarrollo y cálculos finales desde predicciones congeladas; revisá visualmente todas las páginas/slides, citas, enlaces y requisitos. Registrá resultados reales del ensayo y qué conceptos dominan ambos. Cumplí aceptación/DoD; si faltan datos administrativos, distinguí borrador de entrega definitiva.
Actualizá README de ejecución real, documentos afectados, uso de IA, matriz de requisitos, índice y checklist. Revisá diff/check y stage solo entregables pertinentes; commit 'docs: finalize TFI report and defense materials' y push origin/main. Informá SHA, archivos finales, verificaciones, pendientes y estado Git. No afirmes envío externo si no se realizó.
```
