# Módulo destinado a crear a las personas.

# Importar clases directamente
import faker
import parameters as par
from random import normalvariate, uniform, randint
from math import inf
from funcion_tiempo import sumar_tiempo


class Persona:
    nombres = set()
    es_faker = faker.Faker("es_MX")

    def __init__(self):
        """nombre: str"""
        self.nombre = self.obtener_nombre()

    def obtener_nombre(self):
        """retorna str"""
        name = self.es_faker.name()
        while name in self.nombres:
            name = self.es_faker.name()
        self.nombres.add(name)
        return name

    def __repr__(self):
        return self.nombre


class Cliente(Persona):

    def __init__(self, adulto):
        """adulto: bool"""
        super().__init__()
        self.adulto = adulto
        self.estatura, self._energia, self._hambre, self._nauseas, self.edad \
            = self.datos_iniciales()
        self.vomito = False

    @property
    def energia(self):
        """retorna int"""
        return self._energia

    @energia.setter
    def energia(self, value):
        """setea la energía entre los parametros establecidos, retorna None"""
        if value < par.ENERGIA_MINIMA:
            self._energia = par.ENERGIA_MINIMA
        elif value > par.ENERGIA_INICIAL:
            self._energia = par.ENERGIA_INICIAL
        else:
            self._energia = value

    @property
    def hambre(self):
        """retorna int"""
        return self._hambre

    @hambre.setter
    def hambre(self, value):
        """setea el hambre entre los parámetros establecidos, retorna None"""
        if value < par.HAMBRE_MINIMA:
            self._hambre = par.HAMBRE_MINIMA
        elif value > par.HAMBRE_MAXIMA:
            self._hambre = par.HAMBRE_MAXIMA
        else:
            self._hambre = value

    @property
    def nauseas(self):
        """retorna int"""
        return self._nauseas

    @nauseas.setter
    def nauseas(self, value):
        """setea las nauseas entre los parámetros estabelcidos, retorna None"""
        if value > par.NAUSEA_MAXIMA:
            self._nauseas = par.NAUSEA_MAXIMA
        else:
            self._nauseas = value

    @property
    def paciencia(self):
        """retorna int, según parámetros establecidos de forma aleatoria"""
        mu = self.energia * par.MULTIPLICADOR_PACIENCIA + par.SUMANDO_PACIENCIA
        return max(min(normalvariate(mu, par.SIGMA_PACIENCIA),
                       par.MAXIMA_PACIENCIA), par.MINIMA_PACIENCIA)

    def datos_iniciales(self):
        """setea la estatura(float), hambre, nauseas y edad (ints), según los
        parámetros establecidos o de forma aleatoria"""
        energia = par.ENERGIA_INICIAL
        hambre = uniform(*par.HAMBRE_INICIAL)
        nauseas = par.NAUSEA_INICIAL
        if self.adulto:
            estatura = min(max(normalvariate(par.MU_ADULTO, par.SIGMA_ADULTO),
                               par.ALTURA_MINIMA), par.ALTURA_MAXIMA)
            edad = randint(*par.EDAD_ADULTOS)
            return estatura, energia, hambre, nauseas, edad
        else:
            estatura = min(max(normalvariate(par.MU_NINO, par.SIGMA_NINO),
                               par.ALTURA_MINIMA), par.ALTURA_MAXIMA)
            edad = randint(*par.EDAD_NINOS)
            return estatura, energia, hambre, nauseas, edad


class Adulto(Cliente):

    def __init__(self, budget):
        """budget: int"""
        super().__init__(True)
        self.budget = budget


class Nino(Cliente):

    def __init__(self, budget=None):
        """budget: int"""
        super().__init__(False)
        self.budget = budget

    @property
    def probabilidad_llorar(self):
        """retorna si el niño llora o no: int"""
        probabilidad = uniform(0, 1)
        if probabilidad < 1 / self.edad:
            return True
        return False


