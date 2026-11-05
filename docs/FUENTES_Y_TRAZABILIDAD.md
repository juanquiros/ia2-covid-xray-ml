# Fuentes, trazabilidad y control de la planificación

Consulta documental inicial **09/10/2026**. Cotejo del Sprint 00 **05/11/2026**. Este registro distingue evidencia documental de decisiones propias. Las instrucciones operativas provienen del usuario; el TFC es objeto de estudio y la consigna aporta requisitos académicos. La solicitud posterior de 00-A habilitó un piloto y el uso de la misma base pública, sin autorizar publicación de datos personales.

## Convenciones

- **[A] Hecho del TFC:** lo reportado en el documento original; no significa que se haya reproducido.
- **[B] Requisito TFI:** exigencia de la consigna, citada por sección.
- **[C] Propuesta propia:** diseño, crítica o cálculo documental de este equipo.
- **[D] Hipótesis:** afirmación por contrastar en experimentos futuros.
- **[E] Bibliografía adicional:** fundamento externo; nunca reemplaza una afirmación sobre lo que hizo el TFC.

Los títulos del roadmap indican el tipo de contenido. Los cálculos sobre tablas publicadas se identifican como reconstrucción documental, nunca como métricas de un modelo nuestro. Los resultados definitivos están **pendientes**; el piloto real 00-A se informa separadamente en [Avance](AVANCE_2026-11-02.md).

## Fuentes primarias locales

| ID | Documento e identificación | Localizador | SHA-256 |
|---|---|---|---|
| TFC | N. I. Vega Lencina y G. S. Armoa, *Modelo basado en redes neuronales convolucionales para el diagnóstico de COVID-19 mediante imágenes de rayos X guiado por CRISP-ML(Q)*, directora Mgter. Karina Eckert, 2023 | `TFC-2023.pdf`, 103 páginas; número impreso coincide con página PDF | `9f98f52deda6bd14999bd2d2d92d46a538597df9e5a9102678ee7694beba3cde` |
| TFI | *Trabajo Final Integrador (TFI). Análisis crítico de un Trabajo Final de Carrera y desarrollo de una solución alternativa basada en aprendizaje automático*, IA II; equipo docente Winnik Vanina y Héctor Ruidias; publicación 02/10/2026 | `C:/Users/quiro/Downloads/Trabajo Final Integrador (TFI)(1).docx`, copia de referencia para Sprint 00. Citas por sección | `30777f5b0d80766ea1036e3aee39a7d6bfa06127886bbb825615dca407c4ad4b` |

Se verificó el TFC en `OneDrive/Facultad - Ingenieria en Informatica/2026/ia2/TFC-2023.pdf`. La planificación inicial usó la copia `Trabajo Final Integrador (TFI) Consignas.docx` de esa misma carpeta, con SHA-256 `86360af8dfb3b6a3c5ae4f5f823bcb879d216b6304544a986d340a1df1e5ca4a`. Los dos DOCX tienen hashes distintos y coinciden en los párrafos y filas de tablas extraídos. Las citas de este sprint remiten a la copia de Descargas indicada arriba. Los originales y los archivos de trabajo de la revisión se mantuvieron fuera del repositorio.

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

La lectura inicial cubrió las 103 páginas. En el Sprint 00 se cotejaron los cuatro conjuntos (tabla 2), las particiones declaradas (tabla 3), las doce pruebas (tablas 4–17), la matriz de D4 (figura 38), el código y el resumen de la CNN (anexos I–IV), la discrepancia de prueba 8 (tabla 25 y registro de época 20) y los 52 casos de revisión profesional (tabla 30). El [registro de ejecución](REGISTRO_EJECUCION.md) distingue este cotejo de la confirmación de los integrantes.

### Discrepancias que deben conservarse

