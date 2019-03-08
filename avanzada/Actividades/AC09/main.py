"""
-- main.py --

Este módulo cuenta con tres clases:
- Tarea,
- Programador,
- Administrador.
"""

from itertools import count
from random import randint, random
import threading
import time


TOTAL = 8 * 60 * 60  # segundos de simulación --> ocho horas
VELOCIDAD = 3600     # rapidez según el tiempo de simulación

# Esta simple función te permite simular minutos de trabajo.
reloj = lambda minutos: time.sleep(minutos * 60 / VELOCIDAD)


class Tarea:
    """
    Pequeña clase que modela una tarea.
    """

    id_iter = count(1)

    def __init__(self):
        """
        Inicializa una nueva tarea.
        Le asigna un identificador, un estado de completitud y una duración.
        """

        self.id_ = next(Tarea.id_iter)
        self._hecho = 0
        self.duracion = randint(30, 120)

    def avanzar(self):
        """
        Permite desarrollar una unidad de trabajo de la tarea.
        Retorna un booleano que indica si la tarea está lista.
        """

        self._hecho += 1
        return self._hecho == self.duracion

    def __repr__(self):
        return f'T{self.id_} [{self._hecho}/{self.duracion}]'


class Programador(threading.Thread):
    """
    Pequeña clase que modela un programador.
    """
    plataforma_entregar_trabajo = threading.Lock()

    def __init__(self, nombre):
        super().__init__()
        self.daemon = True
        self.nombre = nombre
        self.tareas = []
        self.lento = self.cualidades()
        self.tarea_actual = None

    @staticmethod
    def cualidades():
        return random() < 0.3

    def entregar_tarea(self):
        with self.plataforma_entregar_trabajo:
            if self.lento:
                reloj(20)
            else:
                reloj(5)
            print("{}: he entregado una tarea".format(self.nombre))
            if self.tareas:
                self.tarea_actual = self.tareas.pop(0)
            else:
                self.tarea_actual = None

    def trabajar(self):
        if self.tarea_actual:
            avanza = False
            if self.lento:
                if random() < 0.6:
                    avanza = True
            else:
                if random() < 0.9:
                    avanza = True
            if avanza:
                if self.tarea_actual.avanzar():
                    print("{}: he terminado una tarea".format(self.nombre))
                    self.entregar_tarea()
        else:
            if self.tareas:
                self.tarea_actual = self.tareas.pop(0)

    def run(self):
        while True:
            self.trabajar()
            reloj(1)


class Administrador():
    """
    Pequeña clase que modela un administrador.
    """
    def __init__(self, programadores):
        self.tareas = []
        self._programadores = programadores
        for _ in range(len(self.programadores)):
            self.crear_tarea()

    @property
    def programadores(self):
        self._programadores.sort(key=lambda x: len(x.tareas))
        return self._programadores

    def trabajar(self):
        programador = self.programadores[0]
        if self.tareas:
            tarea = self.tareas.pop(0)
            print(list(map(lambda x: (x.nombre, x.tareas), self.programadores)))
            print("Nueva tarea id={} de {} minutos para {}".format(
                tarea.id_, tarea.duracion, programador.nombre))
            programador.tareas.append(tarea)
        self.crear_tarea()
        reloj(randint(10, 15))

    def crear_tarea(self):
        nueva_tarea = Tarea()
        self.tareas.append(nueva_tarea)

    def abrir_oficina(self):
        for programador in programadores:
            programador.start()


if __name__ == '__main__':
    # Aquí tienes una lista con ocho nombres para los programadores.
    # No hay un bonus por reconocer cuál es la temática entre ellos.

    nombres = [
        'Alex',
        'Matt',
        'Jamie',
        'Nick',
        'Nebil',
        'Belén',
        'Cristian',
        'Jaime',
    ]

    # Aquí deberías escribir unas pocas líneas de código.
    # Hmmm... por ejemplo, crear las instancias en juego.
    # ###################################################
    programadores = [Programador(name) for name in nombres]
    admin = Administrador(programadores)
    admin.abrir_oficina()

    # ###################################################

    tiempo_inicial = time.time()
    while time.time() - tiempo_inicial < (TOTAL / VELOCIDAD):

        # Aquí comienza la simulación síncrona.
        # Deberías escribir algo de código acá.
        # (Recuerda borrar el pass, obviamente)
        # #####################################
        admin.trabajar()


        # #####################################
    print("El administrador ha cerrado la oficina")
    print('Fin de simulación.')
