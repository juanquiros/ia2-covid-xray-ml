# Ejecución vigente del TFI

**Estado al 08/11/2026: Sprint 04 cerrado.** Este índice reemplaza los nueve planes [archivados](../archivo/planificacion_inicial/README.md). El sprint correctivo original fue documental. La solicitud posterior de **00-A** autorizó un prototipo preliminar HOG + RF y Dummy, ya implementado con CV exploratoria real: [avance](../AVANCE_2026-11-02.md) y [registro](../REGISTRO_EJECUCION.md). El piloto se registra por separado.

Núcleo para COVID=1 frente a normal=0. Tras pasar a grises y 128×128, ambos candidatos reciben HOG fijo (9 orientaciones, celdas 8×8, bloques 2×2, L2-Hys). **C2 Random Forest** es la propuesta principal y **C1 StandardScaler + SVM lineal** el segundo candidato. **B0 `DummyClassifier(strategy="most_frequent")`** es la línea base.

| Orden | Plan activo | Cierre esperado | Estado |
|---|---|---|---|
| 00 | [Análisis TFC](SPRINT_00_ANALISIS_TFC.md) | Evidencias, alcance y revisión por integrantes | Cerrado el 05/11/2026 |
| 01 | [Datos y EDA](SPRINT_01_DATOS_EDA.md) | Entorno, datos autorizados, manifiesto/split y EDA de desarrollo | Cerrado el 08/11/2026 |
| 02 | [HOG y baseline](SPRINT_02_HOG_BASELINE.md) | Preprocesamiento/HOG fijo y B0 en CV | Cerrado el 08/11/2026 |
| 03 | [Modelos y CV](SPRINT_03_MODELOS_CV.md) | C1/C2 iniciales frente a B0 | Cerrado el 08/11/2026 |
| 04 | [Tuning y evaluación](SPRINT_04_TUNING_EVALUACION.md) | Selección, registro previo, test único, errores e interpretación | Cerrado el 08/11/2026 |
| 05 | [Informe y defensa](SPRINT_05_INFORME_DEFENSA.md) | Entrega académica y ensayo; sin experimentos nuevos | No iniciado |

Antes de ejecutar un plan, leer [Roadmap](../ROADMAP_TFI.md), [Teoría](../TEORIA_Y_STACK.md), [Comparativa](../COMPARATIVA_TFC_VS_PROPUESTA.md), [Fuentes](../FUENTES_Y_TRAZABILIDAD.md), este índice y estado del repositorio. El roadmap reúne el protocolo; cada sprint concreta sus tareas sin ampliar alcance.

Cada ejecución requiere una solicitud nueva, revisión del cierre anterior y registro breve de evidencia real. Las casillas vacías son trabajo futuro. Actualizar checklist y documentación, verificar el diff e informar el estado del sprint. Para 00, dejar el diff local. Commit y push de 00 requieren solicitud expresa. Si falta una decisión humana indispensable, registrar cuál y continuar solo con tareas independientes.

Repositorio: `juanquiros/ia2-covid-xray-ml`, rama `main`. Antes de modificar, verificar remoto, rama y cambios locales; preservar trabajo existente. Revisar diff y `git diff --check` e incluir solo archivos pertinentes. Cuando corresponda publicar, hacer push a `origin/main` sin forzar e informar SHA y resultado.

El test se reserva mediante manifiesto, sin mecanismos de bloqueo. 04 fija la selección y comparadores antes de evaluarlo una vez; interpretar errores no autoriza ajustar de nuevo. Estadística: media/desvío CV y McNemar solo si corresponde. 05 usa resultados existentes.

**Próximo sprint:** 05, informe final y defensa. Los resultados experimentales están en el [informe de evaluación](../../reports/evaluacion.md). La aprobación comunicada por el equipo y la versión verificada constan en el [registro de ejecución](../REGISTRO_EJECUCION.md). Los pendientes administrativos están en [Fuentes](../FUENTES_Y_TRAZABILIDAD.md).

La selección final se hará por F1 macro medio en desarrollo, con cinco folds comunes si los datos y grupos lo permiten. La CNN se mantiene como referencia histórica mientras falte evidencia de equivalencia. Las tareas anticipadas de 00-A se registran por separado.