| ID | Evidencia exacta | Tratamiento |
|---|---|---|
| D01 | P. 21 dice datasets equilibrados; tabla 2 p. 36 da D1=10972/10192 | No afirmar balance exacto de D1 |
| D02 | P. 33 declara 80/10/10; tabla 3 p. 43 da 1018 por clase para validation y test de D1 | No inventar conteos exactos de train; mostrar diferencia con el 10 % de positivos |
| D03 | Tabla 3: D2 test 496/496; figura 32 p. 47 suma 495 COVID y 496 normales | Reportar ambas evidencias; manifiestos no disponibles |
| D04 | Tabla 3: D3 test 361/361; figura 35 p. 50 suma 362/362 | No ocultar divergencia ni reconstruir IDs inexistentes |
| D05 | La prosa de p. 38 puede ubicar el segundo MaxPooling después de la tercera convolución. La figura 25 (p. 39) y los anexos I–II (pp. 69, 72) lo ubican entre la segunda y la tercera. La figura 26 (p. 40) omite los pooling en el esquema general | Reconstruir tres convoluciones y dos MaxPooling, después de la primera y segunda |
| D06 | Anexo I p. 68 usa `rescale=1./255` en train/validación. El generador de test del anexo IV p. 75 omite ese ajuste | Inconsistencia confirmada en código publicado; efecto en resultados no demostrado |
| D07 | Anexo III p. 73 omite reescalado y modo grayscale; modelo p. 72 recibe un canal | Riesgo de incompatibilidad de inferencia; no afirmar qué versión ejecutaron |
| D08 | Tabla 16 p. 56 y tabla 25 p. 91 repiten cifras de prueba 7 para prueba 8; log época 20 p. 91 da otras | Mantener ambos registros, sin corregir silenciosamente |

No hay evidencia suficiente para afirmar pacientes compartidos entre particiones. Ausencia de manifiestos, semillas y versiones limita la verificación; no prueba por sí sola data leakage.

## Matriz de requisitos de la consigna [B]

