# Sprint 05 · Tuning y congelamiento de selección

**Estado:** no iniciado. Depende del cierre 04.

# Objetivo

Ajustar hiperparámetros en desarrollo, seleccionar por protocolo y congelar pipeline, comparadores y evaluación antes de abrir test.

# Por qué existe este sprint

La selección y el tuning son parte del aprendizaje. Separarlos de evaluación final previene que el test se convierta en otra validación.

# Conocimientos previos necesarios

Hiperparámetros, GridSearchCV/RandomizedSearchCV, PCA, CV de selección, optimismo, presupuesto computacional y estadística pareada. Teoría §§11,17–18.

# Entradas

Cierre 04, resultados iniciales, tiempos/hardware, features/folds y protocolo del roadmap. Test debe seguir sellado y sin evaluación.

# Tareas

- [ ] Verificar aceptación 04 y ausencia de uso previo del test.
- [ ] Registrar espacio de búsqueda, scorer, presupuesto, hilos, memoria y semilla antes de ejecutarlo.
- [ ] Aplicar grillas base del roadmap: C/ponderación SVM, ausencia/PCA95 %, profundidad/hojas/features RF y C de logística.
- [ ] Usar GridSearchCV para espacios pequeños; RandomizedSearchCV solo con distribuciones y n_iter explícitos si hay ampliación justificada.
- [ ] Mantener scaler/PCA dentro de cada train de CV y respetar grupos/folds persistidos.
- [ ] Conservar todos los cv_results, fallos, medias/desvíos y tiempos, sin borrar configuraciones de bajo desempeño.
- [ ] Seleccionar por F1 macro medio con tolerancia operativa ≤0,005 y desempate por tiempo total de ajuste, luego tamaño, definidos antes de selección.
- [ ] Fijar umbral estándar y calibración ausente salvo validación adicional explícita solo en desarrollo.
- [ ] Reajustar final y comparadores predefinidos en todo desarrollo; guardar hash de artefactos locales y protocolo final.
- [ ] Conservar estimadores de los folds de la configuración seleccionada para interpretación retenida en 07; si se necesitan ajustes adicionales con esa configuración fija, presupuestarlos en desarrollo y registrarlos antes de test.
- [ ] Predefinir métricas, bootstrap, contraste primario, multiplicidad, comparabilidad CNN y lote único de test de 06.

# Archivos futuros involucrados

Crear `src/models/optimizar.py`, `configs/busqueda.json`, `configs/evaluacion_final.json`, `tests/test_busqueda.py`, `results/metrics/tuning_cv.csv`, `results/reports/seleccion_modelo.md` y `results/reports/protocolo_congelado.md`. Guardar pipelines locales en `models/` con hashes referenciados en informe; modificar configuración/modelos, README, decisiones y documentos afectados de forma consistente.

# Implementación esperada

Búsqueda CPU acotada, base 37 configuraciones×5 folds=185 fits más extras/reajustes; confirmar factibilidad con tiempos de 04. Selección automática según reglas previas, no juicio posterior basado en test. Reportar mejores valores CV como estimaciones de selección, no resultados finales sin sesgo. Si hay grupos, asegurar que se entregan a splitters y transformaciones apropiadas en API de versión usada. El documento congelado define IDs de comparadores, clase positiva, hash de split, métricas y condiciones estadísticas.

# Pruebas

Usar fixtures para demostrar que fit de scaler/PCA recibe solo train por fold, que configuración incompatible falla, que grilla y presupuesto se contabilizan y que mismo input/seed conserva selección bajo tolerancia numérica. Verificar desempate con casos simulados, test inaccesible y consistencia de hashes tras serialización. Revisar convergencia y memoria reales en búsqueda de desarrollo.

# Resultados esperados

Selección final fundamentada **antes de test**, reporte completo de tuning, artefactos congelados y protocolo que 06 consumirá sin cambiar decisiones. Aún no hay métricas test propias.

# Criterios de aceptación

