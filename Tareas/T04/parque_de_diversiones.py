# Módulo destinado a implementar la simulación del parque de diversiones.

# importar como pdd
import cargar_archivos as c_a
from personas import Operador, Limpiador, Tecnico, Grupo, Adulto
import parameters as par
from eventos import Evento, Lluvia, DiaColegio, Ruziland
from random import uniform, choice, choices
from funcion_tiempo import sumar_tiempo, diferencia
from estadisticas import Estadisticas


class ParqueDeDiversiones:

    def __init__(self):
        """self.atracciones: {str(id_): Atraccion} -> instancia con operadores
        self.restaurantes: {str(id_): estaurant}, self._eventos: List[Evento],
        arrivals: {str(día): Arrival}, operadores_en_colacion: List[Operador],
        porteros: List[Operador], grupos: List[Grupo], 
        dias_simulacion: Generator[str], iteracion: int, dia_actual: str, 
        _limpiadores: List[Limpiador], _tecnicos: List[Tecnico], 
        restricciones: bools, operadores_disponibles: List[Operador],
        profesores_disponibles: List[Adulto], estadisticas: Estadisticas,
        atraccion_falladora: atraccion,
        arma el parque y llama a un nuevo día."""
        self.atracciones = c_a.load_attractions()
        for atraccion in self.atracciones.values():
            atraccion.operador = Operador(atraccion.id_, self.llamar_limpieza,
                                          self.llamar_tecnico)
        self.restaurantes = c_a.load_restaurants()
        self._eventos = []
        self.arrivals = c_a.load_arrivals()
        self.operadores_en_colacion = []
        self.porteros = [Operador() for _ in range(3)]
        self.grupos = []
        self.dias_simulacion = (dia for dia in par.DIAS_SIMULACION)
        self.iteracion = 1
        self.dia_actual = None
        self._limpiadores = [Limpiador() for _ in
                             range(len(self.atracciones) //
                                   par.PROPORCION_LIMPIADORES)]
        self._tecnicos = [Tecnico() for _ in range(len(self.atracciones) //
                                                   par.PROPORCION_TECNICOS)]
        self.restriccion_lluvia = False
        self.restriccion_colegio = False
        self.restriccion_ruziland = False
        self.operadores_disponibles = []
        self.profesores_disponibles = []
        self.estadisticas = Estadisticas()
        self.atraccion_falladora = None
        self.dia_nuevo()

    @property
    def limpiadores(self):
        """retorna a los limpiadores ordenados por el largo de sus llamados"""
        self._limpiadores.sort(key=lambda limpiador: len(limpiador.llamados))
        return self._limpiadores

    @property
    def tecnicos(self):
        """retorna a los tecnicos ordenados por el largo de sus llamados"""
        self._tecnicos.sort(key=lambda tecnico: len(tecnico.llamados))
        return self._tecnicos

    @property
    def max_capacity(self):
        """retorna la capacidad máxima del parque: int"""
        ret = sum([a.capacidad for a in self.atracciones.values()]
                  + [r.capacidad for r in self.restaurantes.values()])
        return par.MULTIPLICANDO_CAPACIDAD * ret

    @property
    def personas_actuales(self):
        """retorna la cantidad de personas que hay en el parque: int"""
        return sum((g.cantidad_personas for g in self.grupos))

    @property
    def eventos(self):
        """retorna los eventos ordenados según su tiempo de ocurrencia"""
        self._eventos.sort(key=lambda x: (x.tiempo[0] + (x.tiempo[1] / 100)))
        return self._eventos

    def agregar_evento(self, tiempo, funcion, descripcion, afectados,
                       entidad_generadora):
        """tiempo: (int, int), funcion: function, descripcion: str,
        afectados: List[str], entidad_generadora: Object, agrega un evento
        a la lista de eventos, retorna None"""
        self._eventos.append(Evento(tiempo, self.dia_actual, funcion,
                                    self.iteracion, descripcion,
                                    " - ".join(entidad for entidad in
                                               afectados),
                                    str(entidad_generadora)))

    def borrar_evento(self, generador):
        """generador: object, borra tooos los eventos futuros de un determinado
        generador. retorna None"""
        self._eventos = list(
            filter(lambda x: (x.generador != str(generador)
                              or str(generador) == "Nebiland"),
                   self.eventos))

    def llega_grupo(self, grupo, tiempo, grupos=False):
        def _llega_grupo():
            """grupo: Grupo o List[Grupo]
            tiempo: (int, int), grupos: bool, ingresa al grupo o los grupos
            si estos no superan la capacidad, retorna bool"""
            if grupos:
                if self.personas_actuales + len(grupo) <= self.max_capacity:
                    for g in grupo:
                        self.grupos.append(g)
                        self.agregar_evento(
                            tiempo, self.tomar_decision(g, tiempo),
                            "tomar decision", ["Grupo"], g)
                return True
            else:
                if self.personas_actuales + grupo.cantidad_personas <= \
                        self.max_capacity:
                    self.grupos.append(grupo)
                    self.agregar_evento(
                        tiempo, self.tomar_decision(grupo, tiempo),
                        "tomar decision", ["Grupo"], grupo)
                    return True
            return False

        return _llega_grupo

    def dia_nuevo(self):
        """reinicia todos los valores para un día nuevo, revisa si es que
        quedan dias de la simulacion y llama a la ejecución del dia siguiente
        si es posible, retorna True"""
        for grupo in self.grupos:
            self.agregar_estadisticas(grupo)
        self.grupos = []
        self._eventos = []
        self.profesores_disponibles = []
        for limpiador in self.limpiadores:
            limpiador.estado_inicial()
        for tecnico in self.tecnicos:
            tecnico.estado_inicial()
        for atraccion in self.atracciones.values():
            if self.restriccion_colegio:
                self.estadisticas.dinero_dias_colegio \
                    += atraccion.dinero_recaudado
            if self.restriccion_ruziland:
                self.estadisticas.fallas_ruziland += atraccion.fallas_totales
            self.estadisticas.llantos[atraccion.id_].append(atraccion.llantos)
            atraccion.cerrar_parque()
            self.borrar_evento(atraccion)
        for restaurant in self.restaurantes.values():
            if self.restriccion_colegio:
                self.estadisticas.dinero_dias_colegio \
                    += restaurant.dinero_recaudado
            self.estadisticas.tiempos_en_restaurant.extend(
                restaurant.tiempos_en_restaurant)
            restaurant.cerrar_parque()
            self.borrar_evento(restaurant)
        try:
            dia = next(self.dias_simulacion)
            self.dia_actual = dia
        except StopIteration:
            return True
        self.restriccion_lluvia = False
        self.restriccion_colegio = False
        self.restriccion_ruziland = False
        self.siguiente_lluvia()
        self.dia_reservado()
        self.llega_archienemigo()
        for operador in self.operadores_disponibles:
            self.atracciones[operador.id_atraccion].operador = operador
        self.agregar_evento(par.HORA_ABRIR, self.abrir_parque, "abrir parque",
                            ["Nebiland"], self)
        return True

    def abrir_parque(self):
        """abre el parque, programa las colaciones, llegadas de grupos y revisa
        si hay restricciones especiales para el dia, retorna True"""
        self.horarios_colacion()
        self.agregar_evento(par.HORA_CIERRE, self.dia_nuevo, "cierre parque",
                            ["Nebiland", "Atraccion", "Restaurant"], self)
        if self.restriccion_colegio:
            self.abrir_dia_colegio()
            return True
        for arrival in self.arrivals[self.dia_actual]:
            tiempo = arrival.time.split(":")
            tiempo = (int(tiempo[0]), int(tiempo[1]))
            grupo = Grupo(arrival.budget, arrival.children)
            if self.restriccion_lluvia:
                if grupo.cantidad_personas > 2:
                    self.estadisticas.personas_por_eventos \
                        += grupo.cantidad_personas
                    continue
            if self.restriccion_ruziland:
                if uniform(0, 1) < par.PROBABILIDAD_RETIRARSE:
                    self.estadisticas.personas_por_eventos \
                        += grupo.cantidad_personas
                    continue
            descrpicion = "entra un grupo al parque"
            self.agregar_evento(tiempo, self.llega_grupo(grupo, tiempo),
                                descrpicion, ["Nebiland", "Grupo"], grupo)
        return True

    def horarios_colacion(self):
        """revisa los horarios preferidos (aleatorio) de los operadores y llama
        al del inicio de sus colaciones y el fin de éstas. retorna None"""
        for atraccion in self.atracciones.values():
            tiempo = atraccion.operador.inicio_colacion()
            self.agregar_evento(tiempo,
                                self.programar_colacion(atraccion.id_, tiempo),
                                "escoger hora colación",
                                ["Atraccion", "Operador"], atraccion.operador)
        horarios_porteria = set()
        for operador in self.porteros:
            tiempo = operador.inicio_colacion()
            while tiempo in horarios_porteria:
                tiempo = operador.inicio_colacion()
            horarios_porteria.add(tiempo)
            self.agregar_evento(tiempo, self.colacion(operador.id_atraccion,
                                                      operador.nombre),
                                "inicio colación", ["Nebiland", "Operador"],
                                operador)
            self.agregar_evento((tiempo[0], 59), self.fin_colacion(
                operador.id_atraccion, operador.nombre), "fin colación",
                                ["Nebiland", "Operador"], operador)

    def programar_colacion(self, id_atraccion, hora_escogida):
        def _programar_colacion():
            """id_atracción: str, hora_escogida: (int, int),
            programa las colaciones reales de los operadores, retorna False"""
            atraccion = self.atracciones[id_atraccion]
            if atraccion.tiempo_fin:
                tiempo = atraccion.tiempo_fin
            else:
                tiempo = hora_escogida
            self.agregar_evento(tiempo, self.colacion(atraccion.id_),
                                "inicio colación", ["Atraccion", "Operador"],
                                atraccion.operador)
            if tiempo[1] >= 1:
                tiempo_fin = (tiempo[0] + 1, tiempo[1] - 1)
            else:
                tiempo_fin = (tiempo[0], 59)
            if tiempo_fin[0] >= par.HORA_CIERRE[0]:
                tiempo_fin = (par.HORA_CIERRE[0] - 1, 59)
            self.agregar_evento(tiempo_fin, self.fin_colacion(atraccion.id_),
                                "fin colación", ["Atraccion", "Operador"],
                                atraccion.operador)
            return False

        return _programar_colacion

    def colacion(self, id_atraccion, nombre=None):
        def _colacion():
            """id_atraccion: str, nombre: str, saca a los operadores de sus
            atracciones para que tengan sus descanso y puedan tomar su
            colación, retorna True"""
            if id_atraccion is not None:
                atraccion = self.atracciones[id_atraccion]
                self.operadores_en_colacion.append(atraccion.operador)
                atraccion.operador = None
                if self.operadores_disponibles:
                    atraccion.operador = self.operadores_disponibles.pop(0)
                else:
                    self.borrar_evento(atraccion)
            else:
                operador = next(filter(lambda x: x.nombre == nombre,
                                       self.porteros))
                self.operadores_en_colacion.append(operador)
                self.porteros = list(filter(lambda x: x is not operador,
                                            self.porteros))

            return True

        return _colacion

    def fin_colacion(self, id_atraccion, nombre=None):
        def _fin_colacion():
            """id_atraccion: str, nombre: str, devuelve a los operadores al
            trabajo y los designa s la misma atracción en la que estaban antes
            o a la portería, retorna False"""
            if id_atraccion is not None:
                atraccion = self.atracciones[id_atraccion]
                if atraccion.operador is not None:
                    self.operadores_disponibles.append(atraccion.operador)
                    atraccion.operador = None
                operador = next(filter(
                    lambda x: x.id_atraccion == id_atraccion,
                    self.operadores_en_colacion))
                self.operadores_en_colacion.remove(operador)
                atraccion.operador = operador
            else:
                operador = next(filter(lambda x: x.nombre == nombre,
                                       self.operadores_en_colacion))
                self.operadores_en_colacion.remove(operador)
                self.porteros.append(operador)
            return True

        return _fin_colacion

    def tomar_decision(self, grupo, tiempo_inicial):
        def _tomar_decision():
            """grupo: Grupo, tiempo_inicial: (int, int), le entrega al grupo,
            las posibilidades de realizar ciertas acciones y éste escoge una
            según una probabilidad, luego crea el evento de su próxima
            decisión, retorna False"""
            self.borrar_evento(grupo)
            probabilidad = uniform(0, 1)
            tiempo = sumar_tiempo(tiempo_inicial, par.TIEMPO_DECIDIR)
            if probabilidad < par.PROBABILIDAD_HACER_FILA:
                atraccion = self.escoger_atraccion(grupo)
                if atraccion:
                    self.agregar_evento(
                        tiempo, self.hacer_fila(grupo, atraccion, tiempo),
                        "hacer fila en atracción", ["Atraccion", "Grupo"],
                        grupo)
                else:
                    self.borrar_evento(grupo)
                    self.agregar_evento(tiempo,
                                        self.retirarse_del_parque(grupo),
                                        "retirarse de nebiland",
                                        ["Nebiland", "Grupo"], grupo)
            elif probabilidad < par.PROBABILIDAD_HACER_FILA \
                    + (grupo.hambre_promedio * par.MULTIPLICANDO_HAMBRE):
                restaurant = self.escoger_restaurant(grupo)
                if restaurant:
                    self.agregar_evento(tiempo, self.comer(grupo, restaurant,
                                                           tiempo),
                                        "comer en restaurante",
                                        ["Restaurant", "Grupo"], grupo)
                else:
                    self.estadisticas.personas_sin_comer \
                        += grupo.cantidad_personas
                    self.agregar_evento(tiempo, self.descansar(grupo, tiempo),
                                        "descansar", ["Grupo"], grupo)
            else:
                self.agregar_evento(tiempo, self.descansar(grupo, tiempo),
                                    "descansar", ["Grupo"], grupo)
            grupo.siguiente_accion = None
            return False

        return _tomar_decision

    def realizar_decision(self, grupo, tiempo_inicial, decision):
        def _realizar_decision():
            """grupo: Grupo, tiempo_inicial: (int, int), decision: str, realiza
            una acción específica, según lo que el grupo decidió anteriormente,
            retorna None."""
            self.borrar_evento(grupo)
            tiempo = sumar_tiempo(tiempo_inicial, par.TIEMPO_DECIDIR)
            if decision == "divertirse":
                atraccion = self.escoger_atraccion(grupo)
                if atraccion:
                    self.agregar_evento(
                        tiempo, self.hacer_fila(grupo, atraccion, tiempo),
                        "hacer fila en atracción", ["Atraccion", "Grupo"],
                        grupo)
                else:
                    self.borrar_evento(grupo)
                    self.agregar_evento(tiempo,
                                        self.retirarse_del_parque(grupo),
                                        "retirarse de nebiland",
                                        ["Nebiland", "Grupo"], grupo)
            elif decision == "comer":
                restaurant = self.escoger_restaurant(grupo)
                if restaurant:
                    self.agregar_evento(tiempo, self.comer(grupo, restaurant,
                                                           tiempo),
                                        "comer en restaurante",
                                        ["Restaurant", "Grupo"], grupo)
                else:
                    self.estadisticas.personas_sin_comer \
                        += grupo.cantidad_personas
                    self.agregar_evento(tiempo, self.descansar(grupo, tiempo),
                                        "descansar", ["Grupo"], grupo)
            else:
                self.agregar_evento(tiempo, self.descansar(grupo, tiempo),
                                    "descansar", ["Grupo"], grupo)
            grupo.siguiente_accion = None
            return False

        return _realizar_decision

    def escoger_atraccion(self, grupo):
        """As seen at: https://stackoverflow.com/questions/3679694/
        a-weighted-version-of-random-choice.
        grupo: Grupo
        retorna la atracción en la que hará fila el grupo"""
        posibles = (a.id_ for a in filter(lambda x: x.permite_entrada(grupo),
                                          self.atracciones.values()))
        posibles = list(set(posibles) - grupo.juegos_visitados)
        if posibles:
            atracciones = [self.atracciones[posibles[i]] for i in
                           range(len(posibles))]
            pesos = [1 / max(1, x.largo_fila) for x in atracciones]
            chosen_one = choices(posibles, weights=pesos)
            grupo.juegos_visitados.add(chosen_one[0])
            return self.atracciones[chosen_one[0]]
        else:
            if not grupo.juegos_visitados:
                return None
            grupo.juegos_visitados = set()
            return self.escoger_atraccion(grupo)

    def escoger_restaurant(self, grupo, posibles=None):
        """grupo: Grupo, posibles: set(str), retorna un restaurant escogido por
        el grupo dentro de sus posibilidades o bien None si no puede ingresar
        a nnguno"""
        if posibles is None:
            posibles = list((r.id_ for r in
                             filter(lambda x: x.permite_entrada(grupo),
                                    self.restaurantes.values())))
        if posibles:
            id_restaurant = choice(posibles)
            restaurant = self.restaurantes[id_restaurant]
            if self.restriccion_colegio:
                if not restaurant.profesor:
                    if self.profesores_disponibles:
                        restaurant.profesor = \
                            self.profesores_disponibles.pop(0)
                    else:
                        _posibles = list(filter(lambda x: x != id_restaurant,
                                                posibles))
                        return self.escoger_restaurant(
                            grupo, _posibles)
            return restaurant
        return None

    def hacer_fila(self, grupo, atraccion, tiempo):
        def _hacer_fila():
            """grupo: Grupo, atraccion: Atraccion, tiempo: (int, int),
            ingresar un grupo a la fila de la atracción. retorna bool (si se
            puede ingresar a la fila o no)."""
            ret = atraccion.agregar_a_fila(grupo, self.agregar_evento, tiempo,
                                           self.realizar_decision,
                                           self.borrar_evento,
                                           self.retirarse_del_parque)
            if not ret:
                self.agregar_evento(tiempo, self.tomar_decision(grupo, tiempo),
                                    "tomar_decision", ["Grupo"], grupo)
            return ret

        return _hacer_fila

    def comer(self, grupo, restaurant, tiempo):
        def _comer():
            """grupo: Grupo, restaurant: Restaurant, tiempo: (int, int),
            intenta ingresar a un grupo al Restaurant, retorna bool"""
            ret = restaurant.entra_grupo(grupo, self.agregar_evento, tiempo,
                                         self.tomar_decision,
                                         self.liberar_profe)
            if not ret:
                self.agregar_evento(tiempo, self.tomar_decision(grupo, tiempo),
                                    "tomar_decision", ["Grupo"], grupo)
            return ret

        return _comer

    def descansar(self, grupo, tiempo_inicio):
        def _descansar():
            """grupo: Grupo, tiempo_inicio: (int, int),
            hace descansar a un grupo y programa el fin de éste,
            retorna True"""
            grupo.descansar()
            tiempo = (tiempo_inicio[0] + 1, tiempo_inicio[1])
            self.agregar_evento(tiempo, self.tomar_decision(grupo, tiempo),
                                "tomar_decision", ["Grupo"], grupo)
            return True

        return _descansar

    def llamar_limpieza(self, id_atraccion, tiempo_inicial, limpiador=None):
        """id_atraccion: str, tiempo_inicial: (int, int), limpiador: Limpiador,
        llama a un limpiador, para que limpie una determinada atracción,
        retorna None"""
        if limpiador is None:
            limpiador = self.limpiadores[0]
        limpiando = limpiador.agregar_llamado(id_atraccion)
        atraccion = self.atracciones[id_atraccion]
        tiempo = sumar_tiempo(tiempo_inicial, (0, limpiador.tiempo_traslado))
        if not limpiando:
            self.estadisticas.llamados_limpieza += 1
            limpiador.limpiando = True
            self.agregar_evento(
                tiempo, self.comenzar_limpiar(limpiador, tiempo, atraccion),
                "trasladarse", ["Atraccion", "Limpiador"], limpiador)

    def comenzar_limpiar(self, limpiador, tiempo_inicial, atraccion):
        def trasladarse():
            """limpiador: Limpiador, tiempo_inicial: (int int),
            atraccion: Atraccion, programa el momento en que el limpiador
            llegará a la atracción  a limpiar, retorna False"""
            tiempo = atraccion.tiempo_fin
            if atraccion.tiempo_fin is None:
                tiempo = tiempo_inicial
            self.agregar_evento(tiempo,
                                self.limpiar(limpiador, tiempo, atraccion),
                                "limpiar atracción",
                                ["Atraccion", "Limpiador"], limpiador)
            return False

        return trasladarse

    def limpiar(self, limpiador, tiempo_inical, atraccion):
        def _limpiar():
            """limpiador: Limpiador, tiempo_iniciao: (int, int),
            atraccion: Atraccion, limpia una atracción, retorna True"""
            tiempo = sumar_tiempo(tiempo_inical, (0,
                                                  atraccion.tiempo_limpieza))
            if atraccion.tiempo_limpieza < 0:
                return False
            self.borrar_evento(atraccion)
            self.agregar_evento(
                tiempo, self.dejar_de_limpiar(limpiador, tiempo, atraccion),
                "dejar de limpiar", ["Atraccion", "Limpiador"], limpiador)
            return True

        return _limpiar

    def dejar_de_limpiar(self, limpiador, tiempo, atraccion):
        def _dejar_de_limpiar():
            """limpiador: Limpiador, tiempo: (int, int), atraccion: Atraccion,
            deja de limpiar una atracción y revisa si quedan más por limpiar,
            retorna False"""
            limpiador.limpiando = False
            atraccion.dejar_de_limpiar(
                self.agregar_evento, tiempo, self.realizar_decision,
                self.borrar_evento, self.retirarse_del_parque)
            limpiador.dejar_de_limpiar(self.llamar_limpieza, tiempo)
            return False

        return _dejar_de_limpiar

    def llamar_tecnico(self, id_atraccion, tiempo_inicial, tecnico=None):
        """id__atraccion: str, tiempo_inicial: (int, int), tecnico: Tecnico,
        llama al técnico para que limpie una determinada atracción,
        retorna None"""
        if tecnico is None:
            tecnico = self.tecnicos[0]
        reparando = tecnico.agregar_llamado(id_atraccion)
        atraccion = self.atracciones[id_atraccion]
        atraccion.fuera_de_servicio = True
        atraccion.inicio_reparacion = tiempo_inicial
        self.borrar_evento(atraccion)
        tiempo = sumar_tiempo(tiempo_inicial, (0, tecnico.tiempo_traslado))
        if not reparando:
            self.estadisticas.llamados_tecnicos += 1
            tecnico.reparando = True
            self.agregar_evento(
                tiempo, self.reparar(tecnico, tiempo, atraccion),
                "reparar atracción", ["Atraccion", "Tecnico"], tecnico)

    def reparar(self, tecnico, tiempo_inicial, atraccion):
        def _reparar():
            """tecnico: Tecnico, tiempo_inicial: (int, int),
            atraccion: Atraccion, repara una atracción, retorna True"""
            atraccion.fallas_totales += 1
            if self.restriccion_ruziland:
                atraccion.fallas_ruziland += 1
            if self.atraccion_falladora is None:
                self.atraccion_falladora = atraccion
            if self.atraccion_falladora.fallas_totales \
                    < atraccion.fallas_totales:
                self.atraccion_falladora = atraccion
            tiempo = sumar_tiempo(tiempo_inicial,
                                  (0, tecnico.tiempo_reparacion))
            self.agregar_evento(
                tiempo, self.dejar_de_reparar(tecnico, tiempo, atraccion),
                "dejar de reparar", ["Atraccion", "Tecnico"], tecnico)
            return True

        return _reparar

    def dejar_de_reparar(self, tecnico, tiempo, atraccion):
        def _dejar_de_reparar():
            """tecnico: Tecnico, tiempo: (int, int), atraccion: Atraccion,
            deja de reparar una atracción, revisa si quedan por reparar,
            retorna False"""

            tecnico.reparando = False
            atraccion.dejar_de_reparar(
                self.agregar_evento, tiempo, self.realizar_decision,
                self.borrar_evento, self.retirarse_del_parque)
            tiempo_fuera_de_servicio = diferencia(tiempo,
                                                  atraccion.inicio_reparacion)
            atraccion.inicio_reparacion = None
            if tiempo_fuera_de_servicio > \
                    self.estadisticas.tiempo_maximo_fuera_de_servicio:
                self.estadisticas.tiempo_maximo_fuera_de_servicio = \
                    tiempo_fuera_de_servicio
            tecnico.dejar_de_reparar(self.llamar_tecnico, tiempo)
            return False

        return _dejar_de_reparar

    def retirarse_del_parque(self, grupo):
        def _retirarse():
            """grupo: Grupo, agrega las estadisticas de un grupo que se retira
            del parque y lo saca de éste. retorna True"""
            self.borrar_evento(grupo)
            for grupo_ in self.grupos:
                if grupo.id_ == grupo_.id_:
                    self.grupos.remove(grupo_)
            self.agregar_estadisticas(grupo)
            return True

        return _retirarse

    def siguiente_lluvia(self):
        """agrega la posibilidad del evento de lluvia, retorna None"""
        self._eventos.append(
            Lluvia(par.HORA_ABRIR, self.dia_actual, self.lluvia,
                   self.iteracion, "lluvia",
                   ["Nebiland", "Atraccion", "Operador"], self))

    def lluvia(self):
        """activa los efectos de un evento externo de lluvia, retorna None"""
        self.restriccion_lluvia = True
        for atraccion in self.atracciones.values():
            if atraccion.type_ in par.TIPOS_QUE_CIERRAN:
                atraccion.fuera_de_servicio = True
                self.operadores_disponibles.append(atraccion.operador)

    def dia_reservado(self):
        """agrega la posibilidad del evento dia colegio, retorna None"""
        self._eventos.append(
            DiaColegio(par.HORA_ABRIR, self.dia_actual, self.dia_colegio,
                       self.iteracion, "dia colegio",
                       ["Nebiland", "Grupo", "Adulto", "Restaurant"], self))

    def dia_colegio(self):
        """activa los efectos de un evento dia colegio, retorna None"""
        self.restriccion_colegio = True

    def abrir_dia_colegio(self):
        """abre el dia, cuando es dia colegio de una forma especial,
        crea grupos de un niño puesto que pueden tomar decisiones por si solos
        y deja a los profesores como dispoibles para que los niños los puedan
        llamar cuando estos quieran comer, retorna None"""
        for arrival in self.arrivals[self.dia_actual]:
            adulto = Adulto(arrival.budget)
            self.profesores_disponibles.append(adulto)
            tiempo = arrival.time.split(":")
            tiempo = (int(tiempo[0]), int(tiempo[1]))
            if arrival.children < 10:
                self.estadisticas.personas_por_eventos += arrival.children + 1
                continue
            grupos = []
            for _ in range(arrival.children):
                grupo = Grupo(arrival.budget / arrival.children, 1,
                              adulto=False)
                grupos.append(grupo)
            self.agregar_evento(tiempo, self.llega_grupo(grupos, tiempo, True),
                                "entra un grupo al parque",
                                ["Nebiland", "Grupo"], adulto)

    def liberar_profe(self, id_restaurant):
        """id_restaurant: str, libera a un profesor que estaba comiendo con un
        niño en el restaurant, retorna None"""
        restaurant = self.restaurantes[id_restaurant]
        self.profesores_disponibles.append(restaurant.profesor)
        restaurant.profesor = None

    def llega_archienemigo(self):
        """agrega la posibilidad del evento invasion ruziland, retorna None"""
        self._eventos.append(
            Ruziland(par.HORA_ABRIR, self.dia_actual, self.invasion_ruziland,
                     self.iteracion, "invasion ruziland",
                     ["Atraccion, Nebiland, Grupo"], self))

    def invasion_ruziland(self):
        """activa lso efectos de una invasión ruziland, retorna None"""
        self.restriccion_ruziland = True
        for atraccion in self.atracciones.values():
            atraccion.invasion_ruziland = True

    def run(self):
        """corre la simulación según el orden de los eventos,
        setea estadisticas para una nueva iteración, retorna None"""
        hora, minuto = par.HORA_CIERRE
        while self.eventos:
            evento = self.eventos.pop(0)
            if evento.tiempo[0] >= hora and evento.tiempo[1] != minuto:
                break
            evento.funcion()
        self.estadisticas.atraccion_falladora = self.atraccion_falladora
        self.estadisticas.siguiente_iteracion()

    def agregar_estadisticas(self, grupo):
        """grupo: Grupo, agrega las estadisticas de un grupo"""
        self.estadisticas.esperas_en_fila.extend(grupo.tiempos_en_fila)
        self.estadisticas.tiempos_perdidos.extend(grupo.tiempos_perdidos)
        if grupo.baja_energia:
            self.estadisticas.personas_retiradas += 1
        else:
            if grupo.adulto:
                self.estadisticas.energia_retirados.append(
                    grupo.adulto.energia)
            for nino in grupo.ninos:
                self.estadisticas.energia_retirados.append(nino.energia)
        self.estadisticas.dinero_no_gastado += grupo.budget

    def __repr__(self):
        return "Nebiland"
