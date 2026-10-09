# Sprint 02 · Exploración y calidad de desarrollo

**Estado:** no iniciado. Depende del cierre 01 y test sellado.

# Objetivo

Comprender la distribución y calidad de imágenes de desarrollo y fijar el contrato inicial de preprocesamiento sin explorar test.

# Por qué existe este sprint

Un descriptor puede capturar bordes ajenos a pulmón o diferencias de equipo. EDA permite identificar riesgos y justificar preparación, sin confundir observación con causalidad médica.

# Conocimientos previos necesarios

Píxel, resolución, intensidad, contraste, textura, procedencia, clases, representatividad y fuga de información. Teoría §§2–6.

# Entradas

Informe y cierre 01, manifiestos de desarrollo/folds, raw autorizado, entorno y decisiones. Acceso a test prohibido salvo comprobación de integridad del sello sin leer imágenes/etiquetas para análisis.

# Tareas

- [ ] Verificar cierre 01, hashes de configuración y separación de acceso.
- [ ] Describir clases, fuentes y grupos de desarrollo; registrar datos faltantes sin inferir atributos sensibles.
- [ ] Examinar dimensiones, canales, intensidades, contraste y calidad con resúmenes reproducibles.
- [ ] Muestrear ejemplos de desarrollo por clase/fuente con semilla; revisar marcas, recortes y posibles atajos.
- [ ] Proponer análisis de calidad sin diagnosticar imágenes ni reetiquetar por inspección visual.
- [ ] Definir preprocesamiento inicial: grises, 128×128, rango, interpolación y aspecto; justificar cada decisión.
- [ ] Documentar incidencias que exigirían volver a 01; no modificar silenciosamente particiones selladas.
- [ ] Producir figuras con ejes/epígrafes y conclusiones de EDA limitadas a desarrollo.

# Archivos futuros involucrados

Crear `notebooks/02_eda.ipynb`, `src/data/eda.py`, `configs/preprocesamiento.json`, `results/reports/eda.md`, figuras EDA y `tests/test_eda_acceso.py`. Modificar decisiones y documentación operativa; solo corregir inventarios a través de incidencia trazable que reabra 01 si es necesario.

# Implementación esperada

EDA regenerable desde script o notebook reiniciado con ejecución completa. Graficar distribución de intensidades/calidad por clase y fuente con tamaño muestral, además de ejemplos autorizados. Guardar IDs de muestras de desarrollo; no publicar imágenes si licencia/privacidad no lo permite. El informe distingue “observado”, “posible explicación” y “acción propuesta”. No construir modelos aquí.

# Pruebas

Verificar que todos los IDs analizados pertenecen a desarrollo, que el módulo rechaza test, que conteos coinciden con manifiesto y que figuras/tablas se regeneran desde sesión limpia. Revisar visualmente ejes, etiquetas, valores y epígrafes. Validar JSON y contrato de tipo/rango sin ejecutar extracción masiva.

# Resultados esperados

Informe EDA con riesgos concretos, faltantes y preprocesamiento inicial fundamentado; todavía sin features de producción ni métricas de clasificadores.

# Criterios de aceptación

Todas las figuras basadas exclusivamente en desarrollo, conteos trazables y hallazgos sin diagnósticos inventados; test intacto; preprocesamiento definido; incidencias de datos resueltas o ruta afectada bloqueada; comandos reproducibles y figuras interpretadas.

# Evidencias a conservar

Manifiesto de IDs analizados, configuración, versiones, comandos, figuras permitidas, resúmenes de calidad, decisiones y registro de no acceso a test.

# Riesgos

Confundir correlación con causa, seleccionar ejemplos convenientes, filtrar casos difíciles por clase y alterar etiquetas usando juicio no clínico.

# Errores frecuentes

EDA del dataset entero después del split; atribuir edad/sexo por apariencia; elegir resize por rendimiento en test; llamar “calidad clínica” a una medida de contraste; publicar radiografías sin revisar permiso.

# Qué debemos comprender antes de cerrarlo

Qué propiedades de imagen cambian HOG/LBP, qué representa la población de desarrollo y por qué el test sigue reservado aun sin haber entrenado modelos.

# Preguntas posibles de defensa

1. ¿Qué hallazgo de EDA motivó una decisión concreta?
2. ¿Por qué una fuente puede actuar como atajo?
3. ¿Cómo seleccionamos ejemplos sin favorecer una conclusión?
4. ¿Qué información pierde resize?
5. ¿Qué diferencia existe entre calidad técnica y diagnóstico?
6. ¿Por qué EDA puede contaminar test?

# Definition of Done

EDA y configuración reproducibles, criterios satisfechos, test intacto, documentación/checklist actualizados y un commit con push. No iniciar 03 automáticamente.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá únicamente SPRINT_02_EDA en juanquiros/ia2-covid-xray-ml/main.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/ejecucion/README.md y docs/ejecucion/SPRINT_02_EDA.md; comprobá cierre y criterios de 01, manifiestos, informes y decisiones. Revisá raíz/remoto/rama/status/diff y preservá cambios previos.
Objetivo: explorar solo desarrollo y fijar contrato de preprocesamiento. Creá notebooks/02_eda.ipynb, src/data/eda.py, configs/preprocesamiento.json, results/reports/eda.md, figuras EDA y tests/test_eda_acceso.py.
Aplicá conteos por clase/fuente/grupo, inspección de dimensiones/canales/intensidad/calidad y muestreo determinista de desarrollo. Definí grises, resize inicial 128x128, rango, interpolación y tratamiento de aspecto con justificación. Separá hallazgos de hipótesis y registrá incidencias sin cambiar test silenciosamente.
Restricciones: no leer test para EDA, no entrenar, no extraer features masivamente, no reetiquetar por diagnóstico supuesto ni publicar datos sin permisos. No ejecutes 03 o posteriores.
Probá que todos los IDs son de desarrollo y se rechaza test; verificá conteos, configuración y regeneración desde sesión limpia. Revisá figuras con ejes/epígrafes y cumplí criterios de aceptación y DoD. Documentá resultados reales, no valores de ejemplo como hallazgos.
Actualizá decisiones, uso de IA, README, índice, checklist y documentos afectados; registrá Cierre real con evidencias. Revisá diff y git diff --check; stage explícito, commit 'analysis: document development data quality and preprocessing' y push origin/main. Informá SHA, pruebas, archivos, limitaciones y estado Git. Detenete al terminar este sprint.
```