class Grupo:
    id_ = 0

    def __init__(self, budget, children, adulto=True):
        """budget: int, children: int, adulto: bool,
        juegos_visitados: str(ids), ultima_accion: str, siguiente_accion: str,
        tiempo_inicio: (int, int), tiempos_perdidos: List[float],
        tiempos_en_fila: List[float], id_: int, baja_energia: bool"""
        if adulto:
            self.adulto = Adulto(budget)
            self.cantidad_personas = 1 + children
            self.ninos = [Nino() for _ in range(children)]
        else:
            self.ninos = [Nino(budget) for _ in range(children)]
            self.adulto = None
            self.cantidad_personas = children
        self.juegos_visitados = set()
        self.ultima_accion = None
        self.siguiente_accion = None
        self.tiempo_inicio = None
        self.tiempos_perdidos = []
        self.tiempos_en_fila = []
        self.id_ = Grupo.id_
        self.baja_energia = False
        Grupo.id_ += 1

    @property
    def energia_minima(self):
        """retorna la energia mínima del grupo: int"""
        if self.adulto:
            energia_adulto = self.adulto.energia
        else:
            energia_adulto = inf
        return min([n.energia for n in self.ninos] + [energia_adulto])

    @property
    def budget(self):
        """retorna el presupuesto del grupo: int"""
        if self.adulto:
            return self.adulto.budget
        else:
            return self.ninos[0].budget

    @budget.setter
    def budget(self, value):
        """setea el presupuesto del grupo, retorna None"""
        if self.adulto:
            self.adulto.budget = value
        else:
            self.ninos[0].budget = value

    @property
    def altura_minima(self):
        """retorna la altura mínima del grupo: float"""
        if self.adulto:
            estatura_adulto = self.adulto.estatura
        else:
            estatura_adulto = inf
        estaturas = [n.estatura for n in self.ninos]
        estaturas.append(estatura_adulto)
        return min(estaturas)

    @property
    def hambre_promedio(self):
        """retorna el hambre promedio del grupo: float"""
        suma = sum(x.hambre for x in self.ninos)
        if self.adulto:
            suma += self.adulto.hambre
        return suma / self.cantidad_personas

    @property
    def paciencia_minima(self):
        """retorna la mínima paciencia del grupo: float"""
        if self.adulto:
            paciencias = [self.adulto.paciencia]
        else:
            paciencias = [inf]
        paciencias += [n.paciencia for n in self.ninos]
        return min(paciencias)

    def subir_atraccion(self, suciedad):
        """suciedad: function, altera la suciedad de la atracción a la que se
        sube el grupo, además aumenta las nauseas con probabilidad de vomito de
        los miembros del grupo, retorna None"""
        if self.adulto:
            self.adulto.nauseas += par.AUMENTO_NAUSEA_ADULTO
            suciedad(par.SUCIEDAD_POR_PERSONA)
        for nino in self.ninos:
            nino.nauseas += par.AUMENTO_NAUSEA_NINO
            suciedad(par.SUCIEDAD_POR_PERSONA)
        if self.adulto and self.adulto.nauseas >= par.RANGO_VOMITO:
            if uniform(0, 1) < par.PROBABILIDAD_VOMITO:
                self.adulto.vomito = True
                suciedad(par.SUCIEDAD_POR_VOMITO)
        for nino in self.ninos:
            if nino.nauseas >= par.RANGO_VOMITO:
                if uniform(0, 1) < par.PROBABILIDAD_VOMITO:
                    nino.vomito = True
                    suciedad(par.SUCIEDAD_POR_VOMITO)

    def bajar_de_atraccion(self, agregar_evento, borrar_evento, retirarse,
                           tiempo, nino_llora):
        """agregar_evento: function, borrar_evento: function,
        retirarse: function, tiempo: (int, int), nino_llora: function, altera
        ciertos parámetros que se deben a bajarse de una atracción y analiza si
         es meritorio de irse del parque, retorna None"""
        self.ultima_accion = "divertirse"
        if self.adulto:
            self.adulto.energia -= par.DISMINUCION_ENERGIA_ADULTOS
            self.adulto.hambre += par.AUMENTO_HAMBRE_ADULTOS
            self.adulto.vomito = False
        for nino in self.ninos:
            nino.energia -= par.DISMINUCION_ENERGIA_NINOS
            nino.hambre += par.AUMENTO_HAMBRE_NINOS
            if nino.probabilidad_llorar and not nino.vomito:
                nino_llora()
                nino.energia -= par.ENERGIA_LLORAR_NINO
                if self.adulto:
                    self.adulto.energia -= par.ENRGIA_LLORAR_ADULTO
            nino.vomito = False
        if self.energia_minima == 0:
            self.leave_nebiland(agregar_evento, borrar_evento, retirarse,
                                tiempo)
        elif self.energia_minima <= par.ENERGIA_IRSE:
            if uniform(0, 1) < par.PROBABILIDAD_IRSE:
                self.leave_nebiland(agregar_evento, borrar_evento, retirarse,
                                    tiempo)

    def leave_nebiland(self, agregar_evento, borrar_evento, retirarse, tiempo):
        """agregar_evento: fucntion, borrar_evento: function,
        tiempo: (int, int), elimina los eventos de un grupo que se quiere
        retirar del parque y lo elimina de este, retorna None"""
        borrar_evento(self)
        self.baja_energia = True
        agregar_evento(sumar_tiempo(tiempo, (0, 1)), retirarse(self),
                       "retirarse del parque", ["Nebiland"], self)

    def descansar(self):
        """aumenta la energía del grupo gracias al descanso, retorna None"""
        if self.adulto:
            self.adulto.energia += par.AUMENTO_ENERGIA
        for nino in self.ninos:
            nino.energia += par.AUMENTO_ENERGIA
        self.ultima_accion = "descansar"

    def comer(self):
        """disminuye el hambre del grupo por comer y aumenta sus nauseas en
        caso de que vengan de una atracción, retorna None"""
        self.descansar()
        if self.adulto:
            self.adulto.hambre -= par.DISMINUCION_HAMBRE
        for nino in self.ninos:
            nino.hambre -= par.DISMINUCION_HAMBRE
        if self.ultima_accion == "divertirse":
            if self.adulto:
                self.adulto.nauseas += par.AUMENTO_NAUSEA_RESTAURANT
            for nino in self.ninos:
                nino += par.AUMENTO_NAUSEA_RESTAURANT
        self.ultima_accion = "comer"

    def planificar_evento(self):
        """planifica el siguiente evento cuando está en la fla de una
        atracción para decidir si esperará en la fila indefinidamente o por
        un tiempo limitado, retorna bool."""
        probabilidad = uniform(0, 1)
        if probabilidad < par.PROBABILIDAD_HACER_FILA:
            self.siguiente_accion = "divertirse"
            return True
        elif probabilidad < par.PROBABILIDAD_HACER_FILA \
                + (self.hambre_promedio * par.MULTIPLICANDO_HAMBRE):
            self.siguiente_accion = "comer"
            return False
        else:
            self.siguiente_accion = "descansar"
            return False

    def __repr__(self):
        if self.adulto:
            adulto = "Grupo a cargo del adulto {}. ".format(self.adulto.nombre)
            if self.ninos:
                ninos = "Niños del grupo: {}.".format(
                    " - ".join([n.nombre for n in self.ninos]))
            else:
                ninos = ""
            return adulto + ninos
        else:
            return "Niño de un colegio: {}".format(self.ninos[0].nombre)


