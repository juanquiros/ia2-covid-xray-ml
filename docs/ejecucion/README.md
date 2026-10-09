# Ejecución vigente del TFI

**Estado al 09/10/2026: seis sprints no iniciados.** Este índice reemplaza los nueve planes [archivados](../archivo/planificacion_inicial/README.md). El sprint correctivo únicamente simplificó documentación; no ejecutó análisis operativo, descarga, HOG ni entrenamiento.

Núcleo: radiografía → grises/128×128 → HOG fijo (9 orientaciones, celdas 8×8, bloques 2×2, L2-Hys) → **C1 StandardScaler + SVM lineal** o **C2 Random Forest**. **B0 DummyClassifier most_frequent** es la única baseline. No hay otros descriptores o candidatos programados.

| Orden | Plan activo | Cierre esperado | Estado |
|---|---|---|---|
| 00 | [Análisis TFC](SPRINT_00_ANALISIS_TFC.md) | Evidencias, alcance y revisión por integrantes | No iniciado |
| 01 | [Datos y EDA](SPRINT_01_DATOS_EDA.md) | Entorno, datos autorizados, manifiesto/split y EDA de desarrollo | No iniciado |
| 02 | [HOG y baseline](SPRINT_02_HOG_BASELINE.md) | Preprocesamiento/HOG fijo y B0 en CV | No iniciado |
| 03 | [Modelos y CV](SPRINT_03_MODELOS_CV.md) | C1/C2 iniciales frente a B0 | No iniciado |
| 04 | [Tuning y evaluación](SPRINT_04_TUNING_EVALUACION.md) | Selección, registro previo, test único, errores e interpretación | No iniciado |
| 05 | [Informe y defensa](SPRINT_05_INFORME_DEFENSA.md) | Entrega académica y ensayo; sin experimentos nuevos | No iniciado |

Antes de ejecutar un plan, leer [Roadmap](../ROADMAP_TFI.md), [Teoría](../TEORIA_Y_STACK.md), [Comparativa](../COMPARATIVA_TFC_VS_PROPUESTA.md), [Fuentes](../FUENTES_Y_TRAZABILIDAD.md), este índice y estado del repositorio. El roadmap reúne el protocolo; cada sprint concreta sus tareas sin ampliar alcance.

Cada ejecución requiere una solicitud nueva, revisión del cierre anterior y registro breve de evidencia real. Las casillas vacías son trabajo futuro. Actualizar checklist/documentación, verificar, hacer commit y push, e informar el cierre sin iniciar el siguiente. Si falta una decisión humana indispensable, registrar cuál y continuar solo con tareas independientes.

Repositorio: `juanquiros/ia2-covid-xray-ml`, rama `main`. Antes de modificar, verificar remoto, rama y cambios locales; preservar trabajo existente. Revisar diff y `git diff --check`, incluir solo archivos pertinentes y hacer push a `origin/main` sin forzar. Informar SHA y resultado real de publicación.

El test se reserva mediante manifiesto, sin mecanismos de bloqueo. 04 fija la selección y comparadores antes de evaluarlo una vez; interpretar errores no autoriza ajustar de nuevo. Estadística: media/desvío CV y McNemar solo si corresponde. 05 usa resultados existentes.

**Próximo:** solicitar 00; no ha comenzado. Pendientes humanos: revisión y comprensión de ambos integrantes; datos administrativos para carátula; fecha/plataforma/tiempos de cátedra; acceso, licencia y comparabilidad de datos en 01, y autorización de sustitución si corresponde.
