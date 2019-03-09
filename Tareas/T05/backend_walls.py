# módulo destinado a obtener y representar a las murallas y los espacios.


from PyQt5.QtCore import QObject, pyqtSignal
from parameters import N, MAPA_SIZE
from random import random
from eventos import PowerUpEvent
from backend_powerups import obtener_power


class Wall(QObject):

    def __init__(self, parent, x, y, size, destructible):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.sizex = size
        self.sizey = size
        self.destructible = destructible
        self.stop_explosion = True

    @property
    def pos(self):
        return self.x + self.sizex/2, self.y + self.sizey/2


class Espacio(QObject):

    liberar_power_up = pyqtSignal(PowerUpEvent)

    def __init__(self, parent, x, y, size, game_started=False):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.sizex = size
        self.sizey = size
        self.ocupado = False
        self.stop_explosion = False
        self.parent = parent
        if game_started:
            self.power_up()

    @property
    def pos(self):
        return self.x + self.sizex/2, self.y + self.sizey/2

    def power_up(self):
        if random() < 0.3:
            self.liberar_power_up.connect(self.parent.power_up)
            self.liberar_power_up.emit(PowerUpEvent(obtener_power(
                self.parent, self.x, self.y, self.sizex)))


def back_walls(parent):
    walls = []
    espacios = []
    with open("mapa.txt") as file:
        currentx = 0
        currenty = 0
        size = N/MAPA_SIZE
        for line in file:
            line = line.replace(" ", "")
            for letter in line.strip():
                if letter == "X":
                    wall = Wall(parent, currentx, currenty, size, False)
                    walls.append(wall)
                elif letter == "P":
                    wall = Wall(parent, currentx, currenty, size, True)
                    walls.append(wall)
                else:
                    espacio = Espacio(parent, currentx, currenty, size)
                    espacios.append(espacio)
                currentx += size
            currentx = 0
            currenty += size
    return walls, espacios
