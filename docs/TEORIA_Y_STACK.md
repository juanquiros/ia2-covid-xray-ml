# Teoría y stack para estudiar y defender el TFI

**Equipo:** Juan Quirós y Andruszyszyn. **Estado:** material de estudio y diseño, 09/10/2026; no hay experimentos propios. Las decisiones operativas se mantienen en [Roadmap](ROADMAP_TFI.md). La evidencia del TFC, la consigna y las referencias E01–E20 se identifican en [Fuentes](FUENTES_Y_TRAZABILIDAD.md).

Este material explica cómo una radiografía se convierte en un vector, cómo se aprende una regla de clasificación y cómo comprobar si funciona sobre datos que no participaron en su construcción. Los ejemplos numéricos son **didácticos**, salvo cuando se indica explícitamente que proceden del TFC. No anticipan resultados del equipo.

# PARTE I · Núcleo del TFI

## 1. IA, ML, aprendizaje supervisado y clasificación

### Qué son IA, ML y Deep Learning

La inteligencia artificial estudia sistemas capaces de realizar tareas como razonar, planificar, percibir o aprender. Machine Learning (ML) es el conjunto de métodos que ajustan un comportamiento a partir de datos. Deep Learning (DL) es una familia de ML basada en redes con múltiples capas que aprenden representaciones. Una CNN pertenece a DL; SVM y Random Forest pertenecen a ML. El enfoque clásico también aprende: lo que elegimos explícitamente es cómo representar la imagen.

**Para qué sirve esta distinción:** nuestra alternativa cambia el mecanismo de representación y clasificación de la CNN original. No basta cambiar TensorFlow por otra biblioteca para obtener una solución metodológicamente diferente.

### Supervisado, no supervisado, clasificación y regresión

En aprendizaje **supervisado** disponemos de ejemplos `(x,y)`: radiografía y etiqueta. El algoritmo aprende una función para predecir y en nuevas x. Clasificación predice una categoría; regresión predice una magnitud continua, por ejemplo un tiempo. Nuestro y es binario, no un grado de enfermedad ni una probabilidad clínica certificada.

En aprendizaje **no supervisado**, el algoritmo busca estructura sin usar etiquetas objetivo: grupos, componentes o anomalías. Nuestro núcleo usa etiquetas; métodos no supervisados como PCA se explican brevemente en la parte II y no se incorporan al experimento.

**Ventaja del supervisado aquí:** coincide con las etiquetas y permite evaluar aciertos/errores. **Limitación:** aprender etiquetas defectuosas puede producir un clasificador fiel al dataset pero poco útil fuera de él.

**Defensa:** explicar por qué clasificación binaria es apropiada para reproducir la tarea de D4 y por qué no equivale a diagnóstico. La CNN original reconoce etiquetas de imágenes; la práctica clínica requiere otros elementos.

## 2. Dataset, features, target y balanceo

Un **dataset** es una colección de observaciones y su información asociada. Aquí cada fila futura del manifiesto representará una imagen, con ID, hash, fuente, clase, grupo/paciente si está disponible y partición. La unidad almacenada puede ser imagen, pero la unidad independiente puede ser paciente: varias radiografías de una persona no son observaciones intercambiables con personas nuevas.

Las **features** son las variables de entrada del clasificador; el **target** es la salida que queremos aprender. Los píxeles son una representación; un vector HOG es otra. Las clases son valores del target. Nuestra convención propuesta es `1=COVID`, `0=normal`; el anexo original usa índices `covid=0`, `no covid=1`. No copiar ese índice y luego calcular recall con positivo=1 sin verificar su significado.

**Cómo funciona el balanceo:** modifica el peso relativo de clases en entrenamiento, mediante pesos, submuestreo o sobremuestreo. No crea información nueva. `class_weight='balanced'` calcula pesos a partir de las frecuencias del train de cada fold. Sobremuestrear antes de particionar puede duplicar ejemplos a ambos lados. No balancear test artificialmente después de ver resultados.

**Ejemplo didáctico:** con 90 normales y 10 positivos, predecir siempre normal logra 90 % de accuracy y recall COVID=0. Un dataset balanceado facilita ver ese fracaso, pero su precision no se traslada automáticamente a una población con otra prevalencia.

**Uso en el TFI:** investigar frecuencias y origen, no suponer que todos los datasets originales están balanceados. D1 tiene 10972/10192; D4 2462/2462 según TFC tabla 2. Solo se usarán las etiquetas originales COVID y normales para nuestra tarea propuesta. No reetiquetar neumonía viral como infección COVID por intuición.

