# módulo destinado a correr el programa del servidor.

import os
import threading
import socket
import re
from json import dumps, loads

HOST = "0.0.0.0"
PORT = 65000
CANTIDAD_CLIENTES = 5


class Server:

    def __init__(self, host, port, cantidad_clientes):
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(cantidad_clientes)
        thread = threading.Thread(target=self.accept_connections_thread,
                                  daemon=True)
        thread.start()

        self.ayudantes = {}
        self.sockets = {}
        self.usuarios_cancion = {}
        self.sockets_cancion = {}

        self.canciones = set()
        self.usuarios = set()
        self.editar_songs = set()
        self.listas_songs = set()
        self.cargar_midis()
        print("Servidor inicializado...")

    def cargar_midis(self):
        files = [file[:-4] for file in os.listdir('midis')]
        files = list(filter(lambda x: not re.match("^\.", x), files))
        for song in files:
            self.canciones.add(song)
            self.usuarios_cancion[song] = []
            self.sockets_cancion[song] = []
            self.listas_songs.add(song)
            with open("chat_midis/"+song+".txt", "w", encoding="utf-8") \
                    as file:
                file.write("")
            with open("notas_midis/"+song+".txt", "w", encoding="utf-8") \
                    as file:
                for nota in self.leer_notas_midi(song):
                    file.write(nota + "\n")

    def leer_notas_midi(self, path):
        with open("midis/" + path + ".mid", "rb") as file:
            for midi in file.readlines():
                header, canal = midi.split(b'MTrk')
                length = bytearray()
                for i in range(4):
                    length.append(canal[i])
                length = int.from_bytes(length, byteorder="big")
                data = [canal[i] for i in range(4, length)]
                notes_on = []
                notes_off = []
                nota = []
                while data:
                    nota.append(data.pop(0))
                    if nota[-1] == 144:
                        nota.append(data.pop(0))
                        nota.append(data.pop(0))
                        notes_on.append(nota)
                        nota = []
                    elif nota[-1] == 128:
                        nota.append(data.pop(0))
                        nota.append(data.pop(0))
                        notes_off.append(nota)
                        nota = []
                return self.convertir_notas_a_string(notes_off)

    def convertir_notas_a_string(self, notas):
        notas_str = []
        notas_numericas = {1: "do", 2: "do#", 3: "re", 4: "mib", 5: "mi",
                           6: "fa", 7: "fa#", 8: "sol", 9: "sol", 10: "la",
                           11: "sib", 12: "si"}
        intensidades_numericas = {8: "pppp", 20: "ppp", 31: "pp", 42: "p",
                                  53: "mp", 64: "mf", 80: "f", 96: "ff",
                                  112: "fff", 127: "ffff"}
        for nota in notas:
            tiempo, nota, intensidad = nota[:-3], nota[-2], nota[-1]
            duracion = self.transformar_tiempo_a_str(tiempo)
            if intensidad == 0:
                notas_str.append("silencio " + duracion)
                continue
            octava = str(int(nota // 12))
            nota_numerica = int(nota % 12) + 1
            nota_real = notas_numericas[nota_numerica]
            intensidad_real = intensidades_numericas[intensidad]
            notas_str.append(" ".join([nota_real, octava, intensidad_real,
                                       duracion]))
        return notas_str

    @staticmethod
    def transformar_tiempo_a_str(tiempo):
        duraciones = {10: "semifusa", 15: "semifusa.",
                      20: "fusa", 30: "fusa.",
                      40: "semicorchea", 60: "semicorchea.",
                      80: "corchea", 120: "corchea.",
                      160: "negra", 240: "negra.",
                      320: "blanca", 480: "blanca.",
                      640: "redonda", 960: "redonda."}
        hexas = [bin(x)[2:].zfill(8) for x in tiempo]
        hexas = [x[1:] for x in hexas]
        return duraciones[int("".join(hexas), 2)]

    def accept_connections_thread(self):
        """As seen at: https://github.com/IIC2233/Syllabus/blob/master/
        Ayudantias/Ayudantia%2013/Ayudantia13_Server.py"""
        n = 0
        while True:
            n += 1
            client_socket, _ = self.sock.accept()
            ayudante = "Ayudante {}".format(n)
            self.ayudantes[client_socket] = ayudante
            self.sockets[ayudante] = client_socket
            print("Se ha conectado {} al servidor de PrograBand".format(
                ayudante))
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()

    def listen_client_thread(self, client_socket):
        ayudante = self.ayudantes[client_socket]
        while True:
            mensaje, largo = self.recibir_mensaje(client_socket)
            if mensaje["motivo"] == "usuario_desconectado":
                self.usuario_desconectado(mensaje["song"], mensaje["user"],
                                          ayudante, largo)
            elif mensaje["motivo"] == "modo_espectador":
                self.modo_espectador(mensaje["user"], mensaje["song"],
                                     ayudante, largo)
            elif mensaje["motivo"] == "cargar_editar_songs":
                self.cargar_editar_songs(ayudante, largo)
            elif mensaje["motivo"] == "cargar_listas_songs":
                self.cargar_listas_songs(ayudante, largo)
            elif mensaje["motivo"] == "cargar_info_sala":
                self.cargar_info_sala(mensaje["song"], ayudante, largo)
            elif mensaje["motivo"] == "descargar":
                self.descargar(mensaje["song"], ayudante, largo)
            elif mensaje["motivo"] == "crear_cancion":
                self.crear_cancion(mensaje["song"], ayudante, largo)
            elif mensaje["motivo"] == "verificar_cancion_repetida":
                self.verificar_cancion_repetida(mensaje["song"], ayudante,
                                                largo)
            elif mensaje["motivo"] == "verificar_usuario_repetido":
                self.verificar_usuario_repetido(mensaje["user"], ayudante,
                                                largo)
            elif mensaje["motivo"] == "desconectar_cliente":
                self.desconectar_cliente(ayudante, client_socket, largo)
                break
            elif mensaje["motivo"] == "mover_cancion":
                self.mover_cancion(mensaje["song"], ayudante, largo)
            elif mensaje["motivo"] == "borrar_nota":
                self.borrar_nota(mensaje["row"], mensaje["song"], ayudante,
                                 largo)
            elif mensaje["motivo"] == "agregar_nota":
                self.agregar_nota(mensaje["song"], mensaje["nota"],
                                  mensaje["duracion"], mensaje["intensidad"],
                                  mensaje["octava"], ayudante, largo)
            elif mensaje["motivo"] == "chat":
                self.chat(mensaje["song"], mensaje["texto"], mensaje["user"],
                          ayudante, largo)
            elif mensaje["motivo"] == "agregar_silencio":
                self.agregar_silencio(mensaje["song"], mensaje["duracion"],
                                      ayudante, largo)
            else:
                raise ValueError(mensaje["motivo"])

    def usuario_desconectado(self, song, user, ayudante, largo):
        print("{} | usuario desconectado de sala edición | {} "
              "| largo mensaje: {}".format(ayudante, song, largo))
        self.usuarios.discard(user)
        self.usuarios_cancion[song].remove(user)
        if self.usuarios_cancion[song]:
            nuevo_usuario = self.usuarios_cancion[song][0]
        else:
            nuevo_usuario = None
        self.sockets_cancion[song].remove(self.sockets[ayudante])
        for socket_usuario in self.sockets_cancion[song]:
            self.enviar(socket_usuario, {"motivo": "usuario_desconectado",
                                         "user": user,
                                         "new": nuevo_usuario})
            ayudante_ = self.ayudantes[socket_usuario]
            print("{} | notificar desconexión usuario | {}".format(
                ayudante_, user))

    def modo_espectador(self, user, song, ayudante, largo):
        print("{} | verificar modo espectador | {} | "
              "largo mensaje: {}".format(ayudante, song, largo))
        self.usuarios.add(user)
        unico = "True"
        if self.usuarios_cancion[song]:
            unico = "False"
        self.usuarios_cancion[song].append(user)
        self.sockets_cancion[song].append(self.sockets[ayudante])
        self.enviar(self.sockets[ayudante], {"motivo": "modo_espectador",
                                             "unico": unico})
        print("{} | responder único en sala | {}".format(ayudante, unico))

    def cargar_editar_songs(self, ayudante, largo):
        print("{} | cargar canciones en edición | "
              "largo mensaje: {}".format(ayudante, largo))
        self.enviar(self.sockets[ayudante], {"motivo": "cargar_editar_songs",
                                             "songs": list(self.editar_songs)})
        print("{} | enviar canciones en edición | {}".format(
            ayudante, "-"))

    def cargar_listas_songs(self, ayudante, largo):
        print("{} | cargar canciones listas |"
              " largo mensaje: {}".format(ayudante, largo))
        self.enviar(self.sockets[ayudante], {"motivo": "cargar_listas_songs",
                                             "songs": list(self.listas_songs)})
        print("{} | enviar canciones listas | {}".format(
            ayudante, "-"))

    def cargar_info_sala(self, song, ayudante, largo):
        print("{} | cargar info sala | {} "
              "| largo mensaje: {}".format(ayudante, song, largo))
        with open("chat_midis/"+song+".txt", "r", encoding="utf-8") as file:
            chat_lines = [line.strip("\n") for line in file]
        with open("notas_midis/"+song+".txt", "r", encoding="utf-8") as file:
            notas_lines = [line.strip("\n") for line in file]
        self.enviar(self.sockets[ayudante], {"motivo": "cargar_info_sala",
                                             "chat": chat_lines,
                                             "notas": notas_lines})
        print("{} | enviar info sala | {}".format(ayudante, song))

    def descargar(self, song, ayudante, largo):
        print("{} | descargar canción | {} "
              "| largo mensaje: {}".format(ayudante, song, largo))
        self.enviar_cancion(song, ayudante)

    def crear_cancion(self, song, ayudante, largo):
        print("{} | crear canción | {} "
              "| largo mensaje: {}".format(ayudante, song, largo))
        self.canciones.add(song)
        self.usuarios_cancion[song] = []
        self.sockets_cancion[song] = []
        self.editar_songs.add(song)
        for socket_cliente in self.sockets.values():
            self.enviar(socket_cliente, {"motivo": "crear_cancion",
                                         "song": song})
            cliente = self.ayudantes[socket_cliente]
            print("{} | notificar canción creada| {}".format(cliente, song))
        with open("chat_midis/"+song+".txt", "w", encoding="utf-8") as file:
            file.write("")
        with open("notas_midis/"+song+".txt", "w", encoding="utf-8") as file:
            file.write("")

    def verificar_cancion_repetida(self, song, ayudante, largo):
        print("{} | verificar canción repetida | {} "
              "| largo mensaje: {}".format(ayudante, song, largo))
        unico = "True"
        if song in self.canciones:
            unico = "False"
        self.enviar(self.sockets[ayudante],
                    {"motivo": "verificar_cancion_repetida",
                     "unico": unico})
        print("{} | responder canción única | {}".format(ayudante, unico))

    def verificar_usuario_repetido(self, user, ayudante, largo):
        print("{} | verificar canción repetida | {} "
              "| largo mensaje: {}".format(ayudante, user, largo))
        unico = "True"
        if user in self.usuarios:
            unico = "False"
        self.enviar(self.sockets[ayudante],
                    {"motivo": "verificar_usuario_repetido",
                     "unico": unico})
        print("{} | responder usuario único | {}".format(ayudante, unico))

    def desconectar_cliente(self, ayudante, client_socket, largo):
        del self.sockets[ayudante]
        del self.ayudantes[client_socket]
        print("{} | cliente desconectado | largo mensaje: {}".format(ayudante,
                                                                     largo))

    def mover_cancion(self, song, ayudante, largo):
        print("{} | mover canción de lista | {}"
              " | largo mensaje: {}".format(ayudante, song, largo))
        if song in self.listas_songs:
            self.listas_songs.discard(song)
            self.editar_songs.add(song)
        elif song in self.editar_songs:
            self.editar_songs.discard(song)
            self.listas_songs.add(song)
        for socket_cliente in self.sockets.values():
            self.enviar(socket_cliente, {"motivo": "mover_cancion",
                                         "song": song})
            cliente = self.ayudantes[socket_cliente]
            print("{} | notificar mover canción| {}".format(cliente, song))

    def borrar_nota(self, row, song, ayudante, largo):
        print("{} | borrar nota | {}-{} "
              "| largo mensaje: {}".format(ayudante, row, song, largo))
        for sock_cliente in self.sockets_cancion[song]:
            cliente = self.ayudantes[sock_cliente]
            print("{} | notificar borrar nota | {}-{}".format(cliente,
                                                              row, song))
            self.enviar(sock_cliente, {"motivo": "borrar_nota",
                                       "row": row})
        with open("notas_midis/"+song+".txt", "r", encoding="utf-8") as file:
            notas_lines = [line.strip("\n") for line in file]
        notas_lines.pop(row)
        with open("notas_midis/"+song+".txt", "w", encoding="utf-8") as file:
            for nota in notas_lines:
                file.write(nota + "\n")

    def agregar_nota(self, song, nota, duracion, intensidad, octava, ayudante,
                     largo):
        str_nota = " ".join([nota, octava, intensidad, duracion])
        print("{} | agregar nota | {}-{} "
              "| largo mensaje: {}".format(ayudante, str_nota, song, largo))
        for sock_cliente in self.sockets_cancion[song]:
            cliente = self.ayudantes[sock_cliente]
            print("{} | notificar agregar nota | {}-{}".format(cliente,
                                                               str_nota, song))
            self.enviar(sock_cliente, {"motivo": "agregar_nota",
                                       "nota_str": str_nota})
        with open("notas_midis/"+song+".txt", "a", encoding="utf-8") as file:
            file.write(str_nota + "\n")

    def agregar_silencio(self, song, duracion, ayudante, largo):
        print("{} | agregar silencio | {} | "
              "largo mensaje: {}".format(ayudante, song, largo))
        for sock_cliente in self.sockets_cancion[song]:
            cliente = self.ayudantes[sock_cliente]
            print("{} | notificar agregar silencio | {}".format(cliente, song))
            self.enviar(sock_cliente, {"motivo": "agregar_nota",
                                       "nota_str": "silencio "+duracion})
        with open("notas_midis/"+song+".txt", "a", encoding="utf-8") as file:
            file.write("silence "+duracion + "\n")

    def chat(self, song, texto, user, ayudante, largo):
        str_texto = user + ": " + texto
        print("{} | agregar mensaje chat | {}-{} "
              "| largo mensaje: {}".format(ayudante, str_texto, song, largo))
        for sock_cliente in self.sockets_cancion[song]:
            cliente = self.ayudantes[sock_cliente]
            print("{} | notificar mensaje chat | {}-{}".format(
                cliente, str_texto, song))
            self.enviar(sock_cliente, {"motivo": "chat",
                                       "texto": str_texto})
        with open("chat_midis/"+song+".txt", "a", encoding="utf-8") as file:
            file.write(str_texto + "\n")

    @staticmethod
    def recibir_mensaje(socket_cliente):
        largo_mensaje = int.from_bytes(socket_cliente.recv(4),
                                       byteorder="big")
        mensaje = bytearray()
        while len(mensaje) < largo_mensaje:
            read_length = min(256, largo_mensaje - len(mensaje))
            mensaje.extend(socket_cliente.recv(read_length))
        return loads(mensaje), str(largo_mensaje)

    @staticmethod
    def enviar(socket_cliente, mensaje):
        mensaje_en_bytes = dumps(mensaje).encode()
        largo_bytes = len(mensaje_en_bytes).to_bytes(4, byteorder="big")
        socket_cliente.sendall(largo_bytes)
        socket_cliente.sendall(mensaje_en_bytes)

    def enviar_cancion(self, song, ayudante):
        print("{} | enviar canción | {} ".format(ayudante, song))
        socket_cliente = self.sockets[ayudante]
        self.enviar(socket_cliente, {"motivo": "descargar",
                                     "song": song})
        bytes_cancion = self.descargar_midi(song)
        largo_bytes = len(bytes_cancion).to_bytes(4, byteorder="big")
        socket_cliente.sendall(largo_bytes)
        socket_cliente.sendall(bytes_cancion)

    def descargar_midi(self, song):
        self.escribir_midi(song)
        return self.leer_midi(song)

    def escribir_midi(self, song):
        """As seen at: https://github.com/IIC2233/Syllabus/issues/718"""
        with open("notas_midis/"+song+".txt", "r", encoding="utf-8") \
                as file:
            notas = [nota.strip("\n") for nota in file]
        header_bytes = self.numbers_to_bytes([1, 1, 160], 2)
        length_header = len(header_bytes).to_bytes(4, byteorder="big")
        header = b'MThd' + length_header + header_bytes

        fin_canal = self.numbers_to_bytes([0, 255, 47, 0])
        data_canal = self.notas_to_bytes(notas) + fin_canal
        length_canal = len(data_canal).to_bytes(4, byteorder="big")
        canal = b'MTrk' + length_canal + data_canal

        midi = header + canal
        with open("midis/"+song+".mid", "wb") as file:
            file.write(midi)

    def notas_to_bytes(self, notas):
        valor_nota = {"do": 1, "do#": 2, "re": 3, "mib": 4, "mi": 5,
                      "fa": 6, "fa#": 7, "sol": 8, "sol#": 9,
                      "la": 10, "sib": 11, "si": 12}
        duraciones = {"semifusa": 10, "semifusa.": 15,
                      "fusa": 20, "fusa.": 30,
                      "semicorchea": 40, "semicorchea.": 60,
                      "corchea": 80, "corchea.": 120,
                      "negra": 160, "negra.": 240,
                      "blanca": 320, "blanca.": 480,
                      "redonda": 640, "redonda.": 960}
        intensidades = {"pppp": 8, "ppp": 20, "pp": 31, "p": 42, "mp": 53,
                        "mf": 64, "f": 80, "ff": 96, "fff": 112, "ffff": 127}
        notas_bytes = bytearray()
        for nota in notas:
            lista_nota = nota.split(" ")
            if lista_nota[0] == "silence" or lista_nota[0] == "silencio":
                duracion = lista_nota[1]
                nota_musical = 0
                intensidad = 0
            else:
                nota_, octava, intensidad_, duracion = lista_nota
                nota_musical = ((int(octava)) * 12) + valor_nota[nota_] - 1
                intensidad = intensidades[intensidad_]
            tiempo_ = duraciones[duracion]
            tiempo = self.procesar_tiempo(tiempo_)
            cero = self.procesar_tiempo(0)
            notas_bytes.extend(cero)
            notas_bytes.extend(self.numbers_to_bytes([144, nota_musical,
                                                      intensidad]))
            notas_bytes.extend(tiempo)
            notas_bytes.extend(self.numbers_to_bytes([128, nota_musical,
                                                      intensidad]))
        return bytes(notas_bytes)

    @staticmethod
    def procesar_tiempo(tiempo):
        binario_list = [letter for letter in bin(tiempo)[2:]]
        lista_binarios = []
        while binario_list:
            while len(binario_list) < 7:
                binario_list.insert(0, "0")
            mini_bin = binario_list[-7:]
            binario_list = binario_list[:-7]
            lista_binarios.insert(0, ["1"] + mini_bin)
        lista_binarios[-1] = ["0"] + lista_binarios[-1][1:]
        lista_enteros = [int("".join(x), 2).to_bytes(1, byteorder="big")
                         for x in lista_binarios]
        lista_bytes = bytearray()
        for bytesito in lista_enteros:
            lista_bytes.extend(bytesito)
        return bytes(lista_bytes)

    def numbers_to_bytes(self, numbers, n=1):
        byte_numbers = bytearray()
        for number in numbers:
            byte_numbers.extend(self.number_to_bytes(number, n))
        return bytes(byte_numbers)

    @staticmethod
    def number_to_bytes(number, n):
        return number.to_bytes(n, byteorder="big")

    @staticmethod
    def leer_midi(song):
        bytes_file = bytearray()
        with open("midis/" + song + ".mid", "rb") as file:
            for midi in file.readlines():
                bytes_file.extend(midi)
        return bytes(bytes_file)


if __name__ == '__main__':
    server = Server(HOST, PORT, CANTIDAD_CLIENTES)
    # en caso de que se quiera mantener el servidor corriendo por siempre.
    while True:
        pass
