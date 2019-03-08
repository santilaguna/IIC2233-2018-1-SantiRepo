import socket
from json import dumps, loads
import sys
from threading import Thread
from time import sleep
from ventana_principal import MiVentana, QApplication

DEFAULT_HOST = socket.gethostname() # cambiado por ip para bonus
DEFAULT_PORT = 65000


class Client:

    def __init__(self, host=None, port=None):
        """
        Esta clase representa a un cliente, el cual se conecta 
        a un servidor en host:port. Ademas, puede enviar y recibir 
        mensajes del servidor
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.ventana = MiVentana(self.pedir_mover, self.desconectar)

        self.enviar({"orden": "crear"})
        mensaje = self.recibir_mensaje()
        self.ventana.agregar_mi_personaje(*mensaje["posicion"])

    def mover_en_servidor(self):
        mensaje = self.recibir_mensaje()
        if mensaje["orden"] == "mover":
            self.ventana.actualizar_posicion_personaje(*mensaje["posicion"])

    def pedir_mover(self, x, y):
        """
        Esta función se llama cada vez que se aprieta una tecla, entregando la
        posición x, y a la que se deberia mover. En este paso deberían enviarle
        un mensaje al servidor indicando que se quiere mover el personaje a la
        posición x, y
        """
        self.enviar({"orden": "mover", "posicion": (x, y)})
        self.mover_en_servidor()

    def desconectar(self):
        """
        Esta función se llama cuando se cierra la interfaz. En este paso
        deberían enviarle un mensaje al servidor indicando que se van a
        desconectar y manejar la desconexion del cliente.
        """
        self.enviar({"orden": "desconectar"})

    def enviar(self, mensaje):
        mensaje_en_bytes = dumps(mensaje).encode()
        largo_bytes = len(mensaje_en_bytes).to_bytes(4, byteorder="big")
        self.sock.sendall(largo_bytes + mensaje_en_bytes)

    def recibir_mensaje(self):
        largo_mensaje = int.from_bytes(self.sock.recv(4),
                                       byteorder="big")
        mensaje = bytearray()
        while len(mensaje) < largo_mensaje:
            read_length = min(256, largo_mensaje - len(mensaje))
            mensaje.extend(self.sock.recv(read_length))

        return loads(mensaje)



if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    client = Client(DEFAULT_HOST, DEFAULT_PORT)
    app.exec_()