**Defensa:** distinguir balance, representatividad y calidad. Dos clases con igual tamaño pueden estar sesgadas por edad, centro, equipo o severidad.

## 3. Píxeles, imágenes y preprocesamiento

### Qué es una imagen para el algoritmo

Un **píxel** es una muestra espacial de intensidad. La **resolución** es la cantidad de filas y columnas; 299×299 no indica por sí sola calidad diagnóstica. Una imagen en **grises** tiene un canal; RGB tiene tres. Convertir a grises no borra marcas, texto ni sesgo de procedencia. La misma intensidad almacenada puede depender del equipo, exposición y procesamiento.

**Textura** describe variaciones locales repetidas de intensidad. **Borde** es una transición relativamente fuerte entre intensidades. **Contraste** expresa diferencias de intensidad entre regiones. HOG enfatiza estructura de gradientes; no sabe, por definición, qué es pulmón o patología.

### Cómo se preprocesa y por qué

Resize interpola una imagen para obtener tamaño fijo. Al reducir puede perderse detalle; al ampliar no aparece nueva información. Un recorte puede quitar anatomía; deformar la proporción puede cambiar estructuras. Por eso se registran resolución, interpolación, tratamiento de aspecto y rango.

Normalización puede significar operaciones diferentes: dividir intensidades de 8 bits por 255, normalizar un histograma para que sume uno o estandarizar features con media y desvío. **No son equivalentes.** Dividir por 255 es válido si la entrada efectivamente tiene ese rango; aplicarlo dos veces o sobre una imagen ya en [0,1] cambia la escala incorrectamente. Si se aprende una media del conjunto, se aprende únicamente en train.

**Uso propuesto:** grises, tamaño inicial 128×128 y contrato de rango/tipo. No agregar ecualización, segmentación o filtros sin pregunta experimental y revisión en desarrollo.

**Ventajas:** comparabilidad de dimensiones y costo controlado. **Limitaciones:** alteración de texturas, pérdida de detalles y persistencia de atajos. Una imagen nítida no implica una etiqueta correcta.

**Defensa:** demostrar qué entra y sale de cada transformación, y explicar por qué una fotografía de prueba no puede tener un preprocesamiento distinto al del entrenamiento. La inconsistencia `/255` entre anexos del TFC es un motivo concreto para centralizar la función, no una demostración del origen de todos sus errores.

## 4. Train, validation, test y generalización

### Qué es cada partición

**Train** ajusta parámetros: coeficientes, umbrales de árboles y medias del scaler. **Validation** compara decisiones que rodean ese ajuste: C, profundidad y tamaño de hojas. **Test** estima el comportamiento final después de tomar las decisiones. No es un recurso para mejorar la configuración.

**Generalización** es capacidad de predecir adecuadamente en nuevos datos del dominio objetivo. No significa rendir bien ante cualquier hospital, equipo o época. Una partición aleatoria del mismo repositorio estima generalización interna, con sus límites.

**Overfitting:** un modelo aprovecha peculiaridades del train que no se sostienen en datos nuevos. **Underfitting:** la representación/capacidad o el ajuste son insuficientes y el desempeño es bajo incluso en train. Comparar train/validation y curvas de aprendizaje ayuda, pero una brecha no identifica por sí sola su causa: también pueden existir cambios de distribución, etiquetas o preprocesamiento.

### Uso en el TFI

Propuesta común: 80 % desarrollo, 20 % test; dentro del 80 %, cinco folds. En cada ajuste se usa aproximadamente 64 % total como train y 16 % como validation. No existe un tercer holdout fijo adicional. Al elegir el modelo, se reajusta en todo desarrollo antes del test. Si hay grupos, los porcentajes son aproximados y se prioriza independencia. La política está en el roadmap y no se reemplaza con el 80/10/10 histórico.

**Ejemplo didáctico:** si elegimos entre dos resoluciones mirando el test y luego informamos la mejor accuracy, el test ya influyó aunque nunca se haya llamado `fit` sobre él. Sus resultados dejan de ser una evaluación final independiente de esa decisión.

**Defensa:** explicar qué decisiones se congelan y cuándo. La mejor cifra de validation entre muchos ensayos tiene sesgo de selección; no es una estimación final imparcial.

## 5. Data leakage y Pipeline

### Qué es y cómo aparece

Data leakage o fuga de información ocurre cuando la construcción del sistema utiliza información que no debería estar disponible para ese ajuste o evaluación. Puede ocurrir entre train/test, entre train/validation, por duplicados, por pacientes repetidos, por variables que codifican la respuesta o por decisiones humanas guiadas por el test.

