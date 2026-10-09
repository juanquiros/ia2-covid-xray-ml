# Teoría y stack para estudiar y defender el TFI

**Equipo:** Juan Quirós y Andruszyszyn. **Estado:** material de estudio y diseño, 09/10/2026; no hay experimentos propios. Las decisiones operativas se mantienen en [Roadmap](ROADMAP_TFI.md). La evidencia del TFC, la consigna y las referencias E01–E20 se identifican en [Fuentes](FUENTES_Y_TRAZABILIDAD.md).

Este material explica cómo una radiografía se convierte en un vector, cómo se aprende una regla de clasificación y cómo comprobar si funciona sobre datos que no participaron en su construcción. Los ejemplos numéricos son **didácticos**, salvo cuando se indica explícitamente que proceden del TFC. No anticipan resultados del equipo.

## 1. De inteligencia artificial a nuestro problema

### Qué son IA, ML y Deep Learning

La inteligencia artificial estudia sistemas capaces de realizar tareas como razonar, planificar, percibir o aprender. Machine Learning (ML) es el conjunto de métodos que ajustan un comportamiento a partir de datos. Deep Learning (DL) es una familia de ML basada en redes con múltiples capas que aprenden representaciones. Una CNN pertenece a DL; SVM y Random Forest pertenecen a ML. El enfoque clásico también aprende: lo que elegimos explícitamente es cómo representar la imagen.

**Para qué sirve esta distinción:** nuestra alternativa cambia el mecanismo de representación y clasificación de la CNN original. No basta cambiar TensorFlow por otra biblioteca para obtener una solución metodológicamente diferente.

### Supervisado, no supervisado, clasificación y regresión

En aprendizaje **supervisado** disponemos de ejemplos `(x,y)`: radiografía y etiqueta. El algoritmo aprende una función para predecir y en nuevas x. Clasificación predice una categoría; regresión predice una magnitud continua, por ejemplo un tiempo. Nuestro y es binario, no un grado de enfermedad ni una probabilidad clínica certificada.

En aprendizaje **no supervisado**, el algoritmo busca estructura sin usar etiquetas objetivo: grupos, componentes o anomalías. PCA es no supervisado y puede estar dentro de un pipeline supervisado. Que no use y no lo exime de ajustarse solo con train: también aprende de la distribución de x.

**Ventaja del supervisado aquí:** coincide con las etiquetas y permite evaluar aciertos/errores. **Limitación:** aprender etiquetas defectuosas puede producir un clasificador fiel al dataset pero poco útil fuera de él.

**Defensa:** explicar por qué clasificación binaria es apropiada para reproducir la tarea de D4 y por qué no equivale a diagnóstico. La CNN original reconoce etiquetas de imágenes; la práctica clínica requiere otros elementos.

## 2. Dataset, features, target y balanceo

Un **dataset** es una colección de observaciones y su información asociada. Aquí cada fila futura del manifiesto representará una imagen, con ID, hash, fuente, clase, grupo/paciente si está disponible y partición. La unidad almacenada puede ser imagen, pero la unidad independiente puede ser paciente: varias radiografías de una persona no son observaciones intercambiables con personas nuevas.

Las **features** son las variables de entrada del clasificador; el **target** es la salida que queremos aprender. Los píxeles son una representación; un histograma HOG/LBP es otra. Las clases son valores del target. Nuestra convención propuesta es `1=COVID`, `0=normal`; el anexo original usa índices `covid=0`, `no covid=1`. No copiar ese índice y luego calcular recall con positivo=1 sin verificar su significado.

**Cómo funciona el balanceo:** modifica el peso relativo de clases en entrenamiento, mediante pesos, submuestreo o sobremuestreo. No crea información nueva. `class_weight='balanced'` calcula pesos a partir de las frecuencias del train de cada fold. Sobremuestrear antes de particionar puede duplicar ejemplos a ambos lados. No balancear test artificialmente después de ver resultados.

**Ejemplo didáctico:** con 90 normales y 10 positivos, predecir siempre normal logra 90 % de accuracy y recall COVID=0. Un dataset balanceado facilita ver ese fracaso, pero su precision no se traslada automáticamente a una población con otra prevalencia.

**Uso en el TFI:** investigar frecuencias y origen, no suponer que todos los datasets originales están balanceados. D1 tiene 10972/10192; D4 2462/2462 según TFC tabla 2. Solo se usarán las etiquetas originales COVID y normales para nuestra tarea propuesta. No reetiquetar neumonía viral como infección COVID por intuición.

**Defensa:** distinguir balance, representatividad y calidad. Dos clases con igual tamaño pueden estar sesgadas por edad, centro, equipo o severidad.

## 3. Píxeles, imágenes y preprocesamiento

### Qué es una imagen para el algoritmo

Un **píxel** es una muestra espacial de intensidad. La **resolución** es la cantidad de filas y columnas; 299×299 no indica por sí sola calidad diagnóstica. Una imagen en **grises** tiene un canal; RGB tiene tres. Convertir a grises no borra marcas, texto ni sesgo de procedencia. La misma intensidad almacenada puede depender del equipo, exposición y procesamiento.

**Textura** describe variaciones locales repetidas de intensidad. **Borde** es una transición relativamente fuerte entre intensidades. **Contraste** expresa diferencias de intensidad entre regiones. HOG enfatiza estructura de gradientes; LBP compara vecindarios. Ninguno sabe, por definición, qué es pulmón o patología.

### Cómo se preprocesa y por qué

Resize interpola una imagen para obtener tamaño fijo. Al reducir puede perderse detalle; al ampliar no aparece nueva información. Un recorte puede quitar anatomía; deformar la proporción puede cambiar estructuras. Por eso se registran resolución, interpolación, tratamiento de aspecto y rango.

Normalización puede significar operaciones diferentes: dividir intensidades de 8 bits por 255, normalizar un histograma para que sume uno o estandarizar features con media y desvío. **No son equivalentes.** Dividir por 255 es válido si la entrada efectivamente tiene ese rango; aplicarlo dos veces o sobre una imagen ya en [0,1] cambia la escala incorrectamente. Si se aprende una media del conjunto, se aprende únicamente en train.

**Uso propuesto:** grises, tamaño inicial 128×128 y contrato de rango/tipo. Para LBP se considerará entrada entera consistente con su comparación local; pequeñas diferencias de punto flotante pueden cambiar patrones. No agregar ecualización, segmentación o filtros sin pregunta experimental y revisión en desarrollo.

**Ventajas:** comparabilidad de dimensiones y costo controlado. **Limitaciones:** alteración de texturas, pérdida de detalles y persistencia de atajos. Una imagen nítida no implica una etiqueta correcta.

**Defensa:** demostrar qué entra y sale de cada transformación, y explicar por qué una fotografía de prueba no puede tener un preprocesamiento distinto al del entrenamiento. La inconsistencia `/255` entre anexos del TFC es un motivo concreto para centralizar la función, no una demostración del origen de todos sus errores.

## 4. Train, validation, test y generalización

### Qué es cada partición

**Train** ajusta parámetros: coeficientes, umbrales de árboles, vectores soporte, medias y componentes. **Validation** compara decisiones que rodean ese ajuste: C, profundidad, descriptor o uso de PCA. **Test** estima el comportamiento final después de tomar las decisiones. No es un recurso para mejorar la configuración.

**Generalización** es capacidad de predecir adecuadamente en nuevos datos del dominio objetivo. No significa rendir bien ante cualquier hospital, equipo o época. Una partición aleatoria del mismo repositorio estima generalización interna, con sus límites.

**Overfitting:** un modelo aprovecha peculiaridades del train que no se sostienen en datos nuevos. **Underfitting:** la representación/capacidad o el ajuste son insuficientes y el desempeño es bajo incluso en train. Comparar train/validation y curvas de aprendizaje ayuda, pero una brecha no identifica por sí sola su causa: también pueden existir cambios de distribución, etiquetas o preprocesamiento.

### Uso en el TFI

