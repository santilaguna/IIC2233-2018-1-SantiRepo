from collections import deque, namedtuple


class Vuelo:

    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
        self.passengers = {}


class PAWControl:

    MAX_PASSENGERS = 5

    def __init__(self):
        """
        :param clients: path del archivo con datos de clientes
        :param booking: path de las reservas
        :param flights: path de los vuelos
        """
        self.clients = None
        self.bookings = None
        self.rejected = []
        self.flights = None

    def _read_clients(self, path):
        """
        :param path: path al archivo de clientes
        :return: estructura de datos con la info de clientes
        """
        clientes = {}
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                name, passport = line.strip("\n").split(",")
                clientes[passport] = name
        return clientes

    def _read_flights(self, path):
        """
        :param path: path al archivo de vuelos
        :return: estructura de datos con los vuelos
        """
        vuelos = {}
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                fid, origin, destination = line.strip("\n").split(",")
                vuelos[fid] = Vuelo(origin, destination)
        return vuelos

    def _read_bookings(self, path):
        """
        :param path: path al archivo de reservas acumuladas
        :return: estructura de datos con las reservas por orden de llegada
        """
        reservas = deque()
        reserva = namedtuple("clase_reserva", ["passport", "fid", "seat"])
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                passport, fid, seat = line.strip("\n").split(",")
                reservas.append(reserva(passport, fid, seat))
        return reservas

    def recovery(self, clients, booking, flights):
        """
        :param clients: path del archivo con datos de clientes
        :param booking: path de las reservas
        :param flights: path de los vuelos
        Este método llama a los métodos de lectura y pobla el sistema
        guardando las estructuras de datos retornadas por dichos métodos
        en las variables clients, bookings, rejected y flights.
        """
        # COMPLETAR BORRANDO pass
        self.clients = self._read_clients(clients)
        self.bookings = self._read_bookings(booking)
        self.flights = self._read_flights(flights)

    def assign_seats(self):
        """
        Método que se encarga de asignar los asientos de acuerdo
        con el orden de llegada de las reservas. Debe actualizar
        el registro de asientos de los aviones para las reservas
        aceptadas y guardar en self.rejected las reservas rechazadas
        """
        # COMPLETAR BORRANDO pass
        for reserva in self.bookings:
            vuelo = self.flights[reserva.fid]
            if reserva.passport in vuelo.passengers.values():
                self.rejected.append(reserva)
                continue
            elif reserva.seat in vuelo.passengers:
                self.rejected.append((reserva.passport, self.clients[reserva.passport], reserva.fid, reserva.seat))
                continue
            else:
                vuelo.passengers[reserva[2]] = reserva.passport

    def passenger_list(self, flight_id):
        '''Recibe el id de un vuelo y RETORNA una lista con todas las tuplas de la forma (seat_number, passport, client_name)'''
        flight_indeed = self.flights[flight_id]
        passenger_list = list()
        # Iteramos en el orden pedido
        for i in range(1, PAWControl.MAX_PASSENGERS + 1):
            seat_number = str(i)
            # Si ya está asignado el asiento, ingresamos los datos
            if seat_number in flight_indeed.passengers:
                passport = flight_indeed.passengers[seat_number]
                client_name = self.clients[passport]
                tuple_asked = (seat_number, passport, client_name)
            # Si el asiento no esta ocupado, dejamos los nombres vacíos
            else:
                tuple_asked = (seat_number, '----', '----')

            passenger_list.append(tuple_asked)
        return passenger_list

    def passengers_to_destination(self, destination):
        set_pasajeros = set()
        for key in self.flights.keys():
            vuelo = self.flights[key]
            if vuelo.destino == destination:
                pasajeros = self.passenger_list(key)
                for pasajero in pasajeros:
                    set_pasajeros.add(pasajero[1])

        return set_pasajeros

    def rejected_bookings(self):
        # COMPLETAR BORRANDO pass
        return self.rejected


if __name__ == '__main__':

    '''Desde aquí NO deben modificar nada'''
    control = PAWControl()
    control.recovery('clients.txt', 'bookings.txt', 'flights.txt')
    control.assign_seats()

    '''Lista de Pasajeros'''
    query12 = control.passenger_list('009')

    print('-'*5 + ' Passenger list ' + '-'*5)
    print("------ Flight {} ------".format('009'))
    print(*query12, sep="\n")

    '''Destino'''
    query21 = control.passengers_to_destination('Concepción')

    print('\n' + '-'*5 + ' Destination ' + '-'*5)
    print("------ Concepción ------")
    print(*query21, sep="\n")

    '''Rejected'''
    print('\n' + '-'*5 + ' Rejected Bookings ' + '-'*5)
    query3 = control.rejected_bookings()
    print(*query3, sep="\n")