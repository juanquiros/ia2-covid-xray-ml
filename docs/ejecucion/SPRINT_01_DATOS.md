# Sprint 01 · Datos, entorno y partición

**Estado:** no iniciado. Depende del cierre verificable de 00.

# Objetivo

Obtener un dataset autorizado y trazable, auditar integridad/grupos y separar desarrollo del test reservado en un entorno reproducible.

# Por qué existe este sprint

El tamaño y nombre del dataset no garantizan equivalencia con D4 ni independencia. La partición define qué generalización podremos medir y debe quedar fijada antes del EDA predictivo.

# Conocimientos previos necesarios

Manifiestos, hashes, etiquetas, procedencia, licencia, paciente como unidad independiente, estratificación, venv y control de versiones. Teoría §§2–6 y 20.

# Entradas

Cierre 00, decisiones, fuentes primarias y enlace de dataset; permisos/licencia verificables; IDs/splits originales si se obtienen. Una sustitución pública equivalente requiere autorización de cátedra según TFI §4. No inferirla del acceso de descarga.

# Tareas

- [ ] Verificar cierre 00, repo y permisos; registrar ruta histórica o nueva población y nivel de comparación.
- [ ] Crear venv, probar compatibilidad de bibliotecas CPU y fijar versiones realmente instaladas.
- [ ] Verificar licencia/versión y obtener datos por vía autorizada; conservar raw inmutable fuera de Git.
- [ ] Inventariar imágenes, dimensiones, canales, hashes, etiquetas, fuentes y paciente/grupo si existen.
- [ ] Detectar corrupción, duplicados exactos, candidatos a duplicados cercanos y etiquetas conflictivas; revisar casos ambiguos antes de particionar.
- [ ] Aplicar reglas objetivas de elegibilidad documentadas; no limpiar en función de aciertos ni forzar 2462 por clase.
- [ ] Separar aproximadamente 80 % desarrollo / 20 % test con grupos y estratificación factible, semilla 42; preservar IDs de split.
- [ ] Fijar cinco folds en desarrollo o justificar k menor por grupos; mismos folds para todos los métodos.
- [ ] Sellar manifiesto de test con hash y política de acceso; evitar distribución de etiquetas/imágenes de test en notebooks EDA.
- [ ] Probar independencia y regeneración; documentar inventarios, exclusiones y riesgos residuales.

# Archivos futuros involucrados

Crear `requirements.txt`, `configs/datos.json`, `src/data/inventario.py`, `src/data/particiones.py`, `tests/test_particiones.py`, `data/manifests/inventario.csv`, `data/manifests/particiones.csv`, `data/manifests/folds.csv` y `results/reports/datos.md`. Mantener raw/processed locales e ignorados. Modificar `.gitignore`, decisiones, registro IA, README y documentos operativos afectados. Los manifiestos solo se publican si son no identificatorios y compatibles con licencia; en otro caso versionar esquema, resumen y hashes e instrucciones de acceso local.

# Implementación esperada

Comandos de inventario y partición idempotentes con rutas configurables, validación de etiquetas y registro de errores. Agrupar por paciente y duplicados; si faltan IDs, no proclamar independencia clínica. Auditoría completa solo estructural antes de sellar, sin explorar asociaciones predictivas del test. El módulo de acceso a test deberá rechazar uso por etapas de desarrollo y permitir apertura explícita únicamente en evaluación final.

# Pruebas

Con fixtures pequeños: imágenes corruptas se detectan; etiquetas desconocidas fallan; ningún ID/hash/grupo cruza desarrollo/test ni folds; misma configuración regenera mismas listas; cada fold tiene clases/grupos suficientes; test no es accesible en modo desarrollo. Comprobar exclusión de datos pesados mediante Git y creación del entorno desde requirements. No entrenar ningún clasificador.

# Resultados esperados

