# Índice operativo de los sprints

**Estado al 09/10/2026:** planes preparados; sprints **00–08 no iniciados**. Esta planificación no constituye la ejecución de sprint 00. El siguiente paso requiere una nueva instrucción expresa del usuario.

## Filosofía y orden

Cada sprint entrega una unidad comprensible, reproducible y revisable. Leer primero [Roadmap](../ROADMAP_TFI.md), [Teoría y stack](../TEORIA_Y_STACK.md), [Comparativa](../COMPARATIVA_TFC_VS_PROPUESTA.md) y [Fuentes](../FUENTES_Y_TRAZABILIDAD.md). El aprendizaje de los dos integrantes es parte del trabajo: entender entradas, decisiones, controles y límites, no solo obtener archivos.

**UN SPRINT NO PUEDE COMENZAR SI EL ANTERIOR NO CUMPLE SUS CRITERIOS DE ACEPTACIÓN.** Si una dependencia no está cerrada, identificar la evidencia faltante y detener solo ese avance; no inventar un cierre ni ejecutar el siguiente sprint. El 00 depende de las fuentes y de una solicitud expresa, no de otro sprint.

| Orden | Documento | Entrega futura | Estado |
|---:|---|---|---|
| 00 | [Análisis del TFC](SPRINT_00_ANALISIS_TFC.md) | Matriz de evidencia y requisitos revisada, decisiones pendientes | No iniciado |
| 01 | [Datos](SPRINT_01_DATOS.md) | Entorno, inventario, grupos, partición y test sellado | No iniciado |
| 02 | [EDA](SPRINT_02_EDA.md) | Calidad y exploración de desarrollo, configuración de preprocesamiento | No iniciado |
| 03 | [Features y baseline](SPRINT_03_FEATURES_BASELINE.md) | HOG/LBP y B0 evaluados en CV de desarrollo | No iniciado |
| 04 | [Modelos](SPRINT_04_MODELOS.md) | C1, C2 y B1 con configuraciones fijas y mismos folds | No iniciado |
| 05 | [Optimización](SPRINT_05_OPTIMIZACION.md) | Búsqueda, selección y protocolo final congelado | No iniciado |
| 06 | [Evaluación](SPRINT_06_EVALUACION.md) | Test único, comparación y estadística válida | No iniciado |
| 07 | [Interpretabilidad](SPRINT_07_INTERPRETABILIDAD.md) | Explicaciones y análisis de errores sin modificar modelo | No iniciado |
| 08 | [Informe y defensa](SPRINT_08_INFORME_DEFENSA.md) | Informe, anexos, presentación y ensayo | No iniciado |

## Contrato experimental común

- Etiqueta propuesta: `1=COVID`, `0=normal`. “NO COVID” se usa en el alcance limitado de D4.
- Partición propuesta: 80 % desarrollo, 20 % test, semilla base 42; grupos por paciente/duplicados tienen prioridad. CV de cinco folds dentro de desarrollo; reducir k solo por factibilidad documentada antes de modelar.
- B0: DummyClassifier most_frequent. B1 adicional: HOG+scaler+logística L2. C1: HOG+scaler+SVM lineal. C2: LBP+RF. PCA es ablación de C1; RBF, KNN y otras combinaciones son opcionales acotadas, no obligaciones de implementación.
- Selección: F1 macro medio en CV; informar media ± desvío muestral por método. Ajustar transformaciones aprendidas dentro de cada fold mediante Pipeline.
- **05 selecciona y congela; 06 evalúa.** El test no decide extractor, modelo, umbral, hiperparámetros ni exclusiones. Comparadores congelados se evalúan juntos en un único lote final; 07 reutiliza predicciones de 06.
- EDA desde 02 solo sobre desarrollo. Antes de sellar, 01 puede auditar el inventario completo para integridad, metadatos, grupos y duplicados, sin buscar patrones predictivos de test.
- La CNN publicada es referencia histórica hasta demostrar equivalencia. No entrenar una CNN como extensión implícita ni aplicar McNemar a accuracies agregadas.

## Definition of Done general

Un sprint se cierra cuando sus tareas y criterios específicos se cumplen con evidencias, las pruebas pertinentes pasan, los resultados documentados coinciden con archivos reales y se registra qué conceptos debe dominar el equipo. Anotar comandos, versiones, semillas, hash de datos/particiones/configuración y limitaciones cuando corresponda. Un valor faltante se informa como no disponible, nunca como cero ni estimación inventada.

Actualizar checklist solo para actividades realizadas. Registrar en el propio sprint una sección de **Cierre real** con fecha, evidencias, pruebas, decisiones, incidencias y estado; en planificación esa sección aún no existe. Actualizar esta tabla y el README raíz al completar el sprint. Si los criterios no se cumplen, el estado es en curso o bloqueado por una dependencia concreta, nunca completado por haber generado archivos.

## Evidencias y resultados

Guardar informes pequeños en `results/reports/`, métricas tabulares en `results/metrics/`, figuras en `results/figures/` y configuración en `configs/`, únicamente cuando existan. Figuras numeradas, con ejes, unidades, epígrafes y lectura en el informe. Los binarios y datasets quedan locales con hashes; manifiestos publicables deben excluir identificadores personales.

En cada afirmación separar [A] fuente original, [B] requisito, [C] decisión y [D] hipótesis. Los resultados reales futuros deben incluir su ejecución de origen. Mantener registro de uso de IA desde 00, con validación realizada y versión solo cuando se conozca.

## Git y gestión de commits

Repositorio exclusivo: `https://github.com/juanquiros/ia2-covid-xray-ml.git`, rama `main` según solicitud. Antes de trabajar: verificar directorio raíz, remote, rama y estado; examinar diferencias existentes y preservarlas. Si hay otro repositorio, no modificarlo. Si el remoto avanzó, integrar de forma segura sin force-push ni pérdida de trabajo.

Un commit coherente por sprint, con documentación y evidencias pertinentes. Stage de archivos explícitos, nunca subir datos pesados o secretos mediante `git add .` sin revisión. Ejecutar controles, `git diff --check`, revisar diff y status; commit y push a `origin/main`. Informar SHA, lista de cambios, pruebas, estado y resultado del push. No afirmar que se publicó si falló la operación.

## Reglas para Codex

Ejecutar **solo** el sprint expresamente solicitado. Leer el sprint anterior y comprobar su cierre antes de realizar trabajo dependiente. No avanzar por iniciativa propia a otro sprint ni resolver objetivos ampliando alcance sin fundamento.

No descargar datasets en 00; no entrenar candidatos en 03; no hacer tuning en 04; no abrir test antes de 06. Pruebas sintéticas unitarias no son evidencia de desempeño real. No introducir TensorFlow, APIs, cloud, UI o infraestructura innecesaria. Si faltan fuentes o autorización de cátedra para sustituir datos, documentar la dependencia y continuar solo tareas independientes.

En una reproducción posterior al test final, no volver a seleccionar ni ajustar por el resultado conocido. Verificar cálculos desde predicciones congeladas; una nueva evaluación con objetivos modificados necesita nuevo protocolo. Los prompts de cada sprint son instrucciones futuras: su presencia en estos documentos no autoriza ejecutarlos ahora.
