# Tarea 3

## Instrucciones de uso o archivo principal a ejecutar para correr la tarea

El archivo principal corresponde al archivo main.py, desde este archivo se debe ejecutar la tarea. 

Por defecto, el programa carga todos los archivos utilizados para el testing, éstos se pueden cambiar de TestingDatabase a Database (o cualquier otro). Los path a cambiar se encuentran en:

**Módulo preprocesamiento.py:**

Línea 45 -> reader=“Database/reviews.csv”

**Módulo base_de_datos.py:**

Línea 29 -> path=“Database/movies.csv”

Línea 35 -> path=“Database/genres.csv”

Línea 48 -> path=“Database/actors.csv”

Línea 59 -> path=“Database/actors.csv”


## Librerías utilizadas

**se incluyen las librerías utilizadas por los ayudantes en main.py**

* sys
* PyQt5
* collections
* cdv
* itertools
* types
* re
* unittest
* os


## Información útil para la corrección

El código presenta un error debido a que el testing fue realizado sólo con consultas buenas =(, para correr el programa sin provocar errores (y evaluar el resto de las funcionalidades con mayor facilidad), sólo se necesitan agregar las siguientes líneas en main.py:

líneas 18-19-20 (18 con la misma identación de la línea anterior)

```python
if isinstance(results[n], Exception):
    self.add_answer(str(results[n]) + "\n")
    continue
```

Líneas 50-51-52 (50 con la misma identación de la línea anterior, después de agregar líneas anteriores)

```python
if isinstance(queries_answers[n], Exception):
    self.add_answer(str(queries_answers[n]) + "\n")
    continue
```

## Preprocesamiento

Al iniciar el programa se realiza un preprocesamiento de los comentarios para eliminar los comentarios del bot en preprocesamiento.py y se escribe un archivo (por defecto clean_reviews.csv) de donde se leerán las consultas después. 

## Lectura de archivos

Para la lectura de los archivos se utilizan las librerías csv y functools, el módulo base_de_datos.py es el encargado de trabajar con los archivos que luego serán utilizados por la librería.

## Comentarios y procesamiento

En el módulo base_de_datos.py, además de cargar los comentarios (desde clean_reviews.csv),  se trabaja con éstos y se procesan para clasificarlos cuando se consulta por best_comments.

## Consultas

Todas las consultas son procesadas en el módulo libreria.py:

* load_database línea 147
* filter_by_date línea 152
* popular_movies línea 165
* best_comments línea 175
* take_movie_while línea 190
* popular_genre línea 205
* popular_actors línea 221
* highest_paid_actors línea 238
* successful_actors línea 252

**El resto de las funciones de la librería sirven de ayuda para procesar las queries**

## Excepciones

En el módulo excepciones.py son implementadas las 3 excepciones pedidas, que son levantadas en la librería según corresponda.

## Testing

En el módulo testing.py se implementan los test de las queries . Por defecto las base de datos lee los archivos de TestingDatabase. La carpeta TestingDatabase es una modificación MiniDatabase para obtener los resultados de los test con mayor facilidad (que fueron obtenidos manualmente).

## Información respecto a la implementación

Para la pregunta take_movie_while se asume (guiándose por el ejemplo) que la forma de preguntar por las columnas es la siguiente:

* ”RT" -> rating_rt
* "Rotten Tomatoes" -> rating_rt
* "IMDb" -> rating_imdb"
* "Internet Movie Database" -> rating_imdb
* "Metacritic" -> rating_metacritic
* ”MC" -> rating_metacritic
* "date" -> date
* "box_office" -> box_office

Para la pregunta best_comments, la popularidad se calcula según la issue 367 y se ordena según lo indicado en la issue 465. Además el valor n se utiliza como límite máximo, es decir, si existen menos películas que cumplan con los requisitos se entregarán sólo esas, incluso ninguna.

En los casos de las preguntas en que se deba ordenar algún dato según algún valor y dos datos tengan el mismo valor, se ordenan de forma aleatoria. Por esto, en algunos casos específicos, se podría tener dos respuestas distintas para la misma pregunta.

El archivo .gitignore sólo restringe los archivos especificados en el enunciado, es decir, los archivos de la carpeta Gui y los archivos csv de Database. Además se asume que estos archivos existirán. Todos los archivos subidos son necesarios para realizar los testing.


