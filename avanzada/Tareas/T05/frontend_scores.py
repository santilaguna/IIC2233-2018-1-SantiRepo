# módulo destinado a implementar la interfaz de los highscores

from PyQt5.QtWidgets import QLabel, QWidget, QApplication, \
    QPushButton, QLineEdit, QGridLayout
from parameters import N, MAPA_SIZE
from backend_scores import cargar_highscores, guardar_scores


class Scores(QWidget):

    def __init__(self, score_one=None, score_two=None):
        super().__init__()
        self.init_gui(score_one, score_two)

    def init_gui(self, score_one, score_two):
        self.setWindowTitle("Highest scores of CWF")
        self.setGeometry(400, 200, 500, 520)
        highscores = cargar_highscores()
        if score_two is not None:
            score = max([score_one, score_two], key=lambda x: x[1])
        else:
            score = score_one
        if score is not None:
            highscores.append(score)
            highscores.sort(key= lambda x: x[1], reverse=True)
        guardar_scores(highscores)
        currenty = 10
        for i in range(10):
            if highscores:
                name, score = highscores.pop(0)
                template = "{} - Nombre: {} - Puntuación: {}"
                new_label = QLabel(template.format(i + 1, name, score), self)
            else:
                new_label = QLabel("{} -".format(i + 1), self)
            new_label.setGeometry(20, currenty, 300, 40)
            currenty += 50
