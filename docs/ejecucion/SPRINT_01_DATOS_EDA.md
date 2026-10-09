# Objetivo

Preparar datos autorizados, entorno y EDA de desarrollo, con un manifiesto y partición reproducibles. **Estado: no iniciado.**

# Por qué lo hacemos

Calidad, procedencia e independencia condicionan la evaluación. Un inventario claro y un split simple previenen errores sin crear infraestructura adicional.

# Conceptos necesarios

Licencia/procedencia, etiquetas, hash y duplicado exacto, paciente/grupo, estratificación, EDA, sesgo y test reservado.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 00; fuente identificada y condiciones de acceso. Si se sustituye por otro dataset público equivalente, autorización de cátedra según consigna §4.

# Tareas

- [ ] Verificar versión/licencia y recuperar datos mediante su acceso autorizado; registrar qué parte de D4 puede reproducirse.
- [ ] Crear venv y requirements con versiones probadas del stack mínimo; registrar comandos y seed 42.
- [ ] Inventariar ID, ruta relativa, hash, clase, fuente y grupo/paciente cuando exista. Detectar archivos ilegibles y duplicados exactos, resolver conflictos con una regla explícita.
- [ ] Registrar split aproximado 80 % desarrollo/20 % test; priorizar separación de pacientes/grupos. Preparar cinco folds comunes, estratificados o agrupados según metadatos viables.
- [ ] Comprobar clases y grupos suficientes antes de aceptar el esquema; documentar riesgo residual si faltan pacientes.
- [ ] Realizar EDA de desarrollo: conteos, tamaños/rangos, calidad, ejemplos y fuentes disponibles. Señalar atajos observables sin inventar causalidad.
- [ ] Fijar contrato de grises/resize 128×128, rango, tipo, interpolación y aspecto; documentar decisiones. No extraer HOG todavía.
- [ ] Mantener casi duplicados perceptuales fuera del alcance salvo evidencia concreta de EDA; no explorar test visualmente ni evaluar modelos.
- [ ] Registrar evidencias y uso de IA, verificar, actualizar checklist e índice; commit y push. No iniciar 02.

# Archivos a crear/modificar

Crear `requirements.txt`, `src/data.py`, `configs/experimento.json`, `data/manifiesto.csv`, `reports/eda.md` y figuras de EDA. Añadir pruebas relevantes de datos/split en `tests/`; actualizar registros y documentos. Datos pesados o identificadores sensibles no se publican.

# Pruebas

Verificar hash/ID único, consistencia de etiquetas, cero intersección de imágenes y grupos conocidos entre particiones y folds, reproducibilidad con seed 42, presencia de clases, lectura/rangos y ausencia de decisiones basadas en test. Probar instalación del entorno. Revisar numeración, ejes y texto de figuras.

# Resultados esperados

Inventario trazable, datos comparables en el nivel demostrado, entorno reproducible y EDA exclusivamente de desarrollo. Test reservado por convención y manifiesto.

# Criterios de aceptación

- [ ] Acceso/licencia y sustituciones autorizadas cuando corresponda; limitaciones declaradas.
- [ ] Split/folds reproducibles, sin cruces conocidos; pacientes ausentes o insuficiencias explícitos.
- [ ] EDA y contrato 128×128 documentados sin abrir evaluación de test.
- [ ] No hay bloqueo programático del test, buscador perceptual ni HOG/modelos ejecutados.
- [ ] Pruebas y documentación verificadas; commit y push confirmados.

# Qué debemos saber explicar

Diferencia entre auditoría estructural y exploración de desarrollo; por qué estratificar no separa pacientes; cómo se determinó comparabilidad con D4 y qué preserva el manifiesto.

# Preguntas posibles de defensa

1. ¿Tener la misma base implica tener el mismo test del TFC?
2. ¿Qué detecta un hash y qué no detecta?
3. ¿Cómo evitar pacientes compartidos si disponemos de IDs?
4. ¿Qué riesgo queda si no disponemos de pacientes?
5. ¿Por qué el test no participa en EDA ni decisiones de calidad visual?
6. ¿Qué puede perderse al reducir a 128×128?

# Prompt para Codex

```text
Ejecutá únicamente SPRINT_01_DATOS_EDA según su plan vigente. Leé primero README.md,
docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md,
docs/FUENTES_Y_TRAZABILIDAD.md, docs/ejecucion/README.md y el registro de ejecución
si existe; inspeccioná Git y las instrucciones aplicables. Verificá evidencia de cierre del sprint 00; no lo des por completo por existir un plan.
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
