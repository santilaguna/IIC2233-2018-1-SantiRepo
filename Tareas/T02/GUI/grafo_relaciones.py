# módulo destinado a obtener las afinidades de los jugadores

from mis_estructuras import Listirijilla, SamePlayerError, HashTable


class Relaciones:

    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.distancias = HashTable()
        for jugador in self.jugadores:
            for coneccion in jugadores:
                if jugador.grado_uno(coneccion):
                    jugador.conecciones.append(coneccion._id)
                    self.distancias.fast_set(jugador._id + coneccion._id,
                                             jugador.relacion(coneccion))

    def buscar_jugador(self, _id):
        for jugador in self.jugadores:
            if jugador._id == _id:
                return jugador

    def buscar_nombre(self, nombre):
        for jugador in self.jugadores:
            if jugador.nombre == nombre:
                return jugador

    def afinidad(self, j1, j2, visitados=Listirijilla(),
                 afinidades=Listirijilla()):
        if j1 == j2:
            raise SamePlayerError
        if j1.grado_uno(j2):
            return j1.relacion(j2)
        visitados.append(j1)
        if len(visitados) > 5:
            return False
        for _id in j1.conecciones:
            player = self.buscar_jugador(_id)
            if player not in visitados:
                afinidad = j1.relacion(player)
                auxiliar_af = self.afinidad(player, j2, visitados)
                if not auxiliar_af:
                    continue
                afinidad += auxiliar_af - 1
                afinidades.append(afinidad)
        return max(afinidades)

    def mejor_amigo(self, jugador):
        mejor = None
        max = 0
        for coneccion in jugador.conecciones:
            player = self.buscar_jugador(coneccion)
            if mejor is None:
                mejor = player
                max = jugador.relacion(player)
            else:
                afinidad = jugador.relacion(player)
                if afinidad > max:
                    max = afinidad
                    mejor = player
        return mejor

    def peor_amigo(self, jugador):
        menor = 1
        enemigo = None
        for player in self.jugadores:
            if player is not jugador:
                afinidad = self.afinidad(jugador, player)
                if afinidad < menor:
                    menor = afinidad
                    enemigo = player
        return enemigo

    def popular(self):
        best = None
        for jugador in self.jugadores:
            if best is None:
                best = jugador
            else:
                if len(jugador.conecciones) > len(best.conecciones):
                    best = jugador
        return best

    def fichaje_estrella(self, jugador):
        estrella = None
        max_chispeza = 0
        for coneccion in jugador.conecciones:
            player = self.buscar_jugador(coneccion)
            if estrella is None:
                estrella = player
                max_chispeza = jugador.relacion(player) * player.overall
            else:
                chispeza = jugador.relacion(player) * player.overall
                if chispeza > max_chispeza:
                    max_chispeza = chispeza
                    estrella = player
        return estrella
