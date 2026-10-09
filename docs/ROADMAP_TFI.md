# Roadmap del TFI de Inteligencia Artificial II

**Equipo:** Juan Quirós y Andruszyszyn. **Fecha:** 09/10/2026. **Estado:** planificación previa a sprint 00; ninguna implementación o experimentación propia ejecutada.

Este proyecto estudiará si características explícitas de radiografías permiten construir una alternativa clásica defendible a la CNN del TFC de Vega Lencina y Armoa (2023). El núcleo compara **HOG + StandardScaler + SVM lineal** con **HOG + Random Forest**, usando **DummyClassifier most_frequent** como única baseline. La elección final dependerá de validación cruzada; no existe un ganador anticipado.

Leer junto con [Teoría y stack](TEORIA_Y_STACK.md), [Comparativa pedagógica](COMPARATIVA_TFC_VS_PROPUESTA.md), [Fuentes y trazabilidad](FUENTES_Y_TRAZABILIDAD.md) y [Ejecución](ejecucion/README.md). Las marcas **[A] TFC**, **[B] consigna**, **[C] propuesta** y **[D] hipótesis** separan evidencia y decisiones. [E] remite a bibliografía adicional registrada en Fuentes. Citas TFC: páginas PDF/impresas, no páginas de un artículo previo.

## 1. Contexto y requisitos [A, B]

El TFC nació en el contexto de pandemia y buscó apoyar el reconocimiento de signos en radiografías de tórax mediante una CNN. La motivación histórica fue la disponibilidad de radiografías y las dificultades de acceso o demora de pruebas de laboratorio (TFC pp. 6–7). No trasladaremos sus afirmaciones sanitarias históricas a recomendaciones médicas actuales.

La consigna pide analizar críticamente el TFC asignado, diseñar una solución distinta, justificar formalmente modelos, comparar una baseline más dos candidatos, implementar un pipeline reproducible y evaluar con test reservado. También exige interpretación, análisis de errores, ética y despliegue conceptual. No exige desarrollar una aplicación web ni superar una cifra de accuracy (TFI §§4–5). La matriz completa de requisitos, formato de informe, rúbrica y pendientes administrativos está en [Fuentes](FUENTES_Y_TRAZABILIDAD.md).

## 2. Reconstrucción del problema original [A]

**Autores:** Nuria Isabel Vega Lencina y Guido Sebastián Armoa. **Directora:** Mgter. Karina Eckert. **Año:** 2023. El documento completo tiene 103 páginas, incluidos código, entrenamientos y entrevistas.

El objetivo general fue desarrollar un prototipo que reconociera signos de COVID-19 en radiografías mediante CNN. Los objetivos específicos fueron establecer el estado del arte, analizar/diseñar la CNN, desarrollar el prototipo y validar resultados junto a un experto (p. 7). La tarea computacional fue clasificación binaria de imágenes; la etiqueta de infección, el signo radiográfico y el diagnóstico clínico no son conceptos equivalentes.

## 3. Datos originales y cuatro configuraciones [A]

La fuente fue **COVID-19 Radiography Database**, publicada en Kaggle por investigadores asociados a Qatar y Dhaka y colaboradores. Según pp. 32–33, son PNG de **299×299 píxeles**. Las clases originales suman **21164 imágenes** (suma documental): 3615 COVID, 10192 normales, 6012 opacidad pulmonar y 1345 neumonía viral.

El TFC atribuye las 3615 COVID a 2473 de PadChest, 183 de una escuela de medicina alemana, 559 de SIRM/GitHub/Kaggle/Tweeter y 400 de otra fuente GitHub. Las normales proceden de RSNA (8851) y Kaggle (1341); opacidad pulmonar de RSNA (6012); neumonía viral de Kaggle (1345). Esto reproduce la procedencia **declarada por el TFC**, sin certificar cada fuente. Los métodos de confirmación y la etapa de enfermedad no son homogéneos ni están detallados por imagen (p. 33).

