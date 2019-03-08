# módulo destinado a funcionalidades de los personajes.

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.Qt import QTest
from eventos import PositionMoveEvent, ReleaseEvent, BombEvent, \
    CambiarVidaEvent, LabelPowerEvent, ScoreEvent
from parameters import N, CANT_VIDAS, TIEMPO, PUNTAJE_TIEMPO, \
    VEL_MOVIMIENTO, TIEMPO_EXPLOSION, TIEMPO_INMUNE, MAPA_SIZE, PUNTAJE_MURO, \
    PUNTAJE_ENEMIGO
from compare import colision


class Player(QThread):

    dead_signal = pyqtSignal(int)
    release_bomb = pyqtSignal(BombEvent)
    cambiar_vida = pyqtSignal(CambiarVidaEvent)
    show_power = pyqtSignal(LabelPowerEvent)
    hide_power = pyqtSignal(LabelPowerEvent)
    score_signal = pyqtSignal(ScoreEvent)

    def __init__(self, parent, name, x, y, *args, **kwargs):
        super().__init__()
        self.player = 1
        self.name = name
        self._score = 0
        self.sizex = 22
        self.sizey = 35
        self._pos = (x - self.sizex/2, y - self.sizey/2)
        self.ready = False
        self._vida = CANT_VIDAS
        self.moving = False
        self.juggernaut = False
        self.rapidin = False
        self.max_bombas = 1
        self.aumento_velocidad = 1
        self.current_bombas = 0
        self.dead_signal.connect(parent.dead_player)
        self.release_bomb.connect(parent.bomb_release)
        self.cambiar_vida.connect(parent.cambiar_vida)
        self.show_power.connect(parent.show_power)
        self.hide_power.connect(parent.hide_power)
        self.score_signal.connect(parent.actualizar_puntaje)
        parent.trigger_pausar.connect(self.pausar)
        parent.trigger_recibir_explosion.connect(self.recibir_dano)
        self.contador_rapidin = None
        self.contador_jugger = None
        self.contador_tiempo = TIEMPO
        self.velocidad = VEL_MOVIMIENTO
        self.time_wait = 100
        self.current_timer = None
        while self.velocidad > 10:
            self.velocidad = int(self.velocidad / 2)
            self.time_wait = int(self.time_wait / 2)
            if self.time_wait <= 10:
                break

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.score_signal.emit(ScoreEvent(value, self.player))

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, value):
        if value > CANT_VIDAS:
            self._vida = CANT_VIDAS
        else:
            self._vida = value

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

    def pausar(self):
        if self.ready:
            self.ready = False
        else:
            self.ready = True

    def set_pos(self, event):
        if event.release:
            self._pos = (event.x, event.y)
        initial = self.pos
        self.pos = (event.x, event.y)
        if self.pos != initial:
            self.ready = True
            self.player_ready.emit(ReleaseEvent(True))
        else:
            self.player_ready.emit(ReleaseEvent(False))

    def soltar_bomba(self):
        if self.current_bombas < self.max_bombas:
            self.release_bomb.emit(BombEvent(self.x + self.sizex / 2,
                                             self.y + self.sizey / 2,
                                             self.player))
            self.current_bombas += 1
            self.explota_bomba()

    def explota_bomba(self):
        if self.current_timer:
            self.current_timer.stop()
            self.current_timer.deleteLater()
            self.current_timer = QTimer()
            self.current_timer.timeout.connect(self.final_timer)
            self.current_timer.setSingleShot(True)
            self.current_timer.start(1000 * TIEMPO_EXPLOSION)
        else:
            self.current_timer = QTimer()
            self.current_timer.timeout.connect(self.initial_timer)
            self.current_timer.setSingleShot(True)
            self.current_timer.start(1000 * TIEMPO_EXPLOSION)

    def final_timer(self):
        self.current_bombas = 0
        self.current_timer = None

    def initial_timer(self):
        self.current_bombas -= 1
        self.current_timer = None

    def catch_power_up(self, e):
        tipo = e.power_up.tipo
        if tipo == "vida":
            self.aumentar_vida()
        elif tipo == "velocidad":
            self.aumento_velocidad = e.power_up.multiplicador
            self.show_power.emit(LabelPowerEvent("velocidad", self.player))
        elif tipo == "bombas":
            self.max_bombas += 1
            self.show_power.emit(LabelPowerEvent("bombas", self.player,
                                                 self.max_bombas))
        elif tipo == "super":
            self.volverse_rapidin(e.power_up.tiempo)
            self.show_power.emit(LabelPowerEvent("super", self.player))
        else:
            self.volverse_inmune(e.power_up.tiempo)

    def puntos_pared(self):
        self.score += PUNTAJE_MURO

    def puntos_enemigo(self):
        self.score += PUNTAJE_ENEMIGO

    def impacto(self):
        if not self.juggernaut:
            self.volverse_inmune(TIEMPO_INMUNE)
            self.vida -= 1
            self.cambiar_vida.emit(CambiarVidaEvent(self.player, -1,
                                                    self.vida))

    def recibir_dano(self, e):
        if colision(self, e.espacio):
            self.impacto()

    def volverse_rapidin(self, tiempo):
        self.rapidin = True
        self.time_wait = int(self.time_wait / 3)
        self.contador_rapidin = tiempo

    def volverse_lento(self):
        self.time_wait *= 3
        self.rapidin = False
        self.hide_power.emit(LabelPowerEvent("super", self.player))

    def volverse_inmune(self, tiempo):
        self.juggernaut = True
        self.show_power.emit(LabelPowerEvent("jugger", self.player))
        self.contador_jugger = tiempo

    def volverse_mortal(self):
        self.juggernaut = False
        self.hide_power.emit(LabelPowerEvent("jugger", self.player))

    def aumentar_vida(self):
        initial = self.vida
        self.vida += 1
        if initial != self.vida:
            self.cambiar_vida.emit(CambiarVidaEvent(self.player, 1,
                                                    self.vida))

    def no_explota(self):
        self.current_bombas -= 1

    def run(self):
        """As seen at: https://github.com/IIC2233/Syllabus/blob/
        master/Ayudantias/Ayudantia%2010/back_end.py and https://github.com/
        IIC2233/Syllabus/blob/master/Ayudantias/Ayudantia%2010/front_end.py"""
        while self.vida > 0:
            if self.ready:
                x, y = self.pos
                velocidad = self.velocidad * self.aumento_velocidad
                if self.rapidin:
                    self.contador_rapidin -= self.time_wait / 1000
                    if self.contador_rapidin <= 0:
                        self.volverse_lento()
                if self.moving == "up":
                    self.pos = (x, y - velocidad)
                elif self.moving == "down":
                    self.pos = (x, y + velocidad)
                elif self.moving == "right":
                    self.pos = (x + velocidad, y)
                elif self.moving == "left":
                    self.pos = (x - velocidad, y)
                self.move_player.emit(PositionMoveEvent(self.x, self.y))
                if self.juggernaut:
                    self.contador_jugger -= self.time_wait / 1000
                    if self.contador_jugger <= 0:
                        self.volverse_mortal()
                self.contador_tiempo -= self.time_wait / 1000
                if self.contador_tiempo <= 0:
                    self.score += PUNTAJE_TIEMPO
                    self.contador_tiempo = TIEMPO
            QTest.qWait(self.time_wait)

        self.dead_signal.emit(self.player)
        self.max_bombas = 0
        self.ready = False
        self.quit()


class PlayerOne(Player):
    move_player = pyqtSignal(PositionMoveEvent)
    player_ready = pyqtSignal(ReleaseEvent)

    def __init__(self, parent, name, x, y):
        super().__init__(parent, name, x, y)
        self.move_player.connect(parent.move_player_one)
        self.player_ready.connect(parent.player_release)

    def move(self, e):
        self.moving = e.side


class PlayerTwo(Player):
    move_player = pyqtSignal(PositionMoveEvent)
    player_ready = pyqtSignal(ReleaseEvent)

    def __init__(self, parent, name, x, y):
        super().__init__(parent, name, x, y)
        self.player = 2
        self.move_player.connect(parent.move_player_two)
        self.player_ready.connect(parent.player_release)

    def move(self, e):
        self.moving = e.side
