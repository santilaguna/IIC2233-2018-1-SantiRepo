import socket
from json import dumps, loads
from random import randint
from threading import Thread
from time import sleep

DEFAULT_HOST = socket.gethostname()
DEFAULT_PORT = 65000


class Server:

    def __init__(self, host=None, port=None):
        """
        Esta clase representa a un cliente, el cual se conecta
        a un servidor en host:port. Ademas, puede enviar y recibir
        mensajes del servidor
        """
        self.sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_servidor.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_servidor.bind((host, port))
        self.sock_servidor.listen(1)
        self.listen_cliente()

    def listen_cliente(self):

        while True:
            socket_cliente, adress = self.sock_servidor.accept()
            while True:
                mensaje = self.recibir_mensaje(socket_cliente)
                if mensaje["orden"] == "desconectar":
                    break
                elif mensaje["orden"] == "crear":
                    x, y = randint(0, 500), randint(0, 500)
                    self.enviar(socket_cliente,
                                {"orden": "crear", "posicion": (x, y)})
                elif mensaje["orden"] == "mover":
                    self.enviar(socket_cliente, mensaje)
            socket_cliente.close()
            print("Jugador se ha desconectado")

    def recibir_mensaje(self, socket_cliente):
        largo_mensaje = int.from_bytes(socket_cliente.recv(4),
                                       byteorder="big")
        mensaje = bytearray()
        while len(mensaje) < largo_mensaje:
            read_length = min(256, largo_mensaje - len(mensaje))
            mensaje.extend(socket_cliente.recv(read_length))
        return loads(mensaje)

    def enviar(self, socket_cliente, mensaje):
        mensaje_en_bytes = dumps(mensaje).encode()
        largo_bytes = len(mensaje_en_bytes).to_bytes(4, byteorder="big")
        socket_cliente.sendall(largo_bytes + mensaje_en_bytes)


if __name__ == '__main__':
    server = Server(DEFAULT_HOST, DEFAULT_PORT)
