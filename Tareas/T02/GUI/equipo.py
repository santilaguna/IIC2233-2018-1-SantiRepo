# módulo destinado a armar el equipo con 11 jugadores
from mis_estructuras import Listirijilla


class Equipo:

    def __init__(self, jugadores, nombre):
        self.nombre = nombre
        self.jugadores = jugadores
        self.matriz_afinidades = None

    @property
    def esperanza(self):
        return self.afinidad * self.calidad

    @property
    def afinidad(self):
        total = 0
        for afinidades in self.matriz_afinidades:
            try:
                total += sum(afinidades)/len(afinidades)
            except ZeroDivisionError:
                total = 0
        return total/11

    @property
    def calidad(self):
        overall = 0
        for jugador in self.jugadores:
            overall += jugador.overall
        return overall/11  # según la issue 295

    def cambio_adentro(self, n_j1, n_j2):
        position1 = None
        position2 = None
        for position in range(len(self.jugadores)):
            jugador = self.jugadores[position]
            if jugador.nombre == n_j1:
                position1 = position
            elif jugador.nombre == n_j2:
                position2 = position
        aux = self.jugadores[position1]
        self.jugadores[position1] = self.jugadores[position2]
        self.jugadores[position2] = aux

    def cambio_fuera(self, n_j1, j2):
        for position in range(len(self.jugadores)):
            jugador = self.jugadores[position]
            if jugador.nombre == n_j1:
                self.jugadores[position] = j2
                break

    def __repr__(self):
        return self.nombre