| Dataset | COVID operativo | NO COVID operativo | Cantidad COVID / NO COVID; total | Depuración y motivo |
|---|---|---|---|---|
| D1 | COVID + neumonía viral + opacidad pulmonar | Normales | 10972 / 10192; **21164** | No. Aumentar ejemplos disponibles; etiquetas amplias |
| D2 | COVID + neumonía viral | Normales | 4960 / 4960; **9920** | No. Excluir opacidad por recomendación profesional y balancear normales; agrupación contextual de pandemia |
| D3 | Solo COVID | Normales | 3615 / 3615; **7230** | No. Hacer más específica la clase positiva |
| D4 | Solo COVID | Normales | 2462 / 2462; **4924** | Sí, revisión manual sin profesional disponible; retirar borrosidad, movimiento, elementos metálicos y errores de colimación |

Fuente: pp. 34–36, tabla 2. D4 conserva el criterio binario de D3 y elimina imágenes de calidad considerada deficiente. El artículo no proporciona en el PDF una lista reproducible de IDs retenidos/excluidos ni reglas cuantitativas de calidad. No podemos reconstruir exactamente el subconjunto con solo estas cantidades.

**Interpretación propia [C]:** en D4, NO COVID significa **normal**, no cualquier radiografía negativa para SARS-CoV-2. El modelo no queda evaluado frente a neumonías no COVID ni al conjunto de enfermedades que aparecen en una población clínica. En D1/D2 la ampliación de etiquetas cambia el problema: sus métricas no comparan exactamente la misma tarea que D4. El balance artificial tampoco representa prevalencia real.

### Partición original: lo declarado y lo verificable [A, C]

P. 33 declara **80 % entrenamiento, 10 % validación, 10 % prueba**. La tabla 3 p. 43 informa:

| Dataset | Validation COVID / NO COVID declarados | Test COVID / NO COVID declarados | Train por resta de tablas 2–3, **inferencia no verificada** |
|---|---|---|---|
| D1 | 1018 / 1018 | 1018 / 1018 | 8936 / 8156 |
| D2 | 496 / 496 | 496 / 496 | 3968 / 3968 |
| D3 | 361 / 361 | 361 / 361 | 2893 / 2893 |
| D4 | 246 / 246 | 246 / 246 | 1970 / 1970 |

Esos train son **cálculos condicionales**, no inventarios confirmados. En D1, 1018 no es el 10 % de 10972: suponiendo las tablas, validation y test son aproximadamente 9,28 % de positivos y 9,99 % de negativos. Además, figura 32 p. 47 suma **495/496** en test D2, y figura 35 p. 50 suma **362/362** en D3; divergen de tabla 3. D4 sí muestra 246/246 en figura 38 p. 53. No existe evidencia para determinar exactamente todos los IDs y conteos efectivos de train/validation/test. La respuesta rigurosa al pedido de exactitud es preservar estas divergencias y solicitar manifiestos en 00–01.

## 4. CNN, entrenamiento y stack original [A]

La reconstrucción técnica prioriza anexos I–II, pp. 68–72, frente a simplificaciones de diagramas. La red tiene **tres convoluciones y dos MaxPooling**, no tres pooling.

| Etapa | Configuración | Salida / parámetros |
|---|---|---|
| Entrada | Grises, un canal | 299×299×1 |
| Conv1 | 32 filtros 3×3, `same`, ReLU | 299×299×32; 320 parámetros |
| MaxPooling1 | 2×2 | 149×149×32 |
| Conv2 | 64 filtros 2×2, `same`, ReLU | 149×149×64; 8256 |
| MaxPooling2 | 2×2 | 74×74×64 |
| Conv3 | 64 filtros 2×2, `same`, ReLU | 74×74×64; 16448 |
| Flatten | Aplanamiento sin aprendizaje | 350464 valores |
| Dense | 64 neuronas, ReLU | 22429760 |
| Dropout | Probabilidad 0,5 durante entrenamiento | 64 |
| Dense salida | 2 neuronas, Softmax | 130 |
| Total | Todos entrenables | **22454914 parámetros** |

Las convoluciones aprenden patrones locales; ReLU introduce no linealidad; pooling reduce resolución; Flatten conecta mapas con Dense; Dropout regulariza; Softmax produce dos puntuaciones normalizadas. Softmax **no garantiza probabilidades calibradas ni porcentajes de acierto individual**. La capa Dense concentra casi todo el volumen paramétrico; es una motivación concreta para explorar otra representación.

