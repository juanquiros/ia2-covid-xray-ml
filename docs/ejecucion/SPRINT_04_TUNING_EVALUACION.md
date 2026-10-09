# Objetivo

Realizar tuning acotado, seleccionar en desarrollo y evaluar test una vez; cerrar errores e interpretación del modelo elegido. **Estado: no iniciado.**

# Por qué lo hacemos

Una evaluación final defendible requiere fijar decisiones antes del test. Reunir tuning, evaluación y explicación en un sprint mantiene claro ese orden y evita reabrir selección.

# Conceptos necesarios

GridSearchCV, F1 macro, media/desvío CV, reajuste final, test retenido, FP/FN, scores, coeficientes/importancias y supuestos de McNemar.

# Entradas

README, roadmap, teoría, comparativa, fuentes e índice de ejecución vigentes; estado Git y registro del cierre anterior cuando exista. Cierre 03: candidatos, HOG fijo, folds, métricas y pruebas; manifiesto de desarrollo/test. Antes de este sprint no hay evaluación de test.

# Tareas

- [ ] Ejecutar GridSearchCV solo en desarrollo: SVM C={0.1,1,10}; RF n_estimators={100,200}, max_depth={None,20}, min_samples_leaf={1,3}. Mantener HOG y restantes parámetros. Cinco folds comunes: 55 ajustes de búsqueda, sin contar reajustes; no es una cuota experimental.
- [ ] Comparar CV y sus límites con B0; guardar resultados por configuración/fold y media/desvío muestral.
- [ ] Seleccionar por mayor F1 macro medio; empate exacto entre candidatos favorece SVM lineal y dentro de grilla se mantiene orden documentado. No descartar resultados incómodos.
- [ ] ANTES DEL TEST: registrar decisión, configuración, parámetros, split y commit de código; fijar B0/C1/C2 como lote final y C1 frente a C2 como único McNemar eventual, bilateral α=0.05. Basta registro sencillo, sin mecanismos de bloqueo.
- [ ] Reajustar modelos fijados con desarrollo completo y evaluar test UNA VEZ; guardar predicciones por ID y scores válidos. No cambiar ganador, umbral ni pipeline por lo observado.
- [ ] Generar matriz y accuracy, precision, recall, especificidad, F1 por clase/F1 macro. ROC-AUC solo con scores continuos válidos y ambas clases; PR/AP solo si desbalance real observado en desarrollo justificó su uso.
- [ ] Analizar FP/FN y aciertos; interpretar al elegido mediante coeficientes HOG de SVM o importancia RF. Permutación solo si aporta claridad sobre desarrollo, declarando sus límites. No SHAP ni mapas clínicos.
- [ ] Aplicar McNemar solo con predicciones individuales de C1/C2 sobre mismas imágenes y unidades razonablemente independientes. Reportar b/c, n, diferencia y p; si no corresponde, justificar. No Wilcoxon, 5×2cv ni bootstrap inferencial.
- [ ] Informar tiempos aproximados de extracción, búsqueda/ajuste e inferencia, tamaño y complejidad; RAM opcional fácil. Contrastar contextualmente con referencia CNN y registrar diferencias de datos/split/hardware.
- [ ] Verificar métricas desde predicciones ya guardadas sin reabrir experimentos, actualizar checklist/registros; commit y push. No iniciar 05.

# Archivos a crear/modificar

Completar `src/evaluation.py` y configuración; guardar `results/tuning_cv.csv`, `results/predicciones_test.csv`, `results/metricas_test.csv`, `reports/evaluacion.md` y figuras. Registrar selección previa en `docs/REGISTRO_EJECUCION.md`. Guardar modelo final local y su identificación/tamaño; no publicar binarios pesados ni datos sensibles.

# Pruebas

Antes del test, verificar separación y Pipeline mediante pruebas de desarrollo, grilla exacta y configuración fijada. Después, comprobar IDs de predicciones, matriz/sumas/fórmulas, signos/clases de scores, pares y supuestos estadísticos. Comprobar carga del modelo con un ejemplo de desarrollo. Reconstruir tablas desde predicciones guardadas; no usar test para decidir mejoras.

# Resultados esperados

Modelo seleccionado, evaluación final trazable, contraste histórico prudente, errores e interpretación accesibles y costo aproximado. Métricas nuevas se informan tal como resulten, sin prometer superioridad.

# Criterios de aceptación

- [ ] Búsqueda restringida y decisión registrada antes de test, con código/configuración identificables.
- [ ] Test evaluado una vez en lote predefinido; ganador no cambiado después.
- [ ] Métricas/matrices y FP/FN verificados; explicación del elegido con límites.
- [ ] McNemar válido o motivo explícito de omisión; no se agrega otro plan estadístico.
- [ ] Costos simples y comparación contextual documentados; commit y push confirmados.

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

# Prompt para Codex

```text
Ejecutá únicamente SPRINT_04_TUNING_EVALUACION según su plan vigente. Leé primero README.md,
docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md,
docs/FUENTES_Y_TRAZABILIDAD.md, docs/ejecucion/README.md y el registro de ejecución
si existe; inspeccioná Git y las instrucciones aplicables. Verificá evidencia de cierre del sprint 03; no lo des por completo por existir un plan.
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