Propuesta común: 80 % desarrollo, 20 % test; dentro del 80 %, cinco folds. En cada ajuste se usa aproximadamente 64 % total como train y 16 % como validation. No existe un tercer holdout fijo adicional. Al elegir el modelo, se reajusta en todo desarrollo antes del test. Si hay grupos, los porcentajes son aproximados y se prioriza independencia. La política está en el roadmap y no se reemplaza con el 80/10/10 histórico.

**Ejemplo didáctico:** si elegimos entre dos resoluciones mirando el test y luego informamos la mejor accuracy, el test ya influyó aunque nunca se haya llamado `fit` sobre él. Sus resultados dejan de ser una evaluación final independiente de esa decisión.

**Defensa:** explicar qué decisiones se congelan y cuándo. La mejor cifra de validation entre muchos ensayos tiene sesgo de selección; no es una estimación final imparcial.

## 5. Data leakage y Pipeline

### Qué es y cómo aparece

Data leakage o fuga de información ocurre cuando la construcción del sistema utiliza información que no debería estar disponible para ese ajuste o evaluación. Puede ocurrir entre train/test, entre train/validation, por duplicados, por pacientes repetidos, por variables que codifican la respuesta o por decisiones humanas guiadas por el test.

**Ejemplo didáctico de escala:** un fold train contiene intensidades medias 10 y 20; validation contiene 100. Si la media se calcula sobre los tres casos, el centro ya incorpora validation. Que no se miren etiquetas no evita la fuga. PCA, imputación y selección de variables presentan el mismo problema si se ajustan globalmente.

**Ejemplo de paciente:** una radiografía en train y otra del mismo paciente en test pueden compartir anatomía, dispositivo y marcas. El algoritmo podría reconocer identidad en lugar de generalizar a pacientes nuevos. Un split estratificado por clase no resuelve esa dependencia.

### Cómo funciona sklearn Pipeline