Entrenamiento: `categorical_crossentropy`, Adam, learning rate **0,0005**, batch **32**, **20 épocas**, `class_mode='categorical'`, `fit_generator`. Train y validation usan `/255`; solo train aplica `shear_range=0.3`, `zoom_range=0.3` y `horizontal_flip=True`. Los pasos se calculan por división entera del número de imágenes entre batch, con posible omisión de remanentes por época; no se detalla su efecto. Se guardan `modelo.h5` y `pesos.h5` (pp. 68–71).

| Herramienta original | Uso documentado |
|---|---|
| Python, Anaconda | Lenguaje y gestión de entorno |
| TensorFlow / Keras | Construcción, entrenamiento y carga CNN; mezcla de imports internos de TensorFlow y Keras |
| NumPy | Arreglos y `argmax` de predicciones |
| Matplotlib | Curvas y figuras |
| scikit-learn | Matriz y reporte de clasificación |
| mlxtend.plotting | Visualización de matriz |
| os | Directorios y almacenamiento |

No hay un archivo de entorno con versiones exactas en el PDF. El hardware declarado es notebook con **16 GB RAM, SSD, Intel Core i7-7700HQ 2,80 GHz**; no se identifica una GPU utilizada. El texto informa entrenamientos de **40 minutos a 6 horas**, según dataset (p. 36); no es una tabla de benchmarks normalizados por ensayo. El anexo V tiene tiempos por época variables; no usarlos como medición directa comparable con hardware nuevo.

## 5. CRISP-ML(Q) original [A] y adaptación [C]

El marco contiene entendimiento del negocio/datos, preparación, modelado, evaluación, despliegue y monitoreo/mantenimiento. El TFC excluye las dos últimas fases por tratarse de prototipo y describe iteración entre datos y modelos (pp. 29–32). Su fortaleza es organizar decisiones y evaluación. La metodología por sí sola no garantiza calidad: necesita controles verificables.

Reutilizaremos las cuatro primeras fases con manifiestos, controles contra leakage y evidencias. Cubriremos despliegue, monitoreo y mantenimiento **conceptualmente** porque lo exige TFI §5.7, sin desarrollar infraestructura. Véase [E15](FUENTES_Y_TRAZABILIDAD.md).

## 6. Las doce pruebas originales [A]

Tres entrenamientos por configuración, doce en total (p. 43). **No son 12 folds de validación cruzada.** Los pares de cada columna son **COVID / NO COVID**, métricas entre 0 y 1; accuracy es global en test. Transcripción de tabla 17 p. 57, contrastada con tablas 4–15 pp. 44–55.

| Dataset | Prueba | Precision C / N | Recall C / N | F1 C / N | Accuracy | Observación propia [C] |
|---|---:|---|---|---|---|---|
| D1 | 1 | 0,6667 / 0,7757 | 0,8310 / 0,5845 | 0,7398 / 0,6667 | 70,78 % | FP relevantes |
| D1 | 2 | 0,5804 / 0,8560 | 0,9470 / 0,3153 | 0,7197 / 0,4609 | 63,11 % | Mayor inclinación hacia positivo |
| D1 | 3 | 0,5142 / 0,9118 | 0,9941 / 0,0609 | 0,6778 / 0,1142 | 52,75 % | Casi no reconoce normales |
| D2 | 4 | 0,4995 / 0,5000 | 0,9455 / 0,0544 | 0,6536 / 0,0982 | 49,95 % | Desempeño cercano a clase constante |
| D2 | 5 | 0,4945 / 0,4400 | 0,9152 / 0,0665 | 0,6421 / 0,1156 | 49,04 % | Ambas clases mal separadas |
| D2 | 6 | 0,4995 / 0,0000 | 1,0000 / 0,0000 | 0,6662 / 0,0000 | 49,95 % | Predice todos positivos |
| D3 | 7 | 0,5142 / 0,9545 | 0,9972 / 0,0580 | 0,6786 / 0,1094 | 52,76 % | Recall alto no implica utilidad global |
| D3 | 8 | 0,5385 / 0,8378 | 0,9669 / 0,1713 | 0,6917 / 0,2844 | 56,91 % | Persisten muchos FP |
| D3 | 9 | 0,4794 / 0,4727 | 0,5470 / 0,4061 | 0,5110 / 0,4368 | 47,65 % | Gran brecha validation/test |
| D4 | 10 | 0,7912 / 0,7984 | 0,8008 / 0,7886 | 0,7960 / 0,7935 | **79,47 %** | Mejor test reportado |
| D4 | 11 | 0,6579 / 0,6858 | 0,7114 / 0,6301 | 0,6836 / 0,6568 | 67,07 % | Inferior a prueba 10 |
| D4 | 12 | 0,6667 / 0,6549 | 0,6423 / 0,6789 | 0,6542 / 0,6667 | 66,06 % | Variación entre entrenamientos |

