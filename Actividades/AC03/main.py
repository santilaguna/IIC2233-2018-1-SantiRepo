from collections import deque


class GraphNode:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conecciones = set()

    def __repr__(self):
        return self.nombre


class Graph:
    def __init__(self):
        self.lista_adyacencia = dict()

    def cargar_archivo(self, path_archivo):
        with open(path_archivo) as file:
            for line in file:
                origen, destino = line.strip("\n").split(",")
                self.agregar_conexion(origen, destino)

    def agregar_conexion(self, origen, destino):
        # agregamos los vértices si es que no existen
        if origen not in self.lista_adyacencia:
            self.lista_adyacencia[origen] = GraphNode(origen)
        if destino not in self.lista_adyacencia:
            self.lista_adyacencia[destino] = GraphNode(destino)
        # agregamos la conección
        self.lista_adyacencia[origen].conecciones.add(destino)

    def quitar_conexion(self, origen, destino):
        nodo = self.lista_adyacencia.get(origen, None)
        if nodo:
            nodo.conecciones.discard(destino)

    def encontrar_camino(self, origen, destino):
        if (origen or destino) not in self.lista_adyacencia.keys():
            return False
        self.trayectorias = []

        def buscar(_origen, _destino):
            if _origen == _destino:
                return True
            vertice = self.lista_adyacencia[_origen]
            for coneccion in vertice.conecciones:
                if (vertice, coneccion) not in self.trayectorias:
                    self.trayectorias.append((vertice, coneccion))
                    if buscar(coneccion, destino):
                        return True
            return False
        return buscar(origen, destino)

    def encontrar_camino_corto(self, origen, destino):
        if not self.encontrar_camino(origen, destino):
            return False
        if origen == destino:
            return []

        def caminos(_origen, _destino, trayectoria=[]):
            trayectoria = trayectoria + [_origen]
            if _origen == _destino:
                return [trayectoria]
            trayectorias = []
            for coneccion in self.lista_adyacencia[_origen].conecciones:
                if coneccion not in trayectoria:
                    nuevas_trayectorias = caminos(
                        coneccion, _destino, trayectoria)
                    for nueva_trayectoria in nuevas_trayectorias:
                        trayectorias.append(nueva_trayectoria)
            return trayectorias
        _caminos = caminos(origen, destino)
        return min(_caminos, key=lambda x: len(x))

    def export_csv(self, path_archivo):
        with open(path_archivo, "w") as file:
            s = ""
            for vertice in self.lista_adyacencia.values():
                for coneccion in vertice.conecciones:
                    s += "{},{}\n".format(vertice.nombre, coneccion)
            file.write(s[:-1])


if __name__ == "__main__":
    print("*" * 20 + "EASY" + "*" * 20)
    grafo_facil = Graph()
    grafo_facil.cargar_archivo("easy.txt")
    print(grafo_facil.encontrar_camino("A", "C"))  # True
    print(grafo_facil.encontrar_camino("B", "A"))  # False
    print(grafo_facil.encontrar_camino_corto("A", "E"))  # [A, B, E]
    print(grafo_facil.encontrar_camino_corto("A", "C"))  # [A, C]
    grafo_facil.quitar_conexion("A", "C")
    print(grafo_facil.encontrar_camino("A", "C"))  # True
    print(grafo_facil.encontrar_camino_corto("A", "C"))  # [A, B, E, C]
    grafo_facil.quitar_conexion("B", "E")
    print(grafo_facil.encontrar_camino("A", "C"))  # True
    print(grafo_facil.encontrar_camino_corto("A", "C"))  # [A, B, D, E, C]
    grafo_facil.quitar_conexion("D", "E")
    print(grafo_facil.encontrar_camino("A", "C"))  # False
    grafo_facil.agregar_conexion("A", "C")
    print(grafo_facil.encontrar_camino("A", "C"))  # True
    grafo_facil.export_csv("easy_output.txt")  # A,B
                                               # A,C
                                               # B,D
                                               # E,C

    print("\n" + "*" * 20 + "MEDIUM" + "*" * 20)
    grafo_medium = Graph()
    grafo_medium.cargar_archivo("medium.txt")
    print(grafo_medium.encontrar_camino("A", "G"))  # True
    print(grafo_medium.encontrar_camino("A", "D"))  # True
    print(grafo_medium.encontrar_camino_corto("A", "G"))  # [A, F, G]
    grafo_medium.quitar_conexion("A", "F")
    grafo_medium.quitar_conexion("A", "I")
    grafo_medium.quitar_conexion("A", "M")
    grafo_medium.quitar_conexion("A", "D")
    grafo_medium.quitar_conexion("A", "E")
    print(grafo_medium.encontrar_camino("A", "G"))  # False

    print("\n" + "*" * 20 + "HARD" + "*" * 20)
    grafo_hard = Graph()
    grafo_hard.cargar_archivo("hard.txt")
    print(grafo_hard.encontrar_camino_corto("A", "Z"))  # [A, 0, 4, 5, L, Z]
    print(grafo_hard.encontrar_camino("A", "G"))  # True
    grafo_hard.agregar_conexion("4", "Z")
    print(grafo_hard.encontrar_camino_corto("A", "Z"))  # [A, 0, 4, Z]
    grafo_hard.quitar_conexion("4", "Z")
    print(grafo_hard.encontrar_camino_corto("A", "Z"))  # [A, 0, 4, 5, L, Z]
    print(grafo_hard.encontrar_camino("X", "Z"))  # False
    grafo_hard.agregar_conexion("X", "B")
    print(grafo_hard.encontrar_camino("X", "Z"))  # True
    print(grafo_hard.encontrar_camino_corto("X", "Z"))  # [X, B, T, L, Z]
