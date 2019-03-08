# módulo destinado a la simulación
from random import uniform, expovariate, randint, sample
from cargar_archivos import competidores


class Evento:

    def __init__(self, tiempo, funcion, competidor=None):
        self.func = funcion
        self.tiempo = round(tiempo, 3)
        self.competidor = competidor

    def funcion(self):
        self.func(self.tiempo, self.competidor)


class Competidor:

    def __init__(self, id_, nombre, sexo, categoria):
        self.nombre = nombre
        self.id_ = id_
        self.velocidad, self.probabilidad_lesion = self.atributos(categoria)
        self.sexo = sexo

    @staticmethod
    def atributos(categoria):
        if categoria == "amateur":
            return uniform(1.4, 2.8), 0.4
        elif categoria == "aficionado":
            return uniform(2.8, 4.2), 0.25
        elif categoria == "profesional":
            return uniform(4.2, 5.7), 0.15
        else:
            raise ValueError

    def distancia_recorrida(self, tiempo):
        return tiempo * self.velocidad


class MotorSimulacion:

    def __init__(self, n, tiempo_i=0, tiempo_max=8 * 60 * 60):
        self.tiempo_inicial = tiempo_i
        self.tiempo_maximo = tiempo_max
        self._eventos = []
        self.competidores = self.cargar_competidores()
        self.eventos_iniciales()
        self.n = n

    @staticmethod
    def cargar_competidores():
        return [Competidor(int(x[0]), x[1], x[2], x[3]) for x in
                competidores()]

    @property
    def eventos(self):
        self._eventos.sort(key=lambda x: x.tiempo)
        return self._eventos

    def eventos_iniciales(self):
        for competidor in self.competidores:
            tiempo = 42000 / competidor.velocidad
            evento = Evento(tiempo, self.llega_meta, competidor)
            tiempo2 = tiempo / 2
            self.eventos.append(Evento(tiempo2, self.atajo, competidor))
            self.eventos.append(evento)
        self.eventos.append(Evento(expovariate(1 / 300), self.lluvia))
        self.eventos.append(Evento(expovariate(1 / 25), self.accidente))

    def atajo(self, tiempo, competidor):
        print("{} | corredor toma atajo | {}".format(tiempo,
                                                     competidor.nombre))
        if uniform(0, 1) < 0.5:
            for evento in self.eventos:
                if evento.competidor:
                    evento.tiempo -= 4000 / competidor.velocidad

    def accidente(self, inicial, _):
        try:
            choice = sample(self.competidores, 5)
        except ValueError:
            choice = self.competidores
        for competidor in choice:
            u = uniform(0, 1)
            if competidor.probabilidad_lesion < u:
                #self.competidores.remove(competidor)
                text = "{} | {} | corredor sufre accidente | {}"
                print(text.format(self.n, inicial, competidor.nombre))
        tiempo = expovariate(1 / 25) + inicial
        self.eventos.append(Evento(tiempo, self.accidente))

    def lluvia(self, tiempo, _):
        for evento in self.eventos:
            if evento.competidor:
                evento.tiempo += 30 * 60 / 4  # corredores llegarán más tarde
        print("{} | {} | inicio lluvia | {}".format(self.n,
                                                    tiempo, "Simulación"))
        tiempo_n = expovariate(1 / 300) + tiempo
        self.eventos.append(Evento(tiempo_n, self.lluvia))

    def llega_meta(self, tiempo, competidor):
        print("{} | {} | corredor llega a la meta | {}".format(
            self.n, tiempo, competidor.nombre))
        self.competidores.remove(competidor)

    def run(self):
        tiempo_actual = 0
        while self.tiempo_maximo >= tiempo_actual and self.eventos:
            evento = self.eventos.pop(0)
            if evento.tiempo < self.tiempo_maximo:
                tiempo_actual = evento.tiempo
                evento.funcion()


def simulacion(nn):
    for i in range(nn):
        motor = MotorSimulacion(i)
        motor.run()


simulacion(100)
