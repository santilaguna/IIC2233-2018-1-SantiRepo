# Tarea 4

Alumno: Santiago Laguna

## Instrucciones de uso o archivo principal a ejecutar para correr la tarea

El archivo principal corresponde al archivo main.py, desde este archivo se debe ejecutar la tarea.  
El programa asume que existen los siguientes archivos en la misma carpeta:

* arrivals.csv
* associations.csv
* attractions.csv
* restaurants.csv

Además crea un archivo “log.txt”, en caso de que este no exista. En caso de existir, añade la información de los eventos al final del archivo.

## Librerías utilizadas

* csv
* math
* random
* itertools
* collections
* faker

## Información útil para la corrección

Hay un error en la impresión de las estadísticas cuando se imprime el máximo tiempo en el que una atracción está fuera de servicio, pues se modifica erróneamente la fecha del llamado cuando el técnico revisa por su siguiente llamado

Salvo lo anterior, se implementó todo (al menos lo intenté), incluyendo los tres eventos externos.

## Información respecto a la implementación

El apellido de las personas está incluido en el nombre.

Cuando Nebiland (ParqueDeDiversiones), es una entidad afectada, en algunos eventos generales (como el cierre del parque) esto incluye a sus atracciones y las personas que permanecen al interior del recinto.

Si dos eventos ocurren en el mismo minuto, se escoge aleatoriamente que evento ocurre primero.

Para que el operador se pueda ir en paz a colación (cuando ocurren dos eventos al mismo tiempo), la duración real de los juegos es adelantada en 0.001 segundos

Cuando un grupo toma decisiones que están cercanas al cierre del parque y de da cuenta que no alcanzará a terminarlas intentará tomar otra decisión.

El tiempo se trunca al minuto cuando se imprime en el log, pero es calculado con decimales, por esto las estadísticas son más exactas.

Cuando un grupo se ve afectado (logs), significa que todos los clientes en él, niños y adultos (si los hay) se pueden ver afectados también.

El tiempo de ejecución es de 2-4 segundos por iteración (en mi pc de 2 gb ram).

Para las estadísticas de la atracción con más fallas se escoge a la atracción con mayor moda entre las atracciones que más fallaron de cada iteración.

Tiempos documentados que indican ser (int, int) pueden llegar a ser también (int, float).

Tiempos promedios en fila incluyen a aquellos que se quedan esperando por una limpieza, una reparación, etc.

Probabilidad de que un grupo escoga entre una fila que tiene 1 persona y otra que no tiene es la misma (con esto se busca evitar ZeroDivisionError)

## Supuestos realizados para la simulación

* La paciencia máxima de una persona es de 100 minutos y la minima de 3 minutos.
* La suciedad inicial es 0
* Paciencia de un cliente puede cambiar con el tiempo (no sólo debido a su energía, podría por ejemplo, estar de mal humor)
* Las edades de las personas se distribuyen de forma lineal
* Un grupo no puede entrar al parque si no se ha superado el limite de personas, pero al entrar todo el grupo si se superaría el límite. 
* Nadie se llama igual a otra persona en Nebiland
* Los operadores se toman una hora entera de colación exceptuando que se tomen la última hora del día, en cuyo caso pierden el tiempo de colación entre que comienza su hora escogida y las personas se bajan de la atracción de la que él esté a cargo. Si es portero, pues tiene suerte.
* Las unidades de tiempo siempre serán las mismas (no se requiere especificar que una hora tiene 60 minutos en parameters.py, por ejemplo)
* La cantidad de técnicos y limpiadores se aproxima hacia abajo (por la política de ahorro de nebiland)
* Se asume que nebiland tiene, al menos, una atracción (que clase de parque de diversiones no tiene atracciones)
* Los clientes saben si cumplen con los requisitos mínimos para las atracciones, por lo que si un miembro de un grupo no tiene la altura minima para subirse a un juego o no se puede pagar la entrada de todos, nunca intentarán hacer fila en esa atracción.
* Si un grupo llega a nebiland y no hay capacidad se retira del parque enojado (y se va a Ruziland)
* El tiempo mínimo de preparación de un plato es un minuto y el máximo es de 30 minutos.
* Si un grupo alcanza a repartirse los platos de comida, pero no alcanza a quedarse el tiempo_máximo en el restaurant porque el parque va a cerrar se preparan los platos y se van comiendo.
* Un grupo se retira de una fila si a cualquier miembro se le acaba la paciencia (porque va a estar insistiendo en irse claramente)
* Las atracciones cierran cuando el tiempo que que queda para que se cierre el parque es menor a la duración del juego más el tiempo de espera
* Cuando un grupo decide irse por falta de energía, se demora un minuto en llegar a la puerta
* Como la atracción ingresa a los jugadores a medida que van llegando a la fila, cuando el juego no ha partido, si un grupo decide irse por paciencia, este se baja del juego si no ha comenzado.
* El operador revisa el nivel de suciedad de su atracción después de que los clientes se bajen de esta.
* Tiempo mínimo de falla es de un minuto
* Los eventos externos ocurren durante todo el día
* Los grupos que lleguen y se encuentren con que el parque esta invadido por su archienemigo, pueden decidir si ser cuidadosos o no.
* Cuando un niño se quiere ir en un día reservado para un colegio,  su profesor llama a su apoderado, pues los profesores se deben quedar cuidando al resto de los niños hasta que cierre el parque.
* Los profesores se quedan conversando entre ellos hasta que un niño le pide que le pague su comida, se quedan con ellos hasta que terminen de comer y luego se devuelven a conversar si es que no llega otro niño.
* No se considera en la capacidad de Nebiland a los operadores, además tampoco se consideran las personas que sabemos que no se subirán a ninguna atracción (ni lo intentarán).
* Se cobra a los grupos a medida que se van de las instalaciones.

## Resumen modularización y aspectos generales

### Entidades

Todo lo referente a las Personas, está implementado en el módulo personas.py. Mientras que  lo relacionado con las Instalaciones, se implementa en el módulo instalaciones.py

### Eventos externos al parque

Los eventos externos al parque están implementados en el módulo eventos.py.

### Registro de eventos

Todo el registro de eventos es llevado a cabo por la clase Evento (módulo eventos.py), además las acciones realizadas durante la simulación se imprimen o no dependiendo de si son una acción como tal o son situaciones que deben ser evaluadas en determinado momento. Para esto las funciones que se le entregan a los eventos tienen un boleado, de forma que sea de fácil acceso en caso de querer revisar cierta información

### Base de datos

El manejo de archivos es realizado en el módulo cargar_archivos.py

### Estadísticas

Para todo el manejo de esta información se implementó la clase Estadísticas, en el módulo estadísticas.py.

### Parámetros

El manejo de los parámetros es realizado en el módulo parameters.py

### Generar datos, documentación y requisitos

La generación de datos es aleatoria y es realizada por los métodos de cada clase (principalmente Persona de personas.py). 

La documentación es especificada como doctrina en cada función y en algunos casos específicos se añaden hashtags(#) explicativos. 

Los requisitos de properties y moderación de la realidad son implementados a lo largo de todo el programa, según se consideró necesario.