class Empleado(Persona):

    def __init__(self):
        super().__init__()

    @staticmethod
    def inicio_colacion():
        """retorna una tupla que indica la hora de comienzo de la colación"""
        probabilidad = uniform(0, 1)
        if probabilidad < par.PROBABILIDADES_COLACION[0]:
            return par.HORAS_COLACION[0]
        elif probabilidad < par.PROBABILIDADES_COLACION[1]:
            return par.HORAS_COLACION[1]
        elif probabilidad < par.PROBABILIDADES_COLACION[2]:
            return par.HORAS_COLACION[2]
        elif probabilidad < par.PROBABILIDADES_COLACION[3]:
            return par.HORAS_COLACION[3]
        elif probabilidad < par.PROBABILIDADES_COLACION[4]:
            return par.HORAS_COLACION[4]
        elif probabilidad < par.PROBABILIDADES_COLACION[5]:
            return par.HORAS_COLACION[5]
        elif probabilidad < par.PROBABILIDADES_COLACION[6]:
            return par.HORAS_COLACION[6]
        elif probabilidad < par.PROBABILIDADES_COLACION[7]:
            return par.HORAS_COLACION[7]
        else:
            return par.HORAS_COLACION[8]


class Limpiador(Empleado):

    def __init__(self):
        """tiempo_traslado: int, llamados: List[str], limpiando: bool"""
        super().__init__()
        self.tiempo_traslado = par.TRASLADO_LIMPIADOR
        self.llamados = []
        self.limpiando = False

    def agregar_llamado(self, id_atraccion):
        """id_atraccion: str, agrega un llamado y retorna si está limpiando"""
        self.llamados.append(id_atraccion)
        return self.limpiando

    def siguiente_llamado(self):
        """retorna el siguiente llamado de la fila"""
        return self.llamados.pop(0)

    def dejar_de_limpiar(self, next_work, tiempo):
        """next_work: function, tiempo: (int, int), deja de limpiar y revisa
        si tiene más atracciones que limpiar, retorna None"""
        self.limpiando = False
        self.llamados = self.llamados[1:]
        if self.llamados:
            next_work(self.siguiente_llamado(), tiempo, self)

    def estado_inicial(self):
        """setea los valores iniciales, retorna None"""
        self.limpiando = False
        self.llamados = []

    def __repr__(self):
        return "Limpiador " + self.nombre