Búsqueda trazable y dentro de presupuesto acordado; comparadores/B0/B1 definidos; métricas y errores reportados; selección respeta reglas predefinidas; test sin acceso; artefactos, thresholds, hashes y análisis estadístico congelados. Si se modifica protocolo tras ver test en futuro, no tratarlo como confirmatorio.

# Evidencias a conservar

Grilla/distribuciones, semillas, cv_results completo, hardware/hilos, tiempos/RAM, avisos, configuración ganadora, regla de selección, hashes de pipelines y protocolo final. No solo captura del mejor score.

# Riesgos

Sobreajustar la búsqueda a CV, PCA costosa, paralelismo que agota RAM, múltiples decisiones no registradas y falsa confianza en diferencias minúsculas.

# Errores frecuentes

Elegir PCA por varianza global incluyendo test, aumentar indefinidamente la búsqueda por resultados poco favorables, tratar desvío CV como IC y usar score del test para desempatar.

# Qué debemos comprender antes de cerrarlo

Por qué optimizar hiperparámetros no es evaluación final, cuánto costó la búsqueda y qué evidencia permitirá o impedirá una comparación estadística con CNN.

# Preguntas posibles de defensa

1. ¿Por qué se eligió esa grilla y ese presupuesto?
2. ¿Qué diferencia costo de tuning y costo de fit final?
3. ¿Dónde se ajustó PCA exactamente?
4. ¿La mejor media CV es imparcial?
5. ¿Qué criterio resuelve un empate práctico?
6. ¿Qué está congelado antes de test?
7. ¿Qué datos necesita McNemar?

# Definition of Done

Búsqueda, selección, artefactos y protocolo auditables; pruebas/criterios completos; test intacto; documentos/checklist actualizados; commit y push. No abrir test ni comenzar 06 automáticamente.

# Prompt para ejecutar este sprint con Codex

```text
Ejecutá exclusivamente SPRINT_05_OPTIMIZACION en juanquiros/ia2-covid-xray-ml/main.
Leé docs/ROADMAP_TFI.md, docs/TEORIA_Y_STACK.md, docs/COMPARATIVA_TFC_VS_PROPUESTA.md, docs/ejecucion/README.md y docs/ejecucion/SPRINT_05_OPTIMIZACION.md; verificá cierre/aceptación 04, resultados y test sellado. Revisá root/remote/rama/status/diff y respetá cambios previos.
Objetivo: tuning solo en desarrollo y selección congelada. Creá src/models/optimizar.py, configs/busqueda.json, configs/evaluacion_final.json, tests/test_busqueda.py, tuning_cv.csv, seleccion_modelo.md y protocolo_congelado.md; guardá modelos localmente con hashes, no en Git.
Antes de buscar registrá espacios, seeds, folds/grupos, scorer F1 macro, presupuesto de fits/RAM/tiempo y reglas de desempate del roadmap. Implementá búsquedas con Pipeline completo, PCA opcional y escalado aprendidos solo en train de cada fold. Conservá cv_results completos; seleccioná y reajustá en todo desarrollo final y comparadores congelados, con threshold estándar. Predefiní el lote de evaluación, métricas, incertidumbre y contrastes estadísticos condicionados a sus supuestos.
Restricciones: no usar test para ninguna decisión ni evaluarlo, no prometer resultados, no ejecutar sprint 06 ni posteriores; opcionales solo con justificación documentada y presupuesto. No entrenar CNN como extensión implícita.
Probá aislamiento de fit, folds, grilla, límites, determinismo, desempate, serialización y bloqueo de test. Cumplí aceptación/DoD y documentá resultados reales de desarrollo sin llamarlos desempeño final imparcial.
Actualizá decisiones, uso IA, README, índice, checklist y todos los documentos afectados. Revisá diff/check, stage específico, commit 'feat: tune candidates and freeze final evaluation protocol' y push origin/main. Informá SHA, pruebas, archivos, selección, incertidumbres y estado Git; detenete antes de test.
```
