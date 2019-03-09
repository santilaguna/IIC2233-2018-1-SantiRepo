# módulo destinado a implementar las bombas.

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.Qt import QTest
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from eventos import PositionMoveEvent, ReleaseEvent, ExplodeEvent, \
    MoveBombEvent
from parameters import TIEMPO_EXPLOSION, RANGO_EXPLOSION, N, MAPA_SIZE,\
    VEL_MOVIMIENTO


class Bomba(QThread):

    id_ = 0
    pixmap = "assets/bomba.png"
    explotar_signal = pyqtSignal(ExplodeEvent)
    move_bomb =  pyqtSignal(MoveBombEvent)

    def __init__(self, parent, x, y, player):
        super().__init__()
        self.player = player
        self.x = x
        self.y = y
        self.sizex = 20
        self.sizey = 20
        self.rango_explosion = RANGO_EXPLOSION * N/MAPA_SIZE
        self.ready = True
        self.parent = parent
        self.id_ = Bomba.id_
        Bomba.id_ += 1
        parent.trigger_pausar.connect(self.pausar)
        parent.trigger_kick_bomb.connect(self.ser_pateada)
        parent.trigger_stop_bomb.connect(self.stop_bomb)
        parent.trigger_move_label_bomb.connect(self.move_label)
        self.move_bomb.connect(parent.move_bomb)

    def encasillar(self, x, y):
        self.x = x
        self.y = y
        self.label = QLabel(self.parent)
        self.label.setGeometry(self.x - 10, self.y - 10, 20, 20)
        self.label.setPixmap(QPixmap(self.pixmap))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)
        self.contador = TIEMPO_EXPLOSION
        self.moving = False
        self.way = None
        self.start()

    def pausar(self):
        if self.ready:
            self.ready = False
        else:
            self.ready = True

    def ser_pateada(self, e):
        if TIEMPO_EXPLOSION - self.contador < 0.5:
            return
        if e.id_ == self.id_:
            self.moving = True
            self.way = e.way

    def stop_bomb(self, e):
        if e.id_ == self.id_:
            self.moving = False
            self.way = None
            self.x = self.label.x()
            self.y = self.label.y()

    def move_label(self, id_):
        if id_ == self.id_:
            self.label.move(self.x, self.y)

    def run(self):
        self.explotar_signal.connect(self.parent.bomb_explode)
        while True:
            QTest.qWait(100)
            if self.ready:
                if self.moving:
                    if self.way == "up":
                        self.y -= (5 * VEL_MOVIMIENTO)
                    elif self.way == "down":
                        self.y += (5 * VEL_MOVIMIENTO)
                    elif self.way == "right":
                        self.x += (5 * VEL_MOVIMIENTO)
                    elif self.way == "left":
                        self.x -= (5 * VEL_MOVIMIENTO)
                    self.move_bomb.emit(MoveBombEvent(self.id_,
                                                      self.x, self.y))
                self.contador -= 0.1
                if self.contador <= 0:
                    self.explotar_signal.emit(
                        ExplodeEvent(self.x, self.y,
                                     self.rango_explosion, self, self.player))
                    break
        QTest.qWait(100)
        self.quit()
        self.label.deleteLater()


class Explode(QThread):

    pixmap = "assets/Bomb_explode_1.png"

    def __init__(self, parent, x, y):
        super().__init__(parent)
        self.label = QLabel(parent)
        self.label.setGeometry(x, y, 50, 50)
        self.label.setPixmap(QPixmap(self.pixmap))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)

    def run(self):
        QTest.qWait(500)
        self.label.deleteLater()
        self.quit()