class Operador(Empleado):

    def __init__(self, id_atraccion=None, llamar_limpieza=None,
                 llamar_tecnico=None):
        """id_atraccion: str, llamar_limpieza: function,
        llamar_tecnico: function"""
        super().__init__()
        self.id_atraccion = id_atraccion
        self.llamar_limipieza = llamar_limpieza
        self.llamar_tecnico = llamar_tecnico

    def __repr__(self):
        return "Operador " + self.nombre


class Tecnico(Empleado):

    def __init__(self):
        """tiempo_traslado: int, tiempo_reparacion: int, llamados: List[str],
        reparando: bool"""
        super().__init__()
        self.tiempo_traslado = par.TRASLADO_TECNICO
        self.tiempo_reparacion = par.TIEMPO_REPARACION
        self.llamados = []
        self.reparando = False

    def agregar_llamado(self, id_atraccion):
        """id_atraccion: str, agrega un llamado y retorna si está reparando"""
        self.llamados.append(id_atraccion)
        return self.reparando

    def siguiente_llamado(self):
        """retorna el siguiente llamado de la fila"""
        return self.llamados.pop(0)

    def dejar_de_reparar(self, next_work, tiempo):
        """next_work: function, tiempo: (int, int), deja de reparar y revisa
        si tiene más atracciones que reparar, retorna None"""
        self.reparando = False
        self.llamados = self.llamados[1:]
        if self.llamados:
            next_work(self.siguiente_llamado(), tiempo, self)

    def estado_inicial(self):
        """setea los vakores iniciales, retorna None"""
        self.reparando = False
        self.llamados = []

    def __repr__(self):
        return "Técnico " + self.nombre