Datos y particiones auditables, conteos reales por clase/grupo/fuente, entorno probado y test sellado; no cifras de desempeño.

# Criterios de aceptación

Licencia/procedencia y autorización de sustitución resueltas cuando aplique; raw íntegro; inventario/exclusiones completos; intersección de IDs/hashes/grupos conocidos igual a cero; proporciones efectivas informadas; folds y test reproducibles; limitación explícita si faltan pacientes. Ninguna dependencia de datos irresuelta se omite para avanzar.

# Evidencias a conservar

Versión/fecha de descarga, licencia, hashes, conteos, manifiestos publicables o hash de versión local, log de exclusiones, reglas, pruebas, entorno y comando de regeneración. No guardar tokens ni identificadores personales en resultados públicos.

# Riesgos

Falta de metadatos, restricciones de licencia, deriva entre versiones, duplicados no exactos, correlación fuente/clase y balance artificial.

# Errores frecuentes

Separar después de sobremuestrear, equiparar D4 por cantidad, ignorar paciente, forzar porcentajes rompiendo grupos, usar test para decidir exclusiones y versionar radiografías.

# Qué debemos comprender antes de cerrarlo

Cuál es la población evaluada, qué significa cada etiqueta, qué garantiza cada control y qué sigue sin verificarse. Saber regenerar la partición y explicar por qué no es el 80/10/10 histórico.

# Preguntas posibles de defensa

1. ¿De dónde proviene cada imagen y cómo verificamos versión?
2. ¿Tenemos D4 exacto o un subconjunto nuevo?
3. ¿Por qué agrupar pacientes y duplicados?
4. ¿Qué se puede auditar antes de sellar test?
5. ¿Por qué no balancear test después?
6. ¿Qué riesgos quedan si faltan IDs de pacientes?
7. ¿Qué demuestra un hash y qué no?

# Definition of Done

Controles y criterios satisfechos, entorno y particiones reproducibles, test sellado, documentación/checklist actualizados, un commit y push confirmado. No comenzar EDA de 02 automáticamente.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá solamente SPRINT_01_DATOS del repositorio juanquiros/ia2-covid-xray-ml, rama main.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/ejecucion/README.md, docs/ejecucion/SPRINT_01_DATOS.md, el cierre 00, fuentes y decisiones. Comprobá criterios de aceptación de 00 antes de avanzar.
Revisá raíz, remote, rama, status y cambios previos; preservalos. Objetivo: entorno probado, dataset autorizado, inventario y partición independiente. Verificá licencia/versión y autorización de cátedra si se sustituyen datos originales por equivalentes.
Creá requirements.txt, configs/datos.json, src/data/inventario.py, src/data/particiones.py, tests/test_particiones.py, manifiestos inventario/particiones/folds y results/reports/datos.md. Implementá auditoría estructural, hashes/duplicados/grupos, reglas de exclusión, split 80/20 aproximado y CV agrupada/estratificada de desarrollo según roadmap. Sellá test y restringí su acceso. Registrá limitaciones de metadatos.
No entrenes modelos, no hagas EDA predictivo de test, no fuerces un D4 ficticio ni publiques datos sensibles o pesados. Si falta permiso/licencia o fuente, detené adquisición dependiente y documentá el bloqueo sin inventar autorización.
Ejecutá pruebas de corrupción, etiquetas, independencia de ID/hash/grupo, determinismo, factibilidad de folds, bloqueo de test y regeneración del entorno. Verificá todos los criterios/DoD del sprint y documentá resultados reales, conteos y comandos.
Actualizá .gitignore, README, decisiones, uso de IA, documentos afectados, índice y checklist; registrá Cierre real solo si corresponde. Revisá diff, git diff --check y stage explícito.
Hacé un commit 'data: add reproducible dataset audit and reserved split' y push a origin/main. Informá SHA, pruebas, archivos, permisos pendientes y estado Git. No ejecutes sprint 02 ni posteriores.
```
