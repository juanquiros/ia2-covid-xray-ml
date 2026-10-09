# Fuentes, trazabilidad y control de la planificación

Fecha de consulta: **09/10/2026**. Este registro permite distinguir evidencia documental de decisiones propias. Las instrucciones operativas provienen del texto solicitado por el usuario; el TFC es un objeto de estudio y la consigna aporta requisitos académicos. Ninguno habilita ejecutar ahora experimentos ni publicar datos personales.

## Convenciones

- **[A] Hecho del TFC:** lo reportado en el documento original; no significa que se haya reproducido.
- **[B] Requisito TFI:** exigencia de la consigna, citada por sección.
- **[C] Propuesta propia:** diseño, crítica o cálculo documental de este equipo.
- **[D] Hipótesis:** afirmación por contrastar en experimentos futuros.
- **[E] Bibliografía adicional:** fundamento externo; nunca reemplaza una afirmación sobre lo que hizo el TFC.

Los títulos del roadmap indican el tipo de contenido. Los cálculos sobre tablas publicadas se identifican como reconstrucción documental, nunca como métricas de un modelo nuestro. Todos los resultados experimentales propios están **pendientes**.

## Fuentes primarias locales

| ID | Documento e identificación | Localizador | SHA-256 |
|---|---|---|---|
| TFC | N. I. Vega Lencina y G. S. Armoa, *Modelo basado en redes neuronales convolucionales para el diagnóstico de COVID-19 mediante imágenes de rayos X guiado por CRISP-ML(Q)*, directora Mgter. Karina Eckert, 2023 | `TFC-2023.pdf`, 103 páginas; número impreso coincide con página PDF | `9f98f52deda6bd14999bd2d2d92d46a538597df9e5a9102678ee7694beba3cde` |
| TFI | *Trabajo Final Integrador (TFI). Análisis crítico de un Trabajo Final de Carrera y desarrollo de una solución alternativa basada en aprendizaje automático*, IA II; equipo docente Winnik Vanina y Héctor Ruidias; publicación 02/10/2026 | `Trabajo Final Integrador (TFI) Consignas.docx`; referencias por sección, sin inventar paginación | `86360af8dfb3b6a3c5ae4f5f823bcb879d216b6304544a986d340a1df1e5ca4a` |

Ambos archivos se localizaron en el directorio `2026/ia2` de la carpeta académica de OneDrive indicada por el usuario. No estaban dentro del repositorio. No se copian a Git: son referencias locales, no entregables creados por este equipo. Para reproducir la revisión, proporcionar esas copias y verificar sus hashes; si cambian, revisar las citas. Las extracciones y renderizados de trabajo se conservaron fuera del repositorio durante esta planificación.

### Cobertura de lectura realizada

| Páginas TFC | Contenido revisado | Uso |
|---|---|---|
| 1–8 | Autoría, resumen, índice, motivación, objetivos y difusión | Identidad y alcance; no confundir con publicación CACIC |
| 9–12 | Contexto sanitario y límites de imágenes | Contextualización histórica; no guía clínica actual |
| 13–31 | IA, redes, métricas, CNN y seis fases CRISP-ML(Q) | Reconstrucción conceptual, con correcciones pedagógicas propias |
| 32–42 | Propuesta, cuatro datasets, preparación, stack, arquitectura, entrenamiento y pruebas | Diseño original |
| 43–60 | Doce pruebas, comparación, validación profesional y fallos | Tablas y análisis crítico |
| 61–62 | Conclusiones, limitaciones y trabajos futuros | Límites explícitos y oportunidades |
| 63–66 | Referencias originales | Identificación de dataset y metodología |
| 67–75 | Anexos I–IV: código, resumen del modelo, predicción y matriz | Verificación de arquitectura y consistencia |
| 76–99 | Anexo V: registros de las 20 épocas de cada entrenamiento y gráficos | Diferenciar validación/test; discrepancia de prueba 8 |
| 100–103 | Tabla de 52 casos y entrevistas | Denominadores, concordancia y contexto del umbral del 75 % |

Se extrajo y revisó texto de las 103 páginas. Se verificaron visualmente tablas, matrices y código decisivos en pp. 43, 44, 47, 50, 53, 57, 69, 72, 73, 75, 100 y 101. Esta lectura documental completa **no ejecuta el sprint 00**, cuyo cierre requerirá la revisión de los integrantes y el registro operativo previsto.

### Discrepancias que deben conservarse

