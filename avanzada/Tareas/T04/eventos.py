# Módulo destinado a la modelamiento de los eventos externos al parque.

# Importar eventos directamente

import parameters as par
from random import expovariate, uniform


class Evento:

    def __init__(self, tiempo, dia, funcion, iteracion, descripcion,
                 afectados, entidad_generadora):
        """tiempo: tuple(int), funcion: class function, dia: str,
        iteracion: int, descrpción: str, afectados: str, generador: str
        """
        self.tiempo = tiempo
        self.dia = dia
        self._funcion = funcion
        self.iteracion = iteracion
        self.descripcion = descripcion
        self.afectados = afectados
        self.generador = entidad_generadora

    @property
    def str_tiempo(self):
        """retorna un string con el tiempo de ocurrencia del evento,
        de la forma hrs:minutos"""
        tiempo1 = str(self.tiempo[0])
        tiempo2 = str(int(self.tiempo[1]))
        if len(tiempo2) < 2:
            tiempo2 = "0" + tiempo2
        return tiempo1 + ":" + tiempo2

    def funcion(self):
        """ejecuta la funcion que contiene, esribe el log del evento en
        log.txt si es que el evento retorna True o False (existen acciones que
        ocurren en determinado momento pero no son eventos como tal).
        retorna None"""
        retorno = self._funcion()
        if retorno:
            self.escribir_log()

    def escribir_log(self):
        """escribe el log del evento, retorna None"""
        with open("log.txt", "a", encoding="utf-8") as file:
            log = "Iteración: {} | Día: {} | Tiempo: {} | Descripción evento:"\
                " {} | Entidades afectadas: {} | Entidad generadora: {} \n"
            file.write(log.format(self.iteracion, self.dia, self.str_tiempo,
                                  self.descripcion, self.afectados,
                                  self.generador))


class Lluvia(Evento):

    def __init__(self, *args, **kwargs):
        """tasa_lluvia: int
        dias_para_lluvia: float"""
        super().__init__(*args, **kwargs)
        self.tasa_lluvia = par.TASA_LLUVIA
        self.dias_para_lluvia = self.siguiente_lluvia

    @property
    def siguiente_lluvia(self):
        """retorna la cantida de dias en que ocurrirá la siguiente lluvia"""
        return int(expovariate(self.tasa_lluvia))

    def funcion(self):
        """realiza la función si no quedan días para lluvia, escribe  su log y
        reinicia el contador para la siguiente lluvia, de lo contrario resta un
         dia al contador"""
        if not self.dias_para_lluvia:
            self._funcion()
            self.escribir_log()
            self.dias_para_lluvia = self.siguiente_lluvia
        else:
            self.dias_para_lluvia -= 1


class DiaColegio(Evento):

    def __init__(self, *args, **kwargs):
        """dias_colegio: set(str)
        probabilidad: float"""
        super().__init__(*args, **kwargs)
        self.dias_colegio = par.DIAS_COLEGIO
        self.probabilidad = par.PROBABILIDAD_DIA_COLEGIO

    def funcion(self):
        """si es que el dia está entre los habilitados para dia colegio,
        existe cierta dprobabilidad de que se realice la función,
        retorna None"""
        if self.dia in self.dias_colegio:
            if uniform(0, 1) < self.probabilidad:
                self._funcion()
                self.escribir_log()


class Ruziland(Evento):

    def __init__(self, *args, **kwargs):
        """dias_ruziland: set(str)
        probabilidad: float"""
        super().__init__(*args, **kwargs)
        self.dias_ruziland = par.DIAS_RUZILAND
        self.probabilidad = par.PROBABILIDAD_INVASION

    def funcion(self):
        """si es que el dia está entre los habilitados para la invasión
        ruziland, existe cierta dprobabilidad de que se realice la función,
        retorna None"""
        if self.dia in self.dias_ruziland:
            if uniform(0, 1) < self.probabilidad:
                self._funcion()
                self.escribir_log()
