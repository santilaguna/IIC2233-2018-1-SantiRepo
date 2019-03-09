# módulo destinado a las clases y funcionalidades de los enemigos.

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.Qt import QTest
from parameters import VEL_MOVIMIENTO, LAMBDA_HOSTIL, A_NO_HOSTIL, \
    B_NO_HOSTIL, N, RANGO_VISION, VIDAS_ENEMIGOS, HOSTILES_INICIALES, \
    COMUNES_INICIALES, AUMENTO_DIFICULTAD, NIVEL_DIFICULTAD
from random import choice, uniform, expovariate
from eventos import MoveEnemyEvent, RangoVisionEvent, SideMoveEvent, \
    RecibirEnemigoEvent
from compare import colision


class Enemigo(QThread):

    add_points = pyqtSignal(int)
    id_ = 0
    move_enemy = pyqtSignal(MoveEnemyEvent)
    die_signal = pyqtSignal(int)

    def __init__(self, parent, x, y, pixmap="assets/Illumi_Zoldyck.png"):
        super().__init__(parent)
        self.sizex = 20
        self.sizey = 30
        self.label = QLabel(parent)
        self.label.setGeometry(x - self.sizex/2, y - self.sizey/2, 20, 30)
        self.pixmap = QPixmap(pixmap)
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)
        self._pos = (x - self.sizex/2, y - self.sizey/2)
        self.vida = VIDAS_ENEMIGOS
        self.side = choice(["up", "down", "left", "right"])
        self.move_enemy.connect(parent.move_enemy)
        self.die_signal.connect(parent.muere_enemigo)
        self.add_points.connect(parent.add_enemy_points)
        self.ready = True
        self.nivel_dificultad = NIVEL_DIFICULTAD
        self._velocidad = VEL_MOVIMIENTO
        self.side_timer = None
        self.last_side = None
        self.time_wait = 100
        self.id_ = Enemigo.id_
        Enemigo.id_ += 1
        while self._velocidad > 10:
            self._velocidad = int(self._velocidad / 2)
            self.time_wait = int(self.time_wait / 2)
            if self.time_wait <= 10:
                break
        parent.trigger_aumento_dificultad.connect(self.aumentar_dificultad)
        parent.trigger_recibir_explosion.connect(self.recibir_dano)
        parent.trigger_pausar.connect(self.pausar)
        parent.trigger_enemy_label_move.connect(self.move_label)
        parent.trigger_enemy_back.connect(self.move_back)
        self.start()

    @property
    def velocidad(self):
        ret =  self._velocidad
        for _ in range(self.nivel_dificultad):
            ret += 1.5
        return ret

    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        if value[0] > N or value[1] > N:
            return
        if value[0] < 0 or value[1] < 0:
            return
        self._pos = value

    @property
    def mid_pos(self):
        x, y = self._pos
        return x + self.sizex/2, y + self.sizey/2

    def set_pos(self, event):
        if event.id_ == self.id_:
            self._pos = (event.x, event.y)

    def aumentar_dificultad(self):
        self.nivel_dificultad += 1

    def change_direction(self):
        options = {"up", "down", "left", "right"}
        options.discard(self.side)
        self.side = choice(list(options))

    def die(self):
        self.die_signal.emit(self.id_)
        self.label.deleteLater()
        self.quit()
        # self.deleteLater()

    def pausar(self):
        if self.ready:
            self.ready = False
        else:
            self.ready = True

    def recibir_dano(self, e):
        if colision(self, e.espacio):
            self.vida -= 1
            self.add_points.emit(e.player)

    def move_label(self, e):
        if e.id_ == self.id_:
            self.label.move(e.x, e.y)
            self.label.hide()
            self.label.show()

    def move_back(self, e):
        if e.id_ == self.id_:
            x = self.label.x()
            y = self.label.y()
            self.pos = (x, y)

    def run(self):
        self.side_timer = 2
        while self.vida > 0:
            if self.ready:
                x, y = self.pos
                if self.side == "up":
                    self.pos = (x, y - self.velocidad)
                elif self.side == "down":
                    self.pos = (x, y + self.velocidad)
                elif self.side == "right":
                    self.pos = (x + self.velocidad, y)
                elif self.side == "left":
                    self.pos = (x - self.velocidad, y)
                self.move_enemy.emit(MoveEnemyEvent(self.x, self.y,
                                                    self.id_))
                self.side_timer -= self.time_wait/1000
                if self.side_timer <= 0:
                    self.change_direction()
                    self.side_timer = 2
            QTest.qWait(self.time_wait)
        self.die()


