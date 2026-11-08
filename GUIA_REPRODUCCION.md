# Reproducción de las métricas y figuras

El archivo `TFI_IA2_Quiros_Andruszyszyn.zip` reúne el informe, la presentación, el código y la evidencia tabular. Para reconstruir los resultados, extraer el ZIP y ejecutar los comandos desde su directorio raíz. Si se parte de una copia del repositorio, obtener la carpeta `evidencia/` del ZIP de entrega y colocarla en la raíz, junto a `src/`. La vía de entrega es el aula virtual.

## Entorno

Usar Python 3.12. El entorno del estudio se fijó con Python 3.12.14 y las versiones de `requirements.txt`. Comandos para PowerShell.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -q tests/test_reproduccion.py
```

La prueba usa ejemplos tabulares sintéticos y comprueba la integridad y el cálculo sin ajustar modelos.

## Evidencia y reconstrucción

| Archivo | Contenido |
|---|---|
| `evidencia/prueba.csv` | 2.752 filas con etiqueta, predicciones de los tres modelos y puntajes COVID de ambos candidatos |
| `evidencia/desarrollo_oof.csv` | 11.009 filas de desarrollo con etiqueta, fold y una predicción por modelo |
| `evidencia/eda.json` | Conteos por tamaño, clase e intensidad |
| `evidencia/pesos_hog.csv` | Cuadrícula de 15 × 15 normas de los coeficientes agrupados del SVM seleccionado |
| `evidencia/sha256.json` | Huellas de integridad de los cuatro archivos |

Los códigos de muestra reemplazan los IDs del estudio y el orden de filas fue permutado. Se conservaron las etiquetas, predicciones, puntajes y folds necesarios para los cálculos. El paquete excluye radiografías, rutas, hashes por imagen, identificadores de pacientes y modelos serializados.

```powershell
.\.venv\Scripts\python.exe -m src.reproducir_entrega --evidencia evidencia --salida reconstruccion
```

La salida incluye `metricas_test.csv`, `metricas_desarrollo.csv` y las cinco figuras del informe. El CSV de prueba debe coincidir con `results/metricas_test.csv` a la precisión numérica de las operaciones. En desarrollo, las métricas de cada par modelo–fold corresponden a `results/modelos_cv.csv`. La reconstrucción omite los tiempos de ajuste y predicción, que son mediciones de las ejecuciones originales.

`results/tuning_cv.csv` contiene los cinco F1 macro por configuración, la media y el desvío muestral. `results/seleccion_pretest.json` registra la decisión de selección y los umbrales fijados. La guía reproduce los cálculos a partir de los datos guardados. El código del experimento conserva el protocolo completo y la evidencia tabular basta para esta reconstrucción sin acceder a imágenes ni abrir el conjunto reservado.

La fuente de imágenes fue [COVID-19 Radiography Database, versión 5](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database/data), bajo las condiciones de uso académico indicadas en su ficha.