| ID | Evidencia exacta | Tratamiento |
|---|---|---|
| D01 | P. 21 dice datasets equilibrados; tabla 2 p. 36 da D1=10972/10192 | No afirmar balance exacto de D1 |
| D02 | P. 33 declara 80/10/10; tabla 3 p. 43 da 1018 por clase para validation y test de D1 | No inventar conteos exactos de train; mostrar diferencia con el 10 % de positivos |
| D03 | Tabla 3: D2 test 496/496; figura 32 p. 47 suma 495 COVID y 496 normales | Reportar ambas evidencias; manifiestos no disponibles |
| D04 | Tabla 3: D3 test 361/361; figura 35 p. 50 suma 362/362 | No ocultar divergencia ni reconstruir IDs inexistentes |
| D05 | Anexos I–II pp. 69,72: tres convoluciones y **dos** MaxPooling; prosa/diagramas pueden inducir tres | Priorizar código y resumen para reconstrucción técnica |
| D06 | Anexo I p. 68 reescala train/validation; anexo IV p. 75 no reescala test | Inconsistencia confirmada en código publicado; efecto en resultados no demostrado |
| D07 | Anexo III p. 73 omite reescalado y modo grayscale; modelo p. 72 recibe un canal | Riesgo de incompatibilidad de inferencia; no afirmar qué versión ejecutaron |
| D08 | Tabla 16 p. 56 y tabla 25 p. 91 repiten cifras de prueba 7 para prueba 8; log época 20 p. 91 da otras | Mantener ambos registros, sin corregir silenciosamente |

No hay evidencia suficiente para afirmar pacientes compartidos entre particiones. Ausencia de manifiestos, semillas y versiones limita la verificación; no prueba por sí sola data leakage.

## Matriz de requisitos de la consigna [B]

| Sección | Requisito | Documento / sprint de cumplimiento futuro |
|---|---|---|
| 4 y 5.1 | TFC asignado, crítica respetuosa y sustentada | Roadmap; 00 |
| 4 | Dataset público equivalente si falta el original: autorización de cátedra y justificación | 00–01; bloqueo solo de sustitución de datos |
| 4 | Protección de información personal; la consigna menciona Ley 25.326 | 01, 07, 08; citar requisito, sin emitir dictamen legal |
| 5.2.1 | Entrada, objetivo, criterio a optimizar, teoría, costo y supuestos de cada modelo | Roadmap y teoría; 03–05 |
| 5.2.2 | Baseline más al menos dos candidatos; selección experimental | 03–06 |
| 5.3 | Pipeline, CV, tuning sin test, semillas, entorno y regeneración completa | 01–06 |
| 5.4 | Métricas justificadas, media/desvío CV, estadística cuando corresponda, test único y contraste equivalente | 05–06 |
| 5.5–5.6 | Errores, interpretabilidad, EDA, curvas apropiadas y figuras interpretadas | 02, 05, 06, 07 |
| 5.7–5.8 | Ética, despliegue conceptual, monitoreo, discusión y límites | 07–08 |
| 7.1 | PDF A4, márgenes 2,5 cm, Arial/Times 11–12 pt, interlineado 1,15–1,5, numeración; 20–30 páginas orientativas sin anexos; APA 7 o IEEE consistente | 08; se propone IEEE |
| 7.1 | Carátula con legajos/docentes/fecha; resumen ≤250 palabras y palabras clave en español e inglés; índices general/figuras/tablas; secciones completas y anexo IA | 08 |
| 7.2 | Repositorio accesible a cátedra o ZIP; resultados regenerables | Todos; última versión anterior a entrega |
| 7.3 | Defensa [15] minutos + [10] preguntas; ambos exponen y dominan todo | 08; confirmar tiempos entre corchetes |
| 7.4 | Nombre `TFI_IA2_Quiros_Andruszyszyn`, sin tildes/espacios; plataforma entre corchetes | 08 |
| 8 | ≥6, ningún criterio insuficiente, defensa individual; única reentrega en 5 días hábiles | 08; organizar revisión por rúbrica |
| 9 | Citas, comprensión del código, declaración obligatoria de IA y resultados verificables | Registro de IA desde 00; anexo en 08 |
| 10 | Posible ejecución y reproducción en defensa | 08; ensayo en entorno limpio |

Ponderaciones de la rúbrica: análisis 15 %, fundamento/modelos 20 %, implementación/reproducibilidad 20 %, evaluación 20 %, visualización/interpretabilidad/ética 10 %, comunicación 15 %.

Pendientes de cátedra: fecha final (`[dd/mm/aaaa]`), plataforma, tiempos entre corchetes y cualquier material estadístico adicional aludido en la nota final del DOCX. No se interpreta esa nota como contenido adjunto disponible. Pendientes del equipo: nombre completo de Andruszyszyn, legajos e institución para carátula.

