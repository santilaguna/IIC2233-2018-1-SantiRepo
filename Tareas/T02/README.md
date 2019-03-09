# Tarea 2


## Instrucciones de uso o archivo principal a ejecutar para correr la tarea

El archivo principal corresponde al archivo Demo.py, que esta ubicado dentro de GUI, desde este archivo se debe ejecutar la tarea. 

Se espera que exista el archivo players_db.csv

Luego de jugar un campeonato para ver los resultados, se debe consultar por los ganadores.

## Librerías utilizadas

* random
* PyQt5
* math

## Información útil para la corrección

Debido a que no existía una forma de interactuar desde la interfaz con las consultas sobre el grado de afinidad estas están implementadas para ser evaluadas desde la consola y están  escritas donde se indica más abajo.

## Afinidad entre jugadores

Para el cálculo de la afinidad entre jugadores se realiza un grado de afinidades, en el módulo grafo_relaciones.py. Este grado tiene como nodos jugadores que a su vez tienen como conexiones los ID de aquellos jugadores con grado uno de relación.

La existencia de relaciones entre dos jugadores y el valor de esta relación se implementa en el módulo jugador.py

El cálculo de la afinidad entre dos jugadores no relacionados se calcula en el módulo grafo_relaciones.py en el método afinidad.

Las consultas y estadísticas del grado de afinidad están implementadas en el módulo grafo_relaciones.py (últimos métodos de Relaciones) -mejor_amigo -peor_amigo -popular -fichaje_estrella 

## Campeonato

El campeonato esta implementado en el módulo torneo.py, que es un árbol binario cuyos nodos son partidos (mismo módulo), que contienen dos equipos (módulo equipo.py) que se enfrentan cuando se llama a jugar_partido (método de Partido) desde simular_torneo (método de Torneo)

Al momento de simular un campeonato desde Demo.py se genera una instancia de Torneo y se arma el árbol a través del método cargar_equipos de Torneo.

Los equipos comienzan en octavos de final y juegan eliminatorias y suben en el árbol solo si ganan. En la semifinal, los perdedores juegan el tercer y cuarto lugar, que es un Partido aparte (se considera que estos perdieron en la semifinal para las estadísticas de fase)

Los partidos se simulan con el método de Partido jugar_partido, donde también ocurren los eventos de los partidos. En este mismo nodo se guardan las estadísticas del partido para ser consultadas más tarde.

Las consultas de los partidos se ejecutan desde Demo.py desde aquí se ejecutan dos métodos de Torneo según la consulta, buscar_partido (según su ID) e info_equipo (según su nombre).

## GUI

Todos los métodos para interactuar con la GUI se implementan en Demo.py

## Base de datos

Para llamar a la base de datos se utiliza el módulo cargar_archivos.py, además en este se define una Clase Str que hereda de str para que el comando split() genera una Listirijilla  en vez de la lista built-in de Python.

## Hackerman

Las estructuras de datos están implementadas en mis_estructuras.py
En esta se encuentran las siguientes clases:
Node -> nodo de Listirijilla
Iterator -> iterarador de Listirijilla
Listirijilla -> lista ligada con funcionalidad similares a la lista de Python
SamePlyaerError -> excepción
NotConectedError -> excepción
HashTable -> tabla de hash que asume hash perfecto tiene 0(n) por lo que es poco eficiente

## Información respecto a la implementación

El archivo .gitignore esta implementado dentro de GUI, lo anterior, se debe a que no se logró solucionar el problema con la interfaz al ejecutar Demo.py desde afuera de la carpeta GUI, por lo que se realiza de esta forma según lo indicado.

Para reducir el tiempo de búsqueda de afinidades entre jugadores no relacionados (de 2 minutos a unos segundos en los peores casos) se considera que los jugadores más distantes estarán a 5 aristas de distancia (mencionado en las issues)

