# Clasificación de radiografías de tórax con HOG

**Universidad Gastón Dachary · Ingeniería en Informática · Inteligencia Artificial II**

**Integrantes** Juan Quirós y Emanuel Andruszyszyn

El trabajo evalúa la clasificación de radiografías etiquetadas COVID o Normal con histogramas de gradientes orientados (HOG). Random Forest fue la propuesta inicial. Comparamos el bosque, SVM lineal y una regla mayoritaria en cinco folds de desarrollo y seleccionamos SVM lineal con C = 0,1 por su F1 macro medio. La CNN del TFC de Vega Lencina y Armoa es una referencia histórica de otra población y partición.

## Resultados en prueba reservada

| Modelo | F1 macro | Exactitud | Recall COVID | Especificidad |
|---|---:|---:|---:|---:|
| Dummy mayoritario | 0,4255 | 74,06 % | 0,00 % | 100,00 % |
| Random Forest | 0,7926 | 86,41 % | 53,36 % | 97,99 % |
| SVM lineal | 0,8719 | 89,93 % | 84,17 % | 91,95 % |

La prueba incluyó 2.752 radiografías. SVM detectó 220 imágenes COVID más que el bosque y produjo 123 falsos positivos adicionales. La independencia por paciente no pudo comprobarse. Los resultados describen un prototipo académico y la distinción entre estas dos clases de la base.

La [guía de reproducción](GUIA_REPRODUCCION.md) explica cómo instalar el entorno y reconstruir tablas y figuras a partir de la evidencia guardada. El [CSV final](results/metricas_test.csv) conserva las métricas sin redondear y el [informe de evaluación](reports/evaluacion.md) explica el protocolo, los errores y la comparación histórica.

El ZIP de entrega reúne el informe, la presentación, el código y la evidencia tabular. La base original se obtiene de la [ficha de Kaggle](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database/data).