## Bibliografía adicional [E]

Consulta web del 09/10/2026. Enlaces a documentación oficial o investigación primaria. Las páginas `stable` evolucionan: fijar versiones ejecutadas en sprint 01. Estas referencias no certifican rendimiento en este dataset.

| ID | Fuente | Sustento y alcance |
|---|---|---|
| E01 | [scikit-learn, Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) | Separar ajuste de transformaciones y evaluación |
| E02 | [scikit-learn, Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) | CV estratificada y agrupada; dependencia entre folds |
| E03 | [scikit-image, HOG](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html) | Gradientes, histogramas y normalización de bloques; referencia a Dalal y Triggs (2005) |
| E04 | [scikit-image, LBP](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_local_binary_pattern.html) | Vecindarios y representación de textura |
| E05 | [scikit-image, API feature](https://scikit-image.org/docs/stable/api/skimage.feature.html) | Parámetros y contratos de HOG/LBP |
| E06 | [scikit-learn, SVM](https://scikit-learn.org/stable/modules/svm.html) | Márgenes, kernels, escalado y costo |
| E07 | [scikit-learn, Ensembles](https://scikit-learn.org/stable/modules/ensemble.html) | Bosques, agregación y restricciones |
| E08 | [scikit-learn, Neighbors](https://scikit-learn.org/stable/modules/neighbors.html) | KNN y dimensionalidad |
| E09 | [scikit-learn, Linear models](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression) | Regresión logística regularizada |
| E10 | [scikit-learn, Decomposition](https://scikit-learn.org/stable/modules/decomposition.html#pca) | PCA y varianza |
| E11 | [scikit-learn, Hyperparameter tuning](https://scikit-learn.org/stable/modules/grid_search.html) | Grilla, búsqueda aleatoria y costo |
| E12 | [scikit-learn, Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) | Métricas de clasificación, curvas y promedios |
| E13 | [scikit-learn, Permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html) | Importancia de variables, correlación y evaluación |
| E14 | [scikit-learn, StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) | Media/desvío aprendidos y transformación consistente |
| E15 | [Studer et al., Towards CRISP-ML(Q), preprint](https://arxiv.org/abs/2003.05155) | Seis fases y aseguramiento de calidad; versión publicada 2021, DOI 10.3390/make3020020, también citada en TFC |
| E16 | [DeGrave, Janizek y Lee, 2021](https://www.nature.com/articles/s42256-021-00338-7) | Evidencia de aprendizaje de atajos en otros sistemas de COVID; motiva auditoría, no demuestra sesgo del TFC |
| E17 | [Demšar, 2006, JMLR](https://jmlr.org/papers/v7/demsar06a.html) | Comparación de clasificadores entre múltiples datasets; no legitima tratar folds dependientes como datasets |
| E18 | [Dietterich, 1998, Neural Computation](https://doi.org/10.1162/089976698300017197) | Pruebas aproximadas y diseño 5×2cv; no aplicar t ingenua sobre folds |
| E19 | [SciPy, Wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html) | Diferencias pareadas, simetría, ceros y empates |
| E20 | [statsmodels, McNemar](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html) | Tabla de discordancias; alternativa exacta binomial |

La [ficha de Kaggle](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database) corresponde al enlace [46] del TFC. La consulta web no devolvió cuerpo legible: **versión, licencia, disponibilidad de metadatos y descarga siguen pendientes de verificación** en 01. Las cantidades históricas provienen del TFC, no de una descarga actual. No se descargó el dataset.

## Control realizado en esta etapa

- Lectura de fuentes primarias y contraste de anexos: realizado.
- Reconstrucción de cuatro datasets y doce pruebas: realizada documentalmente, con discrepancias abiertas.
- Plan experimental, teoría, baseline, dos candidatos principales y alternativas: documentados.
- Sprints 00–08: redactados, **no ejecutados**; todos conservan tareas pendientes.
- Resultados nuevos, entrenamiento, tuning y conclusiones experimentales: inexistentes.
- Verificación estructural y de enlaces locales: realizada antes del commit de planificación; 15 archivos Markdown, nueve sprints con 17 secciones obligatorias y entre 6 y 8 preguntas cada uno, 60 preguntas en teoría, 28 en comparativa, 18 secciones comparativas y dos diagramas comparativos. Sin enlaces locales rotos ni cercos de código desbalanceados. El cierre Git se informa con SHA en la entrega, sin introducir un segundo commit circular.

La revisión documental no valida clínicamente el sistema ni confirma hipótesis de desempeño. La aprobación de cada sprint se registra solamente cuando existan sus evidencias reales.
