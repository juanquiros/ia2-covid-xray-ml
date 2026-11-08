# HOG y línea base en desarrollo

## Representación

Se usaron las 11.009 imágenes de desarrollo y los cinco folds del manifiesto definitivo del Sprint 01. La extracción leyó del ZIP únicamente las rutas de desarrollo y verificó el SHA-256 de cada imagen contra el manifiesto antes de decodificarla. El preprocesamiento compartido convierte a grises y redimensiona a 128 × 128 por interpolación bilineal con antialiasing. HOG utiliza 9 orientaciones, celdas de 8 × 8, bloques de 2 × 2, normalización L2-Hys y `transform_sqrt=False`. Los 15 × 15 bloques, con cuatro celdas y nueve orientaciones por bloque, producen 8.100 atributos.

La matriz tiene **11.009 × 8.100** valores finitos de tipo `float32`. La extracción secuencial tardó aproximadamente **80,5 s** en Windows con un Intel Core i5-1135G7 y Python 3.12.14, unos 7,3 ms por imagen. Ese tiempo incluye lectura del ZIP, verificación de hashes, decodificación, preprocesamiento y HOG. La escritura de artefactos y la evaluación de Dummy quedaron fuera de ese intervalo.

## Línea base

En cada fold, `DummyClassifier(strategy="most_frequent")` tomó la clase más frecuente de las etiquetas de entrenamiento y predijo una vez para cada imagen de validación. COVID=1 es la clase positiva y Normal=0 es la negativa. Se usó `zero_division=0` para las métricas con denominador nulo. F1 macro promedia el F1 de ambas clases con el mismo peso. La especificidad es la proporción de normales correctamente clasificadas.

| Fold | Imágenes de validación | COVID reales | Exactitud | Precisión COVID | Recall COVID | F1 COVID | Especificidad | F1 macro |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2.202 | 572 | 0,740236 | 0 | 0 | 0 | 1 | 0,425365 |
| 2 | 2.202 | 571 | 0,740690 | 0 | 0 | 0 | 1 | 0,425515 |
| 3 | 2.202 | 571 | 0,740690 | 0 | 0 | 0 | 1 | 0,425515 |
| 4 | 2.202 | 571 | 0,740690 | 0 | 0 | 0 | 1 | 0,425515 |
| 5 | 2.201 | 571 | 0,740572 | 0 | 0 | 0 | 1 | 0,425476 |
| **Media** | | | **0,740576** | **0** | **0** | **0** | **1** | **0,425478** |
| **Desvío estándar muestral** | | | **0,000197** | **0** | **0** | **0** | **0** | **0,000065** |

Las medias ponderan por igual los cinco folds. Los desvíos describen la variación entre ellos. Las 11.009 predicciones fuera de fold fueron Normal. Así, Dummy acertó las 8.153 imágenes normales y dejó sin detectar las 2.856 de COVID. Su exactitud de alrededor del 74 % refleja la proporción de la clase mayoritaria. El recall de COVID y el F1 macro muestran lo que se pierde al mirar solo la exactitud. [Métricas por fold sin redondear](../results/baseline_cv.csv)

## Verificación y reproducción interna

Se verificó la correspondencia entre cada fila, ID, etiqueta y fold en el manifiesto, el índice y las predicciones fuera de fold. Los archivos por imagen contienen solo IDs de desarrollo. Además de comprobar forma, tipo y finitud en toda la matriz, se reextrajeron diez vectores, uno por combinación de clase y fold, y coincidieron exactamente. Las métricas por fold, la media y el desvío se recalcularon desde las predicciones guardadas.

Desde la raíz del repositorio, con el entorno del Sprint 01, ejecutar estos comandos. Para repetir una extracción, indicar otra carpeta de salida. Si el manifiesto no está disponible, regenerarlo con el procedimiento de 01. El programa exige el SHA-256 registrado antes de abrir el ZIP. [Reproducción del Sprint 01](../docs/ejecucion/SPRINT_01_DATOS_EDA.md#reproducción-local)

```powershell
.\.venv\Scripts\python.exe -m src.baseline --config configs/experimento.json --output data/processed/sprint_02
.\.venv\Scripts\python.exe -m src.baseline --config configs/experimento.json --output data/processed/sprint_02 --verify-only
```

`data/processed/sprint_02/` contiene `hog.npy`, `index.csv`, `predictions_oof.csv`, `baseline_cv.csv` y `summary.json`. Para reutilizar la matriz, `row` en `index.csv` es el índice de fila desde cero y `validation_fold` identifica el fold del manifiesto, del 1 al 5. El resumen registra versiones, configuración, tiempos y hashes. La verificación puede ejecutarse sobre los artefactos guardados sin leer el ZIP.
