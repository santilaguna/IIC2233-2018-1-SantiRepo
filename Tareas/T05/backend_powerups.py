# módulo destinado a las mejoras y los poderes de los jugadores.

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QObject, pyqtSignal
from random import random
from eventos import PowerUpEvent
from compare import colision


class PowerUp(QObject):

    unstore_me = pyqtSignal(QObject)

    def __init__(self, parent, x, y, size):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.sizex = size
        self.sizey = size
        self.parent = parent
        self.pixmap = None
        self.label = None
        parent.trigger_recibir_explosion.connect(self.recibir_explosion)
        self.unstore_me.connect(parent.remove_power_up)

    def show(self):
        self.label = QLabel(self.parent)
        self.label.setGeometry(self.x, self.y, self.sizex, self.sizey)
        self.label.setPixmap(QPixmap(self.pixmap))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)

    def recibir_explosion(self, e):
        if colision(self, e.espacio):
            self.catched()

    def catched(self):
        self.label.deleteLater()
        self.deleteLater()
        self.unstore_me.emit(self)
        self.parent = None
        self.setParent(None)


class Vida(PowerUp):
    def __init__(self, parent, x, y, size):
        super().__init__(parent, x, y, size)
        self.tipo = "vida"
        self.pixmap = "assets/vida.png"
        self.show()


class Velocidad(PowerUp):
    def __init__(self, parent, x, y, size):
        super().__init__(parent, x, y, size)
        self.multiplicador = 1.25
        self.tipo = "velocidad"
        self.pixmap = "assets/velocidad.png"
        self.show()


class CantidadDeBombas(PowerUp):
    def __init__(self, parent, x, y, size):
        super().__init__(parent, x, y, size)
        self.tipo = "bombas"
        self.pixmap = "assets/mas_bombas.png"
        self.show()


class SuperVelocidad(PowerUp):
    def __init__(self, parent, x, y, size):
        super().__init__(parent, x, y, size)
        self.tipo = "super"
        self.tiempo = 10
        self.pixmap = "assets/supervelocidad.png"
        self.show()


class Juggeraut(PowerUp):
    def __init__(self, parent, x, y, size):
        super().__init__(parent, x, y, size)
        self.tipo = "jugger"
        self.tiempo = 5
        self.pixmap = "assets/juggernaut.png"
        self.show()


def obtener_power(parent, x, y, size):
    valor = random()
    if valor < 0.2:
        return Vida(parent, x, y, size)
    elif valor < 0.4:
        return Velocidad(parent, x, y, size)
    elif valor < 0.6:
        return CantidadDeBombas(parent, x, y, size)
    elif valor < 0.8:
        return SuperVelocidad(parent, x, y, size)
    else:
        return Juggeraut(parent, x, y, size)
