# IA II · TFI · Clasificación de radiografías con Machine Learning

**Universidad Gastón Dachary · Inteligencia Artificial II · Ingeniería en Informática.**
**Integrantes:** Juan Quirós y Andruszyszyn (nombre completo y legajos pendientes).

Propuesta principal: **radiografía → preprocesamiento → HOG → Random Forest → COVID (1) / Normal (0)**, como alternativa a la CNN del TFC de 2023. DummyClassifier es la baseline; SVM lineal permanece como candidato para comparación posterior. La selección académica definitiva dependerá de experimentos, sin favorecer artificialmente a RF. Es un prototipo académico, sin validación clínica.

**Estado al 02/11/2026:** sprint preliminar **00-A implementado**. Piloto real de 200 imágenes de desarrollo (100 por clase), cinco folds, RF frente a Dummy, predicción individual y pruebas automatizadas. No se hizo tuning ni se creó/evaluó un test final. Los sprints académicos **00–05 permanecen pendientes**; el prototipo no acredita su cierre.

## Instalación y pruebas

Desde la raíz del repositorio, con Python 3.12 (verificado con 3.12.14 en Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m src.piloto --help
```

Las pruebas generan imágenes sintéticas en carpetas temporales para verificar software. Sus métricas no son resultados académicos. Las versiones directas y transitivas verificadas están fijadas en requirements.txt.

## Datos y ejecución

Fuente: [COVID-19 Radiography Database, Kaggle](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database), referencia [46] del TFC. Se utilizó la versión 5, con uso académico/no comercial indicado por sus autores. La [procedencia del piloto](reports/piloto_2026-11-02/README.md) registra versión, atribución y hashes. Esta muestra no reproduce el subconjunto D4 depurado manualmente.

Descargar el ZIP desde Kaggle y guardarlo como `data/raw/covid19-radiography-database.zip`. SHA-256 utilizado: `15f44e7111a74f048a54a41bf699637ffaad51b08a9d4a622ff5596879cb7f2b`. Puede verificarse con `Get-FileHash`; si cambia, no asumir que se reproduce la muestra. Dataset y modelo permanecen locales, excluidos de Git.

**La preparación siguiente corresponde a la etapa anterior a definir test.** Audita hashes de COVID/Normal, excluye copias exactas conservando la primera ruta ordenada y extrae una muestra con seed 42. Rechaza duplicados con etiquetas contradictorias. Los 200 hashes seleccionados quedan asignados a desarrollo y deberán excluirse del futuro test; el resto queda sin asignar. Si ya existe un split académico, usar directamente su carpeta de desarrollo, sin volver a preparar desde toda la base.

```powershell
.\.venv\Scripts\python.exe -m src.data --archive data/raw/covid19-radiography-database.zip --output data/raw/pilot_development --max-per-class 100
.\.venv\Scripts\python.exe -m src.piloto train --data-dir data/raw/pilot_development --max-per-class 100 --folds 5 --output output/piloto_2026-11-02
.\.venv\Scripts\python.exe -m src.piloto predict --model output/piloto_2026-11-02/random_forest.joblib --image data/raw/pilot_development/NORMAL/Normal-1224.png
```

La última imagen pertenece a desarrollo: demuestra la interfaz, no una evaluación independiente. Cargar únicamente archivos joblib propios/de confianza. Si la salida ya contiene archivos, elegir otra carpeta para preservar la ejecución previa. No hace falta reentrenar para consultar los resultados guardados.

El cargador admite `COVID/*.png` y `NORMAL/*.png`, o la estructura Kaggle `COVID/images/` y `Normal/images/`; no recorre masks ni subcarpetas arbitrarias. También acepta JPEG/TIFF/BMP compatibles. Rechaza imágenes ilegibles y duplicados exactos en la muestra. `--max-per-class` limita imágenes sin reemplazo; seed 42 y orden estable permiten repetir la selección.

Si hay identificadores fiables, proporcionar `--patients-csv ruta.csv`, con columnas `path,patient_id` para todas las imágenes seleccionadas (rutas relativas a data-dir, separador `/`). Se usa StratifiedGroupKFold. Sin ese archivo se usa StratifiedKFold y se declara que la independencia de pacientes no está garantizada. No inferir pacientes de nombres como COVID-123.

Preprocesamiento: RGB a grises, uint8/255 o uint16/65535; flotantes solo en [0,1]; resize bilineal directo con antialiasing a 128×128, sin recorte ni conservación de aspecto; salida float32. No se hace min-max por imagen. HOG: 9 orientaciones, celdas (8,8), bloques (2,2), L2-Hys y transform_sqrt=False: **8100 atributos**. RF: 100 árboles, profundidad sin límite, hoja mínima 1, random_state=42 y n_jobs=-1; sin StandardScaler.

Cada ejecución guarda manifiesto, predicciones fuera de fold (OOF), métricas por fold, configuración/versiones, tres figuras y un RF reajustado con todo el desarrollo del piloto. Las métricas y matrices proceden de OOF, no del reajuste final. SVM, tuning y test quedan para la comparación posterior.

## Evidencia y documentación

Resultado preliminar: accuracy media **RF 0,7500 ± 0,0919**, frente a **Dummy 0,5000 ± 0,0000**. Se informa desvío muestral entre cinco folds, no intervalo de confianza. La muestra es pequeña, balanceada artificialmente y sin IDs explícitos de pacientes; no demuestra superioridad frente al TFC.

- [Informe breve del avance](docs/AVANCE_2026-11-02.md).
- [Resultados, figuras y procedencia](reports/piloto_2026-11-02/README.md).
- [Registro del sprint](docs/REGISTRO_EJECUCION.md) y [uso de IA](docs/REGISTRO_IA.md).

- [Roadmap](docs/ROADMAP_TFI.md): análisis del TFC y protocolo vigente.
- [Teoría y stack](docs/TEORIA_Y_STACK.md): núcleo de estudio y conceptos complementarios.
- [Comparativa](docs/COMPARATIVA_TFC_VS_PROPUESTA.md): evidencia original frente a propuesta pendiente.
- [Ejecución](docs/ejecucion/README.md): seis sprints activos, todavía no iniciados.
- [Fuentes y trazabilidad](docs/FUENTES_Y_TRAZABILIDAD.md): referencias, discrepancias y requisitos académicos.
- [Planificación inicial archivada](docs/archivo/planificacion_inicial/README.md): historial sin vigencia operativa.

**Próximos pasos:** revisión académica por ambos integrantes, auditoría completa de datos/pacientes, definición de split definitivo y comparación posterior con SVM. El código de 00-A se reutilizará donde corresponda; ningún sprint posterior se ejecuta automáticamente.
