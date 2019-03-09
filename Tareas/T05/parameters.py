# módulo destinado a escribir los parámetros del juego.

# velocidad de movimiento del personaje principal.
VEL_MOVIMIENTO = 5

# cantidad de vidas del personaje principal.
CANT_VIDAS = 3

# tiempo en segundos que demora una bomba en explotar.
TIEMPO_EXPLOSION = 5

# tiempo en segundos que debe transcurrir para recibir puntos por tiempo.
TIEMPO = 60

# cantidad de puntos otorgados por sobrevivir cierta cantidad de tiempo.
PUNTAJE_TIEMPO = 200

# cantidad de puntos recibidos por enemigo eliminado.
PUNTAJE_ENEMIGO = 50

# puntaje otorgado por destruir un muro.
PUNTAJE_MURO = 20

# puntaje necesario para que ocurra un aumento en la dificultad.
AUMENTO_DIFICULTAD = 1000

# rango de visión que tendrán los enemigos.
RANGO_VISION = 100

# tiempo inmune al rango de visíon y daño luego de ser dañado por un enemigo.
TIEMPO_INMUNE = 2

# distribución del tiempo de aparición de enemigos no hostiles.
A_NO_HOSTIL = 5
B_NO_HOSTIL = 10

# distribución del tiempo de aparici ́on de enemigos hostiles.
LAMBDA_HOSTIL = 0.1

# tamaño (en pixeles) de la grilla que corresponde al mapa (no la ventana),
# se recomienda un mininmo de 500 dados los tamaños de los objetos.
N = 750

# considerar que tamaño de jugador es de 22x35 pixeles.
# tamaño del mapa (se asume n x n) no puede ser cero.
MAPA_SIZE = 15

# rango de casillas de la explosión de las bombas.
RANGO_EXPLOSION = 2

# cantidad de vidas que tendrán los enemigos.
VIDAS_ENEMIGOS = 1

# cantidad de enemigos hostiles iniciales.
HOSTILES_INICIALES = 1

# cantidad de enemigos comunes iniciales.
COMUNES_INICIALES = 2

# distancia mínima de aparación de los enemigos en pixeles respecto
# del centro de un jugador y el centro de una casilla vacia.
DISTANCIA_MINIMA = 150

# Nivel inicial de dificultad.
NIVEL_DIFICULTAD = 0