### Validation no es test

| Prueba | Accuracy train | Accuracy validation | Accuracy test |
|---|---:|---:|---:|
| 1 | 0,8292 | 0,8552 | 0,7078 |
| 2 | 0,8478 | 0,8725 | 0,6311 |
| 3 | 0,8511 | 0,8730 | 0,5275 |
| 4 | 0,8715 | 0,6099 | 0,4995 |
| 5 | 0,8806 | 0,6069 | 0,4904 |
| 6 | 0,8752 | 0,6633 | 0,4995 |
| 7 | 0,8009 | 0,8920 | 0,5276 |
| 8 | 0,8009* | 0,8920* | 0,5691 |
| 9 | 0,8387 | 0,9034 | 0,4765 |
| 10 | 0,8410 | 0,8208 | 0,7947 |
| 11 | 0,8122 | 0,8562 | 0,6707 |
| 12 | 0,7909 | 0,8375 | 0,6606 |

Fuente: tablas 16–17 pp. 56–57. *En prueba 8, tabla 16 y tabla 25 repiten la prueba 7; el log de época 20 p. 91 informa train=0,8581, validation=0,8906, train loss=0,3219 y validation loss=0,2650. Se conserva la discrepancia. No se debe llamar “90 % de rendimiento final” al 90,34 % de validation de prueba 9: su test fue 47,65 %.

### Resultado principal: prueba 10 de D4

La figura 38 p. 53 contiene, con COVID como positivo, **VP=197, FN=49, FP=52, VN=194**, total 492. Es coherente con 391/492≈79,47 %. Sensibilidad 80,08 %, especificidad 78,86 %, precision positiva 79,12 % y F1 positivo 79,60 %. La especificidad es el recall de la clase NO COVID. Estas son cifras del TFC o cálculos directos de su tabla; no resultados nuestros.

El TFC atribuye la mejora a depuración (p. 61), pero **[C] esa atribución causal no queda aislada**: cambiaron imágenes, tamaño y posiblemente particiones, con variabilidad aleatoria. Tres ensayos no separan esos efectos. El 75 % considerado viable surge de la entrevista p. 102; es un criterio contextual del profesional, no una certificación clínica ni nuestro umbral de aprobación.

## 7. Validación profesional [A] y alcance [C]

Se seleccionaron **52 radiografías del test**, no una cohorte externa, y participó un solo médico, Dr. Osvaldo Luqui, R4 en diagnóstico por imágenes (pp. 43, 58–59; anexo VI pp. 100–101).

| Comparación | Evidencia original | Lectura correcta |
|---|---|---|
| Médico frente a red | 37 coincidencias, 12 discrepancias, 3 indefinidas | 37/49≈75,51 % entre casos clasificables; el texto redondea a 75 %. No dividir por 52 para obtener esa concordancia |
| Red frente a etiquetas | VP19, VN22, FP6, FN5 | 41/52≈78,85 % de aciertos; 24 positivos y 28 negativos |
| Médico frente a etiquetas | VP16, VN21, FP4, FN8 | 37/49≈75,51 % entre definidos; abstención 3/52 |

Los casos indefinidos son 10, 35 y 39 y tienen etiqueta NO COVID; la red acierta dos de ellos. En los **mismos 49 casos**, la red acierta 39 (reconstrucción documental del anexo). No comparar 41/52 y 37/49 como prueba de superioridad. La coincidencia médico/red tampoco es exactitud frente a etiquetas: ambos pueden equivocarse de la misma manera.

El análisis de fallos p. 60 identifica, según el profesional, signos de enfermedad crónica/complicaciones en algunos FN; para FP no halló patrón común y sugirió errores aleatorios o mala técnica. No son demostraciones etiológicas. El estudio es pequeño, con selección no descrita como aleatoria y sin varios lectores: aporta revisión cualitativa, no validación clínica generalizable. La “validación cruzada” mencionada para múltiples médicos p. 59 alude a acuerdo entre lectores y no equivale a K-fold de ML.

