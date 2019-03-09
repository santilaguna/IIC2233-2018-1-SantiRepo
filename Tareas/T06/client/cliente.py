# módulo destinado a implementar el programa del cliente.

from PyQt5.Qt import QTest
from PyQt5.QtCore import pyqtSignal, QThread
from eventos import TextEvent, InfoSalaEvent
from json import dumps, loads
from convertidor_midi import convertir_a_midi
import re
import socket
import threading
import sys


class Cliente(QThread):

    senal_nuevo_editor = pyqtSignal()
    borrar_nota_signal = pyqtSignal(int)
    cargar_info_sala_signal = pyqtSignal(InfoSalaEvent)
    cambiar_texto_lista_notas = pyqtSignal(TextEvent)
    cambiar_texto_lista_chat = pyqtSignal(TextEvent)
    modo_espectador_signal = pyqtSignal()
    cambiar_texto_canciones_editar = pyqtSignal(TextEvent)
    cambiar_texto_canciones_listas = pyqtSignal(TextEvent)
    abrir_cancion_escogida = pyqtSignal(TextEvent)
    limpiar_listas_canciones = pyqtSignal()
    input_invalido = pyqtSignal(TextEvent)

    def __init__(self, parent, host, port):
        super().__init__(parent)
        self.parent = parent
        self.host = host
        self.port = port
        self.establecer_conexion_servidor()

        self.cancion_actual = None
        self.usuario = None
        self.cambiar_texto_canciones_listas.connect(parent.set_listas_text)
        self.cambiar_texto_canciones_editar.connect(parent.set_editar_text)
        self.abrir_cancion_escogida.connect(parent.open_song_edit)
        self.limpiar_listas_canciones.connect(parent.reiniciar_textos)
        self.input_invalido.connect(parent.popup)
        self.canciones_en_edicion = set()
        self.canciones_listas = set()
        self.espectador = False
        self.usuario_invalido = True
        self.cancion_invalida = True

    def establecer_conexion_servidor(self):
        """As seen at: https://github.com/IIC2233/Syllabus/blob/master/
        Ayudantias/Ayudantia%2013/Ayudantia13_cliente.py"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            self.connected = True
            thread = threading.Thread(target=self.listen_thread, daemon=True)
            thread.start()

        except ConnectionRefusedError:
            print("Conexión con el servidor rechazada")
            self.sock.close()
            self.quit()
            self.deleteLater()
            sys.exit()

    def listen_thread(self):
        while True:
            mensaje = self.recibir_mensaje_de_servidor()
            if mensaje["motivo"] == "modo_espectador":
                if mensaje["unico"] == "False":
                    self.espectador = True
                    self.modo_espectador_signal.emit()
            elif mensaje["motivo"] == "cargar_editar_songs":
                self.cargar_editar_songs_server(mensaje["songs"])
            elif mensaje["motivo"] == "cargar_listas_songs":
                self.cargar_listas_songs_server(mensaje["songs"])
            elif mensaje["motivo"] == "cargar_info_sala":
                self.cargar_info_sala_signal.emit(
                    InfoSalaEvent(mensaje["notas"], mensaje["chat"]))
                self.enviar_mensaje_a_servidor({"motivo": "chat",
                                                "song": self.cancion_actual,
                                                "texto": "se ha conectado",
                                                "user": self.usuario})
            elif mensaje["motivo"] == "crear_cancion":
                self.nueva_cancion_desde_servidor(mensaje["song"])
            elif mensaje["motivo"] == "verificar_usuario_repetido":
                if mensaje["unico"] == "True":
                    self.usuario_invalido = False
            elif mensaje["motivo"] == "verificar_cancion_repetida":
                if mensaje["unico"] == "True":
                    self.cancion_invalida = False
            elif mensaje["motivo"] == "descargar":
                song_bytes = self.recibir_cancion()
                convertir_a_midi(mensaje["song"], song_bytes)
                self.input_invalido.emit(TextEvent("Canción descargada"))
            elif mensaje["motivo"] == "mover_cancion":
                self.mover_cancion_servidor(mensaje["song"])
            elif mensaje["motivo"] == "borrar_nota":
                self.borrar_nota_signal.emit(mensaje["row"])
            elif mensaje["motivo"] == "agregar_nota":
                self.agregar_nota_desde_servidor(mensaje["nota_str"])
            elif mensaje["motivo"] == "chat":
                self.agregar_mensaje_chat_servidor(mensaje["texto"])
            elif mensaje["motivo"] == "usuario_desconectado":
                self.usuario_desconectado(mensaje["user"], mensaje["new"])
            else:
                raise ValueError(mensaje["motivo"])

    def modo_espectador(self):
        self.enviar_mensaje_a_servidor({"motivo": "modo_espectador",
                                        "user": self.usuario,
                                        "song": self.cancion_actual})

    def cargar_editar_songs(self):
        self.enviar_mensaje_a_servidor({"motivo": "cargar_editar_songs"})

    def cargar_editar_songs_server(self, songs):
        for song in songs:
            self.cambiar_texto_canciones_editar.emit(TextEvent(song))
            self.canciones_en_edicion.add(song)

    def cargar_listas_songs(self):
        self.enviar_mensaje_a_servidor({"motivo": "cargar_listas_songs"})

    def cargar_listas_songs_server(self, songs):
        for song in songs:
            self.cambiar_texto_canciones_listas.emit(TextEvent(song))
            self.canciones_listas.add(song)

    def pedir_info_sala(self):
        self.enviar_mensaje_a_servidor({"motivo": "cargar_info_sala",
                                        "song": self.cancion_actual})

    def nueva_cancion_desde_servidor(self, song):
        self.cambiar_texto_canciones_editar.emit(TextEvent(song))
        self.canciones_en_edicion.add(song)

    def editar_cancion(self, e):
        self.verificar_usuario(e.user)
        if not self.usuario_invalido:
            self.usuario = e.user
            self.cancion_actual = e.text
            self.abrir_cancion_escogida.emit(TextEvent(e.text))

    def escuchar_cancion(self, e):
        self.cancion_actual = e.text

    def editar_cancion_lista(self, e):
        if self.cancion_actual in self.canciones_listas:
            self.verificar_usuario(e.user)
            if not self.usuario_invalido:
                self.mover_cancion()
                self.usuario = e.user
                self.abrir_cancion_escogida.emit(TextEvent(
                    self.cancion_actual))

    def descargar_cancion_lista(self):
        if (self.cancion_actual is not None) and \
                (self.cancion_actual in self.canciones_listas):
            self.enviar_mensaje_a_servidor({"motivo": "descargar",
                                            "song":  self.cancion_actual})

    def crear_cancion(self, e):
        self.verificar_usuario(e.user)
        self.verificar_nueva_cancion(e.text)
        if not self.usuario_invalido:
            if not self.cancion_invalida:
                self.usuario = e.user
                self.cancion_actual = e.text
                self.enviar_mensaje_a_servidor({"motivo": "crear_cancion",
                                                "song": e.text})
                QTest.qWait(200)
                self.abrir_cancion_escogida.emit(TextEvent(e.text))

    def verificar_nueva_cancion(self, song):
        if len(song) < 6:
            self.input_invalido.emit(TextEvent("Canción debe tener al menos "
                                               "6 caracteres"))
            return False
        self.verificar_cancion_repetida(song)
        if self.cancion_invalida:
            self.input_invalido.emit(TextEvent("Nombre canción ya existe"))
            return False
        return True

    def verificar_usuario(self, user):
        if re.search(" ", user):
            self.input_invalido.emit(TextEvent("Usuario no debe tener "
                                               "espacios"))
            return False
        elif len(user) < 6:
            self.input_invalido.emit(TextEvent("Usuario debe tener al menos "
                                               "6 caracteres"))
            return False
        self.verificar_usuario_repetido(user)
        if self.usuario_invalido:
            self.input_invalido.emit(TextEvent("Nombre usuario ya existe"))
            return False
        return True

    def verificar_cancion_repetida(self, song):
        self.cancion_invalida = True
        self.enviar_mensaje_a_servidor({"motivo": "verificar_cancion_repetida",
                                        "song": song})
        QTest.qWait(200)

    def verificar_usuario_repetido(self, user):
        self.usuario_invalido = True
        self.enviar_mensaje_a_servidor({"motivo": "verificar_usuario_repetido",
                                        "user": user})
        QTest.qWait(200)

    def mover_cancion(self):
        self.enviar_mensaje_a_servidor({"motivo": "mover_cancion",
                                        "song": self.cancion_actual})

    def mover_cancion_servidor(self, song):
        if song in self.canciones_listas:
            self.canciones_listas.discard(song)
            self.canciones_en_edicion.add(song)
        elif song in self.canciones_en_edicion:
            self.canciones_en_edicion.discard(song)
            self.canciones_listas.add(song)
        self.actualizar_canciones()

    def actualizar_canciones(self):
        self.limpiar_listas_canciones.emit()
        for song in self.canciones_listas:
            self.cambiar_texto_canciones_listas.emit(TextEvent(song))
        for song in self.canciones_en_edicion:
            self.cambiar_texto_canciones_editar.emit(TextEvent(song))

    def borrar_nota(self, row):
        if not self.espectador:
            self.enviar_mensaje_a_servidor({"motivo": "borrar_nota",
                                            "row": row,
                                            "song": self.cancion_actual})

    def agregar_silencio(self, e):
        duracion = e.text.lower()
        if re.search(" ", duracion):
            self.input_invalido.emit(TextEvent("Duración no debe tener "
                                               "espacios"))
            return
        duracion_convertida = self.convertir_duracion(duracion)
        if not duracion_convertida:
            return
        self.enviar_mensaje_a_servidor({"motivo": "agregar_silencio",
                                        "song": self.cancion_actual,
                                        "duracion": duracion_convertida})

    def agregar_nota(self, e):
        nota = e.nota.lower()
        octava = e.octava.lower()
        duracion = e.duracion.lower()
        intensidad = e.intensidad.lower()
        if re.search(" ", nota):
            self.input_invalido.emit(TextEvent("Nota no debe tener "
                                               "espacios"))
            return
        elif re.search(" ", octava):
            self.input_invalido.emit(TextEvent("Octava no debe tener "
                                               "espacios"))
            return
        elif re.search(" ", duracion):
            self.input_invalido.emit(TextEvent("Duración no debe tener "
                                               "espacios"))
            return
        elif re.search(" ", intensidad):
            self.input_invalido.emit(TextEvent("Intensidad no debe tener "
                                               "espacios"))
            return
        nota_convertida = self.convertir_nota(nota)
        duracion_convertida = self.convertir_duracion(duracion)
        intensidad_convertida = self.convertir_intensidad(intensidad)
        octava_convertida = self.convertir_octava(octava, nota_convertida)
        if (not nota_convertida) or (not duracion_convertida) or \
                (not intensidad_convertida) or (not octava_convertida):
            return
        self.enviar_mensaje_a_servidor({"motivo": "agregar_nota",
                                        "song": self.cancion_actual,
                                        "nota": nota_convertida,
                                        "duracion": duracion_convertida,
                                        "intensidad": intensidad_convertida,
                                        "octava": octava_convertida})

    def convertir_duracion(self, duracion):
        if duracion.isdigit():
            conversiones = {10: "semifusa", 15: "semifusa.",
                            20: "fusa", 30: "fusa.",
                            40: "semicorchea", 60: "semicorchea.",
                            80: "corchea", 120: "corchea.",
                            160: "negra", 240: "negra.",
                            320: "blanca", 480: "blanca.",
                            640: "redonda", 960: "redonda."}
            if int(duracion) in conversiones:
                duracion = conversiones[int(duracion)]
        duraciones = {"redonda": "redonda", "1": "redonda",
                      "redonda.": "redonda.", "1.": "redonda.",
                      "blanca": "blanca", "2": "blanca",
                      "blanca.": "blanca.", "2.": "blanca.",
                      "negra": "negra", "3": "negra",
                      "negra.": "negra.", "3.": "negra.",
                      "corchea": "corchea", "4": "corchea",
                      "corchea.": "corchea.", "4.": "corchea.",
                      "semicorchea": "semicorchea", "5": "semicorchea",
                      "semicorchea.": "semicorchea.", "5.": "semicorchea.",
                      "fusa": "fusa", "6": "redonda",
                      "fusa.": "fusa.", "6.": "redonda.",
                      "semifusa": "semifusa", "7": "semifusa",
                      "semifusa.": "semifusa.", "7.": "semifusa."}
        if duracion not in duraciones:
            self.input_invalido.emit(
                TextEvent("La duración no existe, recuerda que puede ser una "
                          "redonda, blanca, negra, corchea, semicorchea,"
                          "fusa o semifusa, o sus equivalentes en valor "
                          "numérico. Además pueden tener un punto (.) al final"
                          "para duración extendida"))
            return None
        else:
            return duraciones[duracion]

    def convertir_intensidad(self, intensidad):
        intensidades = {"pppp": "pppp", "8": "pppp", "ppp": "ppp", "20": "ppp",
                        "pp": "pp", "31": "pp", "p": "p", "42": "p",
                        "mp": "mp", "53": "mp", "mf": "mf", "64": "mf",
                        "f": "f", "80": "f", "ff": "ff", "96": "ff",
                        "fff": "fff", "112": "fff", "ffff": "ffff",
                        "127": "ffff"}
        if intensidad not in intensidades:
            self.input_invalido.emit(
                TextEvent("La intensidad no existe, recuerda que puede ser: "
                          "pppp, ppp, pp, p, mp, mf, f, ff, fff o ffff, "
                          "o bien, su equivalente valor numérico."))
            return None
        else:
            return intensidades[intensidad]

    def convertir_octava(self, octava, nota):
        if not nota:
            return None
        if not re.fullmatch("[1-9]|10", octava):
            self.input_invalido.emit(
                TextEvent("Octava inválida, recuerda que la octava debe ser "
                          "un número del 0 al 10"))

            return None
        valor_nota = {"do": 1, "do#": 2, "re": 3, "mib": 4, "mi": 5,
                      "fa": 6, "fa#": 7, "sol": 8, "sol#": 9,
                      "la": 10, "sib": 11, "si": 12}
        octava_numerica = ((int(octava)) * 12) + valor_nota[nota] - 1
        if octava_numerica > 127:
            self.input_invalido.emit(
                TextEvent("Combinación octava inválida, recuerda que  si la "
                          "octava es 10 el valor numérico de la nota no puede"
                          " superar al de un sol"))

            return None
        return str(octava)

    def convertir_nota(self, nota):
        notas = {"do": "do", "c": "do", "1": "do",
                 "do#": "do#", "c#": "do#", "2": "do#", "dd": "do#",
                 "re": "re", "d": "re", "3": "re",
                 "mib": "mib", "eb": "mib", "4": "mib", "d#": "mib",
                 "mi": "mi", "e": "mi", "5": "mi",
                 "fa": "fa", "f": "fa", "6": "fa",
                 "fa#": "fa#", "f#": "fa#", "7": "fa#", "gb": "fa#",
                 "sol": "sol", "g": "sol", "8": "sol",
                 "sol#": "sol", "g#": "sol#", "9": "sol#", "ab": "sol#",
                 "la": "la", "a": "la", "10": "la",
                 "sib": "sib", "bb": "sib", "a#": "sib", "11": "sib",
                 "si": "si", "b": "si", "12": "si"}
        if nota not in notas:
            self.input_invalido.emit(
                TextEvent("La nota no existe, recuerda que la nota debe estar "
                          "entre las siguiente opciones: do, re, mi, fa, sol, "
                          "la, si, do#, fa#, sol#, o sus equivalentes "
                          "en nomenclatura inglesa o numérica"))
            return None
        else:
            return notas[nota]

    def agregar_nota_desde_servidor(self, nota):
        self.cambiar_texto_lista_notas.emit(TextEvent(nota))

    def agregar_mensaje_chat(self, e):
        self.enviar_mensaje_a_servidor({"motivo": "chat",
                                        "song": self.cancion_actual,
                                        "texto": e.text,
                                        "user": self.usuario})

    def agregar_mensaje_chat_servidor(self, texto):
        self.cambiar_texto_lista_chat.emit(TextEvent(texto))

    def usuario_desconectado(self, usuario, nuevo_editor):
        if nuevo_editor == self.usuario:
            self.senal_nuevo_editor.emit()
        if usuario is None:
            raise TypeError("usuario es None")

    def enviar_mensaje_a_servidor(self, mensaje):
        mensaje_en_bytes = dumps(mensaje).encode()
        largo_bytes = len(mensaje_en_bytes).to_bytes(4, byteorder="big")
        self.sock.sendall(largo_bytes)
        self.sock.sendall(mensaje_en_bytes)

    def recibir_mensaje_de_servidor(self):
        largo_mensaje = int.from_bytes(self.sock.recv(4),
                                       byteorder="big")
        mensaje = bytearray()
        while len(mensaje) < largo_mensaje:
            read_length = min(256, largo_mensaje - len(mensaje))
            mensaje.extend(self.sock.recv(read_length))
        return loads(mensaje)

    def recibir_cancion(self):
        largo_mensaje = int.from_bytes(self.sock.recv(4),
                                       byteorder="big")
        mensaje = bytearray()
        while len(mensaje) < largo_mensaje:
            read_length = min(256, largo_mensaje - len(mensaje))
            mensaje.extend(self.sock.recv(read_length))
        return mensaje

    def cerrar_ventana(self):
        self.enviar_mensaje_a_servidor({"motivo": "desconectar_cliente"})
        self.quit()
        self.deleteLater()

    def desconectarse_de_sala(self):
        self.enviar_mensaje_a_servidor({"motivo": "chat",
                                        "song": self.cancion_actual,
                                        "texto": "se ha desconectado",
                                        "user": self.usuario})
        self.enviar_mensaje_a_servidor({"motivo": "usuario_desconectado",
                                        "song": self.cancion_actual,
                                        "user": self.usuario})
        self.modo_espectador_signal.disconnect()
        self.cargar_info_sala_signal.disconnect()
        self.cambiar_texto_lista_chat.disconnect()
        self.cambiar_texto_lista_notas.disconnect()
        self.borrar_nota_signal.disconnect()
        self.senal_nuevo_editor.disconnect()
        self.espectador = False
        self.cancion_actual = None
        self.usuario = None

    def start(self, priority=None):
        self.cargar_listas_songs()
        self.cargar_editar_songs()