`Pipeline` encadena transformadores y estimador. Al hacer `fit`, cada transformador aprende y transforma el train antes del siguiente paso; al predecir, aplica las transformaciones aprendidas sin reajustar. En CV, cada pipeline se clona y ajusta exclusivamente dentro del fold. No se debe escalar por fuera y pasar a la búsqueda una matriz ya ajustada globalmente. La documentación oficial [E01](https://scikit-learn.org/stable/common_pitfalls.html) sustenta esta separación.

Contrato conceptual, **no implementación**:

```text
fold train -> descriptor fijo -> fit scaler -> fit PCA opcional -> fit clasificador
fold val   -> mismo descriptor -> transform scaler -> transform PCA -> predict
```

HOG/LBP fijos por imagen no aprenden estadísticas del conjunto y pueden cachearse de manera segura si los IDs y configuración se controlan. El cache no autoriza elegir parámetros mirando test ni reutilizar un scaler/PCA de otro fold.

**Ventajas:** consistencia entre ajuste e inferencia, menor riesgo de errores, serialización de una unidad. **Limitaciones:** no protege contra un manifiesto incorrecto, duplicados cruzados, etiquetas mal mapeadas o selección humana tras test. La prueba futura debe verificar qué IDs recibió cada `fit`, no solo que exista un objeto llamado Pipeline.

**Defensa:** describir un caso de fuga sin etiquetas, uno por paciente y uno por selección de modelo. Distinguir fuga de información de inconsistencia de escala: la omisión de `/255` del TFC es lo segundo, no necesariamente lo primero.

## 6. Cross-validation y Stratified K-Fold

K-fold divide desarrollo en k partes y repite k ajustes: cada parte valida una vez y las otras entrenan. Permite observar variabilidad por partición y comparar métodos con los mismos folds. **StratifiedKFold** intenta conservar proporciones de clase; ayuda a evitar folds sin positivos, pero no corrige sesgo de origen. Con grupos se necesita una estrategia que mantenga paciente/duplicados juntos, como StratifiedGroupKFold cuando es viable. Véase [E02](https://scikit-learn.org/stable/modules/cross_validation.html).

**Parámetros:** k, shuffle, random_state y, cuando corresponda, groups. No improvisar más folds que grupos independientes por clase. La semilla define una partición, no una garantía científica.

**Uso:** cinco folds comunes para B0, B1, C1 y C2; guardar valor por fold, media y desvío estándar muestral. Si un fold no permite calcular AUC por falta de clase, registrarlo y corregir el diseño en desarrollo; no reemplazar por cero.

**Ventajas:** usa eficientemente datos de desarrollo y muestra inestabilidad. **Limitaciones:** más costo y dependencias porque se solapan conjuntos de entrenamiento. Cinco valores no equivalen a cinco datasets independientes. CV anidada agrega una capa interna para tuning y otra externa para estimar ese proceso, con mayor costo; nuestro mínimo usa CV de selección más test reservado.

**Defensa:** explicar por qué comparar dos modelos con folds distintos mezcla el efecto del algoritmo con el de la partición, y por qué una media CV de búsqueda puede ser optimista.

## 7. CNN original y sus componentes

Esta sección es explicación pedagógica [C]. La arquitectura exacta y resultados [A] se encuentran en roadmap y TFC pp. 68–72. Las piezas no implican que debamos implementar otra CNN.

| Componente | Qué hace y cómo funciona | Uso original / límite que debemos explicar |
|---|---|---|
| Convolución | Aplica pesos compartidos sobre vecindarios; suma productos y sesgo | Aprende patrones locales; no trae conocimiento clínico incorporado |
| Kernel | Matriz pequeña de pesos, como 3×3 | Su tamaño es hiperparámetro; sus valores se aprenden |
| Filtro | Kernel con todos los canales de entrada que genera un canal de salida | 32, 64 y 64 filtros en tres capas originales |
| Feature map | Mapa de activaciones de un filtro | Conserva organización espacial antes de Flatten |
| Padding `same` | Trata bordes para conservar tamaño espacial con stride uno | No elimina efectos artificiales de los bordes |
| ReLU | `max(0,z)` | No linealidad; un valor negativo no significa necesariamente “información irrelevante” |
| MaxPooling | Toma el máximo en regiones, aquí 2×2 | Reduce resolución; también pierde ubicación fina; hay dos pooling en anexo II |
| Flatten | Reordena el tensor como vector | No aprende pesos; produce 350464 valores en el original |
| Dense | Combina todas las entradas con pesos y sesgos | Dense(64) tiene 22429760 parámetros por `(350464+1)×64` |
| Dropout | Durante train anula aleatoriamente activaciones con probabilidad p y reescala según implementación | p=0,5; no borra permanentemente neuronas ni se usa igual en inferencia |
| Softmax | Convierte logits en valores positivos cuya suma es uno mediante exponenciales normalizadas | Dos clases; no garantiza calibración |
| Cross entropy | Penaliza asignar poca probabilidad a la etiqueta correcta: `-Σ y_k log p_k` | Categórica con dos salidas; no es accuracy |
| Adam | Actualiza pesos con promedios móviles del gradiente y su cuadrado | Optimizador del original; no modelo de clasificación separado |
| Learning rate | Controla tamaño de actualización de pesos | 0,0005; muy grande puede desestabilizar, muy pequeño ralentizar |
| Batch | Grupo de ejemplos usado por actualización | 32 imágenes; limita memoria y afecta dinámica del ajuste |
| Epoch | Recorrido de entrenamiento definido por pasos | 20 en el TFC; división entera de pasos puede omitir remanentes |

**Ejemplo didáctico:** un kernel podría responder a transiciones de intensidad y una capa posterior combinar esas respuestas. Que una visualización parezca resaltar pulmón no prueba que el modelo haya aprendido un mecanismo de enfermedad.

**Ventaja CNN:** aprende representación y clasificador conjuntamente. **Limitaciones en este trabajo:** numerosos parámetros, dependencia del conjunto y costo documentado. No se concluye que CNN sea inadecuada para imágenes: es una elección técnicamente razonable cuyo protocolo y desempeño se pueden examinar.

**Defensa:** reconstruir entrada→convoluciones/pooling→Flatten→Dense→Dropout→Softmax, diferenciar kernel de filtro y explicar por qué el Dense domina parámetros. Aclarar que la diferencia train/test publicada puede requerir auditar código antes de atribuirla al algoritmo.

## 8. HOG desde los píxeles hasta el vector

### Qué es y para qué sirve

Histogram of Oriented Gradients resume **direcciones de cambio de intensidad** en regiones. Convierte estructura local en un vector fijo apto para SVM/logística. El procedimiento se fundamenta en [E03](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html) y sus parámetros en [E05](https://scikit-image.org/docs/stable/api/skimage.feature.html).

### Cómo funciona

Se calculan diferencias horizontales y verticales, `gx` y `gy`; magnitud `sqrt(gx²+gy²)` y orientación `atan2(gy,gx)`. En cada **celda**, los píxeles votan a bins de orientación ponderados por magnitud. Se reúnen celdas en **bloques**, se normaliza su energía y se concatenan histogramas. Un bloque puede solaparse con otro, por eso una celda contribuye varias veces.

### Ejemplo y dimensiones propuestas [C]

En una radiografía, contornos de costillas o márgenes del tórax generan gradientes; también los textos laterales. Con 128×128 píxeles, celdas 8×8, bloques 2×2 y 9 orientaciones: 16×16 celdas, 15×15 bloques y `15×15×2×2×9 = 8100` features. Es un cálculo de diseño, no extracción realizada.

**Parámetros:** resolución, orientations, pixels_per_cell, cells_per_block, block_norm; fijar explícitamente L2-Hys y transform_sqrt desactivado inicialmente. No depender de defaults de una biblioteca que pueden diferir del diseño.

**Ventajas:** construcción inspeccionable y sin entrenamiento profundo. **Limitaciones:** alta dimensión, sensibilidad a registro/escala y aprendizaje de artefactos. La visualización HOG muestra el descriptor, no importancia predictiva ni mapa de enfermedad.

**Defensa:** calcular longitud del vector, explicar por qué normalizar por bloques y distinguir extraer features de aprender pesos del clasificador.

## 9. LBP y textura

Local Binary Pattern describe un vecindario comparando cada vecino con el píxel central: mayor o igual produce 1; menor produce 0. Una secuencia ordenada de bits codifica el patrón. Se construyen histogramas de códigos en regiones; estos describen textura. `P` controla vecinos y `R` radio. La variante `uniform` agrupa patrones por estructura de transiciones y reduce categorías ([E04](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_local_binary_pattern.html)).

**Ejemplo didáctico:** alrededor de un centro de intensidad 100, vecinos mayores/menores generan un código como 11000011 según orden fijado. Rotar el orden cambia el código básico; la variante elegida determina qué invariancias se buscan. No interpretar el entero como intensidad o gravedad.

**Uso propuesto [C]:** P=8, R=1, `uniform`; histogramas normalizados en 4×4 regiones espaciales. Diez bins por región dan 160 features. Un histograma global sería más pequeño pero perdería ubicación. Concatenar regiones conserva una localización gruesa. No entrenar RF con el valor de código por píxel sin definir representación.

**Ventajas:** compacto, económico y complementario a bordes. **Limitaciones:** ruido cambia comparaciones; la agregación pierde detalles y no segmenta pulmones. Los parámetros son hiperparámetros si se comparan, por lo que solo se eligen en desarrollo.

**Defensa:** explicar comparación binaria, histograma y diferencia con HOG. Una característica de textura no es una etiqueta médica interpretable por sí sola.

## 10. Scaling y StandardScaler

StandardScaler aprende por feature la media μ y escala σ del train, y transforma `z=(x−μ)/σ`. Guarda esos valores para validation/test; no vuelve a estimarlos. Reduce el dominio de columnas con escalas grandes sobre distancias, márgenes y regularización. Un feature constante requiere tratamiento definido por biblioteca, no división manual por cero. Véase [E14](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).

**Ejemplo didáctico:** si una variable varía entre 0 y 1000 y otra entre 0 y 1, distancia euclídea sin escala estará dominada por la primera. Aun con HOG normalizado por bloques, columnas pueden tener distinta variabilidad; evaluamos un pipeline con escalado consistente.

**Uso:** SVM, logística y KNN; PCA se aplicaría después de scaler. RF usa umbrales ordenados y no requiere escalado por ese motivo. Estandarizar histograma LBP para KNN no es lo mismo que normalizarlo para sumar uno.

**Ventajas:** facilita ajustes y hace regularización comparable por escala. **Limitaciones:** sensibilidad a outliers; puede aumentar peso de columnas con poca varianza y no elimina correlación. Nunca ajustar con test.

**Defensa:** explicar qué parámetros aprende el scaler y dónde se guarda, aunque el modelo final sea “solo un SVM”.

## 11. PCA y reducción de dimensionalidad

PCA encuentra direcciones ortogonales que concentran varianza de las features centradas. Proyecta cada vector sobre componentes y conserva menos coordenadas. Se calcula a partir de una descomposición matricial; **no necesita ni optimiza etiquetas**. La varianza explicada indica proporción de variabilidad de entrada conservada, no porcentaje de accuracy ni de información clínica. Referencia [E10](https://scikit-learn.org/stable/modules/decomposition.html#pca).

**Ejemplo didáctico:** dos features de bordes muy correlacionadas pueden resumirse con una dirección común. Pero un detalle de poca varianza podría separar clases: eliminarlo puede empeorar clasificación.

**Uso propuesto [C]:** ablación HOG→scaler→PCA(95 % varianza)→SVM frente a la misma ruta sin PCA. El número efectivo de componentes se aprende dentro de cada fold y puede diferir. Debe ser compatible con rango de la matriz y solver; una fracción de varianza no es intercambiable con un número fijo al elegir solver.

**Parámetros:** n_components, solver, whiten y semilla si el algoritmo es aleatorio. Comenzar sin whitening; probarlo sin justificación agrega otra decisión y costo.

**Ventajas:** puede comprimir correlación y acelerar clasificador. **Limitaciones:** PCA cuesta tiempo/memoria, puede perder señal y combina features; baja interpretabilidad de componentes. No ajustarlo sobre todo desarrollo antes de CV ni sobre test aunque no use etiquetas.

**Defensa:** diferenciar selección de variables de proyección, explicar 95 % de varianza y reconocer que PCA no garantiza mejor generalización.

## 12. SVM lineal y RBF

### Qué es y cómo funciona

Support Vector Machine busca una frontera con margen amplio entre clases. En el caso lineal decide con `w·x+b`; los ejemplos que condicionan la frontera se relacionan con vectores soporte. Una formulación de margen suave usa etiquetas ±1 y minimiza `1/2 ||w||² + C Σ ξ_i`, con restricciones `y_i(w·x_i+b)≥1−ξ_i` y `ξ_i≥0`. Variantes como LinearSVC pueden usar pérdida hinge al cuadrado: registrar la variante implementada. [E06](https://scikit-learn.org/stable/modules/svm.html).

**C** grande penaliza más violaciones del margen y debilita regularización relativa; C pequeño favorece margen más regularizado. No significa que C grande siempre mejore.

Un **kernel** calcula similitud equivalente a un producto en otro espacio. RBF usa `exp(−gamma ||x−x'||²)`; gamma alto implica influencia más local y puede producir fronteras complejas. Lineal no usa gamma. El escalado cambia distancias y, por lo tanto, el efecto del kernel.

### Uso, ventajas y límites [C]

HOG produce muchos atributos y una SVM lineal brinda una prueba inicial razonable de separación con margen. Su inferencia depende de productos con coeficientes; RBF depende de vectores soporte y puede ser mucho más costosa al crecer n. No anunciar ahorro hasta medir extracción más clasificador.

Score de `decision_function` no es probabilidad, pero sirve para ranking ROC/PR. Activar estimación probabilística en una SVM puede agregar calibración y costo; no es necesario para AUC. Se debe registrar qué signo corresponde a COVID.

**Defensa:** dibujar mentalmente frontera y margen; explicar parámetro aprendido w frente a hiperparámetro C; justificar lineal primero y RBF solo como alternativa controlada.

## 13. Random Forest

Un árbol divide el espacio mediante reglas del tipo `feature_j ≤ umbral`. En clasificación se eligen divisiones que reducen impureza, por ejemplo Gini `1−Σ p_k²`. Un Random Forest entrena muchos árboles con muestras bootstrap y subconjuntos aleatorios de features en cada división; agrega sus predicciones. Busca reducir variación de árboles individuales. [E07](https://scikit-learn.org/stable/modules/ensemble.html).

**Parámetros:** n_estimators, max_depth, min_samples_leaf, max_features, class_weight, bootstrap y random_state. Cantidad de árboles suele estabilizar promedio pero aumenta memoria/latencia; árboles muy profundos pueden memorizar. No existe una única función de pérdida global optimizada conjuntamente como en logística.

**Uso propuesto [C]:** LBP compacto y no lineal como segundo candidato principal. HOG también es compatible, pero miles de atributos correlacionados elevan costo y complican interpretación. Si cambia representación entre RF y SVM, la comparación es de pipelines completos.

**Ventajas:** relaciones no lineales, pocas exigencias de escalado y flexibilidad. **Limitaciones:** un bosque no es transparente como un solo árbol; su importancia por impureza puede favorecer ciertos atributos y no prueba causalidad. Inferencia recorre muchos árboles y puede pesar más que un modelo lineal.

**Defensa:** explicar bootstrap, selección aleatoria de features, ensemble y por qué regularizar hojas/profundidad.

## 14. KNN

K vecinos más cercanos guarda ejemplos y clasifica una entrada mediante las etiquetas de sus k vecinos según distancia. Puede votar uniformemente o ponderar por distancia. El aprendizaje casi no optimiza parámetros globales; buena parte del costo se desplaza a inferencia y almacenamiento. [E08](https://scikit-learn.org/stable/modules/neighbors.html).

**Parámetros:** k, weights, métrica y p de Minkowski (p=1 Manhattan, p=2 euclídea), algoritmo de búsqueda. Se requiere escala coherente; una distancia dominada por variables arbitrarias deja de representar similitud útil.

**Curse of dimensionality:** al aumentar dimensiones, cubrir el espacio requiere muchos más datos y distancias pueden perder contraste. HOG de 8100 atributos no garantiza vecinos semánticamente cercanos. Por eso la alternativa inicial es LBP más compacto; PCA sería otra decisión a validar, no una cura universal.

**Uso [C]:** candidato opcional para entender similitud y contrastar costo de inferencia; no desplaza a C1/C2. **Ventaja:** puede mostrar ejemplos de referencia. **Limitación:** ejemplos similares pueden compartir equipo o marcas, no patología.

**Defensa:** explicar por qué “entrena rápido” no significa “sistema barato” y cómo k pequeño/grande modifica variación/suavidad de frontera.

## 15. Regresión logística y baseline

Aunque su nombre dice regresión, la regresión logística modela `P(y=1|x)` mediante una sigmoide de `w·x+b`. Al aplicar un umbral produce una **clasificación**. Ajusta coeficientes minimizando log-loss binaria más regularización, por ejemplo L2: penalizar pesos grandes limita complejidad. Su frontera en el espacio original de features es lineal; no requiere que los píxeles sigan una distribución normal. [E09](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression).

**Parámetros:** C o fuerza de regularización según API, penalización, solver, class_weight, tolerancia y max_iter. Un aviso de no convergencia no debe ocultarse. Probabilidades estimadas no están automáticamente calibradas para otra prevalencia.

**Uso [C]:** B1=HOG+scaler+logística L2, referencia adicional interpretable. C1=SVM y C2=RF siguen siendo los dos candidatos principales. B0 es **DummyClassifier most_frequent**, que predice la clase más frecuente del train sin mirar la imagen. Sirve para comprobar si el sistema extrae algo útil por encima de una regla trivial.

**Ejemplo didáctico:** en datos exactamente balanceados B0 tiene accuracy cercana a 50 %, pero F1 macro depende de la clase predicha y de la convención para denominadores nulos. No inventar 0,5 para todas sus métricas. ROC-AUC de scores constantes, con ambas clases presentes, representa falta de discriminación, no una buena referencia clínica.

**Defensa:** justificar baseline como control y reconocer que si los candidatos no la superan hay un resultado que investigar, no algo que deba esconderse.

## 16. Métricas con la clase positiva explícita

### Matriz y fórmulas

Convención de este TFI: filas reales, columnas predichas, orden `[0 normal,1 COVID]`. Así, la matriz es `[[VN,FP],[FN,VP]]`. Los gráficos del TFC usan COVID primero: cambiar orden cambia posición, no definición.

| | Predicho normal | Predicho COVID |
|---|---:|---:|
| Real normal | VN | FP |
| Real COVID | FN | VP |

| Métrica | Fórmula | Pregunta |
|---|---|---|
| Accuracy | `(VP+VN)/N` | ¿Cuántos aciertos sobre todas las imágenes? |
| Precision positiva | `VP/(VP+FP)` | De lo marcado COVID, ¿cuánto tiene etiqueta COVID? |
| Recall / sensibilidad | `VP/(VP+FN)` | De los COVID, ¿cuántos recuperamos? |
| Especificidad | `VN/(VN+FP)` | De los normales, ¿cuántos reconocemos? |
| F1 positivo | `2VP/(2VP+FP+FN)` | ¿Cómo se equilibran precision y recall positivos? |
| F1 macro | `(F1_normal+F1_COVID)/2` | ¿Cómo tratamos ambas clases con igual peso? |

**Ejemplo didáctico:** VP=8, FN=2, FP=4, VN=6 en 20 imágenes da accuracy=70 %, precision≈66,7 %, recall=80 %, especificidad=60 %, F1 positivo≈72,7 %. Es un ejemplo inventado para aprender, **no un resultado experimental**. Permite ver por qué accuracy no describe qué error predomina.

El **F1 weighted** pondera por soporte y puede ocultar bajo desempeño minoritario; **macro** asigna el mismo peso a cada clase. El soporte es cantidad de ejemplos reales de la clase. Fijar tratamiento de divisiones por cero y documentarlo; una métrica indefinida no es evidencia de rendimiento nulo salvo convención explícita.

### ROC, AUC y precision-recall

Una curva **ROC** recorre umbrales y relaciona sensibilidad con tasa de falsos positivos `FP/(FP+VN)=1−especificidad`. **ROC-AUC** resume ranking: si se eligen un positivo y un negativo al azar, mide ordenación correcta considerando empates. No es porcentaje de diagnósticos correctos a un umbral.

La curva **PR** relaciona precision y recall y depende de prevalencia. Es informativa cuando hay pocos positivos. “AUC-PR” puede referirse a áreas calculadas de formas distintas: el proyecto reportará **Average Precision (AP)** con nombre explícito y no la confundirá con integración trapezoidal. Usar scores continuos, no solo predicciones binarias; un modelo puede tener buen ranking y mal umbral. Fundamento de implementaciones en [E12](https://scikit-learn.org/stable/modules/model_evaluation.html).

### Qué debemos defender

F1 macro será la métrica de selección propuesta, acompañada siempre por sensibilidad y especificidad. Un falso negativo puede producir falsa tranquilidad si se usa indebidamente como diagnóstico; un falso positivo puede inducir evaluaciones innecesarias. No asignaremos costos clínicos numéricos ni recomendaremos tratamiento. La consigna pide estudiar implicancias, no validar medicina.

TFC prueba 10: 79,47 % es accuracy test; 82,08 % es accuracy validation; 79,60 % es F1 COVID. Son métricas diferentes. El 75 % de coincidencia médico/red tampoco equivale a accuracy contra etiquetas.

## 17. Hiperparámetros y optimización

Un **parámetro aprendido** surge de fit: coeficientes SVM/logística, umbrales de árboles, media del scaler o componentes PCA. Un **hiperparámetro** organiza ese aprendizaje: C, profundidad, vecinos, resolución, celdas HOG o n_components. Elegir entre extractores también es selección de modelo.

**GridSearchCV** ensaya combinaciones de una grilla y compara por CV. **RandomizedSearchCV** toma un número definido de combinaciones de distribuciones/listas; permite controlar costo cuando rangos son grandes. No garantizan el mejor modelo imaginable, solo el mejor encontrado según protocolo. Véase [E11](https://scikit-learn.org/stable/modules/grid_search.html).

**Ejemplo de presupuesto [C]:** 4 valores de C × 2 pesos × 5 folds son 40 ajustes, no ocho. Agregar PCA duplica esa familia, más el costo de ajustar PCA en cada fold. La búsqueda base del roadmap propone 185 ajustes para SVM/PCA/RF/logística, sin opcionales. Antes de ejecutarla medir un piloto de desarrollo, estimar RAM/tiempo y fijar límites.

**Uso:** scorer F1 macro y métricas secundarias, folds comunes, semillas, `cv_results_`, fallos y tiempos guardados. No eliminar una corrida por baja métrica; registrar motivos técnicos si falla. Umbral estándar salvo decisión validada exclusivamente en desarrollo.

**Defensa:** explicar por qué no usar test en tuning y por qué la mejor media de búsqueda es optimista. Una prueba estadística posterior no elimina la contaminación de haber elegido viendo test.

## 18. Estadística para interpretar evidencia

### Media, dispersión e incertidumbre

La **media** resume valores: `m=Σx_i/k`. El **desvío estándar muestral** es `sqrt(Σ(x_i−m)²/(k−1))`; cuantifica dispersión, no incertidumbre de una media bajo cualquier diseño. En CV hay entrenamiento compartido, por lo que `media ± desvío` es descriptivo y no un intervalo de confianza de 95 %.

Un intervalo de confianza depende de supuestos y procedimiento de muestreo. Bootstrap remuestrea unidades; si hay varias imágenes por paciente, remuestrear pacientes conserva mejor la estructura que imágenes independientes. No produce una cohorte externa ni corrige selección sesgada del dataset.

**Significancia:** un p-valor mide cuán incompatibles son los datos con una hipótesis nula bajo un modelo de muestreo; no es probabilidad de que un clasificador sea mejor. Un efecto pequeño puede ser significativo con mucha muestra, y uno relevante puede no serlo con poca. Reportar diferencia, intervalo y tamaño de muestra. No significativo no demuestra igualdad.

### McNemar

Compara dos clasificadores fijos sobre las mismas unidades. Se cuentan `b`: A acierta y B falla, y `c`: A falla y B acierta. Bajo igualdad de tasas de error, las discordancias no deberían favorecer sistemáticamente uno. Con versión exacta se usa distribución binomial sobre b+c; si b+c=0 no hay evidencia de diferencia por discordancias. [E20](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html).

**Ejemplo didáctico:** A y B pueden tener accuracy similar pero fallar en personas diferentes; las accuracies solas no reconstruyen b y c. McNemar no compara directamente F1, AUC o tiempo. Pares de imágenes de un mismo paciente tampoco son automáticamente independientes.

**Uso [C]:** prueba bilateral final contra B0, si hay independencia y predicciones pareadas; CNN solo con evidencia comparable individual. Elegir comparaciones y α antes de test, con ajuste por multiplicidad si se agregan varias.

### Wilcoxon y otras pruebas pareadas

Wilcoxon de rangos con signo estudia diferencias pareadas, usando signos y rangos de magnitudes. Requiere justificar independencia de pares y simetría de diferencias; ceros/empates afectan variantes del cálculo. No es una solución automática por “no normalidad”. [E19](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html).

Demšar [E17](https://jmlr.org/papers/v7/demsar06a.html) trata comparación sobre múltiples datasets; no autoriza a llamar datasets independientes a cinco folds del mismo conjunto. Dietterich [E18](https://doi.org/10.1162/089976698300017197) analiza pruebas aproximadas y propone el diseño 5×2cv para determinadas comparaciones de algoritmos. Ese diseño exige repetir entrenamiento sobre cinco divisiones bipartitas; no se puede aplicarle su fórmula a cualquier CV disponible.

**Defensa:** saber cuándo **no corresponde** una prueba es parte del rigor. En esta etapa solo planificamos métodos; no calculamos p-valores ni significancia de hipótesis propias.

## 19. Interpretabilidad sin prometer explicaciones clínicas

Interpretabilidad consiste en comprender relaciones entre entrada, representación y decisión del modelo. Una explicación puede ser **global** (qué variables usa en general) o **local** (por qué cambió score para un ejemplo). Explicar una función matemática no prueba causalidad médica.

**Coeficientes:** en modelos lineales muestran dirección y magnitud condicionadas a escala y correlación. Mapear un peso HOG a bloque/orientación ayuda a interpretar el descriptor; con PCA se requiere retroproyección. Dos variables correlacionadas pueden repartirse el peso.

**Feature importance por impureza:** resume cuánto reducen impureza las variables en árboles. Puede favorecer variables con más oportunidades de división; no es evidencia independiente de generalización.

**Permutation importance:** se altera el orden de una variable en datos retenidos y se mide cuánto cae una métrica. Repetir permutaciones ayuda a estudiar variabilidad; features correlacionadas pueden sustituirse, y permutar una sola puede crear combinaciones poco realistas. Preferir grupos de regiones/descriptores para este diseño. Véase [E13](https://scikit-learn.org/stable/modules/permutation_importance.html).

**SHAP:** distribuye contribuciones a una predicción según un juego de referencia y supuestos de atribución; depende de la representación y del conjunto de fondo. Puede ser costoso y difícil de explicar en miles de features. No es obligatorio: solo añadirlo con una pregunta concreta no cubierta por coeficientes/permutaciones.

**Uso [C]:** desarrollo retenido o predicciones fuera de fold para explicaciones; test solo para descripción final congelada. Comparar FP/FN con aciertos sin modificar pipeline después. Un mapa HOG no es una explicación del clasificador; una región importante puede contener texto del hospital.

**Defensa:** distinguir importancia de causalidad, exactitud de interpretación y explicación del modelo de diagnóstico del paciente.

## 20. Reproducibilidad y control de versiones

Una **seed** inicializa un generador pseudoaleatorio y ayuda a repetir una secuencia. Registrar semillas de split, folds, RF, búsqueda, PCA aleatoria y bootstrap. Mismo número con distinta biblioteca/hardware no garantiza resultado idéntico. Fijar también hilos cuando se mida costo.

Un **entorno virtual venv** aísla dependencias. `requirements.txt` registra versiones probadas para instalar el entorno; no basta listar nombres sin versiones. Configuración debe separar decisiones del código y definir rutas relativas. Los resultados necesitan hash de datos, partición, configuración y commit que los produjeron.

**Git** versiona cambios; **GitHub** aloja y permite revisar el repositorio. Un commit agrupa una unidad coherente; su SHA identifica contenido/historia, no acredita corrección científica. `.gitignore` previene subir rutas no deseadas, pero no protege archivos ya versionados ni borra historial. No subir datos sensibles, tokens, datasets pesados ni artefactos binarios sin propósito.

**Uso [C]:** manifiestos publicables y resultados pequeños en Git; datos y modelos pesados locales con hashes e instrucciones. Registrar uso de IA: herramienta, versión conocida o “no informada”, etapa, finalidad y verificación humana/técnica. No inventar la versión exacta del asistente ni reemplazar revisión por “lo dijo la IA”.

**Defensa:** demostrar regeneración desde datos autorizados y entorno limpio, no solo abrir un notebook con outputs viejos.

## 21. Inferencia, latencia, drift y mantenimiento

**Inferencia** aplica el pipeline ya ajustado a una nueva entrada. **Latencia** es tiempo hasta obtener salida; debe especificar si incluye lectura, resize, features y carga de modelo. Medir proceso frío y caliente por separado si importa, reportar mediana/p95 y hardware. **Throughput** es cantidad de imágenes por unidad de tiempo; no equivale a latencia individual.

**Data drift** es cambio de distribución de entradas; por ejemplo, otro equipo radiográfico. **Concept drift** cambia la relación entre entradas y etiqueta; **model drift** suele usarse para degradación del rendimiento con el tiempo. Una distribución distinta no demuestra degradación, y medir degradación requiere etiquetas fiables.

**Monitoreo conceptual:** calidad, formatos, origen y tiempos; métricas posteriores cuando haya etiquetas y permisos. **Reentrenamiento:** proceso controlado de nueva versión con datos auditados, validación y posibilidad de rollback; no reacción automática a toda alerta.

**Uso [C]:** describir una inferencia local versionada y sus requisitos. No desplegar API, web o sistema clínico. La facilidad de serialización no resuelve validación real, seguridad ni integración sanitaria.

**Defensa:** aclarar qué mediría el prototipo y qué requeriría una implementación real fuera de alcance.

## 22. CRISP-ML(Q) y aseguramiento de calidad

Es un marco del ciclo de vida de ML con atención explícita a riesgos y calidad. Sus seis fases conectan entendimiento del problema/datos, preparación, modelado, evaluación, despliegue y monitoreo/mantenimiento. Las fases pueden iterar; calidad no significa simplemente completar una lista. [E15](https://arxiv.org/abs/2003.05155).

**Uso original [A]:** el TFC aplica hasta evaluación y excluye despliegue/monitoreo por ser prototipo (p. 32). **Uso nuestro [C]:** 00 define problema/evidencias; 01–03 preparan datos y features; 04–05 modelan; 06 evalúa; 07 interpreta; 08 integra e incluye despliegue conceptual.

**Ejemplo:** riesgo “duplicado entre train y test” exige un control de hashes/grupos y evidencia de cero intersecciones conocidas. No se resuelve escribiendo “seguimos CRISP-ML(Q)”. Los riesgos residuales también se documentan.

**Defensa:** relacionar una fase, un riesgo, un control y un artefacto verificable del proyecto.

## 23. Stack recomendado y decisiones de simplicidad [C]

No se fijan versiones sin probar compatibilidad; sprint 01 construirá el entorno. Cada herramienta resuelve un componente concreto.

| Elemento | Qué es / uso y componente dependiente | Por qué elegirlo y alternativa |
|---|---|---|
| Python | Lenguaje para adquisición, features, entrenamiento y evaluación | Ecosistema común a consigna; R también viable, pero cambiar lenguaje no aporta al objetivo |
| NumPy | Arreglos numéricos; imágenes, vectores y cálculos | Base compatible con scikit-learn/image; listas Python son insuficientes para operaciones eficientes |
| pandas | Tablas; manifiestos, métricas y comparación | Facilita joins por ID y CSV; biblioteca csv bastaría para tareas pequeñas, pero crecen controles tabulares |
| Matplotlib | Figuras estáticas; EDA, matrices, curvas y errores | Exportación controlable; seaborn es opcional y no necesario para gráficos exigidos |
| scikit-learn | Pipeline, modelos, CV, tuning y métricas | API común; implementar solvers a mano agregaría errores sin requisito |
| scikit-image | Carga/transformación y HOG/LBP | Descriptores oficiales y reproducibles; OpenCV sería alternativa, no incorporar ambos sin necesidad |
| Jupyter | Entorno de exploración narrativa | Útil para EDA y estudio; scripts son alternativa y deben sostener la regeneración para evitar estado oculto |
| Git | Versionado de código/documentos/configuración | Historial y comparación; copias de carpetas no ofrecen trazabilidad equivalente |
| GitHub | Remoto oficial y revisión | Permite acceso a cátedra; ZIP sigue siendo alternativa de entrega admitida |
| venv | Aislamiento local de dependencias | Suficiente para stack CPU; conda sería alternativa si hubiera necesidad binaria concreta |
| SciPy, si se usa estadística | Dependencia científica que puede aportar prueba binomial/estadística | Declararla explícitamente si el código la importa; no agregar varias bibliotecas para un mismo contraste |
| pytest, en implementación | Herramienta de pruebas de contratos | Justifica su costo por controles de fuga, métricas y serialización; unittest es alternativa sin dependencia |

No se necesita TensorFlow o PyTorch para los candidatos clásicos; Docker o cloud no resuelven un requisito actual; una base de datos, frontend, API, MLflow o Kubernetes ampliarían el trabajo sin mejorar por sí mismos validez experimental. Los cuadernos no reemplazan módulos probados. Si surge una necesidad concreta, registrar decisión y costo antes de agregar tecnología.

## 24. Glosario de consulta rápida

| Término | Significado en este proyecto |
|---|---|
| IA | Disciplina de sistemas para tareas de percepción, razonamiento, aprendizaje y decisión. |
| ML | Métodos que ajustan una función o estructura a partir de datos. |
| DL | Familia de ML con redes de múltiples capas y representaciones aprendidas. |
| Supervisado | Aprende con entradas y etiquetas objetivo. |
| No supervisado | Encuentra estructura sin etiquetas objetivo para el ajuste. |
| Clasificación | Predicción de una categoría discreta. |
| Regresión | Predicción de una magnitud continua; no confundir con nombre “regresión logística”. |
| Dataset | Conjunto de observaciones y metadatos asociados. |
| Feature | Variable numérica de entrada al clasificador. |
| Target | Variable que se intenta predecir. |
| Clase | Categoría del target, aquí COVID o normal. |
| Etiqueta operativa | Regla concreta que define qué ejemplos integran una clase. |
| Balanceo | Ajuste de frecuencias o pesos de clases durante entrenamiento. |
| Prevalencia | Proporción de positivos en una población/conjunto. |
| Representatividad | Correspondencia de muestra con población objetivo. |
| Procedencia | Fuente, centro o proceso que originó una imagen. |
| Manifiesto | Tabla de IDs, hashes, clases, grupos y particiones. |
| Hash | Huella de contenido para identificar versión o duplicado exacto. |
| Grupo | Unidad que debe permanecer junta al particionar, como paciente. |
| Domain shift | Diferencia entre distribución de entrenamiento y otra población/dominio. |
| Shortcut | Patrón espurio fácil de explotar que no representa el fenómeno pretendido. |
| Train | Datos usados para ajustar parámetros en una etapa concreta. |
| Validation | Datos usados para comparar decisiones durante desarrollo. |
| Test | Datos reservados para la evaluación final congelada. |
| Holdout | Partición retenida fuera del ajuste. |
| Fold | Una de las partes utilizadas en validación cruzada. |
| Cross-validation | Repetición sistemática de entrenamiento/validación dentro de desarrollo. |
| StratifiedKFold | CV que procura preservar proporción de clases. |
| StratifiedGroupKFold | CV que mantiene grupos unidos y procura proporciones de clase. |
| CV anidada | CV externa de evaluación de un procedimiento con CV interna de tuning. |
| OOF | Predicción de un ejemplo por un ajuste que no lo usó en su train. |
| Leakage | Uso de información fuera de la frontera permitida de aprendizaje/selección. |
| Overfitting | Ajuste a particularidades que no generalizan. |
| Underfitting | Ajuste/representación insuficiente incluso en datos de entrenamiento. |
| Generalización | Rendimiento en datos nuevos del dominio pertinente. |
| Píxel | Muestra espacial de intensidad de imagen. |
| Resolución | Número de filas y columnas de píxeles. |
| Grises | Imagen de un canal de intensidad. |
| Resize | Cambio de tamaño por interpolación. |
| Contraste | Diferencia de intensidad entre regiones. |
| Textura | Estructura local de variaciones de intensidad. |
| Borde | Transición marcada de intensidad. |
| Normalización | Ajuste de rango o norma; debe especificarse cuál. |
| Estandarización | Transformación según media y escala aprendidas en train. |
| CNN | Red con convoluciones para aprender representaciones locales. |
| Convolución | Operación local con pesos compartidos. |
| Kernel CNN | Matriz de pesos de un filtro; distinto del kernel de SVM. |
| Filtro | Operador aprendido que genera un canal de activaciones. |
| Feature map | Mapa de activaciones tras un filtro. |
| Padding | Tratamiento de bordes en operaciones espaciales. |
| Stride | Desplazamiento de ventana entre posiciones. |
| ReLU | Activación que devuelve máximo entre cero y entrada. |
| MaxPooling | Reducción espacial seleccionando máximos por ventana. |
| Flatten | Conversión de tensor a vector sin aprendizaje. |
| Dense | Capa de conexiones completas con pesos y sesgos. |
| Dropout | Anulación aleatoria de activaciones durante train. |
| Softmax | Conversión de logits en valores que suman uno. |
| Logit | Puntuación previa a transformación probabilística. |
| Cross entropy / log-loss | Pérdida que penaliza poca probabilidad a la etiqueta correcta. |
| Adam | Optimizador adaptativo basado en momentos del gradiente. |
| Learning rate | Tamaño de actualización durante optimización. |
| Batch | Conjunto procesado en una actualización. |
| Epoch | Recorrido definido por pasos de entrenamiento. |
| Data augmentation | Generación de variaciones de train conservando etiqueta bajo supuestos. |
| HOG | Histogramas locales de orientaciones del gradiente. |
| Gradiente | Dirección y magnitud del cambio local de intensidad. |
| Celda HOG | Región que acumula votos de orientaciones. |
| Bloque HOG | Grupo de celdas normalizado conjuntamente. |
| Bin | Intervalo o categoría de un histograma. |
| LBP | Código de comparaciones de vecinos con el centro. |
| Histograma | Conteos/frecuencias de categorías, normalizables. |
| PCA | Proyección lineal en direcciones de mayor varianza. |
| Componente | Dirección aprendida por PCA y coordenada resultante. |
| Varianza explicada | Proporción de variabilidad representada por componentes. |
| SVM | Clasificador basado en margen y regularización. |
| Hiperplano | Frontera lineal en el espacio de features. |
| Margen | Separación geométrica de frontera respecto a ejemplos. |
| Support vectors | Ejemplos que determinan la solución de margen en formulaciones SVM. |
| C | Control inverso de regularización en las configuraciones propuestas. |
| Kernel SVM | Función de similitud que permite fronteras no lineales implícitas. |
| RBF / gamma | Kernel radial y parámetro que controla su alcance local. |
| RF | Conjunto de árboles aleatorizados cuyas salidas se agregan. |
| Bootstrap | Remuestreo con reemplazo. |
| Ensemble | Combinación de varios estimadores. |
| Impureza | Mezcla de clases dentro de un nodo. |
| KNN / k | Clasificación por vecinos y cantidad considerada. |
| Distancia | Regla numérica de similitud/disimilitud entre vectores. |
| Curse of dimensionality | Dificultad de cobertura y comparación en dimensión elevada. |
| Regresión logística | Modelo de clasificación con sigmoide de combinación lineal. |
| Sigmoide | Función que transforma un real a (0,1). |
| Regularización L2 | Penalización de magnitud cuadrática de coeficientes. |
| Baseline / B0 | Referencia mínima, aquí clase más frecuente. |
| B1 / C1 / C2 | Logística adicional / SVM lineal HOG / RF LBP. |
| StandardScaler | Transformador con media/escala por feature. |
| Pipeline | Encadenamiento de transformaciones y estimador. |
| Fit / transform | Aprender estado / aplicarlo sin reaprender. |
| Parámetro | Valor aprendido durante ajuste. |
| Hiperparámetro | Configuración fijada o seleccionada fuera del ajuste de parámetros. |
| Tuning | Selección de hiperparámetros mediante validación. |
| GridSearchCV | Evaluación CV de una grilla de configuraciones. |
| RandomizedSearchCV | Evaluación CV de combinaciones muestreadas. |
| VP / VN | Positivo / negativo correctamente clasificado. |
| FP / FN | Negativo marcado positivo / positivo marcado negativo. |
| Accuracy | Proporción global de aciertos. |
| Precision | Proporción real positiva entre predicciones positivas. |
| Recall / sensibilidad | Proporción de positivos reales recuperados. |
| Especificidad | Proporción de negativos reales reconocidos. |
| F1 | Media armónica de precision y recall. |
| Macro / weighted | Promedio igual por clase / ponderado por soporte. |
| Soporte | Número de ejemplos reales de una clase. |
| Score / threshold | Puntuación continua / umbral para decidir etiqueta. |
| Calibración | Correspondencia entre probabilidades y frecuencias observadas. |
| ROC / AUC | Curva sensibilidad–FP y área de discriminación. |
| PR / AP | Curva precision–recall y resumen Average Precision. |
| Media / desvío | Centro aritmético / dispersión de valores. |
| Intervalo de confianza | Rango producido por un procedimiento con cobertura bajo supuestos. |
| Significancia / p-valor | Evidencia contra una hipótesis bajo un modelo de muestreo. |
| McNemar | Comparación pareada de tasas de error mediante discordancias. |
| Wilcoxon | Prueba sobre rangos con signo de diferencias pareadas. |
| 5×2cv | Diseño de cinco divisiones bipartitas con intercambio train/validation. |
| Holm | Ajuste secuencial de multiplicidad para familia de contrastes. |
| Coeficiente | Peso aprendido en modelo lineal. |
| Feature importance | Resumen de uso/influencia de atributos, dependiente del método. |
| Permutation importance | Cambio de métrica tras permutar una variable o grupo. |
| SHAP | Atribuciones basadas en contribuciones de un juego de referencia. |
| Seed | Estado inicial de aleatoriedad reproducible. |
| requirements.txt / venv | Dependencias declaradas / entorno aislado. |
| Git / GitHub / commit | Versionado / remoto / unidad identificada por SHA. |
| Inferencia | Aplicación del pipeline congelado. |
| Latencia / throughput | Tiempo por respuesta / volumen procesado por tiempo. |
| Data drift | Cambio en distribución de entradas. |
| Concept drift | Cambio de relación entre entrada y objetivo. |
| Model drift | Degradación del comportamiento del modelo con el tiempo. |
| Monitoreo / reentrenamiento | Seguimiento de calidad / generación controlada de nueva versión. |
| CRISP-ML(Q) | Marco de ciclo de vida de ML con aseguramiento de calidad. |
| Ablación | Comparación controlada quitando/añadiendo un componente. |
| Definition of Done | Evidencia y criterios verificables para cerrar un sprint. |

# Preguntas posibles de defensa

Las respuestas cortas son un punto de partida: ambos integrantes deberán ampliarlas con evidencia propia después de ejecutar el proyecto. Ninguna respuesta presupone resultados futuros.

| # | Pregunta | Respuesta corta | Qué concepto evalúa |
|---:|---|---|---|
| 1 | ¿Por qué no utilizar otra CNN? | La consigna pide alternativa; características explícitas y modelos clásicos permiten estudiar otro compromiso de representación/costo. | Alcance y elección |
| 2 | ¿Qué modelo fue utilizado originalmente? | CNN de tres convoluciones, dos pooling, Flatten, Dense 64, Dropout 0,5 y salida Softmax de dos clases. | Evidencia del TFC |
| 3 | ¿Qué resultado obtuvo? | Mejor test publicado: 79,47 % de accuracy, prueba 10 de D4; no es nuestro resultado. | Trazabilidad |
| 4 | ¿Por qué el dataset 4 funcionó mejor? | Los autores lo atribuyen a limpieza; el diseño no aísla causalmente limpieza, tamaño, partición y azar. | Crítica metodológica |
| 5 | ¿Qué limitaciones tenía el TFC? | Calidad, costo, portabilidad y acceso al experto; además identificamos límites de replicación y selección sobre test. | Evidencia e interpretación |
| 6 | ¿Qué hace HOG? | Resume orientaciones de gradientes por celdas y bloques normalizados. | Representación |
| 7 | ¿Qué longitud tendrá HOG inicialmente? | 8100 con 128², celdas 8², bloques 2², 9 bins; es una dimensión propuesta. | Cálculo de features |
| 8 | ¿Qué describe LBP? | Patrones locales de comparación de intensidades agregados en histogramas de textura. | Textura |
| 9 | ¿Por qué SVM? | Es un candidato de margen regularizado para vectores HOG de alta dimensión; aún no sabemos si ganará. | Justificación experimental |
| 10 | ¿Qué controla C? | Compromiso entre regularización/margen y penalización de errores. | Hiperparámetros |
| 11 | ¿Qué diferencia hay entre lineal y RBF? | RBF introduce similitudes no lineales con gamma y mayor costo potencial; lineal usa un hiperplano. | Kernels |
| 12 | ¿Qué es PCA? | Proyección no supervisada en direcciones de mayor varianza. | Reducción |
| 13 | ¿Qué significa explicar 95 % de varianza? | Retener ese porcentaje de variación de features; no 95 % de accuracy ni señal clínica. | Interpretación PCA |
| 14 | ¿PCA siempre mejora? | No; cuesta recursos y puede eliminar señal discriminativa de poca varianza. | Límites |
| 15 | ¿Por qué no tocar el test set? | Debe evaluar una solución cuyas decisiones ya están congeladas. | Independencia |
| 16 | ¿Qué es data leakage? | Uso de información fuera del conjunto permitido para ajustar o seleccionar. | Validez |
| 17 | ¿PCA puede filtrar información sin etiquetas? | Sí, aprende direcciones de la distribución; debe ajustarse dentro de cada train. | Fuga no supervisada |
| 18 | ¿Por qué usar cross-validation? | Compara métodos con varias particiones de desarrollo y describe variabilidad. | Validación |
| 19 | ¿Por qué estratificar? | Para procurar presencia y proporción de clases en folds, sin garantizar representatividad. | Muestreo |
| 20 | ¿Qué pasa con varias imágenes de un paciente? | Se agrupan en una misma partición; estratificar por clase no alcanza. | Dependencia |
| 21 | ¿Qué diferencia existe entre precision y recall? | Precision condiciona a predicción positiva; recall a etiqueta positiva real. | Métricas |
| 22 | ¿Qué implica un falso negativo? | Imagen etiquetada COVID clasificada normal; puede ser riesgoso si se usa indebidamente como diagnóstico. | Errores y alcance |
| 23 | ¿Qué implica un falso positivo? | Imagen normal marcada COVID; puede generar evaluaciones innecesarias en un uso indebido. | Errores |
| 24 | ¿Por qué accuracy alta puede engañar? | Puede reflejar clase mayoritaria y ocultar fracaso en positivos. | Desbalance |
| 25 | ¿Por qué F1 macro? | Equilibra peso de clases; se complementa con sensibilidad/especificidad. | Selección |
| 26 | ¿Qué mide ROC-AUC? | Ordenación de scores entre clases a través de umbrales, no accuracy final. | Ranking |
| 27 | ¿Qué aporta AP? | Resume precision–recall; su lectura requiere prevalencia y método de integración explícitos. | PR |
| 28 | ¿Por qué baseline? | Permite saber si aprender de imágenes aporta frente a una regla trivial. | Control experimental |
| 29 | ¿La regresión logística es regresión en este caso? | Modela probabilidad con sigmoide y se usa para clasificación binaria. | Familia de modelos |
| 30 | ¿Cómo funciona Random Forest? | Agrega árboles entrenados con bootstrap y selección aleatoria de atributos. | Ensemble |
| 31 | ¿Por qué limitar profundidad de RF? | Reduce capacidad de memorizar y costo; se valida en desarrollo. | Regularización |
| 32 | ¿Por qué KNN puede ser lento al predecir? | Debe comparar la nueva entrada con ejemplos almacenados. | Costo |
| 33 | ¿Qué es la maldición de dimensionalidad? | Aumentan necesidades de datos y se debilita utilidad de distancias al crecer dimensión. | Geometría |
| 34 | ¿Qué aprende StandardScaler? | Media y escala por atributo del train correspondiente. | Preprocesamiento |
| 35 | ¿Qué protege Pipeline? | Ajuste coherente de transformaciones dentro de folds; no corrige pacientes repetidos. | Diseño y límites |
| 36 | ¿Qué diferencia parámetro e hiperparámetro? | Uno se aprende en fit; el otro configura o selecciona cómo se aprende. | Optimización |
| 37 | ¿GridSearch siempre es mejor que RandomizedSearch? | No; depende de espacio y presupuesto. Ninguno garantiza óptimo global. | Búsqueda |
| 38 | ¿Qué significa generalizar? | Predecir en nuevos casos del dominio evaluado, no en toda población imaginable. | Validez externa |
| 39 | ¿Cómo detectarían overfitting? | Revisando brecha train/CV y curvas, además de auditar cambios de datos/preprocesamiento. | Diagnóstico técnico |
| 40 | ¿Qué es CRISP-ML(Q)? | Marco de seis fases con riesgos y controles de calidad del ciclo ML. | Metodología |
| 41 | ¿Cómo garantizan reproducibilidad? | Entorno probado, versiones, datos/particiones identificados, configuración, semillas, código y comandos. | Trazabilidad |
| 42 | ¿Una semilla basta? | No; también influyen datos, versiones, hardware y paralelismo. | Reproducibilidad |
| 43 | ¿Qué ventajas aporta ML clásico frente a CNN aquí? | Podría facilitar costo y análisis de descriptores; son hipótesis que debemos medir. | Honestidad experimental |
| 44 | ¿Podemos usar McNemar con 79,47 % y otra accuracy? | No; necesitamos predicciones de ambos sobre las mismas unidades. | Estadística pareada |
| 45 | ¿Podemos aplicar Wilcoxon a cinco folds sin más? | No; comparten entrenamiento y no son pares independientes de datasets. | Supuestos |
| 46 | ¿Media ± desvío CV es un IC del 95 %? | No; describe dispersión entre folds y requiere otros supuestos para inferencia. | Incertidumbre |
| 47 | ¿No significativo demuestra igualdad? | No; puede faltar potencia y tampoco establece equivalencia. | Significancia |
| 48 | ¿Importancia demuestra causalidad? | No; explica dependencia del modelo y puede reflejar correlación o atajos. | Interpretabilidad |
| 49 | ¿Por qué no usar SHAP siempre? | Añade costo y supuestos; primero hay que definir qué pregunta resuelve. | Simplicidad |
| 50 | ¿Se comparó con varios médicos? | No: un profesional, 52 imágenes, tres indefinidas y 49 comparables. | Validación original |
| 51 | ¿75 % de acuerdo significa 75 % de diagnóstico correcto? | No; acuerdo y acierto frente a etiquetas son cantidades distintas. | Denominadores |
| 52 | ¿Es D4 una prueba de COVID frente a todas las enfermedades? | No: su clase negativa son pulmones normales. | Etiquetas y población |
| 53 | ¿Qué harían si faltan IDs de D4? | Declarar imposibilidad de réplica exacta y justificar alternativa; autorización de cátedra si sustituimos datos. | Comparabilidad |
| 54 | ¿Qué revela la omisión de /255 en anexo IV? | Inconsistencia del código publicado; no prueba que haya causado las cifras reportadas. | Evidencia y causalidad |
| 55 | ¿Qué medirían para afirmar menor costo? | Pipeline completo, búsqueda, ajuste, inferencia, RAM y tamaño bajo condiciones comparables. | Benchmark |
| 56 | ¿Qué es data drift? | Cambio de distribución de entrada; no demuestra por sí solo caída de rendimiento. | Monitoreo |
| 57 | ¿Qué harían si otro modelo gana en test? | Informarlo sin cambiar selección; una revisión exigiría un nuevo protocolo/test independiente. | Test único |
| 58 | ¿Qué pasa si nadie supera la baseline? | Se reporta el resultado, se auditan fallos y se discuten límites sin inventar mejoras. | Integridad |
| 59 | ¿Cómo declaran uso de IA? | Herramienta/versión conocida, etapa, finalidad y verificación en el anexo exigido. | Autoría |
| 60 | ¿Qué se completó en esta etapa? | Lectura, investigación y planificación; ningún sprint ni entrenamiento propio. | Estado real |
