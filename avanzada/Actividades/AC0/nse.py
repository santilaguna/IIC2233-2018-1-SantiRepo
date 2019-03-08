# coding=utf-8

import abc
from  collections import deque


class Humano(metaclass=abc.ABCMeta):

    def __init__(self, nombre, multi=1.15, int=0.5):
        self.nombre = nombre
        self._inteligencia = int
        self._multiplicador_inteligencia = multi

    @property
    def inteligencia(self):
        return self._inteligencia

    @inteligencia.setter
    def inteligencia(self, value):
        self._inteligencia = value

    @abc.abstractmethod
    def atacar(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def aumentar_inteligencia(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class Extraterrestre(metaclass=abc.ABCMeta):

    def __init__(self, multi_res=1.2, multi_fuerza=1.25, res=0.6, fuerza=0.4):
        self._fuerza = fuerza
        self._multiplicador_fuerza = multi_fuerza
        self._resistencia = res
        self._multiplicador_resistencia = multi_res

    @property
    def fuerza(self):
        return self._fuerza

    @fuerza.setter
    def fuerza(self, value):
        self._fuerza = value

    @property
    def resistencia(self):
        return self._resistencia

    @resistencia.setter
    def resistencia(self, value):
        self._resistencia = value

    @abc.abstractmethod
    def atacar(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def aumentar_resistencia(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def aumentar_fuerza(self, *args, **kwargs):
        raise NotImplementedError


class Supersaiyayin(Humano, Extraterrestre):

    def __init__(self, nombre):
        super().__init__(nombre)
        self._vida = 1000
        self._ki = 10

    @property
    def ki(self):
        return self._ki

    @ki.setter
    def ki(self, value):
        self._ki = value

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, value):
        if value < 0:
            self._vida = 0
        else:
            self._vida = value


    def atacar(self, personaje):
        ataque = (self.fuerza * personaje.vida *
                           (1 - personaje.resistecia))
        personaje.vida -= ataque + (ataque * 0.1 * self.inteligencia)
        self.aumentar_fuerza()
        self.aumentar_inteligencia()
        self.aumentar_resistencia()

    def aumentar_resistencia(self):
        self.resistencia *= self._multiplicador_resistencia

    def aumentar_fuerza(self, *args, **kwargs):
        self.fuerza *= self._multiplicador_fuerza

    def aumentar_inteligencia(self, *args, **kwargs):
        self.inteligencia *= self._multiplicador_inteligencia

    def obtener_ki_externo(self, personajes):
        self.ki += sum((0.7 * p.ki for p in personajes))

    def genkidama(self, personaje):
        personaje.vida -= (self.fuerza * personaje.vida * self.ki * 0.01)
        self.ki = 0

    def __call__(self, *args, **kwargs):
        print("Yo {} estoy practicando".format(self.nombre))
        self.ki += 10


# puede ser o no abstracta.
class Villano:

    def __init__(self):
        self._vida = 500
        self._ki = 30
        self.bolas = deque()
        self.nombre = None
        self.fuerza = 0.2

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, value):
        if value < 0:
            self._vida = 0
        else:
            self._vida = value

    def agregar_bola(self, bola):
        print("Encontré la", end=" ")
        bola()  #importante que llame a la bola, recomendar el uso de end=" ".
        self.bolas.append(bola)

    def usar_bolas(self):
        print("Yo {} usaré las Bolas Del Código".format(self.nombre))
        while self.bolas:
            bola = self.bolas.popleft()
            self.fuerza += self.fuerza * 0.01 * bola.numero


class VillanoHumano(Humano, Villano):

    def __init__(self, nombre):
        self._vida = 500
        self.resistencia = 0.3 # muy importante que pongan este atributo,
        # funciona igualmente si lo ubican en villano.
        super().__init__(nombre, multi=1.1, int=0.2)

    def atacar(self, personaje):
        ataque = (self.fuerza * personaje.vida *
                  (1 - personaje.resistecia))
        personaje.vida -= ataque + (ataque * 0.1 * self.inteligencia)
        self.aumentar_inteligencia()

    def aumentar_inteligencia(self, *args, **kwargs):
        self.inteligencia *= self._multiplicador_inteligencia

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class VillanoExtraterrestre(Villano, Extraterrestre):

    def __init__(self):
        super().__init__(multi_fuerza=1.3, multi_res=1.15, res=0.3, fuerza=0.2)
        self.nombre = "Hernán"

    def atacar(self, personaje):
        ataque = (self.fuerza * personaje.vida *
                  (1 - personaje.resistecia)/2)
        personaje.vida -= ataque
        self.aumentar_fuerza()
        self.aumentar_resistencia()

    def aumentar_resistencia(self):
        self.resistencia *= self._multiplicador_resistencia

    def aumentar_fuerza(self, *args, **kwargs):
        self.fuerza *= self._multiplicador_fuerza


class BolaDelCodigo:
    numero = 1
    def __init__(self):
        self.numero = BolaDelCodigo.numero
        BolaDelCodigo.numero += 1
        self.color  = "naranjo"

    def __call__(self, *args, **kwargs):
        print("Bola Del Código número {}, color {}".format(self.numero,
                                                           self.color))
