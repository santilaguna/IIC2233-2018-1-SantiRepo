# módulo destinado a construir el árbol del torneo
import funciones_utiles as fu
from mis_estructuras import Listirijilla


"""As seen at https://github.com/IIC2233/contenidos/blob/master/semana-03/
01-arboles%20y%20listas%20ligadas.ipynb"""


class Partido:
    _id = 16

    def __init__(self, equipo1=None, equipo2=None, padre=None):
        self._id = Partido._id
        Partido._id -= 1
        if Partido._id == 0:
            Partido._id = 16
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.padre = padre
        self.hijo_izquierdo = None
        self.hijo_derecho = None
        self.amarillas_eq1 = Listirijilla()
        self.amarillas_eq2 = Listirijilla()
        self.faltas_eq1 = 0
        self.rojas_eq1 = Listirijilla()
        self.rojas_eq2 = Listirijilla()
        self.faltas_eq2 = 0
        self.goles1 = 0
        self.goles2 = 0
        self.ganador = None

    def jugar_partido(self):
        position = 0
        for jugador in self.equipo1.jugadores:
            prob = 5
            for afinidad in self.equipo1.matriz_afinidades[position]:
                if afinidad < 0.8:
                    prob += 2
            position += 1
            if fu.probabilidad(prob):
                self.faltas_eq1 += 1
            if fu.probabilidad(20):
                self.amarillas_eq1.append(jugador.nombre)
            if fu.probabilidad(5):
                self.rojas_eq1.append(jugador.nombre)

        position = 0
        for jugador in self.equipo2.jugadores:
            prob = 5
            for afinidad in self.equipo2.matriz_afinidades[position]:
                if afinidad < 0.8:
                    prob += 2
            position += 1
            if fu.probabilidad(prob):
                self.faltas_eq2 += 1
            if fu.probabilidad(20):
                self.amarillas_eq2.append(jugador.nombre)
            if fu.probabilidad(5):
                self.rojas_eq2.append(jugador.nombre)

        esperanza1 = self.equipo1.esperanza * (1-(self.faltas_eq1/100))
        esperanza2 = self.equipo2.esperanza * (1-(self.faltas_eq2/100))
        self.goles1 = ((esperanza1/40)**2)//1
        self.goles2 = ((esperanza2/40)**2)//1
        if self.goles1 > self.goles2:
            ganador = self.equipo1
            perdedor = self.equipo2
        elif self.goles1 < self.goles2:
            ganador = self.equipo2
            perdedor = self.equipo1
        else:
            if esperanza1 > esperanza2:
                if fu.probabilidad(80):
                    ganador = self.equipo1
                    perdedor = self.equipo2
                else:
                    ganador = self.equipo2
                    perdedor = self.equipo1
            else:
                if fu.probabilidad(20):
                    ganador = self.equipo1
                    perdedor = self.equipo2
                else:
                    ganador = self.equipo2
                    perdedor = self.equipo1
        self.ganador = ganador.nombre
        return ganador, perdedor

    def __repr__(self):
        try:
            padre = self.padre._id
        except AttributeError:
            padre = None
        return "ID: {}, Padre: {}, Equipo 1: {}, Equipo 2: {}"\
            .format(self._id, padre, self.equipo1, self.equipo2)


