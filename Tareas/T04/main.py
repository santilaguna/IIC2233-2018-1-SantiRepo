# Módulo destinado a la clase simulación junto con correr el programa y
# mostrar las estadísticas.

from parque_de_diversiones import ParqueDeDiversiones
import parameters as par


class Simulacion:

    def __init__(self, iteraciones=par.NUMERO_ITERACIONES):
        """iteraciones: int"""
        self.iteraciones = iteraciones
        self.nebiland = ParqueDeDiversiones()

    def correr_simulacion(self):
        """corre la simulación una cantidad de iteraciones y luego imprime las
        estadisticas promedio. retorna None"""
        for _ in range(self.iteraciones):
            self.nebiland.run()
            self.estado_inicial_simulacion()
        self.nebiland.estadisticas.imprimir_estadisticas()

    def estado_inicial_simulacion(self):
        """volvemos a setear los valores a los iniciales de la simulación,
        retorna None"""
        self.nebiland.atraccion_falladora = None
        self.nebiland.grupos = []
        self.nebiland._eventos = []
        for limpiador in self.nebiland.limpiadores:
            limpiador.estado_inicial()
        for tecnico in self.nebiland.tecnicos:
            tecnico.estado_inicial()
        for atraccion in self.nebiland.atracciones.values():
            atraccion.cerrar_parque()
            atraccion.suciedad = par.SUCIEDAD_INICIAL
            atraccion.fuera_de_servicio = False
            atraccion.fallas_totales = 0
        for restaurant in self.nebiland.restaurantes.values():
            restaurant.cerrar_parque()
        self.nebiland.iteracion += 1
        self.nebiland.dias_simulacion = (dia for dia in par.DIAS_SIMULACION)
        self.nebiland.dia_nuevo()


simulacion_nebiland = Simulacion()
simulacion_nebiland.correr_simulacion()
