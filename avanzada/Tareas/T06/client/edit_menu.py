# módulo destinado a la interfaz de la edición de canciones.


# from PyQt5.Qt import QTest, QTextCursor
# from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit
from my_widgets import MyListWidget
from eventos import TextEvent, NotaEvent


class EditMenu(QWidget):

    modo_espectador_signal = pyqtSignal()
    menu_principal = pyqtSignal()
    mover_cancion_actual = pyqtSignal()
    senal_eliminar_nota = pyqtSignal(int)
    senal_agregar_nota = pyqtSignal(NotaEvent)
    senal_agregar_silencio = pyqtSignal(TextEvent)
    senal_enviar_mensaje = pyqtSignal(TextEvent)
    cargar_info_sala_signal = pyqtSignal()

    def __init__(self, parent, cliente, cancion):
        # noinspection PyArgumentList
        super().__init__()
        self.parent = parent
        self.cliente = cliente
        self.cliente.cambiar_texto_lista_notas.connect(
            self.agregar_nota_a_lista)
        self.cliente.cambiar_texto_lista_chat.connect(
            self.agregar_mensaje_chat)
        self.cliente.cargar_info_sala_signal.connect(
            self.cargar_info_sala)
        self.cliente.borrar_nota_signal.connect(self.borrar_nota_servidor)
        self.cliente.senal_nuevo_editor.connect(self.nuevo_editor)
        self.setGeometry(200, 80, 700, 700)
        self.setWindowTitle("Menú de edición de {}".format(cancion))
        self.menu_principal.connect(self.parent.menu_principal)
        self.mover_cancion_actual.connect(self.cliente.mover_cancion)

        self.basic_lista_notas_label = QLabel("Lista notas", self)
        self.basic_lista_notas_label.setGeometry(350, 10, 320, 30)
        self.basic_lista_notas_label.setAlignment(Qt.AlignCenter)
        self.lista_notas = MyListWidget(self)
        self.lista_notas.setGeometry(350, 50, 320, 350)
        self.lista_notas.itemClicked.connect(self.conectar_borrar_nota)
        self.senal_eliminar_nota.connect(self.cliente.borrar_nota)

        self.basic_nota_label = QLabel("Nota:", self)
        self.basic_nota_label.setGeometry(20, 30, 50, 30)
        self.nota_edit = QLineEdit("", self)
        self.nota_edit.setGeometry(100, 30, 220, 30)

        self.basic_octava_label = QLabel("Octava:", self)
        self.basic_octava_label.setGeometry(20, 80, 70, 30)
        self.octava_edit = QLineEdit("", self)
        self.octava_edit.setGeometry(100, 80, 220, 30)

        self.basic_intensidad_label = QLabel("Intensidad:", self)
        self.basic_intensidad_label.setGeometry(20, 130, 70, 30)
        self.intensidad_edit = QLineEdit("", self)
        self.intensidad_edit.setGeometry(100, 130, 220, 30)

        self.basic_duracion_label = QLabel("Duración:", self)
        self.basic_duracion_label.setGeometry(20, 180, 70, 30)
        self.duracion_edit = QLineEdit("", self)
        self.duracion_edit.setGeometry(100, 180, 220, 30)

        self.button_agregar_nota = QPushButton("Agregar nota", self)
        self.button_agregar_nota.setGeometry(50, 380, 250, 30)
        self.button_agregar_nota.clicked.connect(
            self.conectar_agregar_nota)
        self.senal_agregar_nota.connect(self.cliente.agregar_nota)

        self.button_agregar_silencio = QPushButton("Agregar silencio", self)
        self.button_agregar_silencio.setGeometry(50, 340, 250, 30)
        self.button_agregar_silencio.clicked.connect(
            self.conectar_agregar_silencio)
        self.senal_agregar_silencio.connect(self.cliente.agregar_silencio)

        self.cliente.modo_espectador_signal.connect(self.modo_espectador)
        self.modo_espectador_signal.connect(self.cliente.modo_espectador)
        self.modo_espectador_signal.emit()

        self.basic_chat_label = QLabel("Sala de chat - modo editor", self)
        self.basic_chat_label.setGeometry(50, 410, 600, 30)
        self.basic_chat_label.setAlignment(Qt.AlignCenter)
        self.lista_chat = MyListWidget(self)
        self.lista_chat.setGeometry(50, 450, 600, 200)
        self.chat_edit = QLineEdit("", self)
        self.chat_edit.setGeometry(50, 660, 450, 30)
        self.chat_button = QPushButton("Enviar mensaje", self)
        self.chat_button.setGeometry(530, 660, 140, 30)
        self.chat_button.clicked.connect(self.conectar_mensaje_chat)

        self.senal_enviar_mensaje.connect(self.cliente.agregar_mensaje_chat)
        self.cargar_info_sala_signal.connect(self.cliente.pedir_info_sala)
        self.cargar_info_sala_signal.emit()

    def cargar_info_sala(self, e):
        for mensaje in e.mensajes:
            self.lista_chat.addItem(mensaje)
        for nota in e.notas:
            self.lista_notas.addItem(nota)

    def nuevo_editor(self):
        self.basic_duracion_label.show()
        self.basic_intensidad_label.show()
        self.basic_nota_label.show()
        self.basic_octava_label.show()
        self.nota_edit.show()
        self.duracion_edit.show()
        self.intensidad_edit.show()
        self.octava_edit.show()
        self.button_agregar_nota.show()
        self.button_agregar_silencio.show()
        self.basic_chat_label.setText("Sala de chat - modo editor")

    def modo_espectador(self):
        self.basic_duracion_label.hide()
        self.basic_intensidad_label.hide()
        self.basic_nota_label.hide()
        self.basic_octava_label.hide()
        self.nota_edit.hide()
        self.duracion_edit.hide()
        self.intensidad_edit.hide()
        self.octava_edit.hide()
        self.button_agregar_nota.hide()
        self.button_agregar_silencio.hide()
        self.basic_chat_label.setText("Sala de chat - modo espectador")

    def conectar_mensaje_chat(self):
        self.senal_enviar_mensaje.emit(TextEvent(self.chat_edit.text()))

    def conectar_agregar_silencio(self):
        self.senal_agregar_silencio.emit(TextEvent(self.duracion_edit.text()))

    def conectar_agregar_nota(self):
        self.senal_agregar_nota.emit(
            NotaEvent(self.nota_edit.text(), self.octava_edit.text(),
                      self.intensidad_edit.text(), self.duracion_edit.text()))

    def conectar_borrar_nota(self, e):
        """As seen at: https://stackoverflow.com/questions/23835847/
        how-to-remove-item-from-qlistwidget"""
        items = self.lista_notas.selectedItems()
        if not items:
            raise ValueError("Item clickeado fuera de lista seleccionados, "
                             "nota que causó error: {}".format(e.text()))
        for item in items:
            self.senal_eliminar_nota.emit(self.lista_notas.row(item))

    def borrar_nota_servidor(self, row):
        self.lista_notas.takeItem(row)

    def agregar_nota_a_lista(self, event):
        self.lista_notas.addItem(event.text)
        self.nota_edit.clear()
        self.octava_edit.clear()
        self.intensidad_edit.clear()
        self.duracion_edit.clear()

    def agregar_mensaje_chat(self, event):
        self.lista_chat.addItem(event.text)
        self.chat_edit.clear()

    def closeEvent(self, QCloseEvent):
        self.mover_cancion_actual.emit()
        self.cliente.desconectarse_de_sala()
        self.menu_principal.emit()
        super().closeEvent(QCloseEvent)