class EnemigoHostil(Enemigo):

    hostil_movement = pyqtSignal(MoveEnemyEvent)
    rango_vision_signal = pyqtSignal(RangoVisionEvent)

    def __init__(self, parent, x, y):
        super().__init__(parent, x, y, "assets/Hisoka.png")
        self.pixmap_hostil = QPixmap("assets/Hisoka_hostil.png")
        self.modo_hostil = False
        self.jugador_perseguido = None
        self.rango_vision = RANGO_VISION
        self.hostil_movement.connect(parent.hostil_movement)
        self.rango_vision_signal.connect(parent.revisar_rango_hostil)
        parent.trigger_activar_hostilidad.connect(self.cambiar_hostilidad)
        parent.trigger_enemy_way.connect(self.hostil_move)

    def cambiar_hostilidad(self, e):
        if e.id_ == self.id_:
            if e.player is False:
                self.label.setPixmap(self.pixmap)
                self.modo_hostil = False
                self.jugador_perseguido = None
            else:
                self.label.setPixmap(self.pixmap_hostil)
                self.modo_hostil = True
                self.jugador_perseguido = e.player

    def hostil_move(self, e):
        if e.id_ == self.id_:
            x, y = self.pos
            if e.side == "up":
                self.pos = (x, y - self.velocidad)
            elif e.side == "down":
                self.pos = (x, y + self.velocidad)
            elif e.side == "right":
                self.pos = (x + self.velocidad, y)
            elif e.side == "left":
                self.pos = (x - self.velocidad, y)
            x_, y_ = self.pos
            if (x_ != x or y_ != y) and e.side == self.last_side:
                self.last_side = None
            else:
                self.last_side = e.side
            self.move_enemy.emit(MoveEnemyEvent(self.x, self.y,
                                                self.id_))
            self.rango_vision_signal.emit(
                RangoVisionEvent(x_, y_, self.id_, self.rango_vision))

    def run(self):
        QTest.qWait(200)
        self.side_timer = 2
        while self.vida > 0:
            if self.ready:
                x, y = self.pos
                if self.modo_hostil:
                    self.hostil_movement.emit(
                        MoveEnemyEvent(self.x + self.sizex/2,
                                       self.y + self.sizey/2, self.id_,
                                       self.jugador_perseguido,
                                       self.last_side))
                else:
                    if self.side == "up":
                        self.pos = (x, y - self.velocidad)
                    elif self.side == "down":
                        self.pos = (x, y + self.velocidad)
                    elif self.side == "right":
                        self.pos = (x + self.velocidad, y)
                    elif self.side == "left":
                        self.pos = (x - self.velocidad, y)
                    self.move_enemy.emit(MoveEnemyEvent(self.x, self.y,
                                                        self.id_))
                    x_, y_ = self.mid_pos
                    self.rango_vision_signal.emit(
                        RangoVisionEvent(x_, y_, self.id_, self.rango_vision))
                    self.side_timer -= self.time_wait/1000
                    if self.side_timer <= 0:
                        self.change_direction()
                        self.side_timer = 2
            QTest.qWait(self.time_wait)
        self.die()


class GeneradorDeEnemigos(QThread):

    enviar_enemigos = pyqtSignal(RecibirEnemigoEvent)
    pedir_lugar_signal = pyqtSignal()
    aumentar_dificultad_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.enviar_enemigos.connect(parent.recibir_enemigos)
        self.pedir_lugar_signal.connect(parent.lugar_despliegue)
        self.aumentar_dificultad_signal.connect(
            parent.aumentar_dificultad_enemigos)
        parent.trigger_pausar.connect(self.pausar)
        self.ready = False
        self.aumentos_dificultad = 0
        self.contador_hostil = self.siguiente_hostil()
        self.contador_comun = self.siguiente_comun()
        self.next_x = None
        self.next_y = None
        self.parent = parent
        self.times = 0
        self.score_1 = 0
        self.score_2 = 0

    def actualizar_puntaje(self, e):
        if e.player == 1:
            self.score_1 = e.score
        else:
            self.score_2 = e.score
        total = self.score_1 + self.score_2 \
                - (self.aumentos_dificultad * AUMENTO_DIFICULTAD)
        if total > AUMENTO_DIFICULTAD:
            self.aumentos_dificultad += 1
            self.aumentar_dificultad_signal.emit()

    def pausar(self):
        if self.ready:
            self.ready = False
        else:
            self.ready = True

    def siguiente_hostil(self):
        parametro = LAMBDA_HOSTIL
        for _ in range(self.aumentos_dificultad):
            parametro /= 2
        ret = expovariate(parametro)
        return ret

    def siguiente_comun(self):
        parametro1 = A_NO_HOSTIL
        parametro2 = B_NO_HOSTIL
        for _ in range(self.aumentos_dificultad):
            parametro1 /= 2
            parametro2 /= 2
        ret = uniform(parametro1, parametro2)
        return ret

    def enemigos_iniciales(self):
        for _ in range(HOSTILES_INICIALES):
            self.pedir_lugar_despliegue()
            QTest.qWait(20)
            self.crear_hostil()
        for _ in range(COMUNES_INICIALES):
            self.pedir_lugar_despliegue()
            QTest.qWait(20)
            self.crear_comun()

    def crear_comun(self):
        if not self.next_x or not self.next_y:
            self.contador_comun = 1
            return
        QTest.qWait(20)
        self.enviar_enemigos.emit(RecibirEnemigoEvent(
            "comun", self.next_x, self.next_y))

    def pedir_lugar_despliegue(self):
        self.pedir_lugar_signal.emit()

    def cambiar_lugar(self, e):
        self.next_x = e.x
        self.next_y = e.y

    def crear_hostil(self):
        if not self.next_x or not self.next_y:
            self.contador_hostil = 1
            return
        QTest.qWait(20)
        self.enviar_enemigos.emit(RecibirEnemigoEvent(
            "hostil", self.next_x, self.next_y))

    def die(self):
        self.quit()

    def run(self):
        self.ready = True
        self.enemigos_iniciales()
        while True:
            self.times = 0
            if self.ready:
                self.contador_hostil -= 0.2
                self.contador_comun -= 0.2
                if self.contador_hostil <= 0:
                    self.contador_hostil = self.siguiente_hostil()
                    self.pedir_lugar_despliegue()
                    self.crear_hostil()
                    self.times += 20
                if self.contador_comun <= 0:
                    self.contador_comun = self.siguiente_comun()
                    self.pedir_lugar_despliegue()
                    self.crear_comun()
                    self.times += 20
            QTest.qWait(200 - self.times)
