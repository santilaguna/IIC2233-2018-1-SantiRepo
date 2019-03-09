# Módulo destinado a implementar las clase galaxia

# importar como ga

import funciones_utiles as fu
import funciones_especificas as fe
import clases as cl
from planeta import Planeta
from random import choice
from datetime import datetime


class Galaxia:

    planetas = {}  # [nombre] = (planeta, nombre galaxia)

    def __init__(self, nombre):
        self.archimago = cl.Archimago()
        self.asteroide = cl.Asteroide()
        self.nombre = nombre
        self.planetas = {}  # [nombre] = planeta
        self.planetas_conquistados = set()
        self.__reserva_mineral = 1000
        self.__reserva_deuterio = 1000

    @property
    def reserva_mineral(self):
        return self.__reserva_mineral

    @reserva_mineral.setter
    def reserva_mineral(self, valor):
        if valor < 0:
            self.__reserva_mineral = 0
        else:
            self.__reserva_mineral = valor

    @property
    def reserva_deuterio(self):
        return self.__reserva_deuterio

    @reserva_deuterio.setter
    def reserva_deuterio(self, valor):
        if valor < 0:
            self.__reserva_deuterio = 0
        else:
            self.__reserva_deuterio = valor

    @property
    def evolucion(self):
        if len(self.planetas) > 2:
            valores = [planeta.evolucion for planeta in self.planetas.values()]
            valores.remove(max(valores))
            valores.remove(min(valores))
            return sum(valores)/len(valores)
        else:
            return 0

    def crear_planeta(self):
        print("Ingrese nombre del planeta (largo mínimo 6): ", end="")
        nombre = fu.pedir_string(6)
        while nombre in Galaxia.planetas:
            print("Ya existe un planeta con este nombre en alguna galaxia",
                  "ingrese nuevamente: ", end="")
            nombre = fu.pedir_string(6)
        n_raza = fe.pedir_raza()
        raza = None
        if n_raza == 1:
            raza = cl.Aprendiz()
        elif n_raza == 2:
            raza = cl.Maestro()
        elif n_raza == 3:
            raza = cl.Asesino()
        nuevo_planeta = Planeta(raza)
        cantidad_a_poblar = (nuevo_planeta.capacidad * 0.75)//1
        nuevo_planeta.soldados = int(cantidad_a_poblar)
        self.planetas[nombre] = nuevo_planeta
        Galaxia.planetas[nombre] = (nuevo_planeta, self.nombre)

    def destruir_planeta(self, nombre):
        if len(self.planetas_conquistados) > 1:
            for name in self.planetas.keys():
                if nombre == name:
                    self.planetas_conquistados.discard(nombre)
                    del self.planetas[name]
                    del Galaxia.planetas[nombre]
                    break
        else:
            print("La galaxia debe tener al menos un planeta conquistado")

    def modificar_planeta(self):
        accion = fe.menu_modificar_galaxia()
        if accion == 1:
            self.crear_planeta()
        elif accion == 2:
            nombre_planeta = self.pedir_planeta()
            if self.planetas[nombre_planeta].conquistado:
                self.destruir_planeta(nombre_planeta)
            else:
                print("El planeta no esta conquistado")
        elif accion == 3:
            nombre_planeta = self.pedir_planeta()
            planeta = self.planetas[nombre_planeta]
            if not planeta.conquistado:
                aumento = fe.aumento_tasa("mineral")
                tasa_inicial = planeta.tasa_minerales
                planeta.tasa_minerales = aumento + tasa_inicial
                Galaxia.planetas[nombre_planeta] = (planeta, self.nombre)
            else:
                print("El planeta ya está conquistado")
        elif accion == 4:
            nombre_planeta = self.pedir_planeta()
            planeta = self.planetas[nombre_planeta]
            if not planeta.conquistado:
                aumento = fe.aumento_tasa("deuterio")
                tasa_inicial = planeta.tasa_deuterio
                planeta.tasa_deuterio = aumento + tasa_inicial
                Galaxia.planetas[nombre_planeta] = (planeta, self.nombre)
            else:
                print("El planeta ya está conquistado")
        elif accion == 5:
            nombre_planeta = self.pedir_planeta()
            planeta = self.planetas[nombre_planeta]
            if not planeta.conquistado:
                aumento = fe.aumento_personas("soldados")
                inicial = len(planeta.soldados)
                planeta.soldados = int(aumento) + inicial
                Galaxia.planetas[nombre_planeta] = (planeta, self.nombre)
            else:
                print("El planeta ya está conquistado")
        elif accion == 6:
            nombre_planeta = self.pedir_planeta()
            planeta = self.planetas[nombre_planeta]
            if not planeta.conquistado:
                if isinstance(planeta.raza, cl.Maestro):
                    aumento = fe.aumento_personas("magos")
                    inicial = len(planeta.magos)
                    planeta.magos = int(int(aumento) + inicial)
                    Galaxia.planetas[nombre_planeta] = (planeta, self.nombre)
                else:
                    print("La raza del planeta señalado no puede generar",
                          "magos")
            else:
                print("El planeta ya está conquistado")
        return accion

    def pedir_planeta(self):
        if not self.planetas:
            print("No hay planetas (No deberiamos llegar nunca aquí)")
            return None
        else:
            self.mostrar_planetas()
            nombre_planeta = fe.pedir_planeta(self.planetas)
            return nombre_planeta

    def mostrar_planetas(self):
        n = 0
        print()
        print("Estos son los planetas de la galaxia {}:".format(self.nombre))
        for planeta in self.planetas.keys():
            n += 1
            print("{0}) {1}".format(n, planeta))

    def pedir_conquistado(self):
        self.mostrar_conquistados()
        print("Escoga el número del planeta con el que deseas invadir")
        nombre_planeta = fu.tomar_decision(list(self.planetas_conquistados))
        return self.planetas[nombre_planeta]

    def mostrar_conquistados(self):
        n = 0
        print()
        print("Estos son los planetas conquistados de la galaxia {}:"
              .format(self.nombre))
        for planeta in self.planetas_conquistados:
            n += 1
            print("{0}) {1}".format(n, planeta))

    def evento(self):
        if fu.probabilidad(50):
            nombre = choice(list(self.planetas_conquistados))
            print("El archimago ha invadido {}".format(nombre))
            planeta = self.planetas[nombre]
            planeta.invasion_archimago(self.archimago, self.reserva_mineral)
            if not self.archimago.vivo:
                print("Unos comerciantes avistan a un descendiente del "
                      + "archimago, se cree que ha decidido seguir el camino "
                      + "del mal y tomar su puesto")
                self.archimago = cl.Archimago()
            if not planeta.conquistado:
                print("El planeta {} ya no está conquisatdo".format(nombre))
                self.planetas_conquistados.discard(nombre)
            if len(self.planetas_conquistados) == 0:
                print("Te has salvado como el archimago atacó a tu último",
                      "planeta, no lo perderás. Sin embargo, mató a todo",
                      "tu ejército, destruyó tus edificios y además",
                      "dejo tus niveles de desarrollo al mínimo.")
                planeta.poblacion = 0
                planeta.torre = None
                planeta.cuartel = None
                planeta.nivel_ataque = 0
                planeta.nivel_economia = 0
                self.planetas_conquistados.add(nombre)
                planeta.conquistado = True
        else:
            nombre = choice(list(self.planetas_conquistados))
            print("Ha caido un asteroide en {}".format(nombre))
            print("Ha muerto la mitad de tu ejército")
            planeta = self.planetas[nombre]
            self.asteroide.impactar(planeta.impacto_asteroide)

    def invadir_planeta(self, defensor):
        invasor = self.pedir_conquistado()
        if not invasor.magos and not invasor.soldados:
            print("El planeta escogido no tiene ejército, fuiste derrotado",
                  "antes de comenzar la batalla")
            return False
        if isinstance(defensor.raza, cl.Maestro):
            invasor.poblacion = defensor.raza.habilidad(invasor.poblacion)
        # creamos entidad invasor
        vida_invasor = sum((soldado.vida for soldado in invasor.soldados))
        vida_invasor += sum((mago.vida for mago in invasor.magos))
        if invasor.torre:
            vida_invasor += invasor.torre.vida
        ataque_invasor = sum((soldado.ataque for soldado in invasor.soldados))
        ataque_invasor += sum((mago.ataque for mago in invasor.magos))
        if invasor.torre:
            ataque_invasor += invasor.torre.ataque
        ataque_invasor *= invasor.ataque()
        # creamos entidad defensor
        vida_defensor = sum((soldado.vida for soldado in defensor.soldados))
        vida_defensor += sum((mago.vida for mago in defensor.magos))
        if defensor.torre:
            vida_defensor += defensor.torre.vida
        ataque_defensor = sum((soldado.ataque for soldado in
                               defensor.soldados))
        ataque_defensor += sum((mago.ataque for mago in defensor.magos))
        if defensor.torre:
            ataque_defensor += defensor.torre.ataque
        ataque_defensor *= defensor.ataque()
        # comienza la batalla
        if vida_defensor == 0:
            print("El planeta estaba vacio, has conquistado un nuevo planeta")
            return True
        if isinstance(invasor.raza, cl.Asesino):
            while vida_invasor > 0:
                print("turno del ejército invasor")
                print("Vida ejército defensor: {}".format(vida_defensor))
                print("Vida ejército invasor: {}".format(vida_invasor))
                if isinstance(invasor.raza, cl.Asesino):
                    ataque = invasor.raza.habilidad(ataque_invasor)
                elif isinstance(invasor.raza, cl.Aprendiz):
                    ataque = ataque_invasor
                    robado = invasor.raza.habilidad()
                    self.reserva_mineral += int(robado)
                else:
                    ataque = ataque_invasor
                vida_defensor -= ataque
                print("Le has quitado {} puntos de vida al ejercito defensor"
                      .format(ataque))
                print()
                if vida_defensor < 0:
                    break
                print("turno del planeta defensor")
                print("Vida ejército defensor: {}".format(vida_defensor))
                print("Vida ejército invasor: {}".format(vida_invasor))
                vida_invasor -= ataque_defensor
                print("Le han quitado {} puntos de vida a tu ejército".format(
                    ataque_defensor))
                print()
        else:
            while vida_defensor > 0:
                print("turno del planeta defensor")
                print("Vida ejército defensor: {}".format(vida_defensor))
                print("Vida ejército invasor: {}".format(vida_invasor))
                vida_invasor -= ataque_defensor
                print("Le han quitado {} puntos de vida a tu ejército".format(
                    ataque_defensor))
                print()
                if vida_invasor < 0:
                    break
                print("turno del ejército invasor")
                print("Vida ejército defensor: {}".format(vida_defensor))
                print("Vida ejército invasor: {}".format(vida_invasor))
                if isinstance(invasor.raza, cl.Aprendiz):
                    robado = invasor.raza.habilidad()
                    self.reserva_mineral += robado
                vida_defensor -= ataque_invasor
                print("Le has quitado {} puntos de vida al ejercito defensor"
                      .format(ataque_invasor))
                print()
        if vida_defensor < 0:
            defensor.magos = int()
            defensor.soldados = int()
            defensor.conquistado = True
            print("Has conquistado un nuevo planeta")
            invasor.raza()
            fe.boost(invasor.soldados, invasor.raza)
            if isinstance(invasor.raza, cl.Maestro):
                fe.boost_magos(invasor.magos)
            if invasor.soldados:
                soldados_iniciales = len(invasor.soldados)
            else:
                soldados_iniciales = 1
            if invasor.soldados:
                magos_iniciales = len(invasor.magos)
            else:
                magos_iniciales = 1
            '''As seen at www.python-course.eu/list_comprehension.php'''
            mago_promedio = sum((mago.vida for mago in invasor.magos))
            if mago_promedio == 0:
                mago_promedio = 1
            if magos_iniciales:
                mago_promedio //= magos_iniciales
            magos_vivos = min((vida_invasor/mago_promedio), magos_iniciales)
            soldado_promedio = sum(
                (soldado.vida for soldado in invasor.soldados))
            if soldados_iniciales:
                soldado_promedio //= soldados_iniciales
            if soldado_promedio == 0:
                soldado_promedio = 1
            soldados_vivos = vida_invasor - (mago_promedio * magos_vivos)
            soldados_vivos //= soldado_promedio
            magos_vivos = int(magos_vivos)
            soldados_vivos = int(soldados_vivos)
            invasor.magos = int(magos_vivos)
            invasor.soldados = int(soldados_vivos)
            print("Sobrevivieron {} magos y {} soldados de tu ejército"
                  .format(magos_vivos, soldados_vivos))
            return True
        else:
            if defensor.magos:
                magos_iniciales = len(defensor.magos)
            else:
                magos_iniciales = 1
            invasor.magos = int()
            invasor.soldados = int()
            print("Han derrotado a tu ejército")
            mago_promedio = sum((mago.vida for mago in defensor.magos))
            mago_promedio //= magos_iniciales
            if mago_promedio == 0:
                mago_promedio = 1
            magos_vivos = min((vida_defensor/mago_promedio),
                              len(defensor.magos))
            if defensor.soldados:
                soldados_iniciales = len(defensor.soldados)
            else:
                soldados_iniciales = 1
            soldado_promedio = sum(
                (soldado.vida for soldado in defensor.soldados))
            soldado_promedio //= soldados_iniciales
            if soldado_promedio == 0:
                soldado_promedio = 1
            soldados_vivos = vida_defensor - (mago_promedio * magos_vivos)
            soldados_vivos //= soldado_promedio
            magos_vivos = int(magos_vivos)
            soldados_vivos = int(soldados_vivos)
            defensor.magos = int(magos_vivos)
            defensor.soldados = int(soldados_vivos)
            print("Sobrevivieron {} magos y {} soldados del ejército defensor"
                  .format(magos_vivos, soldados_vivos))
            return False

    def comprar_planeta(self, nombre_planeta):
        fe.comprar_planeta(self, nombre_planeta)

    def realizar_mejoras(self, planeta):
        fe.realizar_mejoras(self, planeta)

    def generar_unidades(self, planeta):
        if not planeta.cuartel:
            print("Debes construir un cuartel en este planeta, si quieres "
                  + "generar unidades")
            return
        tipo = "Soldados"
        raza = planeta.raza
        if raza.capacidad == planeta.poblacion:
            print("Población al máximo")
            return
        print("Capacidad máxima: {}".format(raza.capacidad))
        print("Población total actual: {}".format(planeta.poblacion))
        print("Estos son los costos de generar unidades:")
        print("Costo mineral soldado: {}".format(
            raza.costo_mineral_soldados))
        print("Costo deuterio soldado: {}".format(
            raza.costo_deuterio_soldados))
        if isinstance(raza, cl.Maestro):
            print("Costo mineral mago: {}".format(
                raza.costo_mineral_magos))
            print("Costo deuterio mago: {}".format(
                raza.costo_deuterio_magos))
            print("¿Qué unidad deseas generar?")
            tipo = fu.tomar_decision(["Soldados", "Magos"])
        print()
        print("¿Cuántas unidades deseas generar?")
        cantidad = fu.pedir_entero(1, raza.capacidad)
        if (cantidad + planeta.poblacion) > raza.capacidad:
            print("Esa cantidad excede la población máxima")
            return
        if tipo == "Soldados":
            mineral = cantidad * raza.costo_mineral_soldados
            deuterio = cantidad * raza.costo_deuterio_soldados
        else:
            mineral = cantidad * raza.costo_mineral_magos
            deuterio = cantidad * raza.costo_deuterio_magos
        if (self.reserva_mineral - mineral) < 0:
            print("Mineral insuficiente")
            return
        elif (self.reserva_deuterio - deuterio) < 0:
            print("Deuterio insuficiente")
            return
        self.reserva_mineral -= mineral
        self.reserva_deuterio -= deuterio
        if tipo == "Soldados":
            planeta.soldados = int(cantidad) + len(planeta.soldados)
            print("se han unido {} soldados al ejército".format(cantidad))
        else:
            planeta.magos = int(cantidad + len(planeta.magos))
            print("se han unido {} magos al ejército".format(cantidad))

    def recolectar_recursos(self, planeta):
        nueva_fecha = datetime.today()
        diferencia = nueva_fecha - planeta.ultima_recoleccion
        segundos = diferencia.total_seconds()
        minerales = segundos * planeta.economia() * planeta.tasa_minerales
        minerales = int(minerales//1)
        deuterio = segundos * planeta.economia() * planeta.tasa_deuterio
        deuterio = int(deuterio//1)
        print("Se han recolectado {} unidades de minerales"
              .format(minerales), end=" ")
        print("y {} unidades de deuterio".format(deuterio))
        self.reserva_mineral += minerales
        self.reserva_deuterio += deuterio
        planeta.ultima_recoleccion = nueva_fecha

    def construir_edificio(self, planeta):
        print()
        print("¿Qué edificio deseas construir?")
        tipo_edificio = fu.tomar_decision(["Torre", "Cuartel", "Volver"])
        if tipo_edificio == "Torre":
            if planeta.torre:
                print("este planeta ya tiene una torre")
                return
            torre = cl.Edificio(150, 300, 1000, 2000)
            if self.reserva_deuterio - torre.costo_deuterio < 0:
                print("Deuterio insuficiente")
                return
            elif self.reserva_mineral - torre.costo_mineral < 0:
                print("Mineral insuficiente")
                return
            self.reserva_deuterio -= torre.costo_deuterio
            self.reserva_mineral -= torre.costo_mineral
            planeta.torre = torre
            print("Torre construida")
        elif tipo_edificio == "Cuartel":
            if planeta.cuartel:
                print("Este planeta ya tiene un cuartel")
                return
            cuartel = cl.Edificio(200, 500, 0, 5000)
            if self.reserva_deuterio - cuartel.costo_deuterio < 0:
                print("Deuterio insuficiente")
                return
            elif self.reserva_mineral - cuartel.costo_mineral < 0:
                print("Mineral insuficiente")
                return
            self.reserva_deuterio -= cuartel.costo_deuterio
            self.reserva_mineral -= cuartel.costo_mineral
            planeta.cuartel = cuartel
            print("Cuartel construido")