## 8. Fortalezas, límites y análisis crítico [A, C]

Fortalezas: problema explícito, dataset público identificado, arquitectura y código anexados, métricas por clase, doce entrenamientos, reconocimiento de errores y consulta profesional. Permiten una crítica verificable y una alternativa concreta.

**Limitaciones explícitas de autores** (pp. 60–62): calidad/técnica radiográfica; afecciones crónicas que dificultan clasificación; alto costo computacional y tiempos; compatibilidad/portabilidad entre bibliotecas; restricciones de contacto profesional durante emergencia sanitaria. Trabajos futuros: multiclase, transferencia ResNet/VGG, mejorar dataset con profesional y evaluación real con interfaz. Esas extensiones no pasan automáticamente a nuestro alcance.

| Evidencia | Implicancia metodológica propia | Clasificación |
|---|---|---|
| D1/D2 reúnen patologías bajo COVID, pp. 34–36 | La etiqueta operativa no es infección confirmada; restringe comparación entre datasets | Decisión metodológica |
| Fuentes heterogéneas, p. 33 | Textos, equipos o procedencia podrían correlacionarse con clase; verificar por fuente | Posible limitación |
| Sin fecha/estadio preciso por imagen, p. 33 | Infección y signos visibles pueden diferir; etiqueta ruidosa para tarea visual | Limitación confirmada de metadatos |
| D4 limpiado sin experto, p. 35 | Puede excluir casos difíciles y cambiar población; “menos sesgo” no está demostrado | Decisión metodológica y posible limitación |
| Normales como única clase negativa de D4 | No evalúa diagnóstico diferencial ante otras patologías | Limitación confirmada del alcance |
| Balance artificial y D1 no exactamente balanceado | Accuracy y precision dependen de composición; no trasladar prevalencia | Decisión metodológica |
| No hay IDs/pacientes/semillas del split en PDF | No puede auditarse independencia; duplicados/pacientes repetidos son riesgos, no hechos probados | Posible limitación |
| Conteos divergentes de tablas/matrices | Replicación exacta no garantizada solo con PDF | Limitación confirmada de documentación |
| Se elige prueba 10 por mejor clasificación en test, pp. 43,58 | Test participa en selección; el mejor valor tiene sesgo de selección potencial | Decisión metodológica; limitación para estimación final independiente |
| 3 entrenamientos por dataset; no CV experimental documentada | No se estima robustez a distintas particiones ni se aísla azar | Oportunidad de mejora |
| `/255` en entrenamiento pero no anexo IV, pp. 68,75 | Diferencia de distribución entre entrenamiento e inferencia; no se sabe si ejecución real fue igual | Inconsistencia confirmada en código publicado |
| Predicción individual sin grayscale explícito, p. 73 | Posible incompatibilidad de canales con entrada de un canal | Posible limitación de reproducibilidad |
| Prueba 9: 90,34 % validation vs 47,65 % test | Auditar preprocesamiento, mapeo, selección y particiones antes de atribuir solo sobreajuste | Oportunidad de mejora |
| No búsqueda sistemática de hiperparámetros ni semillas documentadas | No se conoce sensibilidad del modelo a configuración/azar | Oportunidad de mejora |
| Sin prueba estadística de comparación reportada | No afirmar mejora estadísticamente significativa de D4 | Limitación confirmada de evaluación reportada |
| Sin explicaciones del modelo por imagen/feature | Opinión sobre fallos no revela mecanismo aprendido | Oportunidad de mejora |
| Un profesional, 52 imágenes del mismo test | Acuerdo limitado; ausencia de validación externa/multilector | Limitación confirmada |
| Dense de 22,43 millones de pesos y notebook, pp. 36,72 | Motiva medir alternativas; no prueba que todo ML clásico sea barato | Oportunidad de mejora |
| Imports mixtos sin lock de entorno, pp. 68–75; portabilidad p. 61 | Reconstrucción puede fallar con versiones actuales | Limitación confirmada de documentación |

La crítica más útil es convertir cada incertidumbre en un control futuro: manifiestos, pipeline único y evaluación separada. No atribuir data leakage entre pacientes ni aprender “marcas de hospital” como un hecho del TFC sin datos que lo prueben. El estudio de DeGrave et al. [E16] motiva investigar atajos, no demuestra que ocurrieran aquí.

