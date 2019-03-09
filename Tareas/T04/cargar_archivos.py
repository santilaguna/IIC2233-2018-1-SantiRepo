# Módulo destinado a cargar los datos desde los archivos.

# Importar como c_a

import csv
from itertools import groupby
from collections import defaultdict, namedtuple
from instalaciones import Restaurant, Atraccion
from parameters import PATH_ARRIVALS, PATH_ASSOCIATIONS, PATH_ATTRACTIONS, \
    PATH_RESTAURANTS


def load_arrivals():
    """Carga el archivo de las llegadas, retorna un diccionario con las
    llegadas -> dia(str): List[Arrivals]"""
    with open(PATH_ARRIVALS, "r", encoding="utf-8", newline="") as file:
        lines = [(x["day"], x["time"], x["budget"], x["children"])
                 for x in csv.DictReader(file)]
    lines = sorted(lines, key=lambda x: x[0])
    Arrival = namedtuple("Arrival_type", ["time", "budget", "children"])
    return {x: [Arrival(t, int(b), int(c)) for d, t, b, c in v] for x, v in
            groupby(lines, lambda x: x[0])}


def load_associations():
    """Carga el archivo de las asociaciones, retorna un diccionario
    con las conecciones de los restaurantes con las
    atracciones -> id_restaurant: {ids_atracciones}"""
    with open(PATH_ASSOCIATIONS, "r", encoding="utf-8", newline="") as file:
        lines = [(x["restaurant_id"], x["attraction_id"]) for x in
                 csv.DictReader(file)]
    lines = sorted(lines, key=lambda x: x[0])
    return {x: {_ for k, _ in v} for x, v in groupby(lines,
                                                     key=lambda x: x[0])}


def load_attractions():
    """Carga el archivo de las atracciones, retorna un diccionario con las
    atracciones instanciadas por id -> id_atraccion: Atraccion"""
    with open(PATH_ATTRACTIONS, "r", encoding="utf-8", newline="") as file:
        lines = csv.DictReader(file)
        return {x["id"]: Atraccion(x["id"], x["name"], int(x["capacity"]),
                                   int(x["adult_cost"]), int(x["child_cost"]),
                                   int(x["duration"]), int(x["min_height"]),
                                   int(x["dirt_limit"]), int(x["max_time"]),
                                   x["type"])
                for x in lines}


def load_restaurants():
    """Carga el archivo de los restaurants, retorno un diccionario con los
    restaurantes instanciados por id -> id_restaurant: Restaurant"""
    with open(PATH_RESTAURANTS, "r", encoding="utf-8", newline="") as file:
        conecciones = defaultdict(list)
        conecciones.update(load_associations())
        lines = csv.DictReader(file)
        return {x["id"]: Restaurant(x["id"], x["name"], int(x["capacity"]),
                                    int(x["adult_cost"]), int(x["child_cost"]),
                                    int(x["max_duration"]),
                                    conecciones[x["id"]]) for x in lines}
