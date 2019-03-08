# módulo destinado a la interfaz del juego

from PyQt5.Qt import QTest, QProgressBar
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from parameters import N, MAPA_SIZE, CANT_VIDAS, AUMENTO_DIFICULTAD
from backend_players import PlayerOne, PlayerTwo
from backend_walls import back_walls, Espacio
from backend_bomb import Bomba, Explode
from frontend_scores import Scores
from eventos import SideMoveEvent, PositionMoveEvent, KeyEvent, \
    PlaceExplodeEvent, PowerUpEvent, MoveEnemyEvent, HostilidadEvent, \
    ScoreEvent, KickBombEvent
from compare import in_range, colisiones, bomb_space, casillas_afectadas, \
    find_label, specific_colision, kick_bomb, revisar_hostilidad, hostil_way, \
    pedir_celdas, colision, move_way
from backend_enemigos import GeneradorDeEnemigos, Enemigo, EnemigoHostil
import pixmaps as pix


class Game(QWidget):

    parent__show_signal = pyqtSignal()
    aumentar_puntaje__dificultad = pyqtSignal(ScoreEvent)
    trigger_aumento_dificultad = pyqtSignal()
    trigger_dano_enemigo_1 = pyqtSignal()
    trigger_dano_enemigo_2 = pyqtSignal()
    trigger_lugar_enemigo = pyqtSignal(PositionMoveEvent)
    trigger_sumar_enemigo_1 = pyqtSignal()
    trigger_sumar_enemigo_2 = pyqtSignal()
    trigger_sumar_pared_1 = pyqtSignal()
    trigger_sumar_pared_2 = pyqtSignal()
    trigger_pausar = pyqtSignal()
    trigger_recibir_explosion = pyqtSignal(PlaceExplodeEvent)
    trigger_power_one = pyqtSignal(PowerUpEvent)
    trigger_power_two = pyqtSignal(PowerUpEvent)
    trigger_initial_one = pyqtSignal(PositionMoveEvent)
    trigger_initial_two = pyqtSignal(PositionMoveEvent)
    trigger_move_player_one = pyqtSignal(SideMoveEvent)
    trigger_move_player_two = pyqtSignal(SideMoveEvent)
    trigger_bomb_one = pyqtSignal()
    trigger_bomb_two = pyqtSignal()
    trigger_no_explota1 = pyqtSignal()
    trigger_no_explota2 = pyqtSignal()
    trigger_enemy_label_move = pyqtSignal(MoveEnemyEvent)
    trigger_enemy_back = pyqtSignal(MoveEnemyEvent)
    trigger_activar_hostilidad = pyqtSignal(HostilidadEvent)
    trigger_enemy_way = pyqtSignal(SideMoveEvent)
    trigger_kick_bomb = pyqtSignal(KickBombEvent)
    trigger_stop_bomb = pyqtSignal(KickBombEvent)
    trigger_move_label_bomb = pyqtSignal(int)

    def __init__(self, name_one, name_two=None):
        super().__init__()
        self.letras = set()
        self.power_ups = []
        self.enemigos = {}
        self.bombas = []
        self.basurero = []
        self.walls, self.espacios_vacios = back_walls(self)
        self.generador_enemigos = GeneradorDeEnemigos(self)
        self.trigger_lugar_enemigo.connect(
            self.generador_enemigos.cambiar_lugar)
        self.aumentar_puntaje__dificultad.connect(
            self.generador_enemigos.actualizar_puntaje)

        self.setWindowTitle("Coding With Fire")
        self.setGeometry(100, 50, N + 300, N + 50)
        self.label_walls = self.set_walls()
        bomber1_pix = QPixmap("assets/bomberman.png")
        self.up_1_pixs = {1: bomber1_pix.copy(*pix.B1),
                          2: bomber1_pix.copy(*pix.B2),
                          3: bomber1_pix.copy(*pix.B3),
                          4: bomber1_pix.copy(*pix.B4),
                          5: bomber1_pix.copy(*pix.B5)}
        self.left_1_pixs = {1: bomber1_pix.copy(*pix.R1).transformed(
            QTransform().scale(-1, 1)),
            2: bomber1_pix.copy(*pix.R2).transformed(
                QTransform().scale(-1, 1)),
            3: bomber1_pix.copy(*pix.R3).transformed(
                QTransform().scale(-1, 1)),
            4: bomber1_pix.copy(*pix.R4).transformed(
                QTransform().scale(-1, 1)),
            5: bomber1_pix.copy(*pix.R5).transformed(
                QTransform().scale(-1, 1))}
        self.right_1_pixs = {1: bomber1_pix.copy(*pix.R1),
                             2: bomber1_pix.copy(*pix.R2),
                             3: bomber1_pix.copy(*pix.R3),
                             4: bomber1_pix.copy(*pix.R4),
                             5: bomber1_pix.copy(*pix.R5)}
        self.down_1_pixs = {1: bomber1_pix.copy(*pix.F1),
                            2: bomber1_pix.copy(*pix.F2),
                            3: bomber1_pix.copy(*pix.F3),
                            4: bomber1_pix.copy(*pix.F4),
                            5: bomber1_pix.copy(*pix.F5)}
        self.atack_1_pixs = {3: bomber1_pix.copy(*pix.A1),
                             2: bomber1_pix.copy(*pix.A2),
                             1: bomber1_pix.copy(*pix.A3)}

        bomber2_pix = QPixmap("assets/bomberman2.png")
        self.up_2_pixs = {1: bomber2_pix.copy(*pix.B1),
                          2: bomber2_pix.copy(*pix.B2),
                          3: bomber2_pix.copy(*pix.B3),
                          4: bomber2_pix.copy(*pix.B4),
                          5: bomber2_pix.copy(*pix.B5)}
        self.left_2_pixs = {1: bomber2_pix.copy(*pix.R1).transformed(
            QTransform().scale(-1, 1)),
            2: bomber2_pix.copy(*pix.R2).transformed(
                QTransform().scale(-1, 1)),
            3: bomber2_pix.copy(*pix.R3).transformed(
                QTransform().scale(-1, 1)),
            4: bomber2_pix.copy(*pix.R4).transformed(
                QTransform().scale(-1, 1)),
            5: bomber2_pix.copy(*pix.R5).transformed(
                QTransform().scale(-1, 1))}
        self.right_2_pixs = {1: bomber2_pix.copy(*pix.R1),
                             2: bomber2_pix.copy(*pix.R2),
                             3: bomber2_pix.copy(*pix.R3),
                             4: bomber2_pix.copy(*pix.R4),
                             5: bomber2_pix.copy(*pix.R5)}
        self.down_2_pixs = {1: bomber2_pix.copy(*pix.F1),
                            2: bomber2_pix.copy(*pix.F2),
                            3: bomber2_pix.copy(*pix.F3),
                            4: bomber2_pix.copy(*pix.F4),
                            5: bomber2_pix.copy(*pix.F5)}
        self.atack_2_pixs = {3: bomber2_pix.copy(*pix.A1),
                             2: bomber2_pix.copy(*pix.A2),
                             1: bomber2_pix.copy(*pix.A3)}

        self.set_stats_one(name_one)
        self.player_one = PlayerOne(self, name_one, N + 150, 10)
        self.label_player_one = QLabel("", self)
        self.label_player_one.setGeometry(N + 150, 10, 22, 35)
        self.label_player_one.setPixmap(self.down_1_pixs[3])
        self.trigger_initial_one.connect(self.player_one.set_pos)
        self.trigger_move_player_one.connect(self.player_one.move)
        self.trigger_bomb_one.connect(self.player_one.soltar_bomba)
        self.trigger_no_explota1.connect(self.player_one.no_explota)
        self.trigger_power_one.connect(self.player_one.catch_power_up)
        self.trigger_sumar_pared_1.connect(self.player_one.puntos_pared)
        self.trigger_sumar_enemigo_1.connect(
            self.player_one.puntos_enemigo)
        self.trigger_dano_enemigo_1.connect(self.player_one.impacto)
        if name_two:
            self.set_stats_two(name_two)
            self.player_two = PlayerTwo(self, name_two, N + 150, N / 2)
            self.label_player_two = QLabel("", self)
            self.label_player_two.setGeometry(N + 150, N / 2, 22, 35)
            self.label_player_two.setPixmap(self.down_2_pixs[3])
            self.trigger_initial_two.connect(self.player_two.set_pos)
            self.trigger_move_player_two.connect(self.player_two.move)
            self.trigger_bomb_two.connect(self.player_two.soltar_bomba)
            self.trigger_no_explota2.connect(self.player_two.no_explota)
            self.trigger_power_two.connect(self.player_two.catch_power_up)
            self.trigger_sumar_pared_2.connect(self.player_two.puntos_pared)
            self.trigger_sumar_enemigo_2.connect(
                self.player_two.puntos_enemigo)
            self.trigger_dano_enemigo_2.connect(self.player_two.impacto)
        else:
            self.player_two = None

        self.pause_button = QPushButton("Pausa", self)
        self.pause_button.setGeometry(N + 20, N + 10, 130, 40)
        self.pause_button.clicked.connect(self.pausa)
        self.back_botton = QPushButton("Salir", self)
        self.back_botton.setGeometry(N + 150, N + 10, 130, 40)
        self.back_botton.clicked.connect(self.back)
        self.setMouseTracking(True)
        self.moving_one = False
        self.moving_two = False
        self.started = False
        self.current2_pix = 1
        self.current2_way = 1  # -1 o 1
        self.current1_pix = 1
        self.current1_way = 1  # -1 o 1
        self.setFocusPolicy(Qt.StrongFocus)

    def set_walls(self):
        walls = []
        with open("mapa.txt") as file:
            currentx = 0
            currenty = 0
            size = N / MAPA_SIZE
            for line in file:
                new_walls = []
                line = line.replace(" ", "")
                for letter in line.strip():
                    if letter == "X":
                        wall = QLabel('', self)
                        wall.setGeometry(currentx, currenty, size, size)
                        wall.setScaledContents(True)
                        wall.setPixmap(QPixmap(
                            "assets/indestructible_wall.png"))
                        new_walls.append(wall)
                    elif letter == "P":
                        wall = QLabel('', self)
                        wall.setGeometry(currentx, currenty, size, size)
                        wall.setScaledContents(True)
                        wall.setPixmap(QPixmap(
                            "assets/destructible_wall.png"))
                        new_walls.append(wall)
                    else:
                        new_walls.append(None)
                    currentx += size
                currentx = 0
                currenty += size
                walls.append(new_walls)
        return walls

    def set_stats_one(self, nombre):
        self.label_nombre_1 = QLabel(nombre, self)
        self.label_nombre_1.setGeometry(N + 50, 10, 150, 30)
        self.labels_vidas_1 = []
        if CANT_VIDAS > 3:
            self.label_nvidas_1 = QLabel(str(CANT_VIDAS), self)
            self.label_nvidas_1.setGeometry(N + 30, 60, 40, 30)
        pixmap = QPixmap("assets/vida.png")
        currentx = N + 100
        tope = (min(CANT_VIDAS, 10))
        for i in range(tope):
            label = QLabel("", self)
            label.setGeometry(currentx, 60, 30, 30)
            label.setPixmap(pixmap.scaled(
                30, 30, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.labels_vidas_1.append(label)
            currentx += 150 / tope

        self.label_power_bombas_1 = QLabel("", self)
        self.label_power_bombas_1.setGeometry(N + 125, 100, 50, 50)
        self.label_power_bombas_1.setScaledContents(True)
        self.label_power_bombas_1.setPixmap(
            QPixmap("assets/mas_bombas.png"))
        self.label_bombas_1 = QLabel("", self)
        self.label_bombas_1.setGeometry(N + 75, 100, 50, 50)
        self.label_power_bombas_1.hide()
        self.label_power_velocidad_1 = QLabel("", self)
        self.label_power_velocidad_1.setGeometry(N + 50, 180, 50, 50)
        self.label_power_velocidad_1.setScaledContents(True)
        self.label_power_velocidad_1.setPixmap(
            QPixmap("assets/velocidad.png"))
        self.label_power_velocidad_1.hide()
        self.label_power_super_1 = QLabel("", self)
        self.label_power_super_1.setGeometry(N + 125, 180, 50, 50)
        self.label_power_super_1.setScaledContents(True)
        self.label_power_super_1.setPixmap(
            QPixmap("assets/supervelocidad.png"))
        self.label_power_super_1.hide()
        self.label_power_jugger_1 = QLabel("", self)
        self.label_power_jugger_1.setGeometry(N + 200, 180, 50, 50)
        self.label_power_jugger_1.setScaledContents(True)
        self.label_power_jugger_1.setPixmap(
            QPixmap("assets/juggernaut.png"))
        self.label_power_jugger_1.hide()

        self.score_bar_1 = QProgressBar(self)
        self.score_bar_1.setRange(0, AUMENTO_DIFICULTAD)
        self.score_bar_1.setGeometry(100, N + 10, N/2 - 150, 30)
        self.score_bar_1.setValue(0)

        self.label_score_1 = QLabel("Score P1", self)
        self.label_score_1.setGeometry(30, N + 10, 80, 30)


    def show_power(self, e):
        tipo = e.tipo
        if tipo == "velocidad":
            if e.player == 1:
                self.label_power_velocidad_1.show()
            else:
                self.label_power_velocidad_2.show()
        elif tipo == "bombas":
            if e.player == 1:
                self.label_power_bombas_1.show()
                self.label_bombas_1.setText(str(e.cantidad))
            else:
                self.label_power_bombas_2.show()
                self.label_bombas_2.setText(str(e.cantidad))
        elif tipo == "super":
            if e.player == 1:
                self.label_power_super_1.show()
            else:
                self.label_power_super_2.show()
        else:
            if e.player == 1:
                self.label_power_jugger_1.show()
            else:
                self.label_power_jugger_2.show()

    def hide_power(self, e):
        tipo = e.tipo
        if tipo == "super":
            if e.player == 1:
                self.label_power_super_1.hide()
            else:
                self.label_power_super_2.hide()
        else:
            if e.player == 1:
                self.label_power_jugger_1.hide()
            else:
                self.label_power_jugger_2.hide()

    def set_stats_two(self, nombre):
        self.label_nombre_2 = QLabel(nombre, self)
        self.label_nombre_2.setGeometry(N + 50, N / 2, 150, 30)
        self.labels_vidas_2 = []
        if CANT_VIDAS > 3:
            self.label_nvidas_2 = QLabel(str(CANT_VIDAS), self)
            self.label_nvidas_2.setGeometry(N + 30, 50 + N / 2, 40, 30)
        pixmap = QPixmap("assets/vida.png")
        currentx = N + 100
        tope = (min(CANT_VIDAS, 10))
        for i in range(tope):
            label = QLabel("", self)
            label.setGeometry(currentx, 50 + N / 2, 30, 30)
            label.setPixmap(pixmap.scaled(
                30, 30, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.labels_vidas_2.append(label)
            currentx += 150 / tope

        self.label_power_bombas_2 = QLabel("", self)
        self.label_power_bombas_2.setGeometry(N + 125, 100 + N / 2, 50, 50)
        self.label_power_bombas_2.setScaledContents(True)
        self.label_power_bombas_2.setPixmap(
            QPixmap("assets/mas_bombas.png"))
        self.label_bombas_2 = QLabel("", self)
        self.label_bombas_2.setGeometry(N + 75, 100 + N / 2, 50, 50)
        self.label_power_bombas_2.hide()
        self.label_power_velocidad_2 = QLabel("", self)
        self.label_power_velocidad_2.setGeometry(N + 50, 180 + N / 2, 50, 50)
        self.label_power_velocidad_2.setScaledContents(True)
        self.label_power_velocidad_2.setPixmap(
            QPixmap("assets/velocidad.png"))
        self.label_power_velocidad_2.hide()
        self.label_power_super_2 = QLabel("", self)
        self.label_power_super_2.setGeometry(N + 125, 180 + N / 2, 50, 50)
        self.label_power_super_2.setScaledContents(True)
        self.label_power_super_2.setPixmap(
            QPixmap("assets/supervelocidad.png"))
        self.label_power_super_2.hide()
        self.label_power_jugger_2 = QLabel("", self)
        self.label_power_jugger_2.setGeometry(N + 200, 180 + N / 2, 50, 50)
        self.label_power_jugger_2.setScaledContents(True)
        self.label_power_jugger_2.setPixmap(
            QPixmap("assets/juggernaut.png"))
        self.label_power_jugger_2.hide()

        self.score_bar_2 = QProgressBar(self)
        self.score_bar_2.setRange(0, AUMENTO_DIFICULTAD)
        self.score_bar_2.setGeometry(N/2 + 100, N + 10, N/2 - 150, 30)
        self.score_bar_2.setValue(0)
        self.label_score_2 = QLabel("Score P2", self)
        self.label_score_2.setGeometry(N/2 + 30, N + 10, 80, 30)

    def keyPressEvent(self, e):
        letter = e.key()
        self.letras.add(letter)
        if Qt.Key_Control in self.letras:
            if Qt.Key_E in self.letras:
                self.back()
            elif Qt.Key_P in self.letras:
                self.pausa()
        if self.started:
            if self.player_two is not None:
                if Qt.Key_W in self.letras:
                    self.current2_pix += self.current2_way
                    self.label_player_two.setPixmap(self.up_2_pixs[
                                                        self.current2_pix])
                    if self.current2_pix == 5:
                        self.current2_way = -1
                    elif self.current2_pix == 1:
                        self.current2_way = 1
                    self.trigger_move_player_two.emit(SideMoveEvent("up"))
                elif Qt.Key_A in self.letras:
                    self.current2_pix += self.current2_way
                    self.label_player_two.setPixmap(self.left_2_pixs[
                                                        self.current2_pix])
                    if self.current2_pix == 5:
                        self.current2_way = -1
                    elif self.current2_pix == 1:
                        self.current2_way = 1
                    self.trigger_move_player_two.emit(SideMoveEvent("left"))
                elif Qt.Key_S in self.letras:
                    self.current2_pix += self.current2_way
                    self.label_player_two.setPixmap(self.down_2_pixs[
                                                        self.current2_pix])
                    if self.current2_pix == 5:
                        self.current2_way = -1
                    elif self.current2_pix == 1:
                        self.current2_way = 1
                    self.trigger_move_player_two.emit(SideMoveEvent("down"))
                elif Qt.Key_D in self.letras:
                    self.current2_pix += self.current2_way
                    self.label_player_two.setPixmap(self.right_2_pixs[
                                                        self.current2_pix])
                    if self.current2_pix == 5:
                        self.current2_way = -1
                    elif self.current2_pix == 1:
                        self.current2_way = 1
                    self.trigger_move_player_two.emit(SideMoveEvent("right"))
                if Qt.Key_F == letter:
                    self.label_player_two.setPixmap(self.atack_2_pixs[1])
                    self.label_player_two.setPixmap(self.atack_2_pixs[2])
                    self.label_player_two.setPixmap(self.atack_2_pixs[3])
                    self.trigger_bomb_two.emit()
                    self.label_player_two.setPixmap(self.atack_2_pixs[2])
                    self.label_player_two.setPixmap(self.atack_2_pixs[1])
                    self.label_player_two.setPixmap(self.down_2_pixs[3])

            if Qt.Key_Up in self.letras:
                self.current1_pix += self.current1_way
                self.label_player_one.setPixmap(self.up_1_pixs[
                                                    self.current1_pix])
                if self.current1_pix == 5:
                    self.current1_way = -1
                elif self.current1_pix == 1:
                    self.current1_way = 1
                self.trigger_move_player_one.emit(SideMoveEvent("up"))
            elif Qt.Key_Left in self.letras:
                self.current1_pix += self.current1_way
                self.label_player_one.setPixmap(self.left_1_pixs[
                                                    self.current1_pix])
                if self.current1_pix == 5:
                    self.current1_way = -1
                elif self.current1_pix == 1:
                    self.current1_way = 1
                self.trigger_move_player_one.emit(SideMoveEvent("left"))
            elif Qt.Key_Down in self.letras:
                self.current1_pix += self.current1_way
                self.label_player_one.setPixmap(self.down_1_pixs[
                                                    self.current1_pix])
                if self.current1_pix == 5:
                    self.current1_way = -1
                elif self.current1_pix == 1:
                    self.current1_way = 1
                self.trigger_move_player_one.emit(SideMoveEvent("down"))
            elif Qt.Key_Right in self.letras:
                self.current1_pix += self.current1_way
                self.label_player_one.setPixmap(self.right_1_pixs[
                                                    self.current1_pix])
                if self.current1_pix == 5:
                    self.current1_way = -1
                elif self.current1_pix == 1:
                    self.current1_way = 1
                self.trigger_move_player_one.emit(SideMoveEvent("right"))
            if Qt.Key_Space == letter:
                self.label_player_one.setPixmap(self.atack_1_pixs[1])
                self.label_player_one.setPixmap(self.atack_1_pixs[2])
                self.label_player_one.setPixmap(self.atack_1_pixs[3])
                self.trigger_bomb_one.emit()
                self.label_player_one.setPixmap(self.atack_1_pixs[2])
                self.label_player_one.setPixmap(self.atack_1_pixs[1])
                self.label_player_one.setPixmap(self.down_1_pixs[3])

    def keyReleaseEvent(self, e):
        letter = e.key()
        self.letras.discard(letter)
        if self.started:
            if self.player_two is not None:
                if Qt.Key_W == letter:
                    self.trigger_move_player_two.emit(SideMoveEvent(None))
                elif Qt.Key_A == letter:
                    self.trigger_move_player_two.emit(SideMoveEvent(None))
                elif Qt.Key_S == letter:
                    self.trigger_move_player_two.emit(SideMoveEvent(None))
                elif Qt.Key_D == letter:
                    self.trigger_move_player_two.emit(SideMoveEvent(None))
                elif Qt.Key_F == letter:
                    self.trigger_move_player_two.emit(SideMoveEvent(None))
            if Qt.Key_Up == letter:
                self.trigger_move_player_one.emit(SideMoveEvent(None))
            elif Qt.Key_Left == letter:
                self.trigger_move_player_one.emit(SideMoveEvent(None))
            elif Qt.Key_Down == letter:
                self.trigger_move_player_one.emit(SideMoveEvent(None))
            elif Qt.Key_Right == letter:
                self.trigger_move_player_one.emit(SideMoveEvent(None))
            elif Qt.Key_Space == letter:
                self.trigger_move_player_two.emit(SideMoveEvent(None))
        while self.letras:
            self.keyPressEvent(KeyEvent(self.letras.pop()))
            QTest.qWait(100)

    def mousePressEvent(self, e):
        """As seen at: https://stackoverflow.com/questions/43453562/
        interaction-between-mousepressevent-and-paintevent-methods"""
        if not self.started:
            if in_range(e.pos().x(), N + 150, N + 173) and \
                    in_range(e.pos().y(), 10, 51):
                self.moving_one = True
            elif in_range(e.pos().x(), N + 150, N + 173) and \
                    in_range(e.pos().y(), N / 2, N / 2 + 41):
                if self.player_two is not None:
                    self.moving_two = True

    def mouseReleaseEvent(self, e):
        if not self.started:
            x = e.pos().x()
            y = e.pos().y()
            if self.moving_one:
                self.trigger_initial_one.emit(PositionMoveEvent(x, y))
            elif self.moving_two:
                self.trigger_initial_two.emit(PositionMoveEvent(x, y))

    def player_release(self, e):
        if self.moving_one:
            if colisiones(self.player_one, self.walls):
                self.trigger_initial_one.emit(
                    PositionMoveEvent(N + 150, 10, True))
                self.label_player_one.move(N + 150, 10)
                self.moving_one = False
                return
            if e.ready:
                if self.player_two is not None:
                    if self.player_two.ready:
                        self.startgame()
                else:
                    self.startgame()
            else:
                self.label_player_one.move(N + 150, 10)
            self.moving_one = False
        elif self.moving_two:
            if colisiones(self.player_two, self.walls):
                self.trigger_initial_two.emit(
                    PositionMoveEvent(N + 150, N / 2, True))
                self.label_player_two.move(N + 150, N / 2)
                self.moving_two = False
                return
            if e.ready:
                if self.player_one.ready:
                    self.startgame()
            else:
                self.label_player_two.move(N + 150, N / 2)
            self.moving_two = False

    def mouseMoveEvent(self, e):
        if not self.started:
            if self.moving_one:
                self.label_player_one.move(e.pos().x(), e.pos().y())
            elif self.moving_two:
                self.label_player_two.move(e.pos().x(), e.pos().y())

    def move_player_one(self, e):
        if self.started:
            if colisiones(self.player_one, self.walls):
                x = self.label_player_one.x()
                y = self.label_player_one.y()
                self.trigger_initial_one.emit((PositionMoveEvent(x, y)))
                return
            elif colisiones(self.player_one, self.enemigos.values()):
                x = self.label_player_one.x()
                y = self.label_player_one.y()
                self.trigger_initial_one.emit((PositionMoveEvent(x, y)))
                self.trigger_dano_enemigo_1.emit()
                return
            bomba = kick_bomb(self.player_one, self.bombas)
            if bomba:
                way, id_ = move_way(self.player_one, bomba)
                self.trigger_kick_bomb.emit(KickBombEvent(way, id_))
            power = specific_colision(self.player_one, self.power_ups)
            if power:
                self.trigger_power_one.emit(PowerUpEvent(power))
                self.power_ups.remove(power)
                power.catched()
            self.label_player_one.move(e.x, e.y)

    def move_player_two(self, e):
        if self.started:
            if colisiones(self.player_two, self.walls):
                x = self.label_player_two.x()
                y = self.label_player_two.y()
                self.trigger_initial_two.emit((PositionMoveEvent(x, y)))
                return
            elif colisiones(self.player_two, self.enemigos.values()):
                x = self.label_player_two.x()
                y = self.label_player_two.y()
                self.trigger_initial_two.emit((PositionMoveEvent(x, y)))
                self.trigger_dano_enemigo_2.emit()
                return
            bomba = kick_bomb(self.player_two, self.bombas)
            if bomba:
                way, id_ = move_way(self.player_two, bomba)
                self.trigger_kick_bomb.emit(KickBombEvent(way, id_))
            power = specific_colision(self.player_two, self.power_ups)
            if power:
                self.trigger_power_two.emit(PowerUpEvent(power))
                power.catched()
            self.label_player_two.move(e.x, e.y)

    def move_enemy(self, e):
        enemigo = self.enemigos[e.id_]
        if colisiones(enemigo, self.walls) or colisiones(enemigo, self.bombas):
            self.trigger_enemy_back.emit(MoveEnemyEvent(e.x, e.y, e.id_))
        elif colision(enemigo, self.player_one):
            self.trigger_enemy_back.emit(MoveEnemyEvent(e.x, e.y, e.id_))
            self.trigger_dano_enemigo_1.emit()
        elif self.player_two is not None:
            if colision(enemigo, self.player_two):
                self.trigger_enemy_back.emit(MoveEnemyEvent(e.x, e.y, e.id_))
                self.trigger_dano_enemigo_2.emit()
            else:
                self.trigger_enemy_label_move.emit(MoveEnemyEvent(
                    e.x, e.y, e.id_))
        else:
            self.trigger_enemy_label_move.emit(MoveEnemyEvent(
                e.x, e.y, e.id_))

    def move_bomb(self, e):
        bomba_ = filter(lambda b: b.id_ == e.id_, self.bombas)
        bomb = next(bomba_)
        if colisiones(bomb, self.enemigos.values()) or \
                colisiones(bomb, self.walls):
            self.trigger_stop_bomb.emit(KickBombEvent(None, e.id_))
        elif colision(self.player_one, bomb):
            self.trigger_stop_bomb.emit(KickBombEvent(None, e.id_))
        elif self.player_two is not None:
            if colision(self.player_two, bomb):
                self.trigger_stop_bomb.emit(KickBombEvent(None, e.id_))
        self.trigger_move_label_bomb.emit(e.id_)

    def revisar_rango_hostil(self, e):
        player = revisar_hostilidad(e, self.player_one, self.player_two)
        if player:
            self.trigger_activar_hostilidad.emit(HostilidadEvent(e.id_,
                                                                 player))
        else:
            self.trigger_activar_hostilidad.emit(HostilidadEvent(e.id_,
                                                                 player))

    def hostil_movement(self, e):
        if e.player == 1:
            side = hostil_way(e.x, e.y, self.player_one, e.last_side)
        else:
            side = hostil_way(e.x, e.y, self.player_two, e.last_side)
        self.trigger_enemy_way.emit(SideMoveEvent(side, e.id_))

    def recibir_enemigos(self, e):
        if e.tipo == "hostil":
            enemigo = EnemigoHostil(self, e.x, e.y)
        else:
            enemigo = Enemigo(self, e.x, e.y)
        self.enemigos[enemigo.id_] = enemigo

    def muere_enemigo(self, id_):
        if id_ in self.enemigos:
            self.basurero.append(self.enemigos[id_])
            del self.enemigos[id_]

    def bomb_release(self, e):
        bomba = Bomba(self, e.x, e.y, e.player)
        space = bomb_space(bomba, self.espacios_vacios)
        if space:
            bomba.encasillar(*space.pos)
            self.bombas.append(bomba)
        else:
            if e.player == 1:
                self.trigger_no_explota1.emit()
            elif e.player == 2:
                self.trigger_no_explota2.emit()

    def bomb_explode(self, e):
        casillas = casillas_afectadas(e, self.espacios_vacios, self.walls)
        for casilla in casillas:
            if isinstance(casilla, Espacio):
                self.explotar_espacio(casilla, e.player)
            else:
                self.detruir_pared(casilla, e.player)
        self.basurero.append(e.bomba)
        self.bombas.remove(e.bomba)

    def detruir_pared(self, pared, player):
        if player == 1:
            self.trigger_sumar_pared_1.emit()
        else:
            self.trigger_sumar_pared_2.emit()
        espacio = Espacio(self, pared.x, pared.y, pared.sizex, True)
        pared.deleteLater()
        self.walls.remove(pared)
        self.espacios_vacios.append(espacio)
        label = find_label(self.label_walls, pared.sizex, *pared.pos)
        label.deleteLater()

    def explotar_espacio(self, casilla, player):
        casilla.ocupado = False
        explode = Explode(self, casilla.x, casilla.y)
        explode.start()
        self.trigger_recibir_explosion.emit(PlaceExplodeEvent(casilla, player))

    def add_enemy_points(self, player):
        if player == 1:
            self.trigger_sumar_enemigo_1.emit()
        else:
            self.trigger_sumar_enemigo_2.emit()

    def cambiar_vida(self, e):
        if e.player == 1:
            if CANT_VIDAS > 3:
                if e.vidas > 10:
                    self.label_nvidas_1.setText(str(e.vidas))
                elif e.vidas == 10:
                    self.label_nvidas_1.setText("")
                    if e.cambio == -1:
                        label = self.labels_vidas_1[9]
                        label.show()
                        label.setVisible(True)
            else:
                if e.cambio == 1:
                    label = self.labels_vidas_1[e.vidas - 1]
                    label.show()
                    label.setVisible(True)
                elif e.cambio == -1:
                    label = self.labels_vidas_1[e.vidas]
                    label.hide()
                    label.setVisible(False)
        elif e.player == 2:
            if CANT_VIDAS > 3:
                if e.vidas > 10:
                    self.label_nvidas_2.setText(str(e.vidas))
                elif e.vidas == 10:
                    self.label_nvidas_2.setText("")
                    if e.cambio == -1:
                        label = self.labels_vidas_2[9]
                        label.show()
                        label.setVisible(True)
            else:
                if e.cambio == 1:
                    label = self.labels_vidas_2[e.vidas - 1]
                    label.show()
                    label.setVisible(True)
                elif e.cambio == -1:
                    label = self.labels_vidas_2[e.vidas]
                    label.hide()
                    label.setVisible(False)

    def lugar_despliegue(self):
        x, y = pedir_celdas(self.espacios_vacios, self.enemigos.values(),
                            self.player_one, self.player_two)
        self.trigger_lugar_enemigo.emit(PositionMoveEvent(x, y))

    def power_up(self, e):
        self.power_ups.append(e.power_up)

    def remove_power_up(self, power):
        if power in self.power_ups:
            self.power_ups.remove(power)

    def actualizar_puntaje(self, e):
        if e.player == 1:
            label_score = e.score
            while label_score > AUMENTO_DIFICULTAD:
                label_score -= AUMENTO_DIFICULTAD
            self.score_bar_1.setValue(label_score)
            self.aumentar_puntaje__dificultad.emit(e)
        else:
            label_score = e.score
            while label_score > AUMENTO_DIFICULTAD:
                label_score -= AUMENTO_DIFICULTAD
            self.score_bar_2.setValue(label_score)
            self.aumentar_puntaje__dificultad.emit(e)

    def aumentar_dificultad_enemigos(self):
        self.trigger_aumento_dificultad.emit()

    def startgame(self):
        self.started = True
        self.player_one.start()
        if self.player_two is not None:
            self.player_two.start()
        self.generador_enemigos.start()

    def pausa(self):
        if self.started:
            self.trigger_pausar.emit()

    def dead_player(self, player):
        if player == 1:
            if self.player_two is not None:
                if self.player_two.vida > 0:
                    self.label_player_one.hide()
                else:
                    self.show_scores()
            else:
                self.show_scores()
        else:
            if self.player_one.vida > 0:
                self.label_player_two.hide()
            else:
                self.show_scores()

    def show_scores(self):
        self.pausa()
        score_1 = [self.player_one.name, self.player_one.score]
        if self.player_two is None:
            score_2 = None
        else:
            score_2 = [self.player_two.name, self.player_two.score]

        self.scores = Scores(score_1, score_2)
        self.hide()
        self.scores.show()

    def back(self):
        """As seen at: https://stackoverflow.com/questions/45098161/
        back-to-previous-window"""
        self.pausa()
        score_1 = [self.player_one.name, self.player_one.score]
        if self.player_two is None:
            score_2 = None
        else:
            score_2 = [self.player_two.name, self.player_two.score]

        self.scores = Scores(score_1, score_2)
        self.hide()
        self.parent__show_signal.emit()