class Torneo:

    def __init__(self, equipos):
        self.nodo_raiz, t_c = self.armar_torneo(equipos)
        self.podio = Listirijilla()
        self.t_c = t_c   # Tercero y cuarto

    def buscar_partido(self, _id):
        if _id == 15:
            return self.t_c
        por_revisar = Listirijilla(self.nodo_raiz)
        while por_revisar:
            current = por_revisar.popleft()
            if current._id == _id:
                return current
            por_revisar.append(current.hijo_izquierdo)
            por_revisar.append(current.hijo_derecho)

    def info_equipo(self, name="Tu Equipo"):
        por_revisar = Listirijilla(self.nodo_raiz)
        por_revisar.append(self.t_c)
        anotados = 0
        recibidos = 0
        faltas = Listirijilla()
        rojas = 0
        amarillas = 0
        eliminador = None
        mejor_fase = "octavos de final"
        existe_el_equipo = False
        while por_revisar:
            current = por_revisar.popleft()
            if current is None:
                continue
            por_revisar.append(current.hijo_derecho)
            por_revisar.append(current.hijo_izquierdo)
            if current.equipo1 == name:
                anotados += current.goles1
                recibidos += current.goles2
                amarillas += current.amarillas_eq1
                rojas += current.rojas_eq1
                for falta in current.faltas_eq1:
                    faltas.append(falta)
                if not current.ganador == name:
                    eliminador = current.ganador
                    if current._id in range(9, 13):
                        mejor_fase = "cuartos de final"
                    elif current._id in range(13, 16):
                        mejor_fase = "semi final"
                    else:
                        mejor_fase = "final"
                    existe_el_equipo = True
            elif current.equipo2 == name:
                anotados += current.goles2
                recibidos += current.goles1
                amarillas += current.amarillas_eq2
                rojas += current.rojas_eq2
                for falta in current.faltas_eq2:
                    faltas.append(falta)
                if not current.ganador == name:
                    eliminador = current.ganador
                    if current._id in range(9, 13):
                        mejor_fase = "cuartos de final"
                    elif current._id in range(13, 16):
                        mejor_fase = "semi final"
                    else:
                        mejor_fase = "final"
                    existe_el_equipo = True
        if self.nodo_raiz.ganador == name:
            existe_el_equipo = True
            eliminador = "Nadie"
            mejor_fase = "final"
        if not existe_el_equipo:
            return False
        info = Listirijilla(mejor_fase)
        info.append(eliminador)
        info.append(anotados)
        info.append(recibidos)
        info.append(faltas)
        info.append(rojas)
        info.append(amarillas)
        return info

    @staticmethod
    def armar_torneo(equipos):
        raiz = Partido()
        tercero = Partido()

        semi = Listirijilla()
        for i in range(2):
            nuevo = Partido(padre=raiz)
            semi.append(nuevo)
            if raiz.hijo_izquierdo is None:
                raiz.hijo_izquierdo = nuevo
                tercero.hijo_izquierdo = nuevo  # no es el padre
            else:
                raiz.hijo_derecho = nuevo
                tercero.hijo_derecho = nuevo    # no es el padre

        cuartos = Listirijilla()
        for i in range(4):
            nuevo = Partido(padre=semi[i//2])
            cuartos.append(nuevo)
            padre = semi[i//2]
            if padre.hijo_izquierdo is None:
                padre.hijo_izquierdo = nuevo
            else:
                padre.hijo_derecho = nuevo

        for i in range(8):
            nuevo = Partido(equipos[2*i], equipos[(2*i)+1], cuartos[i//2])
            padre = cuartos[i//2]
            if padre.hijo_izquierdo is None:
                padre.hijo_izquierdo = nuevo
            else:
                padre.hijo_derecho = nuevo
        return raiz, tercero

    def simular_torneo(self):
        for id_partido in range(1, 13):
            partido = self.buscar_partido(id_partido)
            ganador, perdedor = partido.jugar_partido()
            if partido.padre.equipo1 is None:
                partido.padre.equipo1 = ganador
            else:
                partido.padre.equipo2 = ganador

        for id_partido in range(13, 15):
            partido = self.buscar_partido(id_partido)
            ganador, perdedor = partido.jugar_partido()
            if partido.padre.equipo1 is None:
                partido.padre.equipo1 = ganador
                t_c = self.buscar_partido(15)
                t_c.equipo1 = perdedor
            else:
                partido.padre.equipo2 = ganador
                t_c = self.buscar_partido(15)
                t_c.equipo2 = perdedor

        t_c = self.buscar_partido(15)  # tercero y cuarto
        p_s = self.buscar_partido(16)  # primero y segundo
        tercero, cuarto = t_c.jugar_partido()
        primero, segundo = p_s.jugar_partido()
        self.podio.append(primero.nombre)
        self.podio.append(segundo.nombre)
        self.podio.append(tercero.nombre)

    def __repr__(self):
        return "Torneo_type"
