from Interfaz import Window
from PyQt5.QtWidgets import QApplication
from torneo import Torneo
from mis_estructuras import Listirijilla
from cargar_archivos import entregar_grafo
from equipo import Equipo
import random
import funciones_utiles as fu


class Juego:
    def __init__(self):
        self.torneo = None
        self.grafo, jugadores = entregar_grafo()
        self.tu_equipo = Equipo(Listirijilla(), "Tu Equipo")
        self.equipos = self.cargar_equipos()
        equiposs = Listirijilla()
        for equipo in self.equipos:
            gui_repr = Listirijilla(equipo.nombre)
            gui_repr.append(equipo.esperanza)
            equiposs.append(gui_repr)

        # No cambiar esta línea
        self.gui = Window(self, jugadores, equiposs)
        #

    def cargar_equipos(self):
        equipos = Listirijilla()
        # podria utilizar un for i in range(16), y llamarlos equipo i
        # con un {}.format, pero es muy fome =D
        nombres_equipos = Listirijilla()
        nombres_equipos.append('Super Campeones')
        nombres_equipos.append('Tatitas FC')
        nombres_equipos.append('Real Madrazo')

        nombres_equipos.append('Scooby doo papa')
        nombres_equipos.append('Alumbrados FC')
        nombres_equipos.append('Ratones FC')
        nombres_equipos.append('Laucheros FC')

        nombres_equipos.append('Coca Juniors')
        nombres_equipos.append('Dream Team')
        nombres_equipos.append('Error 404 legs not found')
        nombres_equipos.append('Con la mente en el juego FC')

        nombres_equipos.append('Gryffindor')
        nombres_equipos.append('Hufflepuff')
        nombres_equipos.append('Ravenclaw')
        nombres_equipos.append('Slytherin')

        positions = Listirijilla()
        for nombre in nombres_equipos:
            jugadores = Listirijilla()
            for i in range(11):
                n = random.randint(0, 200)
                while n in positions:
                    n = random.randint(0, 200)
                positions.append(n)
                jugadores.append(self.grafo.jugadores[n])
            equipo = Equipo(jugadores, nombre)
            equipo.matriz_afinidades = self.afinidad_equipo(jugadores)
            equipos.append(equipo)
        return equipos

    def cambio_jugador(self, j1, j2, en_cancha):  # j1 sale, j2 entra
        if en_cancha:
            self.tu_equipo.cambio_adentro(j1, j2)
        else:
            real_player = self.grafo.buscar_nombre(j2)
            self.tu_equipo.cambio_fuera(j1, real_player)
        self.tu_equipo.matriz_afinidades = self.afinidad_equipo(
            self.tu_equipo.jugadores)
        self.gui.cambiar_esperanza(self.tu_equipo.esperanza)

    def entra_jugador(self, jugador):
        real_player = self.grafo.buscar_nombre(jugador)
        self.tu_equipo.jugadores.append(real_player)
        if len(self.tu_equipo.jugadores) == 11:
            self.tu_equipo.matriz_afinidades = self.afinidad_equipo(
                self.tu_equipo.jugadores)
            self.gui.cambiar_esperanza(self.tu_equipo.esperanza)

    def simular_campeonato(self, equipos):
        while len(self.tu_equipo.jugadores) < 11:
            n = random.randint(0, 200)
            self.tu_equipo.jugadores.append(self.grafo.jugadores[n])
            if len(self.tu_equipo.jugadores) == 11:
                self.tu_equipo.matriz_afinidades = self.afinidad_equipo(
                    self.tu_equipo.jugadores)
            self.gui.cambiar_esperanza(self.tu_equipo.esperanza)
        if len(self.equipos) < 16:
            self.equipos.append(self.tu_equipo)
        self.torneo = Torneo(self.equipos)
        self.torneo.simular_torneo()

    def afinidad_equipo(self, jugadores):
        # como no existe un patrón de relaciones es más eficiente definir
        # las relaciones de a una
        arquero = Listirijilla()
        defensa1 = Listirijilla()
        defensa2 = Listirijilla()
        defensa3 = Listirijilla()
        defensa4 = Listirijilla()
        medio1 = Listirijilla()
        medio2 = Listirijilla()
        medio3 = Listirijilla()
        medio4 = Listirijilla()
        delantero1 = Listirijilla()
        delantero2 = Listirijilla()

        af = self.grafo.afinidad(jugadores[0], jugadores[2])
        arquero.append(af)
        defensa2.append(af)
        af = self.grafo.afinidad(jugadores[0], jugadores[3])
        arquero.append(af)
        defensa3.append(af)

        af = self.grafo.afinidad(jugadores[1], jugadores[2])
        defensa1.append(af)
        defensa2.append(af)
        af = self.grafo.afinidad(jugadores[1], jugadores[5])
        defensa1.append(af)
        medio1.append(af)

        af = self.grafo.afinidad(jugadores[2], jugadores[3])
        defensa2.append(af)
        defensa3.append(af)
        af = self.grafo.afinidad(jugadores[2], jugadores[6])
        defensa2.append(af)
        medio2.append(af)

        af = self.grafo.afinidad(jugadores[3], jugadores[4])
        defensa4.append(af)
        defensa3.append(af)
        af = self.grafo.afinidad(jugadores[3], jugadores[7])
        defensa3.append(af)
        medio3.append(af)

        af = self.grafo.afinidad(jugadores[4], jugadores[8])
        defensa4.append(af)
        medio4.append(af)

        af = self.grafo.afinidad(jugadores[5], jugadores[6])
        medio1.append(af)
        medio2.append(af)
        af = self.grafo.afinidad(jugadores[5], jugadores[9])
        medio1.append(af)
        delantero1.append(af)

        af = self.grafo.afinidad(jugadores[6], jugadores[7])
        medio3.append(af)
        medio2.append(af)
        af = self.grafo.afinidad(jugadores[6], jugadores[9])
        medio2.append(af)
        delantero1.append(af)

        af = self.grafo.afinidad(jugadores[7], jugadores[8])
        medio3.append(af)
        medio4.append(af)
        af = self.grafo.afinidad(jugadores[7], jugadores[10])
        medio3.append(af)
        delantero2.append(af)

        af = self.grafo.afinidad(jugadores[8], jugadores[10])
        delantero2.append(af)
        medio4.append(af)

        af = self.grafo.afinidad(jugadores[9], jugadores[10])
        delantero1.append(af)
        delantero2.append(af)
        matriz = Listirijilla(arquero)
        matriz.append(defensa1)
        matriz.append(defensa2)
        matriz.append(defensa3)
        matriz.append(defensa4)
        matriz.append(medio1)
        matriz.append(medio2)
        matriz.append(medio3)
        matriz.append(medio4)
        matriz.append(delantero1)
        matriz.append(delantero2)
        return matriz

    def consulta_usuario(self):
        info = self.torneo.info_equipo()
        self.gui.resetear_respuestas()
        info_usuario = "Mejor fase: " + str(info[0]) + "\n"
        info_usuario += "Eliminado por: " + str(info[1]) + "\n"
        info_usuario += "Goles anotados: " + str(info[2]) + "\n"
        info_usuario += "Goles recibidos: " + str(info[3]) + "\n"
        info_usuario += "Faltas realizadas: "
        for falta in info[4]:
            info_usuario += falta + ", "
        info_usuario =  info_usuario[:-2]
        info_usuario+= "\n"
        info_usuario += "Tarjetas rojas: " + str(info[5]) + "\n"
        info_usuario += "Tarjetas amarillas: " + str(info[6]) + "\n"
        self.gui.agregar_respuesta(info_usuario)

    def consulta_equipo(self, nombre):
        self.gui.resetear_respuestas()
        info = self.torneo.info_tu_equipo(nombre)
        if not info:
            self.gui.agregar_respuesta("Equipo no encontrado")
        else:
            info_equipo = "Mejor fase: " + info[0] + "\n"
            info_equipo += "Eliminado por: " + info[1] + "\n"
            info_equipo+= "Goles anotados: " +info[2] + "\n"
            info_equipo += "Goles recibidos: " +info[3] + "\n"
            info_equipo += "Faltas realizadas: "
            for falta in info[4]:
                info_equipo += falta + ", "
            info_equipo =  info_equipo[:-2]
            info_equipo+= "\n"
            info_equipo += "Tarjetas rojas: " + str(info[5]) + "\n"
            info_equipo += "Tarjetas amarillas: " + str(info[6]) + "\n"
            self.gui.agregar_respuesta(info_equipo)

    def consulta_ganadores(self):
        self.gui.resetear_resultados()
        resultado = "Primer lugar: " + self.torneo.podio[0] + "\n"
        resultado += "Segundo lugar: " + self.torneo.podio[1] + "\n"
        resultado += "Tercer lugar: " + self.torneo.podio[2] + "\n"
        self.gui.agregar_resultado(resultado)

    def consulta_partido(self, _id):
        self.gui.resetear_respuestas()
        if not _id.isdigit() or int(_id) not in range(1, 17):
            self.gui.agregar_respuesta("El ID del partido debe ser un entero "
                                       "entre 1 y 16")
        else:
            partido = self.torneo.buscar_partido(int(_id))
            info = "Ganador: " + partido.ganador + "\n\n"

            info += "Equipo 1: " + partido.equipo1.nombre + "\n"
            info += "Goles: " + partido.goles1 + "\n"
            info += "Faltas: "
            for falta in partido.faltas_eq1:
                info += falta + ", "
            info = info[:-2] + "\n"
            info += "Tarjetas rojas: " + partido.rojas_eq1 + "\n"
            info += "Tarjetas amarillas: " + partido.amarillas_eq1 + "\n"
            info += "\n"

            info += "Equipo 2: " + partido.equipo2.nombre + "\n"
            info += "Goles: " + partido.goles2 + "\n"
            info += "Faltas: "
            for falta in partido.faltas_eq2:
                info += falta + ", "
            info = info[:-2] + "\n"
            info += "Tarjetas rojas: " + partido.rojas_eq2 + "\n"
            info += "Tarjetas amarillas: " + partido.amarillas_eq2 + "\n"

            self.gui.agregar_respuesta(info)

    def consulta_fase(self, numero):
        self.gui.resetear_respuestas()
        if not numero.isdigit() or int(numero) not in range(1, 5):
            self.gui.agregar_respuesta("El número de fase debe ser un entero "
                                       "entre 1 y 4, donde 1 son los octavos "
                                       "de final y 4 la final")
        else:
            ganadores = Listirijilla()
            perdedores = Listirijilla()
            if int(numero) == 1:
                inicio = 1
                final = 9
            elif int(numero) == 2:
                inicio = 9
                final = 13
            elif int(numero) == 3:
                inicio = 13
                final = 15
            else:
                inicio = 16
                final = 17
            for _id in range(inicio, final):
                partido = self.torneo.buscar_partido(_id)
                ganadores.append(partido.ganador)
                if partido.equipo1.nombre == partido.ganador:
                    perdedores.append(partido.equipo2.nombre)
                else:
                    perdedores.append(partido.equipo1.nombre)
            info = "Perdieron en esta fase: "
            for equipo in perdedores:
                info += equipo + ", "
            info = info[:-2] + "\n"
            info += "Ganaron en esta fase: "
            for equipo in ganadores:
                info += equipo + ", "
            info = info[:-2] + "\n"
            self.gui.agregar_respuesta(info)

# NO CAMBIAR NADA PARA ABAJO
if __name__ == '__main__':

    app = QApplication([])

    a = Juego()

    app.exec_()
