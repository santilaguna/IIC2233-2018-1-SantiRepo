# módulo destinado a implementar la interfaz del cliente y correr el programa.

# from PyQt5.Qt import QTest, QTextCursor
# from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, \
    QPushButton, QLineEdit, QErrorMessage
from cliente import Cliente
from my_widgets import MyListWidget
from edit_menu import EditMenu
from eventos import TextEvent
import sys
import json

CLIENT_HOST = "localhost"
CLIENT_PORT = 65000


class StartMenu(QWidget):

    enviar_solicitud_editar = pyqtSignal(TextEvent)
    enviar_solicitud_escuchar = pyqtSignal(TextEvent)
    enviar_solicitud_editar_cancion_lista = pyqtSignal(TextEvent)
    enviar_solicitud_crear_cancion = pyqtSignal(TextEvent)

    def __init__(self):
        # noinspection PyArgumentList
        super().__init__()
        self.setGeometry(200, 80, 1000, 680)
        self.setWindowTitle("PrograBand")
        self.cliente = Cliente(self, CLIENT_HOST, CLIENT_PORT)

        self.basic_user_label = QLabel("Ingrese nombre usuario:", self)
        self.basic_user_label.setGeometry(30, 30, 180, 30)
        self.user_edit = QLineEdit("", self)
        self.user_edit.setGeometry(200, 30, 700, 30)

        self.button_editar = QPushButton("Editar", self)
        self.button_editar.setGeometry(30, 510, 450, 40)
        self.button_editar.clicked.connect(
            self.conectar_editar_cancion_lista)
        self.enviar_solicitud_editar_cancion_lista.connect(
            self.cliente.editar_cancion_lista)
        self.button_descargar = QPushButton("Descargar", self)
        self.button_descargar.setGeometry(520, 510, 450, 40)
        self.button_descargar.clicked.connect(
            self.cliente.descargar_cancion_lista)

        self.basic_new_song_label = QLabel("Ingrese nombre nueva canción:",
                                           self)
        self.basic_new_song_label.setGeometry(30, 580, 200, 30)
        self.new_song_edit = QLineEdit("", self)
        self.new_song_edit.setGeometry(240, 580, 520, 30)
        self.button_new_song = QPushButton("Crear canción", self)
        self.button_new_song.setGeometry(830, 580, 140, 30)
        self.button_new_song.clicked.connect(self.conectar_crear_cancion)
        self.enviar_solicitud_crear_cancion.connect(
            self.cliente.crear_cancion)

        self.set_boxes()
        self.setMouseTracking(True)
        self.cliente.start()

    def set_boxes(self):
        """As seen at: https://stackoverflow.com/questions/47835929/
        how-set-two-scroll-bars-vertical-and-horizontal-to-the-same
        -widget-in-pyqt-env and https://stackoverflow.com/questions/50180751/
        how-to-fill-a-qhboxlayout-to-align-multiple-qgroupboxes-without-
        creating-fillin"""

        self.label_canciones_en_edicion = QLabel("Canciones en edición", self)
        self.label_canciones_en_edicion.setGeometry(50, 130, 400, 20)
        self.label_canciones_en_edicion.setAlignment(Qt.AlignCenter)
        self.text_canciones_en_edicion = MyListWidget(self)
        self.text_canciones_en_edicion.setGeometry(50, 150, 400, 350)
        self.text_canciones_en_edicion.itemClicked.connect(
            self.conectar_cliente_edicion)
        self.enviar_solicitud_editar.connect(self.cliente.editar_cancion)

        self.label_canciones_listas = QLabel("Canciones listas", self)
        self.label_canciones_listas.setGeometry(550, 130, 400, 20)
        self.label_canciones_listas.setAlignment(Qt.AlignCenter)
        self.text_canciones_listas = MyListWidget(self)
        self.text_canciones_listas.setGeometry(550, 150, 400, 350)
        self.text_canciones_listas.itemClicked.connect(
            self.conectar_cliente_escuchar)
        self.enviar_solicitud_escuchar.connect(self.cliente.escuchar_cancion)

    def conectar_crear_cancion(self):
        self.enviar_solicitud_crear_cancion.emit(
            TextEvent(self.new_song_edit.text(), self.user_edit.text()))

    def conectar_editar_cancion_lista(self):
        self.enviar_solicitud_editar_cancion_lista.emit(
            TextEvent("", self.user_edit.text()))

    def conectar_cliente_escuchar(self, e):
        self.enviar_solicitud_escuchar.emit(TextEvent(e.text(),
                                                      self.user_edit.text()))

    def conectar_cliente_edicion(self, e):
        self.enviar_solicitud_editar.emit(TextEvent(e.text(),
                                                    self.user_edit.text()))

    def open_song_edit(self, event):
        self.hide()
        self.screen = EditMenu(self, self.cliente, event.text)
        self.screen.show()

    def set_editar_text(self, event):
        self.text_canciones_en_edicion.addItem(event.text)

    def reiniciar_textos(self):
        self.text_canciones_listas.clear()
        self.text_canciones_en_edicion.clear()

    def popup(self, e):
        """As seen at: https://stackoverflow.com/questions/40227047/
        python-pyqt5-how-to-show-an-error-message-with-pyqt5"""
        error_dialog = QErrorMessage(self)
        error_dialog.showMessage(e.text)
        error_dialog.show()

    def set_listas_text(self, event):
        self.text_canciones_listas.addItem(event.text)

    def closeEvent(self, QCloseEvent):
        """As seen at: https://stackoverflow.com/questions/9249500/
        pyside-pyqt-detect-if-user-trying-to-close-window"""
        self.cliente.cerrar_ventana()
        super().closeEvent(QCloseEvent)

    def menu_principal(self):
        self.screen.hide()
        self.show()


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print("type", type_)
        print("value", value)
        print("traceback", traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    my_app = StartMenu()
    my_app.show()
    app.exec()
