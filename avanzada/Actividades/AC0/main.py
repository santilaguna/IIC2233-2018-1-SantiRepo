# coding=utf-8

import abc
from collections import deque


class Ser(abc.ABC):
    def __init__(self, nombre, fuerza, resistencia, vida, *args, **kwargs):
        self.fuerza = fuerza
        self.resistencia = resistencia
        self.nombre = nombre
        self.vida = vida
        super().__init__()

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

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, value):
        if value < 0:
            self._vida = 0
        else:
            self._vida = value

    @abc.abstractmethod
    def atacar(self, *args, **kwargs):
        """Este método debe implementar un ataque capaz de dañar a otros seres,
        en vez de pass se puede sustituir por raise NotImplementedError"""
        pass

    def __repr__(self):
        return self.nombre


class Humano(Ser):

    def __init__(self, nombre, fuerza=0.4, res=0.6, vida=1000, int_=50,
                 multi_res=1.2, *args, **kwargs):
        self.inteligencia = int_
        self._multi_res = multi_res
        super().__init__(nombre, fuerza, res, vida, *args, **kwargs)

    @property
    def inteligencia(self):
        return self._inteligencia

    @inteligencia.setter
    def inteligencia(self, value):
        self._inteligencia = value

    def atacar(self, ataque, *args, **kwargs):
        ataque += (ataque * self.inteligencia / 100)
        return ataque

    def practicar(self):
        self.resistencia *= self._multi_res


class Extraterrestre(Ser):

    def __init__(self, nombre, fuerza=0.5, res=0.7, vida=500, multi_res=1.3,
                 *args, **kwargs):
        self._multiplicador_resistencia = multi_res
        super().__init__(nombre, fuerza, res, vida)

    def atacar(self, *args, **kwargs):
        self.aumentar_resistencia()

    def aumentar_resistencia(self, *args, **kwargs):
        self.resistencia *= self._multiplicador_resistencia


class Supersaiyayin(Extraterrestre, Humano):

    def __init__(self, nombre, ki=30, *args, **kwargs):
        super().__init__(nombre, vida=1000, *args, **kwargs)
        self.ki = ki
        self.cola = True

    @property
    def ki(self):
        return self._ki

    @ki.setter
    def ki(self, value):
        self._ki = value

    def atacar(self, personaje, *args, **kwargs):
        vida_inicial_enemigo = personaje.vida
        ataque = self.fuerza * (1 - personaje.resistencia)
        ataque = super().atacar(ataque, *args, **kwargs)
        personaje.vida -= ataque
        dif_vida = vida_inicial_enemigo - personaje.vida  #  en caso de matar
        print(f"{self} le quita {dif_vida} a {personaje}")

    def obtener_ki_externo(self, *personajes):
        self.ki += sum((0.7 * p.ki for p in personajes))

    def perder_cola(self):
        if self.cola:
            self.cola = False
            self.resistencia *= 0.4

    def practicar(self):
        print(f"Yo {self} estoy practicando")
        super().practicar()


class Hakashi(Extraterrestre):

    def __init__(self, nombre="Hernán", *args, **kwargs):
        super().__init__(nombre, *args, **kwargs)
        self.ki = 10
        self.bolas = deque()

    def atacar(self, personaje, *args, **kwargs):
        vida_inicial_enemigo = personaje.vida
        ataque = self.fuerza  * (1 - personaje.resistencia) / 2
        personaje.vida -= ataque
        super().atacar(*args, **kwargs)
        dif_vida = vida_inicial_enemigo - personaje.vida  #  en caso de matar
        print(f"{self} le quita {dif_vida} a {personaje}")

    def agregar_bola(self, bola):
        print("Encontré la", end=" ")
        bola()  # importante que llame a la bola, recomendar el uso de end=" ".
        self.bolas.append(bola)

    def usar_bolas(self):
        print(f"Yo {self} usaré las Bolas Del Código")
        while self.bolas:
            bola = self.bolas.popleft()
            self.fuerza += self.fuerza * 0.01 * bola.numero


class BolaDelCodigo:

    numero = 1

    def __init__(self):
        self.numero = BolaDelCodigo.numero
        BolaDelCodigo.numero += 1

    def __call__(self, *args, **kwargs):
        print(f"Bola Del Código número {self.numero}")


# instanciamos las clases que serán importadas..

popa = Hakashi("Popa")
johnny = Supersaiyayin("Johnny")
chaobug = Supersaiyayin("Chaobug")
billis = Hakashi("Billis")
bola1 = BolaDelCodigo()
bola2 = BolaDelCodigo()
bola3 = BolaDelCodigo()

supersaiyayin1 = chaobug
supersaiyayin2 = johnny
villano1 = billis
villano2 = popa
