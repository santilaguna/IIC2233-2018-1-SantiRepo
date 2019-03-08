# módulo destinado a implementar los eventos de interacción de la interfaz.


class MousePressed:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class TextEvent:

    def __init__(self, text, user=None):
        self.text = text
        self.user = user

class NotaEvent:

    def __init__(self, nota, octava, intensidad, duracion):
        self.nota = nota
        self.octava = octava
        self.intensidad = intensidad
        self.duracion = duracion

class InfoSalaEvent:

    def __init__(self, notas, mensajes):
        self.notas = notas
        self.mensajes = mensajes
