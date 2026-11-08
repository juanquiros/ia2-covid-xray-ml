# Guía de práctica para la defensa

## Distribución sugerida de la exposición

| Tramo | Diapositivas | Expositor | Tiempo orientativo |
|---|---|---|---:|
| Problema, TFC y población | 1–3 | Juan Quirós | 4 min |
| HOG, folds y selección | 4–5 | Juan Quirós | 3 min |
| Prueba, errores y pesos | 6–8 | Emanuel Andruszyszyn | 6 min |
| Alcance y cierre | 9 | Emanuel Andruszyszyn | 2 min |

Cada integrante practica las dos partes y responde preguntas sobre el trabajo completo. La consigna propone un bloque de preguntas de diez minutos.

## Preguntas de práctica

1. **¿Por qué elegimos por F1 macro?** La clase Normal es mayoritaria. Dummy obtiene 74,06 % de exactitud reservada al predecir siempre Normal y tiene recall COVID cero. F1 macro pondera los F1 de ambas clases por igual.
2. **¿Dónde se ajusta StandardScaler?** Dentro del pipeline y con el entrenamiento de cada fold. La validación se transforma con esas estadísticas. En el reajuste final el escalador usa todo desarrollo, con la prueba separada.
3. **¿Para qué sirve reservar el test?** Permite estimar el resultado de un procedimiento que ya fijó modelo, comparadores, métricas y umbrales. Reconstruir la matriz de confusión a partir del CSV no vuelve a abrir las imágenes ni reevalúa el modelo.
4. **¿Es válida una comparación directa con la CNN?** El 79,47 % se obtuvo en 492 imágenes de D4 balanceadas y depuradas manualmente. La prueba propia tiene 2.752 imágenes y aproximadamente 26 % COVID. También difieren la partición y el criterio de selección. La comparación es histórica.
5. **¿Qué se gana y qué se pierde con SVM frente a Random Forest?** Detectó 220 radiografías COVID más, con 123 falsos positivos adicionales. El F1 macro fue 0,8719 frente a 0,7926. El bosque conservó mayor especificidad.
6. **¿Qué muestra el gráfico de pesos HOG?** La norma conjunta de los coeficientes de un bloque sobre características estandarizadas. Agrega signos y orientaciones y no explica una imagen individual. Los pesos en los bordes permiten plantear la hipótesis de atajos.
7. **¿Por qué omitimos McNemar?** Hay predicciones pareadas por imagen, pero faltan IDs fiables para comprobar independencia entre pacientes. Los desacuerdos se informan como conteos descriptivos.
8. **¿Qué se necesita para repetir los cálculos?** Las etiquetas y predicciones de los tres modelos, los puntajes de los candidatos y los folds de desarrollo. El ZIP permite correr la guía sin radiografías.
9. **¿Qué exigiría considerar un uso real?** Validación externa con grupos por paciente, más patologías, revisión profesional, criterios de abstención y monitoreo. Una versión reentrenada tendría que pasar otra evaluación independiente.

## Ejercicio de exposición

Cada integrante explica en voz alta el paso de gradientes a 8.100 atributos, reconstruye el recall de SVM como 601/714 e interpreta por separado el 89,93 % propio y el 79,47 % histórico. En la segunda vuelta, el otro integrante pregunta dónde se ajusta el escalador y qué ocurriría si se eligiera un nuevo umbral a partir de la curva de prueba.
