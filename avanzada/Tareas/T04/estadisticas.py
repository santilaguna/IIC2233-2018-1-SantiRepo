# módulo destinaod a crear un objeto que guarde las estadísticas y trabaje
# con ellas
from collections import namedtuple, defaultdict
from cargar_archivos import load_attractions


EstadisticasIteracion = namedtuple(
    "EstadisticasIteracion_type",
    ["esperas_en_fila", "llantos", "personas_retiradas", "energia_retirados",
     "dinero_dias_colegio", "fallas_ruziland", "atraccion_falladora",
     "personas_sin_comer", "tiempos_en_restaurant",
     "tiempo_maximo_fuera_de_servicio", "tiempos_perdidos",
     "llamados_tecnicos", "llamados_limpieza", "personas_por_eventos",
     "dinero_no_gastado"])


def mean(iterable):
    """retorna el promedio del iterable"""
    largo = len(list(iterable))
    if largo == 0:
        largo += 1
    return sum(iterable) / largo


def best(iterable):
    elements = {}
    for element in iterable:
        if element in elements:
            elements[element] += 1
        else:
            elements[element] = 1
    return max(elements, key=lambda x: elements[x])


class Estadisticas:

    def __init__(self):
        """esperas en fila: List[float]
        llantos: {str(id_atraccion): List[int]}
        personas_retiradas: int
        energia_retirados: List[float]
        dinero_dias_colegio: int
        fallas_ruziland: int
        atraccion_falladora: str
        personas_sin_comer: int
        tiempo_en_restaurant: List[float]
        tiempo_maximo_fuera_de_servicio: float
        tiempos_perdidos: List[float]
        llamados_tecnicos: int
        llamados_limpieza: int
        personas_por_eventos: int
        dinero_no_gastado: int
        iteraciones: List[EstadisticasIteracion]"""
        self.esperas_en_fila = []
        self.llantos = defaultdict(list)
        self.personas_retiradas = 0
        self.energia_retirados = []
        self.dinero_dias_colegio = 0
        self.fallas_ruziland = 0
        self.atraccion_falladora = None
        self.personas_sin_comer = 0
        self.tiempos_en_restaurant = []
        self.tiempo_maximo_fuera_de_servicio = 0
        self.tiempos_perdidos = []
        self.llamados_tecnicos = 0
        self.llamados_limpieza = 0
        self.personas_por_eventos = 0
        self.dinero_no_gastado = 0
        self.iteraciones = []

    def siguiente_iteracion(self):
        """guarda las estadisticas de la iteración en una namedtuple, se añade
        esta a self.iteraciones y luego se llama a resetear estadísticas"""
        llantos = {k: mean(v) for k, v in self.llantos.items()}
        iteracion = \
            EstadisticasIteracion(
                mean(self.esperas_en_fila), llantos,
                self.personas_retiradas, mean(self.energia_retirados),
                self.dinero_dias_colegio, self.fallas_ruziland,
                self.atraccion_falladora, self.personas_sin_comer,
                mean(self.tiempos_en_restaurant),
                self.tiempo_maximo_fuera_de_servicio,
                mean(self.tiempos_perdidos), self.llamados_tecnicos,
                self.llamados_limpieza, self.personas_por_eventos,
                self.dinero_no_gastado)
        self.iteraciones.append(iteracion)
        self.resetear_estadisticas()

    def resetear_estadisticas(self):
        """reinicia las estadisticas para una nueva iteración, retorna None"""
        self.esperas_en_fila = []
        self.llantos = defaultdict(list)
        self.personas_retiradas = 0
        self.energia_retirados = []
        self.dinero_dias_colegio = 0
        self.fallas_ruziland = 0
        self.atraccion_falladora = None
        self.personas_sin_comer = 0
        self.tiempos_en_restaurant = []
        self.tiempo_maximo_fuera_de_servicio = 0
        self.tiempos_perdidos = []
        self.llamados_tecnicos = 0
        self.llamados_limpieza = 0
        self.personas_por_eventos = 0
        self.dinero_no_gastado = 0

    def imprimir_estadisticas(self):
        """Imprime el promedio de las estadisticas de todas las iteraciones
        retrona None"""
        promedio_esperas = mean([x.esperas_en_fila for x in self.iteraciones])
        print("Tiempo promedio en fila: {}".format(promedio_esperas))
        llantos_dicts = [x.llantos for x in self.iteraciones]
        atracciones = load_attractions()
        for id_atraccion in atracciones:
            promedio_llantos = mean([x[id_atraccion] for x in llantos_dicts])
            print("Promedio llantos diarios de {}: {}".format(
                atracciones[id_atraccion], promedio_llantos))
        promedio_personas_retiradas = mean([x.personas_retiradas for x in
                                            self.iteraciones])
        print("Personas retiradas por energía: {}".format(
            promedio_personas_retiradas))
        promedio_energia_retirados = mean([x.energia_retirados for x in
                                           self.iteraciones])
        print("Energía promedio al momento de salir del parque: {}".format(
            promedio_energia_retirados))
        promedio_dinero_colegio = mean([x.dinero_dias_colegio for x in
                                        self.iteraciones])
        print("Dinero ganado día colegio: {}".format(promedio_dinero_colegio))
        promedio_fallas_ruziland = mean([x.fallas_ruziland for x in
                                         self.iteraciones])
        print("Fallas por invasión ruziland: {}".format(
            promedio_fallas_ruziland))
        atraccion_mas_falladora = best([x.atraccion_falladora for x in
                                        self.iteraciones])
        print("Atracción con más fallas totales: {}".format(
            atraccion_mas_falladora))
        promedio_sin_comer = mean([x.personas_sin_comer for x in
                                   self.iteraciones])
        print("Personas que no pudieron comer: {}".format(promedio_sin_comer))
        promedio_en_restaurant = mean([x.tiempos_en_restaurant for x in
                                       self.iteraciones])
        print("Tiempo promedio en restaurant: {}".format(
            promedio_en_restaurant))
        promedio_fuera_de_servicio = mean([x.tiempo_maximo_fuera_de_servicio
                                           for x in self.iteraciones])
        print("Tiempo máximo atracción fuera de servicio: {}".format(
            promedio_fuera_de_servicio))
        promedio_tiempos_perdidos = mean([x.tiempos_perdidos
                                          for x in self.iteraciones])
        print("Tiempo promedio perdido: {}".format(promedio_tiempos_perdidos))
        promedio_llamados_limpieza = mean([x.llamados_limpieza
                                           for x in self.iteraciones])
        print("Promedio llamados limpieza: {}".format(
            promedio_llamados_limpieza))
        promedio_llamados_tecnicos = mean([x.llamados_tecnicos
                                           for x in self.iteraciones])
        print("Promedio llamados técnicos: {}".format(
            promedio_llamados_tecnicos))
        promedio_afuera = mean([x.personas_por_eventos
                                for x in self.iteraciones])
        print("Personas que no entraron por eventos externos: {}".format(
            promedio_afuera))
        promedio_no_gastado = mean([x.dinero_no_gastado
                                    for x in self.iteraciones])
        print("Dinero no gastado: {}".format(promedio_no_gastado))
        print("Nota: tiempos medidos en minutos")
