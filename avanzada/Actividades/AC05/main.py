# Aquí van tus imports, estos pueden servirte
from collections import namedtuple
from operator import attrgetter
from functools import reduce

# from operator import attrgetter
# from functools import reduce

# ---------- FUNCIONES DE CSV ----------


def cleaner(line):
    *info, legendary = line.rstrip("\n").lower().split(",")
    return info + [legendary.lower() == "true"]

def obtener_data(nombre_archivo, nombre_tupla):
    """
    Esta función se utiliza para obtener un generador que les entregue los
    pokémones o entrenadores.

    Para generar pokémones deben usar "obtener_data('pokemondb.csv', 'Pokémon')"
    Para generar entrenadores, "obtener_data('entrenadoresdb.csv', 'Entrenador')"

    :param nombre_archivo: Nombre de la base de datos que deseen utilizar
    :param nombre_tupla: Nombre de las namedtuple
    :return: Generador de namedtuples
    """
    with open(nombre_archivo, mode="r", encoding="UTF-8") as file:
        data = file.readline().rstrip("\n").split(",")
        entidad = namedtuple(nombre_tupla, data)
        for line in file:
            yield entidad(*cleaner(line))


# ---------- FUNCIONES ----------


def pokédex_regional(generación, pokémones):
    """
    Retorna un generador con todos los pokémones de cierta generación que
    se encuentran en el iterable pokémones
    :param gen: int del 1 al 7
    :param pokémones: iterable de pokémones
    :return: generador
    """
    return (pok for pok in pokémones if int(pok.generacion) == int(generación))

def obtener_estadística(estadística, pokémon):
    """
    Recibe una estadística como string y un pokémon, y debe retornar el valor
    de la estadística del pokémon.

    :param estadística: string de estadística
    :param pokémon: pokémon
    :return: int
    """
    est = attrgetter(estadística)
    return int(est(pokémon))

def obtener_estadística_promedio(estadística, pokémones):
    """
    Recibe una estadística en forma de string y un iterable de pokémones,
    y debe retornar el promedio de esa estadística para todos los pokémones.

    :param estadística: string de estadística
    :param pokémones: iterable de pokémones
    :return: float
    """
    pokes = list(pokémones)
    est = lambda pok: obtener_estadística(estadística, pok)
    valores = (est(x) for x in pokes)
    return reduce(lambda x, y: x + y, valores)/len(pokes)


def pokémones_buena_estadística(estadística, pokémones):
    """
    Recibe una estadística y un iterable de pokémones y
    debe retornar un generador de todos los pokémones
    cuya estadística sea mejor que el promedio.

    :param estadística: string de estadística
    :param pokémones: iterable de pokémones
    :return: generador
    """
    promedio = obtener_estadística_promedio(estadística, pokémones)
    est = lambda pok: obtener_estadística(estadística, pok)
    return filter(lambda x: est(x) > promedio, pokémones)


def pokémon_para_entrenador(entrenador, pokémones):
    """
    Recibe un entrenador y un iterable de pokémones y debe
    retornar un generador para los 6 mejores pokémones del entrenador.

    :param entrenador: entrenador
    :param pokémones: iterable de pokémones
    :return: generador
    """
    favorita = entrenador.estadistica_favorita
    est = lambda pok: obtener_estadística(favorita, pok)
    tipo = entrenador.tipo_favorito
    pokes = pokémones_buena_estadística(favorita, pokémones)
    pokes = filter(lambda x: x.tipo_1 == tipo or x.tipo_2 == tipo, pokes)
    if not entrenador.legendario:
        pokes = filter(lambda x: x.legendario == False, pokes)
    pokes = sorted(pokes, key=lambda x: est(x), reverse=True)
    pokes = pokes[:6]
    return (pok for pok in pokes)

    # una forma más limpia de hacerlo habría sido: (pero usaba for)
    # for i in range(6):
    #   try:
    #       yield pokes[i]
    #   except IndexError:
    #       break

def poder_total_entrenador(entrenador, pokémones):
    """
    Recibe un entrenador y un iterable de pokémones, 
    y retorna el poder total de este.

    :param entrenador: entrenador
    :param pokémones: iterable de pokémones
    :return: int
    """

    # para esta parte asumi que los pokémones son todos y que debo
    # formar un equipo con ellos según la función anterior
    equipo = pokémon_para_entrenador(entrenador, pokémones)
    est = lambda pok: obtener_estadística("total", pok)
    return reduce(lambda x, y: est(x) + est(y), equipo)


# ---------- AQUI SE CORRE EL CÓDIGO ----------

if __name__ == "__main__":

    def consultas(tipo, estadistica):
        pokemones = list(obtener_data("pokemondb.csv", "pokemon"))
        entrenadores = obtener_data("entrenadoresdb.csv", "entrenador")
        filtrados = filter(lambda x: x.tipo_favorito.lower() == tipo.lower()
                                     and x.estadistica_favorita.lower() ==
                                     estadistica.lower(), entrenadores)
        equipos = (set(pokémon_para_entrenador(x, pokemones)) for x in
                   filtrados)
        set_comun = reduce(lambda x, y: x.intersection(y), equipos)
        print("—— Poḱemones en comun: {} y {} ——".format(tipo, estadistica))
        for pok in set_comun:
            print(pok.nombre)

    consultas("Hoja", "Ataque")
    consultas("Agua", "Defensa_Especial")
    consultas("Fuego", "Ataque_Especial")

    # ------------- CONSULTA -------------
    # Aquí debe realizar la consulta de todos los Pokémon que se repitan en los equipos de cada entrenador con el
    # tipo favorito y estadística favorita que se les entregó

    # -------------
    # TESTEOS
    # -------------
    # Hoja y ataque
    # -------------
    # Tsareena
    # Breloom
    # Dhelmise
    # Cacturne
    # -----------------------
    # Agua y defensa_especial
    # -----------------------
    # Mantine
    # Araquanid
    # Toxapex
    # Pyukumuku
    # -----------------------
    # Fuego y ataque_especial
    # -----------------------
    # Chandelure
    # Volcarona

    pass
