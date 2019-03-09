# módulo destinado a implementar una

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPlainTextEdit, QListWidget
from PyQt5.QtCore import pyqtSignal
from eventos import MousePressed


class MyTextEdit(QPlainTextEdit):

    presionar_mouse = pyqtSignal(MousePressed)
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        font = QFont('SansSerif', 15)
        font.setPointSize(15)
        self.setFont(font)
        self.show()

    def mousePressEvent(self, e):
        self.presionar_mouse.emit(MousePressed(e.pos().x(), e.pos().y()))


class MyListWidget(QListWidget):

    presionar_texto = pyqtSignal()
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        font = QFont('SansSerif', 14)
        self.setFont(font)
        self.show()
