# Módulo destinado a cargar los archivos

from jugador import Jugador
from mis_estructuras import Listirijilla
from grafo_relaciones import Relaciones

class Str(object):

    """As seen at: https://stackoverflow.com/questions/2673651/
    inheritance-from-str-or-int"""
    def __init__(self, *args, **kwargs):
        self.data = str(*args, **kwargs)

    def split(self, letter):
        ret = Listirijilla()
        aux = self.data
        while aux != "":
            new = ""
            while aux[0] != letter:
                new += aux[0]
                aux = aux[1:]
                if not aux:
                    break
            ret.append(new)
            aux = aux[1:]
            if not aux:
                break
        return ret

def entregar_grafo():
    with open("players_db.csv", "r", encoding="utf-8") as file:
        jugadores = Listirijilla()
        jugadores_str = Listirijilla()
        file.readline()
        for line in file:
            jugador = line.strip("\n")
            jugador = Str(jugador).split(",")
            nuevo_jugador = Jugador(_id=int(jugador[0]), alias=jugador[1],
                                    nombre=jugador[2], club=jugador[3], liga=
                                    jugador[4], nacionalidad=jugador[5],
                                    overall=int(jugador[6]))
            if len(jugadores_str) < 200:
                jugadores_str.append(jugador)
            jugadores.append(nuevo_jugador)
        relaciones = Relaciones(jugadores)
    return relaciones, jugadores_str