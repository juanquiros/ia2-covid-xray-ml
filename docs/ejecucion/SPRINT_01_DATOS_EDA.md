# Objetivo

Preparar datos autorizados, entorno y EDA de desarrollo, con un manifiesto y partición reproducibles. **Estado: cerrado el 08/11/2026.** Inventario, partición, cinco folds y [EDA de desarrollo](../../reports/sprint_01/README.md) verificados.

# Por qué lo hacemos

Calidad, procedencia e independencia condicionan la evaluación. Un inventario claro y un split simple previenen errores sin crear infraestructura adicional.

# Conceptos necesarios

Licencia/procedencia, etiquetas, hash y duplicado exacto, paciente/grupo, estratificación, EDA, sesgo y test reservado.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 00; fuente identificada y condiciones de acceso. Si se sustituye por otro dataset público equivalente, autorización de cátedra según consigna §4.

# Tareas

- [x] Verificar versión/licencia y recuperar datos mediante su acceso autorizado; registrar qué parte de D4 puede reproducirse.
- [x] Reutilizar el entorno Python 3.12.14, fijar las dependencias del lector de metadatos y verificar `pip check`.
- [x] Inventariar ID, ruta relativa, hash, clase, fuente y grupo/paciente cuando exista. Detectar archivos ilegibles y duplicados exactos, resolver conflictos con una regla explícita.
- [x] Registrar split aproximado 80 % desarrollo/20 % test; priorizar separación de pacientes/grupos. Preparar cinco folds comunes, estratificados o agrupados según metadatos viables.
- [x] Comprobar clases y grupos suficientes antes de aceptar el esquema; documentar riesgo residual si faltan pacientes.
- [x] Realizar EDA de desarrollo por clase y tamaño, cuantificar indicadores de intensidad, revisar ejemplos y documentar dominios de referencia y el posible sesgo por origen.
- [x] Fijar contrato de grises/resize 128×128, rango, tipo, interpolación y aspecto; documentar decisiones. No extraer HOG todavía.
- [x] Mantener casi duplicados perceptuales fuera del alcance salvo evidencia concreta de EDA; no explorar test visualmente ni evaluar modelos.
- [x] Registrar evidencias y uso de IA, actualizar el índice y verificar el diff local. Commit y push quedan sujetos a solicitud expresa.

# Archivos a crear/modificar

El código de auditoría reutiliza el lector de `src/data.py` y la lógica de CV del piloto. La [configuración](../../configs/experimento.json) fija versión, ZIP, semilla, proporción, folds y tamaño de entrada. El inventario, el manifiesto y el resumen reproducidos quedan en `data/processed/sprint_01/`, excluidos de Git junto con las imágenes crudas. El [informe](../../reports/sprint_01/README.md) publica agregados y figuras.

# Pruebas

Verificar hash/ID único, consistencia de etiquetas, cero intersección de imágenes y grupos conocidos entre particiones y folds, reproducibilidad con seed 42, presencia de clases, lectura/rangos y ausencia de decisiones basadas en test. Probar instalación del entorno. Revisar numeración, ejes y texto de figuras.

# Resultados esperados

Inventario trazable, datos comparables en el nivel demostrado, entorno reproducible y EDA exclusivamente de desarrollo. Test reservado por convención y manifiesto.

# Criterios de aceptación

- [x] Acceso/licencia y sustituciones autorizadas cuando corresponda; limitaciones declaradas.
- [x] Split/folds reproducibles, sin cruces conocidos; pacientes ausentes o insuficiencias explícitos.
- [x] EDA y contrato 128×128 documentados sin abrir evaluación de test.
- [x] No hay bloqueo programático del test, buscador perceptual ni HOG/modelos ejecutados.
- [x] Pruebas pertinentes, regeneración del manifiesto y documentación verificadas.

# Qué debemos saber explicar

Diferencia entre auditoría estructural y exploración de desarrollo; por qué estratificar no separa pacientes; cómo se determinó comparabilidad con D4 y qué preserva el manifiesto.

# Preguntas posibles de defensa

1. ¿Tener la misma base implica tener el mismo test del TFC?
2. ¿Qué detecta un hash y qué no detecta?
3. ¿Cómo evitar pacientes compartidos si disponemos de IDs?
4. ¿Qué riesgo queda si no disponemos de pacientes?
5. ¿Por qué el test no participa en EDA ni decisiones de calidad visual?
6. ¿Qué puede perderse al reducir a 128×128?

# Reproducción local

Desde la raíz, usar el entorno con las versiones de `requirements.txt`. En la [ficha de Kaggle](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database/data) seleccionar la versión 5 y guardar el ZIP en `data/raw/covid19-radiography-database.zip`. El comando comprueba el SHA-256 fijado en la configuración antes de abrir el ZIP. Elegir una ruta de salida nueva para preservar una ejecución previa.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m src.auditoria --config configs/experimento.json --output data/processed/sprint_01
.\.venv\Scripts\python.exe -m src.eda data/processed/sprint_01/resumen.json --output reports/sprint_01
```

El inventario tiene una fila por ruta elegible, con ID SHA-256 del nombre de fuente versionado y la ruta, SHA-256 del archivo, etiqueta, fuente, dominio de referencia, paciente si se conoce, estado y el ID canónico en caso de duplicado. El manifiesto añade `partition` y `validation_fold` de 1 a 5 para desarrollo. En test el fold queda vacío.

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
Revisá el diff e informá verificaciones y pendientes.
Hacé commit o push solo si el usuario lo solicita expresamente.
No ejecutes ni inicies el siguiente sprint.
```
