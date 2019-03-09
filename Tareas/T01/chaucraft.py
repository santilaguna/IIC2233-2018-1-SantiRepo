# Módulo destinado a implementar la clase chaucraft

# importar como ch

import funciones_utiles as fu
import funciones_especificas as fe
from copy import deepcopy
from galaxia import Galaxia


class ChauCraft:

    def __init__(self):
        self.galaxias = {}

    def run(self):
        print("Hola! Bienvenido a ChauCraft")
        accion = fe.menu_chaucraft()
        while accion != 5:
            if accion == 1:
                self.crear_galaxia()
            elif accion == 2:
                if self.galaxias:
                    print("¿Cuál galaxia deseas modificar?")
                nombre_galaxia = self.pedir_galaxia()
                if nombre_galaxia:
                    galaxia = self.galaxias[nombre_galaxia]
                    self.modificar_galaxia(galaxia)
            elif accion == 3:
                self.consultas_galaxias()
            elif accion == 4:
                if self.galaxias:
                    print("¿En que galaxia deseas jugar?")
                nombre_galaxia = self.pedir_galaxia()
                if nombre_galaxia:
                    galaxia = self.galaxias[nombre_galaxia]
                    self.jugar_en_galaxia(galaxia)
            accion = fe.menu_chaucraft()
        print()
        print("¡Gracias por jugar ChauCraft!")

    def crear_galaxia(self):
        print("Ingrese nombre galaxia (largo minimo 6): ", end="")
        nombre = fu.pedir_string(6)
        while nombre in self.galaxias.keys():
            print("Ya existe una galaxia con ese nombre")
            print("Ingrese nombre nuevamente: ", end="")
            nombre = fu.pedir_string(6)
        galaxia = Galaxia(nombre)
        self.galaxias[nombre] = galaxia
        print("¿Cuántos planetas desea crear? (mínimo 1): ", end="")
        cantidad = fu.pedir_entero(1)
        for planeta in range(cantidad):
            galaxia.crear_planeta()
        print("¿Con que planeta deseas partir conquistado?")
        nombre_planeta = galaxia.pedir_planeta()
        galaxia.planetas[nombre_planeta].conquistado = True
        galaxia.planetas_conquistados.add(nombre_planeta)
        for planeta in galaxia.planetas.values():
            if planeta.conquistado:
                planeta.poblacion = int()
        self.actualizar_datos()

    def modificar_galaxia(self, galaxia):
        accion = galaxia.modificar_planeta()
        while accion != 7:
            accion = galaxia.modificar_planeta()
        self.actualizar_datos()
        print()
        print("Se han guardado las modificaciones en la galaxia")
        print()

    def consultas_galaxias(self):
        if not self.galaxias:
            print("Debes crear al menos una galaxia para poder realizar esta"
                  + " acción")
            return
        accion = fe.menu_consultas_galaxias()
        while accion != 5:
            if accion == 1:
                self.informacion_usuario()
            elif accion == 2:
                self.informacion_planeta()
            elif accion == 3:
                self.mejor_galaxia()
            elif accion == 4:
                fe.ranking_planetas(Galaxia.planetas)
            print()
            accion = fe.menu_consultas_galaxias()

    def informacion_usuario(self):
        for galaxia in self.galaxias.values():
            print()
            print(galaxia.nombre, end=":")
            print()
            print("Reserva de minerales: {}".format(galaxia.reserva_mineral))
            print("Reserva de deuterio: {}".format(galaxia.reserva_deuterio))
            print("Planetas Conquistados:", end=" ")
            for planeta in galaxia.planetas_conquistados:
                print("-  {}".format(planeta), end="  ")
            print()

    def informacion_planeta(self):
        for galaxia in self.galaxias.values():
            galaxia.mostrar_planetas()
        nombre_planeta = fe.pedir_planeta(Galaxia.planetas)
        planeta = Galaxia.planetas[nombre_planeta][0]
        ngalaxia = Galaxia.planetas[nombre_planeta][1]
        print("Planeta {} de la galaxia {}".format(nombre_planeta, ngalaxia))
        print("Raza: {}".format(str(planeta.raza)))
        print("Población actual: {}".format(planeta.poblacion))
        planeta.imprimir_fecha()
        print("Nivel de ataque: {}".format(planeta.nivel_ataque))
        print("Nivel de economia: {}".format(planeta.nivel_economia))
        if planeta.conquistado:
            print("Estado de conquista: conquistado")
        else:
            print("Estado de conquista: no conquistado")
        print("Edificios: ", end="")
        if planeta.torre:
            print("Torre", end=" ")
        if planeta.cuartel:
            print("Cuartel", end=" ")
        if not planeta.cuartel and not planeta.torre:
            print("No tiene", end="")
        print()
        print("Nivel de evolucion: {}".format(planeta.evolucion))
        print("Tasa minerales por segundo: {}".format(planeta.tasa_minerales))
        print("Tasa deuterio por segundo: {}".format(planeta.tasa_deuterio))
        print()

    def mejor_galaxia(self):
        valor = 0
        mejor = None
        for galaxia in self.galaxias.values():
            if galaxia.evolucion > valor:
                mejor = galaxia
                valor = galaxia.evolucion
        if mejor:
            print("La mejor galaxia es: {}".format(mejor.nombre))
        else:
            print("No hay galaxias con al menos tres planetas")
        print()

    def jugar_en_galaxia(self, galaxia_real):
        galaxia = deepcopy(galaxia_real)  # creamos una galaxia auxiliar
        accion = fe.menu_jugar()
        while accion != 3:
            if accion == 1:
                nombre_planeta = galaxia.pedir_planeta()
                planeta = galaxia.planetas[nombre_planeta]
                if fu.probabilidad(20):
                    galaxia.evento()
                if planeta.conquistado:
                    sub_accion = fe.planeta_conquistado()
                    if sub_accion == 1:
                        galaxia.construir_edificio(planeta)
                    elif sub_accion == 2:
                        galaxia.generar_unidades(planeta)
                    elif sub_accion == 3:
                        galaxia.recolectar_recursos(planeta)
                    elif sub_accion == 4:   # posible implementación de salir
                        galaxia.realizar_mejoras(planeta)
                else:
                    sub_accion = fe.planeta_no_conquistado()
                    if sub_accion == 1:
                        victoria = galaxia.invadir_planeta(planeta)  # invadido
                        if victoria:
                            galaxia.planetas_conquistados.add(nombre_planeta)
                    elif sub_accion == 2:
                        galaxia.comprar_planeta(nombre_planeta)
            elif accion == 2:
                self.galaxias[galaxia.nombre] = deepcopy(galaxia)
                for nombre_planeta in Galaxia.planetas:
                    planeta, nombre_galaxia = Galaxia.planetas[nombre_planeta]
                    if nombre_galaxia == galaxia.nombre:
                        Galaxia.planetas[nombre_planeta] =\
                            (galaxia.planetas[nombre_planeta], nombre_galaxia)
                self.actualizar_datos()
                # utilizamos deepcopy por si seguimos realizando modificaciones
            accion = fe.menu_jugar()

    def pedir_galaxia(self):
        if not self.galaxias:
            print("Debes crear al menos una galaxia para poder realizar esta"
                  + " acción")
            return None
        else:
            self.mostrar_galaxias()
            nombre_galaxia = fe.pedir_galaxia(self.galaxias)
            return nombre_galaxia

    def mostrar_galaxias(self):
        n = 0
        print()
        print("Estas son los galaxias de ChauCraft")
        for galaxia in self.galaxias.keys():
            n += 1
            print("{0}) {1}".format(n, galaxia))

    def actualizar_datos(self):
        with open("galaxias.csv", "w", encoding="utf-8") as galaxias_file:
            galaxias_file.write("nombre: string, minerales: int, deuterio: int"
                                + "\n")
            for galaxia in self.galaxias.values():
                line = "{}, {}, {} \n".format(
                    galaxia.nombre, galaxia.reserva_mineral,
                    galaxia.reserva_deuterio)
                galaxias_file.write(line)
        with open("planetas.csv", "w", encoding="utf-8") as planetas_file:
            first_line = "conquistado: bool, galaxia: string, magos: int, " \
                         "nombre: string, tasa_deuterio: int, " \
                         "tasa_minerales: int, raza: string, " \
                         "nivel_ataque: int, nivel_economia: int, " \
                         "cuartel: bool, torre: bool, " \
                         "ultima_recoleccion: datetime, soldados: int \n"
            planetas_file.write(first_line)
            for nombre_planeta in Galaxia.planetas.keys():
                planeta, nombre_galaxia = Galaxia.planetas[nombre_planeta]
                # Se utilizan variables auxiliares para tener un mayor orden
                a = planeta.conquistado
                b = nombre_galaxia
                c = len(planeta.magos)
                d = nombre_planeta
                e = planeta.tasa_deuterio
                f = planeta.tasa_minerales
                g = str(planeta.raza)
                h = planeta.nivel_ataque
                i = planeta.nivel_economia
                if planeta.cuartel:
                    j = True
                else:
                    j = False
                if planeta.torre:
                    k = True
                else:
                    k = False
                ll = planeta.formato_fecha()
                m = len(planeta.soldados)
                line = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} \n"\
                    .format(a, b, c, d, e, f, g, h, i, j, k, ll, m)
                planetas_file.write(line)
