import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QPushButton)
import backend as back


class MyLabel(QLabel):
    rut = 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.boton = QPushButton("Eliminar", self)
        self.ocupado = False
        self.label = QLabel(*args, **kwargs)
        self.boton.clicked.connect(self.borrar_mensaje)
        self.boton.hide()
        self.rut = MyLabel.rut
        MyLabel.rut += 1

    def borrar_mensaje(self):
        boton = self.sender()
        back.borrar_label(self.rut)
        self.ocupado = False
        self.boton.hide()
        self.label.setText("")


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):

        self.setGeometry(100, 100, 400, 400)
        self.boton = QPushButton('&Send', self)
        self.boton.resize(self.boton.sizeHint())
        self.edit_notas = QLineEdit("Esciba su nota ", self)
        self.boton.clicked.connect(self.send)

        self.labels = [[MyLabel("", self) for i in range(3)]
                       for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.labels[i][j].move(i*120, j*120)
                self.labels[i][j].label.move(i*120, j*120+30)

        hbox = QHBoxLayout()
        hbox.addWidget(self.edit_notas)
        hbox.addWidget(self.boton)


        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)


        self.setLayout(vbox)
        self.setWindowTitle('Notas')

    def send(self):
        texto, nota_valida = back.procesar_texto(self.edit_notas.text())
        if nota_valida:
            for fila in self.labels:
                for label in fila:
                    if not label.ocupado:
                        label.label.setText(texto)
                        label.boton.show()
                        back.agregar_texto(texto, label.rut)
                        label.ocupado = True
                        return



if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    form.show()
    sys.exit(app.exec_())