## 9. Pregunta, hipótesis y objetivos propios [C, D]

¿Puede un enfoque clásico basado en HOG distinguir COVID de normal con desempeño comparable al de la CNN del TFC y menor complejidad computacional? Se estudiará mediante dos clasificadores sobre una representación común, respetando los límites de comparabilidad de los datos. Menor costo y explicación técnica más accesible son hipótesis: no se promete superar 79,47 % ni obtener validación clínica.

El objetivo es formalizar entradas y etiquetas, implementar una baseline y dos candidatos, compararlos reproduciblemente y discutir errores, límites y relación con la CNN. **COVID=1, normal=0**. El objetivo de selección es F1 macro medio de CV, acompañado de recall y especificidad. En empate exacto entre candidatos se prefiere SVM lineal por simplicidad; dentro de una grilla se conserva el orden documentado. Las consecuencias de FP/FN se discuten sin inventar costos clínicos numéricos.

## 10. Pipeline mínimo y configuración [C]

`Radiografía → grises y resize 128×128 → HOG fijo → clasificador → COVID / normal`.

| Ruta | Configuración inicial | Función |
|---|---|---|
| B0 | DummyClassifier(strategy="most_frequent") | Control trivial; aprende la clase mayoritaria del train e ignora las features |
| C1 | HOG → StandardScaler → LinearSVC(C=1) | Frontera lineal regularizada sobre el vector HOG |
| C2 | HOG → RandomForestClassifier(n_estimators=100, max_depth=None, min_samples_leaf=1) | Reglas no lineales sobre el mismo vector; sin escalado necesario |

HOG: **128×128**, `orientations=9`, `pixels_per_cell=(8,8)`, `cells_per_block=(2,2)`, `block_norm="L2-Hys"`, `transform_sqrt=False`. Produce `15×15×2×2×9=8100` atributos. Es cálculo de diseño, no extracción ejecutada. Se fijarán rango, tipo, interpolación y tratamiento de aspecto en 01; se implementarán una sola vez en 02. No hay búsqueda de configuraciones HOG.

LinearSVC usará regularización L2, pérdida squared_hinge y `class_weight=None`; registrar solver/tolerancia/max_iter y atender convergencia sin ocultar avisos. RF mantiene `max_features="sqrt"`, bootstrap y `class_weight=None`; seed 42 en operaciones aleatorias. C1 y C2 reciben la misma información HOG: el scaler de C1 es parte de su pipeline.

**Fuera del experimento inicial:** LBP, PCA, KNN, regresión logística, SVM RBF y SHAP. Se conservan brevemente como teoría complementaria; no son tareas opcionales programadas. PCA solo podrá reconsiderarse ante un problema **medido** de memoria, tiempo, dimensionalidad o convergencia, con decisión explícita que revise el alcance antes de implementarla. Tener 8100 atributos por sí solo no demuestra tal problema.

## 11. Datos, EDA y particiones [C]

Se prioriza la base del TFC y una definición comparable a D4. Versión, licencia, disponibilidad, metadatos e IDs de D4 siguen pendientes. No inventar el subconjunto depurado ni repetir limpieza subjetiva para alcanzar una cifra. Si no se recupera el original y se sustituye por un dataset público equivalente, justificar y obtener autorización de cátedra según consigna §4.

Crear un manifiesto sencillo con ID, ruta relativa, hash, etiqueta, fuente y paciente/grupo cuando exista; agregar partición y fold. La auditoría estructural identifica archivos ilegibles y duplicados exactos por hash antes del split; resolver duplicados/etiquetas contradictorias con una regla documentada. La búsqueda perceptual de casi duplicados queda fuera inicialmente: solo se reconsidera si EDA aporta evidencia concreta.

Reservar aproximadamente **80 % desarrollo y 20 % test**, seed **42**. Priorizar pacientes/grupos separados si hay identificadores viables. Dentro de desarrollo usar **StratifiedKFold(n_splits=5, shuffle=True, random_state=42)** cuando sea razonable asumir independencia; si hay grupos, usar una partición agrupada viable, por ejemplo StratifiedGroupKFold. Comprobar clases y grupos suficientes; si no los hay, documentar y revisar el protocolo antes de entrenar. No fabricar IDs de paciente a partir del nombre de archivo.

