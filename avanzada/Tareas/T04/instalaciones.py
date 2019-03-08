# Módulo destinado a la implementación de las instalaciones.

# Importar clases directamente
from random import expovariate
import parameters as par
from funcion_tiempo import sumar_tiempo, comparar_tiempo, diferencia


class Instalacion:

    def __init__(self, id_, nombre, capacidad, costo_adulto, costo_nino,
                 tiempo_uso, *args, **kwargs):
        """id_: str, nombre: str, capacidad: int, costo_adulto: int,
        costo_nno: int, tiempo_uso: int"""
        self.id_ = id_
        self.nombre = nombre
        self.capacidad = capacidad
        self.costo_adulto = costo_adulto
        self.costo_nino = costo_nino
        self.tiempo_uso = tiempo_uso
        self.fuera_de_servicio = False
        self.dinero_recaudado = 0
        self.grupos = []

    @property
    def cantidad_personas(self):
        """retorna la cantidad de personas que están usando la instalación"""
        return sum(grupo.cantidad_personas for grupo in self.grupos)

    def permite_entrada(self, grupo):
        """grupo: Grupo, evalúa si el grupo cumple con los requsitos mínimos
        de entrada a la instalación, retorna un booleano"""
        costo_total = 0
        if grupo.adulto:
            costo_total += self.costo_adulto
        for _ in range(len(grupo.ninos)):
            costo_total += self.costo_nino
        if grupo.budget >= costo_total:
            ret = True
        else:
            ret = False
        return ret

    def cobrar_grupo(self, grupo):
        """grupo: Grupo, cobra al grupo por los servicios, retorna None"""
        costo_total = 0
        if grupo.adulto:
            costo_total += self.costo_adulto
        for _ in range(len(grupo.ninos)):
            costo_total += self.costo_nino

        grupo.budget -= costo_total
        if grupo.budget < 0:
            raise ValueError(str(grupo))
        self.dinero_recaudado += costo_total


class Restaurant(Instalacion):

    def __init__(self, id_, name, capacity, adult_cost, child_cost,
                 max_duration, juegos_asociados):
        """juegos_asociados: set(str)
        profesor: Adulto
        tiempos_en_restaurant: List[int]"""
        super().__init__(id_, name, capacity, adult_cost, child_cost,
                         max_duration)
        self.juegos_asociados = juegos_asociados
        self.profesor = None
        self.tiempos_en_restaurant = []

    @property
    def tiempo_preparacion_adultos(self):
        """retorna el tiempo de preparación de los platos de adultos"""
        return max(min(expovariate(par.TASA_PREPARACION_ADULTOS),
                       par.TIEMPO_MAXIMO_PREPARACION),
                   par.TIEMPO_MINIMO_PREPARACION)

    @property
    def tiempo_preparacion_ninos(self):
        """retorna el tiempo de preparación de los platos de niños"""
        return max(min(expovariate(par.TASA_PREPARACION_NINOS),
                       par.TIEMPO_MAXIMO_PREPARACION),
                   par.TIEMPO_MINIMO_PREPARACION)

    def permite_entrada(self, grupo):
        """grupo: Grupo, evalúa si el grupo cumple con los requsitos mínimos
        de entrada al restaurant, retorna un booleano"""
        if grupo.juegos_visitados - self.juegos_asociados or self.capacidad \
                < (grupo.cantidad_personas + self.cantidad_personas):
            return False
        return super().permite_entrada(grupo)

    def entra_grupo(self, grupo, agregar_evento, tiempo_inicial,
                    tomar_decision, liberar_profe):
        """El grupo entra al restaurant y se determina cuánto tiempo se
        tardará el grupo en preparar sus platos, si no se alcanzan a repartir
        los platos antes del cierre del parque, el grupo toma otra decisión"""
        tiempos_preparacion = [self.tiempo_preparacion_ninos for _ in
                               grupo.ninos]
        if grupo.adulto:
            tiempos_preparacion += [self.tiempo_preparacion_adultos]
        tiempo_final = sumar_tiempo(
            tiempo_inicial, (0, self.tiempo_uso + max(tiempos_preparacion)))
        if tiempo_final[0] >= par.HORA_CIERRE[0]:
            return False
        self.grupos.append(grupo)
        self.tiempos_en_restaurant.append(diferencia(
            tiempo_final, tiempo_inicial))
        agregar_evento(tiempo_final,
                       self.liberar_mesas(grupo, agregar_evento, tiempo_final,
                                          tomar_decision, liberar_profe),
                       "liberar_mesas", ["Restaurant", "Grupo"], self)
        return True

    def liberar_mesas(self, grupo, agregar_evento, tiempo_final,
                      tomar_decision, liberar_profe):
        def _liberar_mesas():
            """grupo: Grupo, agregar_evento: function, tiempo_final: (int, int)
            tomar_decision: function, liberar_profe: function
            libera las mesas que está usando un grupo para permitirle el
            espacio a otros grupos, retorna False"""
            self.cobrar_grupo(grupo)
            for grupo_ in self.grupos:
                if grupo.id_ == grupo_.id_:
                    self.grupos.remove(grupo_)
            grupo.comer()
            agregar_evento(tiempo_final, tomar_decision(grupo, tiempo_final),
                           "tomar_decision", ["Grupo"], grupo)
            liberar_profe(self.id_)
            return False

        return _liberar_mesas

    def cerrar_parque(self):
        """reinicia los valores al cerrar el parque, retorna None"""
        self.grupos = []
        self.profesor = None
        self.dinero_recaudado = 0
        self.tiempos_en_restaurant = []

    def __repr__(self):
        return "Restaurant {} id: {}".format(self.nombre, self.id_)


