# Objetivo

Realizar tuning acotado, seleccionar en desarrollo y evaluar test una vez; cerrar errores e interpretación del modelo elegido. **Estado: cerrado el 08/11/2026.** Selección fijada en desarrollo, lote reservado único y métricas recalculadas desde las predicciones.

# Por qué lo hacemos

Una evaluación final defendible requiere fijar decisiones antes del test. Reunir tuning, evaluación y explicación en un sprint mantiene claro ese orden y evita reabrir selección.

# Conceptos necesarios

GridSearchCV, F1 macro, media/desvío CV, reajuste final, test retenido, FP/FN, scores, coeficientes/importancias y supuestos de McNemar.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 03 en `f315c05`. Usar el manifiesto de 01, HOG e índice de 02 y los resultados verificados de 03. Antes de este sprint no hay evaluación reservada.

# Tareas

- [x] Ejecutar GridSearchCV solo en desarrollo: SVM C={0.1,1,10}; RF n_estimators={100,200}, max_depth={None,20}, min_samples_leaf={1,3}. Mantener HOG y restantes parámetros. Cinco folds comunes: 55 ajustes de búsqueda, sin contar reajustes; no es una cuota experimental.
- [x] Comparar CV y sus límites con B0; guardar resultados por configuración/fold y media/desvío muestral.
- [x] Seleccionar por mayor F1 macro medio; empate exacto entre candidatos favorece SVM lineal y dentro de grilla se mantiene orden documentado. No descartar resultados incómodos.
- [x] ANTES DEL TEST: registrar decisión, configuración, parámetros, split, commit base y hashes del código local; fijar B0/C1/C2 como lote final y C1 frente a C2 como único McNemar eventual, bilateral α=0.05. Basta registro sencillo, sin mecanismos de bloqueo.
- [x] Reajustar modelos fijados con desarrollo completo y evaluar test UNA VEZ; guardar predicciones por ID y scores válidos. No cambiar ganador, umbral ni pipeline por lo observado.
- [x] Generar matriz y accuracy, precision, recall, especificidad, F1 por clase/F1 macro. ROC-AUC solo con scores continuos válidos y ambas clases; PR/AP solo si desbalance real observado en desarrollo justificó su uso.
- [x] Analizar FP/FN y aciertos; interpretar al elegido mediante coeficientes HOG de SVM o importancia RF. Permutación solo si aporta claridad sobre desarrollo, declarando sus límites. No SHAP ni mapas clínicos.
- [x] Aplicar McNemar solo con predicciones individuales de C1/C2 sobre mismas imágenes y unidades razonablemente independientes. Reportar b/c, n, diferencia y p; si no corresponde, justificar. No Wilcoxon, 5×2cv ni bootstrap inferencial.
- [x] Informar tiempos aproximados de extracción, búsqueda/ajuste e inferencia, tamaño y complejidad; RAM opcional fácil. Contrastar contextualmente con referencia CNN y registrar diferencias de datos/split/hardware.
- [x] Verificar métricas desde predicciones ya guardadas sin reabrir experimentos, actualizar checklist y registros y dejar el diff local para revisión. Commit y push requieren solicitud expresa.

# Archivos a crear/modificar

[Búsqueda por configuración](../../results/tuning_cv.csv), [registro previo](../../results/seleccion_pretest.json), [métricas reservadas](../../results/metricas_test.csv) e [informe](../../reports/evaluacion.md) con figuras. Las predicciones por ID, el modelo elegido y su registro de ejecución quedan en `data/processed/sprint_04_test/`, fuera de Git.

# Pruebas

Antes del test, verificar separación y Pipeline mediante pruebas de desarrollo, grilla exacta y configuración fijada. Después, comprobar IDs de predicciones, matriz/sumas/fórmulas, signos/clases de scores, pares y supuestos estadísticos. Comprobar carga del modelo con un ejemplo de desarrollo. Reconstruir tablas desde predicciones guardadas; no usar test para decidir mejoras.

# Resultados esperados

Modelo seleccionado, evaluación final trazable, contraste histórico prudente, errores e interpretación accesibles y costo aproximado. Métricas nuevas se informan tal como resulten, sin prometer superioridad.

# Criterios de aceptación

- [x] Búsqueda restringida y decisión registrada antes de test, con código/configuración identificables.
- [x] Test evaluado una vez en lote predefinido; ganador no cambiado después.
- [x] Métricas/matrices y FP/FN verificados; explicación del elegido con límites.
- [x] McNemar válido o motivo explícito de omisión; no se agrega otro plan estadístico.
- [x] Costos simples, comparación contextual, pruebas y diff local verificados.

# Qué debemos saber explicar

Por qué selección y test tienen funciones distintas, qué significa mejor CV, por qué la importancia no es causalidad, cuándo no corresponde McNemar y por qué superar 79,47 % no demuestra superioridad clínica.

# Preguntas posibles de defensa

1. ¿Cuántas configuraciones se buscaron y por qué esas?
2. ¿Qué decisiones quedaron registradas antes de test?
3. ¿Qué ocurre si otro comparador supera al elegido en test?
4. ¿Qué diferencia existe entre score SVM y probabilidad?
5. ¿Qué pares requiere McNemar y qué mide?
6. ¿Por qué no aplicar una prueba sobre accuracies agregadas del PDF?
7. ¿Qué limitan los coeficientes HOG o las importancias RF?
8. ¿Qué incluye el tiempo de inferencia informado?

# Reproducción interna

Desde la raíz, con el entorno fijado en `requirements.txt`, verificar el cierre de 03. Esta verificación incluye el manifiesto, HOG, índice y predicciones de Dummy. Si faltan artefactos, seguir el procedimiento del sprint correspondiente.

```powershell
.\.venv\Scripts\python.exe -m src.comparacion --config configs/experimento.json --output data/processed/sprint_03 --verify-only
.\.venv\Scripts\python.exe -m src.tuning --config configs/experimento.json --output data/processed/sprint_04_svm --candidate linear_svm
.\.venv\Scripts\python.exe -m src.tuning --config configs/experimento.json --output data/processed/sprint_04_rf --candidate random_forest
.\.venv\Scripts\python.exe -m src.tuning --config configs/experimento.json --output data/processed/sprint_04_busqueda --merge-from data/processed/sprint_04_svm data/processed/sprint_04_rf
Copy-Item -LiteralPath data/processed/sprint_04_busqueda/tuning_cv.csv -Destination results/tuning_cv.csv
.\.venv\Scripts\python.exe -m src.final --config configs/experimento.json --selection results/seleccion_pretest.json --freeze-from data/processed/sprint_04_busqueda
```

El último comando registra la selección y los hashes del código, configuración y artefactos antes de leer imágenes reservadas. La prueba del flujo usa imágenes sintéticas.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

El siguiente comando corresponde a la única ejecución del lote reservado. Con predicciones existentes, usar el comando de análisis para reconstruir métricas y figuras sin abrir el ZIP ni reajustar.

```powershell
.\.venv\Scripts\python.exe -m src.final --config configs/experimento.json --selection results/seleccion_pretest.json --evaluate-to data/processed/sprint_04_test
.\.venv\Scripts\python.exe -m src.analisis_final --config configs/experimento.json --selection results/seleccion_pretest.json --evaluation data/processed/sprint_04_test --results results/metricas_test.csv --figures reports/evaluacion
```

La evidencia de búsqueda en `data/processed/sprint_04_busqueda/tuning.json` conserva los avisos y tiempos por candidato. El registro de ejecución reservada incluye sus hashes, los tiempos y el identificador del modelo.