La EDA visual y decisiones sobre distribución, calidad, ejemplos y posibles atajos se hacen en desarrollo. El inventario mínimo necesario para particionar no habilita explorar errores o métricas del test. Guardar el split como tabla basta: **no se implementan mecanismos programáticos de bloqueo o sellado**. Si faltan pacientes queda riesgo residual explícito. No imponer balance artificial ni aumentar datos como tarea inicial.

## 12. Validación y tuning acotado [C]

Los tres modelos se comparan sobre los mismos cinco folds de desarrollo. HOG es determinista por imagen; StandardScaler aprende media/escala exclusivamente en el train de cada fold mediante Pipeline. No calcular estadísticas globales antes de CV. Registrar métricas por fold y **media ± desvío estándar muestral**; los folds comparten entrenamiento y no son cinco datasets independientes.

03 compara configuraciones iniciales; 04 realiza **GridSearchCV** sobre ambos candidatos con los mismos folds y F1 macro. Única grilla:

| Candidato | Hiperparámetros buscados | Configuraciones |
|---|---|---:|
| C1 | C: 0.1, 1, 10 | 3 |
| C2 | n_estimators: 100, 200; max_depth: None, 20; min_samples_leaf: 1, 3 | 8 |

La grilla suma 11 configuraciones × 5 folds = **55 ajustes de CV**, sin contar la comparación inicial ni reajustes finales. Es una cuenta de costo prevista, no un objetivo de cantidad ni permiso para ampliar búsqueda. No usar RandomizedSearchCV ni ensayos de otros descriptores. Registrar tiempos aproximados y fallos técnicos. La mejor media de búsqueda es una estimación de selección potencialmente optimista; el test final cubre la evaluación retenida.

## 13. Orden de evaluación y estadística [C]

Todo ocurre en 04, en este orden:

1. Tuning exclusivamente en desarrollo.
2. Comparar CV de B0/C1/C2, incluida dispersión y límites.
3. Seleccionar candidato por la regla de 09, aunque el resultado no supere B0.
4. Congelar por escrito configuración, parámetros, split, commit de código y decisión. Un registro breve basta; el commit final vincula los artefactos. Predefinir comparadores y, si procede, un solo contraste C1 frente a C2.
5. Reajustar los modelos fijados con todo desarrollo y evaluar **test una única vez**, en un lote de B0/C1/C2 predefinido. La selección ya no cambia por resultados de test.
6. Guardar predicciones por ID, matriz de confusión, accuracy, precision, recall, especificidad, F1 por clase y F1 macro. ROC-AUC solo con scores continuos válidos y ambas clases; curva PR/AP solo si el desbalance observado en desarrollo justifica su aporte.
7. Analizar FP/FN, aciertos y limitaciones de calidad/procedencia. Interpretar el modelo elegido sin modificarlo.
8. Aplicar McNemar **solo si corresponde**: mismas imágenes, predicciones individuales pareadas, comparadores fijos y unidades razonablemente independientes. Documentar discordancias b/c, n, diferencia de accuracy y p bilateral; α=0.05 fijado antes de test. Puede usarse la variante exacta binomial. Si no se cumplen supuestos, explicar la omisión.

La estadística principal es descriptiva: media/desvío CV y test reservado. No se agregan Wilcoxon, 5×2cv, bootstrap inferencial ni múltiples contrastes. El bootstrap interno de RF es parte del algoritmo y no constituye un plan estadístico adicional. McNemar compara tasas de error, no F1 ni superioridad clínica. Con cifras agregadas del PDF no puede hacerse contraste pareado contra CNN.

La referencia histórica es accuracy **79,47 %**, precision COVID **0,7912**, recall **0,8008**, F1 **0,7960**. Se comparan métricas equivalentes y se declaran diferencias de población, split, preprocesamiento y hardware. Si no hay test idéntico, la comparación es contextual; superar esa cifra no prueba superioridad controlada.

## 14. Interpretación, costo y figuras [C]

Si gana SVM, examinar coeficientes asociados a bloques/orientaciones HOG con cuidado por escala y correlación. Si gana RF, mostrar importancia de features por impureza y sus sesgos; permutation importance solo si aporta una explicación comprensible sobre datos de desarrollo y se identifica su condición de evaluación. No exigir guardar todos los modelos de folds ni crear conjuntos adicionales para explicaciones. Los coeficientes/importancias no son mapas clínicos ni prueba causal.

