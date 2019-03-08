# Tarea 1


## Instrucciones de uso o archivo principal a ejecutar para correr la tarea

El archivo principal corresponde al archivo main.py, desde este archivo se debe ejecutar la tarea. Sin embargo, se espera que existan los archivos planeta.csv y galaxia.csv y que éstos, estén en la misma carpeta (con al menos el header), de lo contrario el juego se inicia desde cero.

Al momento de jugar, para seleccionar una opción debe escribir el número de la acción que desea realizar, o bien (cuando se especifique) escribir el nombre del planeta o galaxia seleccionado.


## Librerías utilizadas

* datetime
* copy
* collections
* random
* abc
* math


## Información útil para la corrección

**Las funcionalidades del juego están en implementadas en el módulo chaucraft.py**

### Clase galaxia

Planetas de todas las galaxias: módulo galaxia.py, linea 15

Planetas de la galaxia: módulo galaxia.py,linea 21

Reserva de minerales galaxia: módulo galaxia.py, linea 23

Reserva de deuterio galaxia: módulo galaxia.py linea 24

Crear planetas: módulo galaxia.py, linea 58

Modificar planeta:  módulo galaxia.py, linea 86

Conquistar planeta (batalla):  módulo galaxia.py, linea 187

Destruir planeta:  módulo galaxia.py, linea 76

### Clase Planeta

El nombre(id) del planeta es utilizado como llave en los diccionarios de la clase Galaxia que contienen como valor una instancia de Planeta: módulo galaxia.py, lineas 15 y 21

Raza planeta: módulo planetas.py, linea 14

Soldados planeta: módulo planeta.py, lineas 15, 75, 79 (largo para cantidad)

Magos planeta: módulo planeta.py, lineas 16, 95, 99 (largo para cantidad)

Población máxima: módulo planeta.py, linea 17

Tasa_minerales: módulo planeta.py, lineas 22, 57, 61

Tasa_deuterio: módulo planeta.py, lineas 23, 66, 70

Última recolección: módulo planeta.py, linea 24

Nivel ataque: módulo planeta.py, linea 19

Nivel economía: módulo planeta.py, linea 18

Conquistado: módulo planeta.py, linea 25

Edificios: módulo planeta.py, lineas 26, 27

Evolución: módulo planeta.py, linea 47

### Otras clases

Grito de guerra raza: módulo clases.py, linea 24

Boost victoria: módulo funciones_especificas.py, linea 210

**Maestro**

Población: módulo clases.py, linea 109

Costo soldado: módulo clases.py, lineas 110, 111

Costo mago: módulo clases.py, lineas 112, 113

Ataque soldados: módulo clases.py, linea 116

Ataque magos: módulo clases.py, linea 124

Vida soldados: módulo clases.py, linea 120

Vida magos: módulo clases.py, linea 128

Habilidad: módulo clases.py, linea 131

Grito de guerra: módulo clases.py, linea 141

**Asesino**

Población: módulo clases.py, linea 36

Costo soldado: módulo clases.py, lineas 37, 38

Ataque soldados: módulo clases.py, linea 41

Vida soldados: módulo clases.py, linea 45

Habilidad: módulo clases.py, linea 48

Grito de guerra: módulo clases.py, linea 60

**Aprendiz**

Población: módulo clases.py, linea 69

Costo soldado: módulo clases.py, lineas 70,71

Ataque soldados: módulo clases.py, linea 74

Vida soldados: módulo clases.py, linea 78

Habilidad: módulo clases.py, linea 84

Grito de guerra: módulo clases.py, linea 100


**Edificios: módulo clases.py linea 11**

**Soldado: módulo clases.py linea 16**

**Mago: módulo clases.py linea 17**

### Funcionalidades del programa
Crear galaxia: módulo chaucraft.py, linea 42

Modificar galaxia:  módulo chaucraft.py, linea 65. Módulo galaxia.py, linea 86

Consultas sobre galaxias:  módulo chaucraft.py, lineas 74, 92, 104, 133. -> módulo
funciones_especificas, linea 97

Jugar en la galaxia:  módulo chaucraft.py, linea 146

Batalla: módulo galaxia.py, linea 189

Eventos:  módulo chaucraft.py, linea 154 ->  módulo galaxia.py, linea 169

### Validación de Input y consola
En el módulo funciones_utiles.py se detalla lo referente a validación de input, junto a otras funciones genéricas.

### Base de datos
Se destina el módulo main.py para cargar el programa

Actualizar datos:  módulo chaucraft.py, linea 197

### Información respecto a la implementación
En este juego el archimago puede morir, en cuyo caso su hijo lo reemplaza y pasa a ser el nuevo archimago.

En caso de que el archimago venza a el último planeta conquistado, este planeta en vez de dejar de estar conquistado, pierde todo el avance que tenía hasta ese momento es decir, muere su ejército, pierde sus edificios y pierde sus niveles de desarrollo. Lo anterior, tiene el fin de que la galaxia no quede inutilizable.

El boost de los soldados y magos al conquistar un planeta se ve limitado por su rango de seteo inicial.

Para la elección de nombres tanto para galaxias como para planetas, se aceptan todos los caracteres que acepte utf-8 incluyendo espacios, a menos que se especifique lo contrario.

Las galaxias deben tener como mínimo un planeta, por lo que se asume que el archivo planeta.csv tendrá al menos un planeta por galaxia en el archivo galaxias.csv.
 

