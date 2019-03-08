# Módulo destinado a implementar las clases de razas y otras clases pequeñas

# importar como cl

import funciones_utiles as fu
from random import randint
from collections import namedtuple
from abc import ABCMeta, abstractmethod
from math import inf

Edificio = namedtuple("Building_type",
                      ["costo_mineral", "costo_deuterio", "ataque", "vida"])
# torre = Edificio(150, 300, 1000, 2000)
# cuartel = Edificio(200, 500, 0, 5000)

Soldado = namedtuple("Soldier_type", ["ataque", "vida"])
Mago = namedtuple("Magician_type", ["ataque", "vida"])


# clase abstracta raza
class Raza(metaclass=ABCMeta):

    # Grito de guerra
    def __call__(self):
        print("Wubba Lubba Dub Dub, hemos logrado conquistar un "
              + "nuevo planeta", end=" ")

    @abstractmethod
    def habilidad(self, dato):
        raise NotImplementedError


class Asesino(Raza):

    def __init__(self):
        self.capacidad = 400  # población máxima por planeta
        self.costo_mineral_soldados = 100
        self.costo_deuterio_soldados = 200

    @property
    def ataque_soldados(self):
        return randint(40, 45)

    @property
    def vida_soldados(self):
        return randint(250, 270)

    def habilidad(self, ataque):
        if fu.probabilidad(40):
            print("Se activa la habilidad de Asesino para atacar doble")
            return ataque * 2
        return ataque

    def __str__(self):
        return "Asesino"

    def __call__(self):
        super().__call__()
        print("¡El poder de las sombras es lo único necesario para ganar "
              + "estas batallas!")


class Aprendiz(Raza):

    def __init__(self):
        self.capacidad = 150  # población máxima por planeta
        self.costo_mineral_soldados = 300
        self.costo_deuterio_soldados = 400

    @property
    def ataque_soldados(self):
        return randint(30, 60)

    @property
    def vida_soldados(self):
        return randint(600, 700)

    def __str__(self):
        return "Aprendiz"

    def habilidad(self, minerales=inf):
        if fu.probabilidad(70):
            print("Se activa la habilidad de Aprendiz para robar minerales")
            if minerales >= 200:
                minerales -= 200
                return 200
            else:
                robado = minerales
                minerales -= robado
                print("La reserva se ha quedado sin minerales")
                return robado
        return 0

    def __call__(self):
        super().__call__()
        print("¡Con una gran defensa y medicinas, nuestros soldados "
              + "son invencibles!")


class Maestro(Raza):

    def __init__(self):
        self.capacidad = 100  # población máxima por planeta
        self.costo_mineral_soldados = 200
        self.costo_deuterio_soldados = 300
        self.costo_mineral_magos = 300
        self.costo_deuterio_magos = 400

    @property
    def ataque_soldados(self):
        return randint(60, 80)

    @property
    def vida_soldados(self):
        return randint(200, 250)

    @property
    def ataque_magos(self):
        return randint(80, 120)

    @property
    def vida_magos(self):
        return randint(150, 200)

    def habilidad(self, poblacion):
        if fu.probabilidad(30):
            print("Los maestros usan su habilidad para matar a la mitad del"
                  + "ejército enemigo")
            return int(poblacion//2)
        return poblacion

    def __str__(self):
        return "Maestro"

    def __call__(self):
        super().__call__()
        print("¡Nuestro conocimiento nos ha entregado una victoria más!")


class Archimago(Asesino, Aprendiz):

    def __init__(self):
        self.vida = 10000
        self.ataque = 400
        self.vivo = True

    def habilidad(self, minerales=inf):
        Aprendiz().habilidad(minerales)
        return Asesino().habilidad(self.ataque)


class Asteroide:

    @property
    def ataque(self):
        return randint(1500, 2500)

    def impactar(self, impacto):
        impacto(self.ataque)
        pass