class Atraccion(Instalacion):

    def __init__(self, id_, name, capacity, adult_cost, child_cost, duration,
                 min_height, dirt_limit, max_time, type_):
        """type_: str, altura_minima: int, limite_suciedad: int,
        maxima_espera: int, operador: Operador, tiempo_fin: (int, int),
        fin_espera: (int, int), _tasa_fallas: float, _suciedad: int,
        fila: List[Grupo], invasion_ruziland: bool, proxima_falla: (int, int)
        fallas_ruziland: int, fallas_totales: int,
        inicio_reparacion: (int, int), self.llantos: int
        """
        super().__init__(id_, name, capacity, adult_cost, child_cost, duration)
        self.type_ = type_
        self.altura_minima = min_height
        self.limite_suciedad = dirt_limit
        self.maxima_espera = max_time
        self.operador = None
        self.tiempo_fin = None
        self.fin_espera = None
        self._tasa_fallas = 1 / (self.tiempo_uso * self.capacidad)
        self._suciedad = par.SUCIEDAD_INICIAL
        self.fila = []
        self.invasion_ruziland = False
        self.proxima_falla = sumar_tiempo(par.HORA_ABRIR,
                                          (0, self.tiempo_entre_fallas))
        self.fallas_totales = 0
        self.fallas_ruziland = 0
        self.inicio_reparacion = None
        self.llantos = 0

    @property
    def suciedad(self):
        """retorna el valor de _suciedad"""
        return self._suciedad

    @suciedad.setter
    def suciedad(self, value):
        """value: int, cambia el valor de _suciedad"""
        self._suciedad = value

    @property
    def largo_fila(self):
        """retorna la cantidad de personas en la fila"""
        return sum(grupo.cantidad_personas for grupo in self.fila)

    @property
    def tiempo_entre_fallas(self):
        """retorna la diferencia de tiempo en minutos en que ocurrirá la
        próxima falla"""
        time = max(par.TIEMPO_FALLA_MINIMA, expovariate(self._tasa_fallas))
        if self.invasion_ruziland:
            return time / 2
        return time

    @property
    def tiempo_limpieza(self):
        """retorna el tiempo que se tarda en limpiar la atracción"""
        return min(self.suciedad - self.limite_suciedad,
                   par.TIEMPO_MAXIMO_LIMPIEZA)

    def nino_llora(self):
        self.llantos += 1

    def aumentar_suciedad(self, value):
        """value: int, cambia el valor de suciedad, retorna None"""
        self.suciedad += value

    def agregar_a_fila(self, grupo, agregar_evento, tiempo, realizar_decision,
                       borrar_evento, retirarse):
        """grupo: Grupo, agregar_evento: function, tiempo: (int, int),
        realizar_decision: function, borrar_evento: function,
        retirarse: function. Evalúa si se puede entrar a la fila,
        retorna bool"""
        tiempo_final = sumar_tiempo(tiempo, (0, self.tiempo_uso +
                                             self.maxima_espera))
        if tiempo_final[0] >= par.HORA_CIERRE[0]:
            return False
        grupo.tiempo_inicio = tiempo
        tiempo_espera = (0, grupo.paciencia_minima)
        if not grupo.planificar_evento():
            funcion = self.salida_por_paciencia(
                grupo, agregar_evento, realizar_decision,
                sumar_tiempo(tiempo, tiempo_espera))
            agregar_evento(sumar_tiempo(tiempo, tiempo_espera), funcion,
                           "Salir de fila(paciencia)", ["Grupo", "Atraccion"],
                           grupo)

        self.fila.append(grupo)
        if not self.tiempo_fin:
            self.esperar_clientes(agregar_evento, tiempo, realizar_decision,
                                  borrar_evento, retirarse)
        return True

    def esperar_clientes(self, agregar_evento, tiempo,
                         realizar_decision, borrar_evento, retirarse):
        """agregar_evento: function, tiempo: (int, int),
        realizar_decision: function, borrar_evento: function,
        retirarse: function. Pasa a los grupos a la fila de espera, evalúa
        si se lleno la capacidad y parte el juego o programa la partida de este
        según el tiempo de espera. retorna None"""
        se_llena = self.subir_grupos()
        if se_llena:
            borrar_evento(self)
            agregar_evento(
                tiempo, self.correr_juego(agregar_evento,
                                          sumar_tiempo(tiempo, (0, 1)),
                                          realizar_decision,
                                          borrar_evento, retirarse),
                "correr juego", ["Grupo", "Atraccion"], self)
        else:
            if not self.fin_espera:
                fin_espera = sumar_tiempo(tiempo, (0, self.maxima_espera))
                self.fin_espera = fin_espera
                agregar_evento(fin_espera,
                               self.correr_juego(agregar_evento, fin_espera,
                                                 realizar_decision,
                                                 borrar_evento, retirarse),
                               "correr juego", ["Grupo", "Atraccion"], self)

    def subir_grupos(self):
        """Sube a los grupos si es que el juego no esta andando y no se ha
        superado la capacidad, retorna bool si se llena la atracción"""
        if self.tiempo_fin:
            return False
        i = 0
        while i < len(self.fila):
            grupo = self.fila[i]
            if grupo.cantidad_personas + self.cantidad_personas \
                    <= self.capacidad:
                self.grupos.append(self.fila.pop(i))
                if self.cantidad_personas == self.capacidad:
                    return True
            i += 1
        return False

    def salida_por_paciencia(self, grupo, agregar_evento, realizar_decision,
                             tiempo):
        def _salida_por_paciencia():
            """grupo: Grupo, agregar_evento: function,
            realizar_decision: function, tiempo: (int, int), programa la
            salida de un grupo de la fila en caso de que se leacabe la
            paciencia  a algún mimebro del grupo, retorna True"""
            agregar_evento(tiempo, realizar_decision(grupo, tiempo,
                                                     grupo.siguiente_accion),
                           "realizar_decision", ["Grupo", "Atraccion"], grupo)
            for grupo_ in self.grupos:
                if grupo.id_ == grupo_.id_:
                    self.grupos.remove(grupo_)
            for grupo_ in self.fila:
                if grupo.id_ == grupo_.id_:
                    self.fila.remove(grupo_)
            grupo.tiempos_perdidos.append(diferencia(tiempo,
                                                     grupo.tiempo_inicio))
            return True

        return _salida_por_paciencia

    def correr_juego(self, agregar_evento, tiempo, realizar_decision,
                     borrar_evento, retirarse):
        def _correr_juego():
            """agregar_evento: function, tiempo: (int, int),
            realizar_decision: function, borrar_evento: function,
            retirarse: function, corre el juego y retorna True si es que está
            el operador y no está fuera de servicio, de lo contrario
            retorna False"""
            if self.operador and not self.fuera_de_servicio:
                self.revisar_estado(tiempo)
                tiempo_ = sumar_tiempo(tiempo, (0, self.tiempo_uso - 0.001))
                if tiempo_[0] >= par.HORA_CIERRE[0]:
                    self.fuera_de_servicio = True
                    return False
                for grupo in self.grupos:
                    grupo.subir_atraccion(self.aumentar_suciedad)
                self.tiempo_fin = sumar_tiempo(tiempo, (0, self.tiempo_uso))
                agregar_evento(tiempo_,
                               self.bajar_grupos(agregar_evento, tiempo_,
                                                 realizar_decision,
                                                 borrar_evento, retirarse),
                               "bajar grupos", ["Grupo", "Atraccion"], self)
                return True
            else:
                return False

        return _correr_juego

    def bajar_grupos(self, agregar_evento, tiempo, realizar_decision,
                     borrar_evento, retirarse):
        def _bajar_grupos():
            """agregar_evento: function, tiempo: (int, int),
            realizar_decision: function, borrar_evento: function,
            retirarse: function. Baja a los grupos cuando se termina el juego
            y hace que tomen nuevas decisiones, retorna False"""
            for grupo in self.grupos:
                self.cobrar_grupo(grupo)
                agregar_evento(
                    tiempo, realizar_decision(grupo, tiempo,
                                              grupo.siguiente_accion),
                    "tomar decision", ["Grupo"], grupo)
                grupo.tiempos_en_fila.append(diferencia(tiempo,
                                                        grupo.tiempo_inicio))
                grupo.bajar_de_atraccion(agregar_evento, borrar_evento,
                                         retirarse, tiempo, self.nino_llora)
            self.grupos = []
            self.revisar_suciedad(tiempo)
            self.tiempo_fin = None
            self.fin_espera = None
            if self.fila:
                self.esperar_clientes(agregar_evento, tiempo,
                                      realizar_decision, borrar_evento,
                                      retirarse)

            return False

        return _bajar_grupos

    def revisar_suciedad(self, tiempo):
        """tiempo: (int, int), revisa el nivel de suciedad de la atracción
        y llama al limpiador en caso de ser necesario. retorna None"""
        if self.suciedad > self.limite_suciedad:
            self.operador.llamar_limipieza(self.id_, tiempo)

    def revisar_estado(self, tiempo_inicial):
        """tiempo_inicial: (int, int), revisa si la atracción fallará en
        el futuro cercano o si esta ya falló y llama al técnico
        de ser necesario. retorna None"""
        tiempo = sumar_tiempo(tiempo_inicial, (0, self.tiempo_uso))
        mayor_tiempo = comparar_tiempo(tiempo, self.proxima_falla)
        if mayor_tiempo == 1:
            self.operador.llamar_tecnico(self.id_, tiempo_inicial)

    def cerrar_parque(self):
        """resetea los valores cuando se cierra el aprque, retorna None"""
        self.dinero_recaudado = 0
        self.fila = []
        self.grupos = []
        self.tiempo_fin = None
        self.fin_espera = None
        self.fuera_de_servicio = False
        self.invasion_ruziland = False
        self.fallas_ruziland = 0
        self.llantos = 0
        self.proxima_falla = sumar_tiempo(par.HORA_ABRIR,
                                          (0, self.tiempo_entre_fallas))

    def dejar_de_limpiar(self, agregar_evento, tiempo,
                         realizar_decision, borrar_evento, retirarse):
        """agregar_evento: function, tiempo: (in, int),
        realizar_decision: function, borrar_evento: function,
        retirarse: function. reinicia los valores antes de limpiar y reinicia
        el funcionamiento del juego. retorna None"""
        self.tiempo_fin = None
        self.fin_espera = None
        self.suciedad = par.SUCIEDAD_INICIAL
        if self.grupos or self.fila:
            self.esperar_clientes(agregar_evento, tiempo,
                                  realizar_decision, borrar_evento, retirarse)

    def dejar_de_reparar(self, agregar_evento, tiempo,
                         realizar_decision, borrar_evento, retirarse):
        """agregar_evento: function, tiempo: (in, int),
        realizar_decision: function, borrar_evento: function,
        retirarse: function. reinicia los valores antes de reparar y reinicia
        el funcionamiento del juego. retorna None"""
        self.fuera_de_servicio = False
        self.tiempo_fin = None
        self.fin_espera = None
        self.proxima_falla = sumar_tiempo(tiempo,
                                          (0, self.tiempo_entre_fallas))
        if self.grupos or self.fila:
            self.esperar_clientes(agregar_evento, tiempo,
                                  realizar_decision, borrar_evento, retirarse)

    def permite_entrada(self, grupo):
        """grupo: Grupo, evalúa si el grupo cumple con los requsitos mínimos
        de entrada a la atracción, retorna un booleano"""
        if self.fuera_de_servicio:
            return False
        if grupo.altura_minima < self.altura_minima:
            return False
        return super().permite_entrada(grupo)

    def __repr__(self):
        ret = "Atracción " + self.nombre
        return ret