| Sección | Requisito | Documento / sprint de cumplimiento futuro |
|---|---|---|
| 4 y 5.1 | TFC asignado, crítica respetuosa y sustentada | Roadmap; 00 |
| 4 | Si los datos originales faltan o resultan insuficientes, un conjunto público equivalente requiere autorización previa de cátedra y justificación en el informe | 00 documenta el requisito. Resolver antes de adoptar el sustituto en 01 |
| 4 | Protección de información personal; la consigna menciona Ley 25.326 | 01, 04, 05; citar requisito, sin emitir dictamen legal |
| 5.2.1 | Entrada, objetivo, criterio a optimizar, teoría, costo y supuestos de cada modelo | Roadmap y teoría; 02–04 |
| 5.2.2 | Baseline más al menos dos candidatos; selección experimental | 02–04 |
| 5.3 | Pipeline, CV, tuning sin test, semillas, entorno y regeneración completa | 01–04 |
| 5.4 | Métricas justificadas, media/desvío CV, estadística cuando corresponda, test único y contraste equivalente | 03–04 |
| 5.5–5.6 | Errores, interpretabilidad, EDA, curvas apropiadas y figuras interpretadas | 01, 03, 04 |
| 5.7–5.8 | Ética, despliegue conceptual, monitoreo, discusión y límites | 04–05 |
| 7.1 | PDF A4, márgenes 2,5 cm, Arial/Times 11–12 pt, interlineado 1,15–1,5, numeración; 20–30 páginas orientativas sin anexos; APA 7 o IEEE consistente | 05; se propone IEEE |
| 7.1 | Carátula con legajos/docentes/fecha; resumen ≤250 palabras y palabras clave en español e inglés; índices general/figuras/tablas; secciones completas y anexo IA | 05 |
| 7.2 | Repositorio accesible a cátedra o ZIP; resultados regenerables | Todos; última versión anterior a entrega |
| 7.3 | Defensa [15] minutos + [10] preguntas; ambos exponen y dominan todo | 05; confirmar tiempos entre corchetes |
| 7.4 | Nombre `TFI_IA2_Quiros_Andruszyszyn`, sin tildes/espacios; plataforma entre corchetes | 05 |
| 8 | ≥6, ningún criterio insuficiente, defensa individual; única reentrega en 5 días hábiles | 05; organizar revisión por rúbrica |
| 9 | Citas, comprensión del código, declaración obligatoria de IA y resultados verificables | Registro de IA desde 00; anexo en 05 |
| 10 | Posible ejecución y reproducción en defensa | 05; ensayo en entorno limpio |

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
| E18 | [Dietterich, 1998, Neural Computation](https://doi.org/10.1162/089976698300017197) | Pruebas aproximadas y diseño 5×2cv; no aplicar t ingenua sobre folds. Ficha disponible en [PubMed](https://pubmed.ncbi.nlm.nih.gov/9744903/) |
| E19 | [SciPy, Wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html) | Diferencias pareadas, simetría, ceros y empates |
| E20 | [statsmodels, McNemar](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html) | Tabla de discordancias; alternativa exacta binomial |

La [ficha de Kaggle](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database/data) identifica la base citada en [46] del TFC. La consulta inicial del 09/10 no devolvió cuerpo legible y no descargó datos. El 02/11 se verificaron metadatos y se descargó la versión 5 para 00-A, como se detalla al final. En 00 se comprobó la ficha de datos de Kaggle y se verificaron referencias bibliográficas por sus fichas o preprints cuando el acceso directo al editor estaba restringido. Las cantidades históricas siguen atribuidas al TFC, sin corregirlas con la versión actual.

## Alcance bibliográfico tras la simplificación

Se conserva la investigación realizada; no se reinicia búsqueda bibliográfica. E03/E05 sustentan HOG; E06 SVM lineal; E07 RF; E01/E02/E11/E12/E14 el protocolo. E20 solo sustenta McNemar condicionado a predicciones pareadas y supuestos. E13 permite estudiar importancia por permutación si aporta una explicación sencilla.

E04 (LBP), E08 (KNN), E09 (logística), E10 (PCA) y E17–E19 (estadística alternativa) quedan como **consulta complementaria**, sin tareas experimentales comprometidas. Que una referencia cubra RBF o búsqueda aleatoria no habilita incorporarlos al núcleo. PCA solo se reconsiderará ante problema medido y decisión explícita.

La secuencia vigente es 00 análisis, 01 datos/EDA, 02 HOG/baseline, 03 modelos/CV, 04 tuning/evaluación/interpretación y 05 informe/defensa. El [archivo histórico](archivo/planificacion_inicial/README.md) no contiene instrucciones activas. Las fuentes primarias, D01–D08 y E01–E20 conservan su valor y atribución.

## Control histórico de la etapa documental · 09/10/2026

- Lectura de fuentes primarias y contraste de anexos: realizado.
- Reconstrucción de cuatro datasets y doce pruebas: realizada documentalmente, con discrepancias abiertas.
- Plan simplificado: HOG compartido, B0 DummyClassifier, C1 SVM lineal y C2 Random Forest; teoría principal y complementaria separadas.
- Seis sprints activos 00–05: redactados, **no iniciados**; nueve planes originales archivados sin ejecutar.
- Resultados nuevos, entrenamiento, tuning y conclusiones experimentales: inexistentes.
- Auditoría correctiva: 13 documentos vigentes (incluido el índice del archivo) con enlaces locales y cercos de código verificados; seis sprints con exactamente doce secciones y tareas sin marcar. Los nueve planes archivados son idénticos byte por byte a sus originales. Se conservaron sin cambios las secciones históricas 1–8 del roadmap, las discrepancias D01–D08 y las veinte referencias E01–E20; la comparativa mantiene 18 secciones y dos diagramas. Se revisó la cobertura de la consigna y la coherencia de HOG, candidatos, grillas y test. El SHA se informa al cerrar este sprint documental.

La revisión documental no valida clínicamente el sistema ni confirma hipótesis de desempeño. La aprobación de cada sprint se registra solamente cuando existan sus evidencias reales.

## Verificación posterior · 02/11/2026

Se descargó la misma base pública por la API de Kaggle tras indicación del usuario: versión 5, actualizada en origen el 19/03/2022, con 3616 COVID y 10192 normales. La diferencia con los 3615 COVID del TFC se mantiene explícita. La descripción indica uso académico/no comercial y la etiqueta de licencia es «Data files © Original Authors»; no se redistribuye el dataset. Los metadatos de ambas clases contienen FILE NAME, FORMAT, SIZE y URL, sin patient_id explícito. Se revisó ese esquema y se auditaron duplicados SHA-256; los nombres de archivo no prueban independencia de pacientes. Detalle de versión, SHA, muestra y exclusiones en [procedencia del piloto](../reports/piloto_2026-11-02/README.md).

La fuente solicita citar M. E. H. Chowdhury et al., «Can AI help in screening Viral and COVID-19 pneumonia?», IEEE Access, 2020, pp. 132665–132676 ([artículo](https://ieeexplore.ieee.org/document/9144185), [preprint de los autores](https://arxiv.org/abs/2003.13145)), y T. Rahman et al., «Exploring the Effect of Image Enhancement Techniques on COVID-19 Detection using Chest X-ray Images», Computers in Biology and Medicine, 2021 ([DOI](https://doi.org/10.1016/j.compbiomed.2021.104319)). Se conservarán estas atribuciones en el informe.

Para implementar se consultaron las API oficiales de [HOG](https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.hog), [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) y [StratifiedGroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html). Las versiones efectivamente ejecutadas constan en requirements.txt y summary.json; no se infieren de la versión de una página web.
