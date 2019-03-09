# módulo destinado a escribir la clase jugador
from mis_estructuras import Listirijilla, NotConectedError


class Jugador:
    def __init__(self, _id, alias, nombre, club, liga, nacionalidad, overall):
        self._id = _id  # no es un atributo privado, solo evita uso de id
        self.alias = alias
        self.nombre = nombre
        self.club = club
        self.club_h = hash(self.club)
        self.liga = liga
        self.liga_h = hash(self.liga)
        self.nacionalidad = nacionalidad
        self.nacionalidad_h = hash(self.nacionalidad)
        self.overall = overall
        self.conecciones = Listirijilla()

    def grado_uno(self, other):
        if self.nacionalidad_h == other.nacionalidad_h:
            if self is not other:
                return True
            else:
                return False
        elif self.liga_h == other.liga_h and self.liga_h:
            return True
        elif self.club_h == other.club_h and self.club_h:
            return True
        else:
            return False

    def relacion(self, other):
        if self.nacionalidad_h == other.nacionalidad_h:
            if self.club_h == other.club_h and self.club_h:
                return 1  # amigos cercanos
            elif self.liga_h == other.liga_h and self.liga_h:
                return 0.95  # amigos lejanos
            else:
                return 0.9  # conocidos
        elif self.liga_h == other.liga_h and self.liga_h:
            return 0.9  # conocidos
        elif self.club_h == other.club_h and self.club_h:
            return 0.9  # conocidos
        else:
            raise NotConectedError

    def __repr__(self):
        return str(self._id)