**Ejemplo didáctico de escala:** un fold train contiene intensidades medias 10 y 20; validation contiene 100. Si la media se calcula sobre los tres casos, el centro ya incorpora validation. Que no se miren etiquetas no evita la fuga. Cualquier transformación que aprenda estadísticas presenta el mismo problema si se ajusta globalmente.

**Ejemplo de paciente:** una radiografía en train y otra del mismo paciente en test pueden compartir anatomía, dispositivo y marcas. El algoritmo podría reconocer identidad en lugar de generalizar a pacientes nuevos. Un split estratificado por clase no resuelve esa dependencia.

### Cómo funciona sklearn Pipeline

`Pipeline` encadena transformadores y estimador. Al hacer `fit`, cada transformador aprende y transforma el train antes del siguiente paso; al predecir, aplica las transformaciones aprendidas sin reajustar. En CV, cada pipeline se clona y ajusta exclusivamente dentro del fold. No se debe escalar por fuera y pasar a la búsqueda una matriz ya ajustada globalmente. La documentación oficial [E01](https://scikit-learn.org/stable/common_pitfalls.html) sustenta esta separación.

Contrato conceptual, **no implementación**:

```text
fold train -> descriptor fijo -> fit scaler -> fit SVM
fold val   -> mismo descriptor -> transform scaler -> predict SVM
```

HOG fijo se calcula por imagen sin aprender estadísticas del conjunto. Reutilizar esos vectores no autoriza seleccionar decisiones mirando test ni reutilizar un scaler de otro fold. RF recibe HOG directamente.

**Ventajas:** consistencia entre ajuste e inferencia, menor riesgo de errores, serialización de una unidad. **Limitaciones:** no protege contra un manifiesto incorrecto, duplicados cruzados, etiquetas mal mapeadas o selección humana tras test. La prueba futura debe verificar qué IDs recibió cada `fit`, no solo que exista un objeto llamado Pipeline.

**Defensa:** describir un caso de fuga sin etiquetas, uno por paciente y uno por selección de modelo. Distinguir fuga de información de inconsistencia de escala: la omisión de `/255` del TFC es lo segundo, no necesariamente lo primero.

## 6. Cross-validation y Stratified K-Fold

K-fold divide desarrollo en k partes y repite k ajustes: cada parte valida una vez y las otras entrenan. Permite observar variabilidad por partición y comparar métodos con los mismos folds. **StratifiedKFold** intenta conservar proporciones de clase; ayuda a evitar folds sin positivos, pero no corrige sesgo de origen. Con grupos se necesita una estrategia que mantenga paciente/duplicados juntos, como StratifiedGroupKFold cuando es viable. Véase [E02](https://scikit-learn.org/stable/modules/cross_validation.html).

**Parámetros:** k, shuffle, random_state y, cuando corresponda, groups. No improvisar más folds que grupos independientes por clase. La semilla define una partición, no una garantía científica.

**Uso:** seed 42 y cinco folds comunes para B0, C1 y C2; guardar valor por fold, media y desvío estándar muestral. Si un fold no permite calcular AUC por falta de clase, registrarlo y corregir el diseño en desarrollo; no reemplazar por cero.

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

Histogram of Oriented Gradients resume **direcciones de cambio de intensidad** en regiones. Convierte estructura local en un vector fijo común a SVM y Random Forest. El procedimiento se fundamenta en [E03](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html) y sus parámetros en [E05](https://scikit-image.org/docs/stable/api/skimage.feature.html).

### Cómo funciona

Se calculan diferencias horizontales y verticales, `gx` y `gy`; magnitud `sqrt(gx²+gy²)` y orientación `atan2(gy,gx)`. En cada **celda**, los píxeles votan a bins de orientación ponderados por magnitud. Se reúnen celdas en **bloques**, se normaliza su energía y se concatenan histogramas. Un bloque puede solaparse con otro, por eso una celda contribuye varias veces.

### Ejemplo y dimensiones propuestas [C]

En una radiografía, contornos de costillas o márgenes del tórax generan gradientes; también los textos laterales. Con 128×128 píxeles, celdas 8×8, bloques 2×2 y 9 orientaciones: 16×16 celdas, 15×15 bloques y `15×15×2×2×9 = 8100` features. Es un cálculo de diseño, no extracción realizada.

**Parámetros:** resolución, orientations, pixels_per_cell, cells_per_block, block_norm; fijar explícitamente L2-Hys y transform_sqrt desactivado inicialmente. No depender de defaults de una biblioteca que pueden diferir del diseño.

**Ventajas:** construcción inspeccionable y sin entrenamiento profundo. **Limitaciones:** alta dimensión, sensibilidad a registro/escala y aprendizaje de artefactos. La visualización HOG muestra el descriptor, no importancia predictiva ni mapa de enfermedad.

**Defensa:** calcular longitud del vector, explicar por qué normalizar por bloques y distinguir extraer features de aprender pesos del clasificador.

**Alcance fijo:** no se buscarán otras resoluciones ni parámetros HOG. Compartir descriptor reduce decisiones y permite comparar los clasificadores sobre la misma representación; no garantiza que HOG conserve toda señal útil.

## 9. Scaling y StandardScaler

StandardScaler aprende por feature la media μ y escala σ del train, y transforma `z=(x−μ)/σ`. Guarda esos valores para validation/test; no vuelve a estimarlos. Reduce el dominio de columnas con escalas grandes sobre distancias, márgenes y regularización. Un feature constante requiere tratamiento definido por biblioteca, no división manual por cero. Véase [E14](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).

**Ejemplo didáctico:** si una variable varía entre 0 y 1000 y otra entre 0 y 1, distancia euclídea sin escala estará dominada por la primera. Aun con HOG normalizado por bloques, columnas pueden tener distinta variabilidad; evaluamos un pipeline con escalado consistente.

**Uso:** solo C1 necesita StandardScaler en su Pipeline. RF trabaja directamente con HOG: sus reglas por umbral no requieren escalado. La normalización L2-Hys de bloques y la estandarización por columnas son operaciones distintas.

**Ventajas:** facilita ajustes y hace regularización comparable por escala. **Limitaciones:** sensibilidad a outliers; puede aumentar peso de columnas con poca varianza y no elimina correlación. Nunca ajustar con test.

**Defensa:** explicar qué parámetros aprende el scaler y dónde se guarda, aunque el modelo final sea “solo un SVM”.

## 10. SVM lineal

### Qué es y cómo funciona

Support Vector Machine busca una frontera con margen amplio entre clases. En el caso lineal decide con `w·x+b`; los ejemplos que condicionan la frontera se relacionan con vectores soporte. Una formulación de margen suave usa etiquetas ±1 y minimiza `1/2 ||w||² + C Σ ξ_i`, con restricciones `y_i(w·x_i+b)≥1−ξ_i` y `ξ_i≥0`. Variantes como LinearSVC pueden usar pérdida hinge al cuadrado: registrar la variante implementada. [E06](https://scikit-learn.org/stable/modules/svm.html).

**C** grande penaliza más violaciones del margen y debilita regularización relativa; C pequeño favorece margen más regularizado. No significa que C grande siempre mejore.



### Uso, ventajas y límites [C]

HOG produce muchos atributos y una SVM lineal brinda una prueba inicial razonable de separación con margen. Su inferencia depende de productos con coeficientes: aproximadamente O(d) para d atributos; aquí d=8100. El ajuste depende de n, d, solver y convergencia. No anunciar ahorro hasta medir extracción más clasificador.

Score de `decision_function` no es probabilidad, pero sirve para ranking ROC/PR. Activar estimación probabilística en una SVM puede agregar calibración y costo; no es necesario para AUC. Se debe registrar qué signo corresponde a COVID.

**Defensa:** dibujar mentalmente frontera y margen; explicar parámetro aprendido w frente a hiperparámetro C; justificar la frontera lineal elegida y distinguirla de las alternativas de la parte II.

**Implementación prevista:** LinearSVC, C inicial 1 y grilla {0.1, 1, 10}; L2 y squared_hinge. Registrar solver y tolerancias, comprobar convergencia. No habilitar kernels alternativos ni calibración como tareas adicionales.

## 11. Random Forest

Un árbol divide el espacio mediante reglas del tipo `feature_j ≤ umbral`. En clasificación se eligen divisiones que reducen impureza, por ejemplo Gini `1−Σ p_k²`. Un Random Forest entrena muchos árboles con muestras bootstrap y subconjuntos aleatorios de features en cada división; agrega sus predicciones. Busca reducir variación de árboles individuales. [E07](https://scikit-learn.org/stable/modules/ensemble.html).

**Parámetros:** n_estimators, max_depth, min_samples_leaf, max_features, class_weight, bootstrap y random_state. Cantidad de árboles suele estabilizar promedio pero aumenta memoria/latencia; árboles muy profundos pueden memorizar. No existe una única función de pérdida global optimizada conjuntamente como en logística.

**Uso propuesto [C]:** HOG compartido con SVM como segundo candidato. Las 8100 features pueden aumentar costo y correlación; se medirá el efecto sin cambiar descriptor preventivamente. Inicial: 100 árboles, profundidad sin límite y hoja mínima 1. Grilla: árboles {100,200}, profundidad {None,20}, hoja mínima {1,3}; max_features="sqrt", class_weight=None y seed 42.

**Ventajas:** relaciones no lineales, pocas exigencias de escalado y flexibilidad. **Limitaciones:** un bosque no es transparente como un solo árbol; su importancia por impureza puede favorecer ciertos atributos y no prueba causalidad. Inferencia recorre muchos árboles y puede pesar más que un modelo lineal.

**Defensa:** explicar bootstrap, selección aleatoria de features, ensemble y por qué regularizar hojas/profundidad.

**Costo:** cada predicción recorre un camino por árbol; aproximadamente O(T·h) con T árboles y profundidad h. Entrenamiento y tamaño dependen de árboles, nodos, ejemplos y features consideradas. Es una descripción general, no un tiempo prometido.

## 12. DummyClassifier como baseline

B0 usa `strategy="most_frequent"`: aprende la clase mayoritaria del train y la predice para todas las imágenes. Ignora los valores HOG; sirve como referencia mínima para saber si los candidatos aportan información sobre las etiquetas. Se evalúa con los mismos folds y métricas.

En datos equilibrados su accuracy puede rondar 50 %, pero F1 macro no vale automáticamente 0,5. Si predice solo una clase, el F1 de la otra puede ser cero bajo la convención declarada. Registrar tratamiento de denominadores nulos y desempate entre frecuencias. La baseline no diagnostica y no se oculta si supera a los candidatos.

**Defensa:** explicar por qué una referencia trivial es necesaria y por qué no hace falta sumar un tercer clasificador entrenable para cumplir baseline más dos candidatos.

## 13. Métricas con clase positiva explícita

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

La curva **PR** relaciona precision y recall y depende de prevalencia. Es informativa cuando hay pocos positivos. “AUC-PR” puede referirse a áreas calculadas de formas distintas: solo si el desbalance observado justifica PR, el proyecto reportará **Average Precision (AP)** con nombre explícito y no la confundirá con integración trapezoidal. Usar scores continuos, no solo predicciones binarias; un modelo puede tener buen ranking y mal umbral. Fundamento de implementaciones en [E12](https://scikit-learn.org/stable/modules/model_evaluation.html).

### Qué debemos defender

F1 macro será la métrica de selección propuesta, acompañada siempre por sensibilidad y especificidad. Un falso negativo puede producir falsa tranquilidad si se usa indebidamente como diagnóstico; un falso positivo puede inducir evaluaciones innecesarias. No asignaremos costos clínicos numéricos ni recomendaremos tratamiento. La consigna pide estudiar implicancias, no validar medicina.

TFC prueba 10: 79,47 % es accuracy test; 82,08 % es accuracy validation; 79,60 % es F1 COVID. Son métricas diferentes. El 75 % de coincidencia médico/red tampoco equivale a accuracy contra etiquetas.

**Alcance:** matriz, accuracy, precision, recall, especificidad, F1 y F1 macro son centrales. ROC-AUC requiere scores continuos válidos y ambas clases; PR/AP requiere además una razón basada en desbalance real. No son gráficos obligatorios por defecto.

## 14. Hiperparámetros y GridSearchCV

Un parámetro surge del ajuste: pesos SVM, medias del scaler o umbrales de árboles. Un hiperparámetro configura ese aprendizaje: C, cantidad de árboles o profundidad. HOG también tiene parámetros de diseño, pero aquí se mantienen fijos para reducir decisiones.

GridSearchCV evalúa cada combinación de la grilla con los mismos cinco folds de desarrollo y selecciona por F1 macro medio [E11]. C1 busca C={0.1,1,10}; C2 busca n_estimators={100,200}, max_depth={None,20}, min_samples_leaf={1,3}. Son 3+8=11 configuraciones, equivalentes a 55 ajustes de CV, más los reajustes que correspondan. Esta cuenta permite estimar costo; no es una cuota a cumplir.

No se usa RandomizedSearchCV ni se amplía HOG. Se guardan resultados por fold, configuración, fallos y tiempos aproximados. StandardScaler se ajusta dentro de cada fold. En igualdad exacta entre candidatos se prefiere SVM; dentro de cada grilla se mantiene orden documentado. El umbral es el estándar del clasificador y no se ajusta mirando test.

**Límites:** la mejor media seleccionada es potencialmente optimista; el test reservado se usa una vez después de fijar todas las decisiones. La búsqueda no garantiza óptimo universal ni confirma superioridad clínica. **Defensa:** distinguir ajuste, selección y evaluación final.

## 15. Media, dispersión y McNemar condicionado

La media CV es `m=Σx_i/k`; el desvío estándar muestral es `sqrt(Σ(x_i−m)²/(k−1))`, con k=5. Media ± desvío describe variación entre folds; no es un intervalo de confianza de 95 %, porque los entrenamientos se solapan. Este resumen descriptivo y el test final constituyen el plan estadístico principal.

McNemar compara errores de dos clasificadores fijos sobre **las mismas unidades**. `b` cuenta casos donde C1 acierta y C2 falla; `c`, lo inverso. Bajo igualdad de tasas de error, las discordancias no deberían favorecer sistemáticamente a uno. La variante exacta bilateral usa una binomial con b+c ensayos y probabilidad 0,5 [E20]. Si b+c=0, no hay discordancias que sustenten diferencia.

Su aplicación exige predicciones individuales pareadas, mismas imágenes/etiquetas y unidades razonablemente independientes. Varias imágenes de un paciente pueden romper el último supuesto. Se predefine únicamente C1 frente a C2 y α=0.05 antes de abrir test. Si los supuestos no se justifican, se informa que no corresponde. No se reconstruyen pares a partir de accuracies del PDF ni se reemplaza por otra prueba automáticamente.

El p-valor no es probabilidad de que un modelo sea mejor; no significativo no demuestra igualdad. Reportar n, b/c, diferencia de accuracy y p con sus límites. McNemar no contrasta F1 ni causalidad. No programar múltiples pruebas, bootstrap inferencial o nuevos entrenamientos estadísticos.

**Defensa:** justificar tanto la aplicación como la omisión; distinguir dispersión CV, tamaño de diferencia y significancia.

## 16. Interpretabilidad y análisis de errores

Interpretabilidad permite examinar relaciones entre representación y decisión. Global describe qué usa el modelo; local describe un caso. Ninguna demuestra causalidad médica. Se explica el candidato elegido en 04 y se revisan FP/FN frente a aciertos sin volver a ajustar por test.

Para SVM lineal, coeficientes HOG muestran dirección y magnitud condicionadas a escala y correlación. Se pueden asociar a bloques/orientaciones, pero un peso no es una lesión; bins correlacionados reparten señal. La visualización HOG es un descriptor, no importancia del clasificador.

Para RF, importancia por impureza resume reducción de impureza en sus árboles. Es una inspección del modelo entrenado, con sesgos y sin validación independiente de generalización. Permutation importance altera una feature y observa caída de métrica [E13]; puede ser útil si es comprensible y se declara el conjunto de desarrollo utilizado. Correlaciones pueden ocultar o repartir importancia; si se calcula sobre train, explicitar su optimismo. No se exige crear nuevos splits ni conservar todos los modelos CV.

Los ejemplos deben señalar artefactos, calidad o fuente solo cuando sean observables, sin inferir diagnóstico clínico. SHAP queda en la parte II y fuera del experimento. **Defensa:** explicar diferencia entre error, importancia y causalidad.

## 17. Reproducibilidad y control de versiones

Una **seed** inicializa un generador pseudoaleatorio y ayuda a repetir una secuencia. Usar seed 42 para split, folds y estimadores aleatorios. Mismo número con distinta biblioteca/hardware no garantiza resultado idéntico. Registrar hardware y condiciones generales al informar costo, sin infraestructura permanente de hilos.

Un **entorno virtual venv** aísla dependencias. `requirements.txt` registra versiones probadas para instalar el entorno; no basta listar nombres sin versiones. Configuración debe separar decisiones del código y definir rutas relativas. Los resultados necesitan hash de datos, partición, configuración y commit que los produjeron.

**Git** versiona cambios; **GitHub** aloja y permite revisar el repositorio. Un commit agrupa una unidad coherente; su SHA identifica contenido/historia, no acredita corrección científica. `.gitignore` previene subir rutas no deseadas, pero no protege archivos ya versionados ni borra historial. No subir datos sensibles, tokens, datasets pesados ni artefactos binarios sin propósito.

**Uso [C]:** manifiestos publicables y resultados pequeños en Git; datos y modelos pesados locales con hashes e instrucciones. Registrar uso de IA: herramienta, versión conocida o “no informada”, etapa, finalidad y verificación humana/técnica. No inventar la versión exacta del asistente ni reemplazar revisión por “lo dijo la IA”.

**Defensa:** demostrar regeneración desde datos autorizados y entorno limpio, no solo abrir un notebook con outputs viejos.

Un manifiesto con IDs/hashes/particiones y un registro breve de configuración, commit y decisiones son suficientes. No se construye un sistema de bloqueo del test. Cada sprint deja evidencia y comandos, sin formularios operativos duplicados.

## 18. Inferencia, costo y despliegue conceptual

Inferencia aplica el modelo fijado a una entrada nueva. Su tiempo depende de lectura, resize, HOG y clasificación; informar qué incluye. Mediremos tiempos aproximados de extracción, búsqueda/entrenamiento e inferencia, tamaño del modelo y complejidad general. RAM puede anotarse si es fácil obtenerla; no requiere profiling ni telemetría.

Data drift describe cambios de distribución de entrada; concept drift, cambios de relación entre entrada y etiqueta. Una distribución distinta no prueba por sí sola degradación; evaluar rendimiento requiere etiquetas fiables. Un monitoreo hipotético observaría calidad, formatos, origen y errores cuando hubiera permisos y etiquetas. Reentrenar requeriría auditar nuevos datos y validar una nueva versión.

Despliegue, integración, monitoreo, drift y reentrenamiento son **solo conceptuales** en el informe. No se desarrolla una API, aplicación ni servicio clínico. **Defensa:** distinguir qué medimos en el prototipo y qué faltaría para un uso real.

## 19. CRISP-ML(Q) y calidad

Es un marco del ciclo de vida de ML con atención explícita a riesgos y calidad. Sus seis fases conectan entendimiento del problema/datos, preparación, modelado, evaluación, despliegue y monitoreo/mantenimiento. Las fases pueden iterar; calidad no significa simplemente completar una lista. [E15](https://arxiv.org/abs/2003.05155).

**Uso original [A]:** el TFC aplica hasta evaluación y excluye despliegue/monitoreo por ser prototipo (p. 32). **Uso nuestro [C]:** 00 define problema/evidencias; 01–02 preparan datos y HOG; 03 compara modelos; 04 ajusta, evalúa e interpreta; 05 integra el informe y despliegue conceptual. Solo las cuatro primeras fases tienen ejecución técnica.

**Ejemplo:** riesgo “duplicado entre train y test” exige un control de hashes/grupos y evidencia de cero intersecciones conocidas. No se resuelve escribiendo “seguimos CRISP-ML(Q)”. Los riesgos residuales también se documentan.

**Defensa:** relacionar una fase, un riesgo, un control y un artefacto verificable del proyecto.

## 20. Stack recomendado

No se fijan versiones sin probar compatibilidad; sprint 01 construirá el entorno. Cada herramienta resuelve un componente concreto.

| Elemento | Qué es / uso y componente dependiente | Por qué elegirlo y alternativa |
|---|---|---|
| Python | Lenguaje para adquisición, features, entrenamiento y evaluación | Ecosistema común a consigna; R también viable, pero cambiar lenguaje no aporta al objetivo |
| NumPy | Arreglos numéricos; imágenes, vectores y cálculos | Base compatible con scikit-learn/image; listas Python son insuficientes para operaciones eficientes |
| pandas | Tablas; manifiestos, métricas y comparación | Facilita joins por ID y CSV; biblioteca csv bastaría para tareas pequeñas, pero crecen controles tabulares |
| Matplotlib | Figuras estáticas; EDA, matrices, curvas y errores | Exportación controlable; seaborn es opcional y no necesario para gráficos exigidos |
| scikit-learn | Pipeline, modelos, CV, tuning y métricas | API común; implementar solvers a mano agregaría errores sin requisito |
| scikit-image | Carga/transformación y HOG | Descriptores oficiales y reproducibles; OpenCV sería alternativa, no incorporar ambos sin necesidad |
| Jupyter | Entorno de exploración narrativa | Útil para EDA y estudio; scripts son alternativa y deben sostener la regeneración para evitar estado oculto |
| Git | Versionado de código/documentos/configuración | Historial y comparación; copias de carpetas no ofrecen trazabilidad equivalente |
| GitHub | Remoto oficial y revisión | Permite acceso a cátedra; ZIP sigue siendo alternativa de entrega admitida |
| venv | Aislamiento local de dependencias | Suficiente para stack CPU; conda sería alternativa si hubiera necesidad binaria concreta |
| SciPy, si se usa estadística | Dependencia científica que puede aportar prueba binomial/estadística | Declararla explícitamente si el código la importa; no agregar varias bibliotecas para un mismo contraste |
| pytest, en implementación | Herramienta de pruebas de contratos | Justifica su costo por controles de fuga, métricas y serialización; unittest es alternativa sin dependencia |

No se necesita TensorFlow o PyTorch para los candidatos clásicos; Docker o cloud no resuelven un requisito actual; una base de datos, frontend, API, MLflow o Kubernetes ampliarían el trabajo sin mejorar por sí mismos validez experimental. Los cuadernos no reemplazan módulos probados. Si surge una necesidad concreta, registrar decisión y costo antes de agregar tecnología.

# PARTE II · Conceptos complementarios fuera del experimento inicial

Estos conceptos ayudan a entender alternativas y responder preguntas. **No constituyen backlog, ablaciones programadas ni candidatos futuros comprometidos.** Ningún sprint activo los implementa por defecto.

| Concepto | Idea, utilidad y límite | Motivo para dejarlo fuera |
|---|---|---|
| LBP [E04] | Compara vecinos con un píxel central y agrega códigos como histograma de textura; sensible a escala, ruido y representación | HOG único evita comparar a la vez descriptor y clasificador |
| PCA [E10] | Aprende direcciones de máxima varianza sin etiquetas y proyecta en menos componentes; varianza no equivale a discriminación | Añade ajuste y puede eliminar señal. Solo reconsiderar por problema medido de memoria, tiempo, dimensionalidad o convergencia, con decisión explícita previa |
| KNN [E08] | Clasifica por vecinos cercanos; distancias dependen de escala y dimensión, e inferencia requiere comparar ejemplos | Ya hay dos candidatos y no hace falta sumar otra familia |
| Regresión logística [E09] | Sigmoide de w·x+b, log-loss y regularización; produce clasificación a partir de un umbral | Solapa referencia lineal con SVM; no habrá B1 |
| SVM RBF [E06] | Kernel exp(−gamma·distancia²), frontera no lineal y dependencia de vectores soporte | Añade gamma, búsqueda y costo; el núcleo fija SVM lineal |
| SHAP | Atribuye contribuciones según referencia y supuestos; no demuestra causalidad y puede ser costoso | Coeficientes/importancias simples cubren la explicación inicial |
| Wilcoxon [E19] | Rangos con signo de diferencias pareadas; requiere independencia y justificar simetría, ceros y empates | Cinco folds solapados no son cinco datasets independientes [E17] |
| 5×2cv [E18] | Cinco divisiones bipartitas con intercambio train/validation para determinados contrastes | Exigiría otro diseño y más entrenamientos; no se aplica a los cinco folds existentes |

PCA, si se autorizara por necesidad real en una revisión posterior, aprendería exclusivamente dentro del train de cada fold. Esta explicación no habilita implementarla ahora.

# Consulta y preguntas de defensa

Los términos complementarios del glosario no agregan tareas al alcance.

## Glosario de consulta rápida

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
| C1 / C2 | SVM lineal sobre HOG escalado / RF sobre HOG. |
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
| 37 | ¿GridSearch siempre es mejor que RandomizedSearch? | Nuestro espacio pequeño usa solo GridSearchCV; no garantiza óptimo global. | Búsqueda |
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
| 49 | ¿Por qué no usar SHAP siempre? | Está fuera del núcleo; coeficientes/importancias simples cubren el objetivo inicial. | Simplicidad |
| 50 | ¿Se comparó con varios médicos? | No: un profesional, 52 imágenes, tres indefinidas y 49 comparables. | Validación original |
| 51 | ¿75 % de acuerdo significa 75 % de diagnóstico correcto? | No; acuerdo y acierto frente a etiquetas son cantidades distintas. | Denominadores |
| 52 | ¿Es D4 una prueba de COVID frente a todas las enfermedades? | No: su clase negativa son pulmones normales. | Etiquetas y población |
| 53 | ¿Qué harían si faltan IDs de D4? | Declarar imposibilidad de réplica exacta y justificar alternativa; autorización de cátedra si sustituimos datos. | Comparabilidad |
| 54 | ¿Qué revela la omisión de /255 en anexo IV? | Inconsistencia del código publicado; no prueba que haya causado las cifras reportadas. | Evidencia y causalidad |
| 55 | ¿Qué medirían para afirmar menor costo? | Tiempos aproximados de extracción, búsqueda, ajuste e inferencia, tamaño y complejidad; RAM solo si es fácil medirla. | Benchmark |
| 56 | ¿Qué es data drift? | Cambio de distribución de entrada; no demuestra por sí solo caída de rendimiento. | Monitoreo |
| 57 | ¿Qué harían si otro modelo gana en test? | Informarlo sin cambiar selección; una revisión exigiría un nuevo protocolo/test independiente. | Test único |
| 58 | ¿Qué pasa si nadie supera la baseline? | Se reporta el resultado, se auditan fallos y se discuten límites sin inventar mejoras. | Integridad |
| 59 | ¿Cómo declaran uso de IA? | Herramienta/versión conocida, etapa, finalidad y verificación en el anexo exigido. | Autoría |
| 60 | ¿Qué se completó en esta etapa? | Lectura, investigación y planificación; ningún sprint ni entrenamiento propio. | Estado real |
