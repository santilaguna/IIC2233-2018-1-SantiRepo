# módulo destinado a la visualización de la interfaz gráfica.

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QApplication,\
    QPushButton, QLineEdit, QGridLayout
from frontend_game import Game
from frontend_scores import Scores
import sys


class GameMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("CWF Game Menu")
        self.setGeometry(400, 250, 200, 200)

        self.start_button = QPushButton('Start', self)
        self.highscores_button = QPushButton("Highscores", self)
        self.quit_button = QPushButton("Salir del juego", self)

        self.grilla = QGridLayout()

        self.grilla.addWidget(self.start_button)
        self.grilla.addWidget(self.highscores_button)
        self.grilla.addWidget(self.quit_button)

        self.setLayout(self.grilla)

        self.start_button.clicked.connect(self.start)
        self.highscores_button.clicked.connect(self.show_highscores)
        self.quit_button.clicked.connect(self.close)

    def start(self):
        self.screen = StartMenu()
        self.screen.parent__show_signal.connect(self.menu_principal)
        self.hide()
        self.screen.show()

    def show_highscores(self):
        self.scores_screen = Scores()
        self.hide()
        self.edit = QLineEdit("", self)
        self.scores_screen.show()

    def menu_principal(self):
        self.show()

    def close(self):
        sys.exit()


class StartMenu(QWidget):

    parent__show_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("CWF Start Menu")
        self.setGeometry(400, 250, 200, 200)

        self.one_button = QPushButton('1 Player', self)
        self.label1 = QLabel("Ingrese nombre jugador 1", self)
        self.edit1 = QLineEdit("Jugador 1", self)
        self.two_button = QPushButton("2 Players", self)
        self.label2 = QLabel("Ingrese nombre jugador 2", self)
        self.edit2 = QLineEdit("Jugador 2", self)
        self.start_button = QPushButton("Start", self)

        self.grilla = QGridLayout()

        self.grilla.addWidget(self.one_button)
        self.grilla.addWidget(self.label1)
        self.grilla.addWidget(self.edit1)
        self.grilla.addWidget(self.two_button)
        self.grilla.addWidget(self.label2)
        self.grilla.addWidget(self.edit2)
        self.grilla.addWidget(self.start_button)

        self.label1.hide()
        self.edit1.hide()
        self.label2.hide()
        self.edit2.hide()
        self.start_button.hide()

        self.setLayout(self.grilla)

        self.start_button.clicked.connect(self.start)
        self.one_button.clicked.connect(self.one_player)
        self.two_button.clicked.connect(self.two_players)

    def start(self):
        if self.label2.isHidden():
            text = self.edit1.text()
            if not text:
                return
            self.screen = Game(text)
        else:
            text_1 = self.edit1.text()
            text_2 = self.edit2.text()
            if not text_2 or not text_1:
                return
            self.screen = Game(text_1, text_2)
        self.hide()
        self.screen.parent__show_signal.connect(self.menu_principal)
        self.screen.show()

    def one_player(self):
        self.one_button.hide()
        self.two_button.hide()
        self.label1.show()
        self.edit1.show()
        self.start_button.show()
        self.grilla.update()

    def two_players(self):
        self.one_button.hide()
        self.two_button.hide()
        self.label1.show()
        self.edit1.show()
        self.label2.show()
        self.edit2.show()
        self.start_button.show()
        self.grilla.update()

    def menu_principal(self):
        self.parent__show_signal.emit()


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(value)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    mi_juego = GameMenu()
    mi_juego.show()
    app.exec()