Medir aproximadamente tiempo de extracción, búsqueda/entrenamiento e inferencia, tamaño del modelo y complejidad general con hardware y alcance de medición declarados. Inferencia debe aclarar si incluye lectura y HOG. RAM es opcional si se obtiene fácilmente. No crear profiling permanente, telemetría ni infraestructura de control de hilos.

Figuras mínimas futuras: EDA de desarrollo, comparación CV, matrices y ejemplos de errores, explicación del elegido. ROC y PR solo bajo las condiciones de 13; curvas de aprendizaje cuando respondan una duda concreta en desarrollo, antes de congelar. Todas deberán tener número, título, ejes/unidades y referencia interpretativa en el texto (TFI §5.6). No generar curvas por cumplir una lista sin utilidad.

## 15. Reproducibilidad y estructura prevista [C]

Python, NumPy, pandas, Matplotlib, scikit-image, scikit-learn, venv y Git/GitHub bastan para el núcleo. Jupyter es opcional para EDA; comandos reproducibles sostienen la ejecución. Fijar versiones probadas en 01 y seed 42. SciPy solo si se importa para McNemar exacto; no sumar frameworks de experimentación.

Estructura **futura, todavía no creada**: `src/data.py`, `src/features.py`, `src/models.py`, `src/evaluation.py`; `configs/experimento.json`; `data/manifiesto.csv`; `results/` para CV, predicciones y métricas; `reports/` para figuras/informe; `tests/` para contratos relevantes; `requirements.txt`; `docs/REGISTRO_EJECUCION.md` y `docs/REGISTRO_IA.md`. Mantener scripts y funciones pequeños; pruebas de separación, transformaciones, métricas y carga del modelo. No crear capas vacías.

El registro breve por sprint contendrá fecha, entradas, decisión, evidencia, limitaciones, comandos y cierre. Versionar manifiestos publicables, configuración y resultados pequeños; excluir datos pesados, identificadores sensibles y credenciales. Declarar IA con herramienta, versión conocida o no informada, propósito y verificación. Reproducibilidad se comprobará con comandos y entorno, no por cantidad de infraestructura.

## 16. Ética, entrega y criterios de éxito [B, C]

Discutir privacidad, licencia, sesgo de fuente/población, FP/FN y uso indebido como diagnóstico. Las cuatro primeras fases CRISP-ML(Q) organizan el trabajo activo. Despliegue, integración, monitoreo, drift y reentrenamiento se describen **solo conceptualmente**, incluyendo costos, latencia, límites y requisitos de una hipotética validación posterior; no se construyen servicios.

Éxito: reconstrucción fiel, baseline y dos candidatos evaluados sin fuga conocida, selección justificada, evidencia reproducible y defensa honesta aunque ningún candidato supere al original. No usar 79,47 % como umbral académico. Informe y defensa deben cubrir formato, resumen bilingüe, bibliografía uniforme, anexo IA y rúbrica de la [matriz de requisitos](FUENTES_Y_TRAZABILIDAD.md). Los pendientes administrativos y de acceso a datos se mantienen explícitos.

## 17. Secuencia de seis sprints [C]

| Sprint | Resultado esperado | Estado |
|---|---|---|
| 00 Análisis TFC | Revisión por integrantes, alcance y trazabilidad aceptados | No iniciado |
| 01 Datos y EDA | Datos autorizados, auditoría, manifiesto/split, EDA y entorno | No iniciado |
| 02 HOG y baseline | HOG fijo probado y B0 evaluada en desarrollo | No iniciado |
| 03 Modelos y CV | C1/C2 iniciales comparados con B0 en folds comunes | No iniciado |
| 04 Tuning y evaluación | Selección, registro previo, test único, errores e interpretación | No iniciado |
| 05 Informe y defensa | Informe, comparación, ética, despliegue conceptual y ensayo | No iniciado |

Planes y prompts en [Ejecución](ejecucion/README.md). Los nueve planes anteriores son [historial archivado](archivo/planificacion_inicial/README.md). Este sprint correctivo solo revisa documentación; **no inicia 00**. Cada sprint futuro exige su solicitud y el cierre verificable del anterior; no encadenarlos automáticamente.
