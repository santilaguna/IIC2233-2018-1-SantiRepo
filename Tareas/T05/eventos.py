# módulo destinado a escribir los eventos que serán entregados a las señales.


class PositionMoveEvent:
    def __init__(self, x, y, release=False):
        self.x = x
        self.y = y
        self.release = release


class SideMoveEvent:
    def __init__(self, side, id_=None):
        self.side = side
        self.id_ = id_


class ReleaseEvent:
    def __init__(self, ready):
        self.ready = ready


class KeyEvent:
    def __init__(self, key):
        self._key = key

    def key(self):
        return self._key


class BombEvent:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player


class ExplodeEvent:
    def __init__(self, x, y, rango, bomba, player):
        self.x = x
        self.y = y
        self.rango = rango
        self.bomba = bomba
        self.player = player


class PlaceExplodeEvent:
    def __init__(self, espacio, player=None):
        self.espacio = espacio
        self.player = player


class CambiarVidaEvent:
    def __init__(self, player, cambio, vidas):
        self.player = player
        self.cambio = cambio
        self.vidas = vidas


class PowerUpEvent:
    def __init__(self, power_up):
        self.power_up = power_up


class LabelPowerEvent:
    def __init__(self, tipo, player, cantidad=None):
        self.tipo = tipo
        self.cantidad = cantidad
        self.player = player


class MoveEnemyEvent:
    def __init__(self, x, y, id_, player=None, last_side=None):
        self.x = x
        self.y = y
        self.id_ = id_
        self.player = player
        self.last_side = last_side


class RangoVisionEvent:
    def __init__(self, x, y, id_, rango_vision):
        self.x = x
        self.y = y
        self.id_ = id_
        self.rango = rango_vision


class HostilidadEvent:
    def __init__(self, id_, player):
        self.id_ = id_
        self.player = player


class RecibirEnemigoEvent:
    def __init__(self, tipo, x, y):
        self.tipo = tipo
        self.x = x
        self.y = y


class ScoreEvent:
    def __init__(self, score, player):
        self.score = score
        self.player = player


class KickBombEvent:
    def __init__(self, way, id_):
        self.way = way
        self.id_ = id_


class MoveBombEvent:
    def __init__(self, id_, x, y):
        self.id_ = id_
        self.x = x
        self.y = y
