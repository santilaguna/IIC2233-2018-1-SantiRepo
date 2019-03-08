# Módulo destinado a implementar la clase planeta

# importar como pl

import funciones_especificas as fe
from datetime import datetime
from clases import Soldado, Mago, Maestro, Edificio
from random import randint


class Planeta:

    def __init__(self, raza):
        self.raza = raza
        self.__soldados = []
        self.__magos = []
        self.capacidad = fe.capacidad(str(self.raza))  # Población máxima
        self.nivel_economia = 0
        self.nivel_ataque = 0
        tasam = randint(1, 10)
        tasad = randint(5, 15)
        self.__tasa_minerales = tasam  # * self.economia()
        self.__tasa_deuterio = tasad  # * self.economia()
        self.ultima_recoleccion = datetime.today()
        self.conquistado = False
        self.torre = None
        self.cuartel = None
        self._poblacion = 0

    @property
    def poblacion(self):
        self._poblacion = len(self.soldados) + len(self.magos)
        return self._poblacion

    @poblacion.setter
    def poblacion(self, value):
        if value == len(self.soldados) + len(self.magos):
            return
        elif value < len(self.soldados) + len(self.magos):
            while (len(self.soldados) + len(self.magos)) > value:
                if self.__magos:
                    self.__magos.pop()
                else:
                    self.__soldados.pop()
            self._poblacion = value
        else:
            raise ValueError

    @property
    def evolucion(self):
        valor = self.nivel_economia + self.nivel_ataque
        valor += ((len(self.magos) + len(self.soldados)) / self.capacidad)
        if self.cuartel:
            valor += 1
        if self.torre:
            valor += 1
        return round(valor, 1)

    @property
    def tasa_minerales(self):
        return self.__tasa_minerales

    @tasa_minerales.setter
    def tasa_minerales(self, value):
        if value in range(0, 11):
            self.__tasa_minerales = value

    @property
    def tasa_deuterio(self):
        return self.__tasa_deuterio

    @tasa_deuterio.setter
    def tasa_deuterio(self, value):
        if value in range(5, 16):
            self.__tasa_deuterio = value

    @property
    def soldados(self):
        return self.__soldados

    @soldados.setter
    def soldados(self, value):
        # setter para batalla y modificar galaxia
        # value debe ser soldados finales que queremos que tenga tipo int
        largo_inicial = len(self.soldados) + 1
        largo_maximo = self.capacidad + 1 - len(self.magos)
        if value < len(self.soldados):
            while len(self.soldados) > value:
                self.__soldados.pop()
        else:
            if value in range(largo_inicial, largo_maximo):
                for soldado in range(value - largo_inicial + 1):
                    nuevo_soldado = Soldado(
                        self.raza.ataque_soldados, self.raza.vida_soldados)
                    self.__soldados.append(nuevo_soldado)

    @property
    def magos(self):
        return self.__magos

    @magos.setter
    def magos(self, value):
        # setter para batalla y modificar galaxia, value tipo int
        largo_inicial = len(self.magos) + 1
        largo_maximo = self.capacidad + 1 - len(self.soldados)
        if value < len(self.magos):
            while len(self.magos) > value:
                self.__magos.pop()
        elif isinstance(self.raza, Maestro):
            if value in range(largo_inicial, largo_maximo):
                for mago in range(value - largo_inicial + 1):
                    nuevo_mago = Mago(
                        self.raza.ataque_magos, self.raza.vida_magos)
                    self.__magos.append(nuevo_mago)

    def economia(self):
        if self.nivel_economia == 0:
            return 1
        elif self.nivel_economia == 1:
            return 1.2
        elif self.nivel_economia == 2:
            return 1.5
        else:
            return 2

    def ataque(self):
        if self.nivel_ataque == 0:
            return 1
        elif self.nivel_ataque == 1:
            return 1.2
        elif self.nivel_ataque == 2:
            return 1.5
        else:
            return 2

    def impacto_asteroide(self, ataque_asteroide):
        cantidad_soldados = len(self.soldados)
        cantidad_magos = len(self.magos)
        self.soldados = int(cantidad_soldados // 2)
        self.magos = int(cantidad_magos // 2)
        if self.torre:
            print("El asteroide ha dañado a tu torre")
            self.torre = self.torre._replace(vida = self.torre.vida
                                                    - ataque_asteroide)
            if self.torre.vida < 1:
                print("Tu torre ha quedado inutilizable")
                self.torre = None
        if self.cuartel:
            print("El asteroide ha dañado a tu cuartel")
            self.cuartel = self.cuartel._replace(vida = self.cuartel.vida
                                                    - ataque_asteroide)
            if self.cuartel.vida < 1:
                print("Tu cuartel ha quedado inutilizable")
                self.cuartel = None

    def invasion_archimago(self, archimago, minerales):
        # si el archimago muere da a luz un hijo
        vida_planeta = sum((soldado.vida for soldado in self.soldados))
        vida_planeta += sum((mago.vida for mago in self.magos))
        if self.torre:
            vida_planeta += self.torre.vida
        ataque_planeta = sum((soldado.ataque for soldado in self.soldados))
        ataque_planeta += sum((mago.ataque for mago in self.magos))
        if self.torre:
            ataque_planeta += self.torre.ataque
        ataque_planeta *= self.ataque()
        if vida_planeta == 0:
            print("Tu planeta estaba desprotegido, el archimago ha arrasado",
                  "con el lugar")
            self.magos = int()
            self.soldados = int(self.capacidad)
            self.torre = Edificio(150, 300, 1000, 2000)
            self.cuartel = Edificio(200, 500, 0, 5000)
            self.nivel_ataque = 3
            self.nivel_economia = 3
            self.conquistado = False
            return
        while vida_planeta > 0:
            print("turno del planeta defensor")
            print("Vida ejercito: {}".format(vida_planeta))
            print("Vida archimago: {}".format(archimago.vida))
            archimago.vida -= ataque_planeta
            print("Le has quitado {} puntos de vida al archimago".format(
                ataque_planeta))
            print()
            if archimago.vida < 0:
                print("El archimago ha muerto")
                archimago.vivo = False
                break
            for turno in range(1, 4):
                print("turno del archimago ({}/3)".format(turno))
                print("Vida ejercito: {}".format(vida_planeta))
                print("Vida archimago: {}".format(archimago.vida))
                ataque = archimago.habilidad(minerales)
                vida_planeta -= ataque
                print("Le han quitado {} puntos de vida al ejercito"
                      .format(ataque))
                if vida_planeta < 1:
                    break
            print()
        if vida_planeta < 1:
            print("El archimago ha derrotado a tu ejército")
            self.magos = int()
            self.soldados = int(self.capacidad)
            self.torre = Edificio(150, 300, 1000, 2000)
            self.cuartel = Edificio(200, 500, 0, 5000)
            self.nivel_ataque = 3
            self.nivel_economia = 3
            self.conquistado = False
        else:
            if self.soldados:
                soldados_iniciales = len(self.soldados)
            else:
                soldados_iniciales = 1
            if self.magos:
                magos_iniciales = len(self.magos)
            else:
                magos_iniciales = 1
            mago_promedio = sum((mago.vida for mago in self.magos))
            mago_promedio //= magos_iniciales
            if mago_promedio == 0:
                mago_promedio = 1
            magos_vivos = min((vida_planeta/mago_promedio), len(self.magos))
            soldado_promedio = sum((soldado.vida for soldado in self.soldados))
            soldado_promedio //= soldados_iniciales
            if soldado_promedio == 0:
                soldado_promedio = 1
            soldados_vivos = vida_planeta - (mago_promedio * magos_vivos)
            soldados_vivos //= soldado_promedio
            self.magos = int(magos_vivos)
            self.soldados = int(soldados_vivos)
            print("Sobrevivieron {0} magos y {1} soldados".format(
                len(self.magos), len(self.soldados)))

    def imprimir_fecha(self):
        print("Última recolección: ", end="")
        print(self.formato_fecha())

    def formato_fecha(self):
        anno = self.ultima_recoleccion.year
        mes = self.ultima_recoleccion.month
        dia = self.ultima_recoleccion.day
        hora = self.ultima_recoleccion.hour
        minn = self.ultima_recoleccion.minute
        seg = self.ultima_recoleccion.second
        return "{}-{}-{} {}:{}:{}".format(anno, mes, dia, hora, minn, seg)
