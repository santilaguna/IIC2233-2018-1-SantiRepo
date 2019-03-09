# Módulo destinado a elaborar funciones específicas de la tarea
# Contiene funciones que dificilmente podrán usadas en otros programas

# importar como fe

import funciones_utiles as fu
from collections import deque
from collections import namedtuple

def capacidad(raza):
    if raza == "Maestro":
        return 100
    elif raza == "Asesino":
        return 400
    else:
        return 150


def pedir_raza():
    print("""Escoga número de raza:
    1) Aprendiz
    2) Maestro
    3) Asesino""")
    n_raza = fu.pedir_entero(1, 3)
    return n_raza


def pedir_planeta(planetas):
    print()
    nombre = input("Ingrese nombre planeta escogido: ")
    while nombre not in planetas.keys():
        nombre = input("No existe este planeta, ingrese nombre nuevamente: ")
    return nombre


def pedir_galaxia(galaxias):
    print()
    nombre = input("Ingrese nombre galaxia escogida: ")
    while nombre not in galaxias.keys():
        nombre = input("No existe esta galaxia, ingrese nombre nuevamente: ")
    return nombre


def menu_modificar_galaxia():
    print("""¿Qué desea modificar en la galaxia?
    1) Agregar un nuevo planeta no conquistado 
    2) Eliminar un planeta conquistado
    3) Aumentar la tasa de minerales por segundo de un planeta no conquistado
    4) Aumentar la tasa de deuterio por segundo de un planeta no conquistado
    5) Aumentar la cantidad de soldados de un planeta no conquistado
    6) Aumentar la cantidad de magos de un planeta no conquistado
    7) Salir de la galaxia""")
    return fu.pedir_entero(1, 7)


def aumento_tasa(tipo_de_tasa):
    print("¿En cuánto desea aumentar la tasa de {}?".format(tipo_de_tasa))
    aumento = input()
    if aumento.isdigit() and int(aumento) > 0:
        return int(aumento)
    else:
        return 0


def aumento_personas(tipo):
    print("¿En cuánto desea aumentar la cantidad de {}?".format(tipo))
    aumento = input()
    if aumento.isdigit():
        if int(aumento) > 0:
            return int(aumento)
        else:
            return 0
    else:
        return 0


def menu_consultas_galaxias():
    print("""¿Qué desea consultar?
    1) Información general del usuario 
    2) Información general de un planeta
    3) Mejor galaxia
    4) Ranking planetas
    5) Salir de consultas""")
    return fu.pedir_entero(1, 5)


def menu_chaucraft():
    print("""¿Qué deseas hacer?
    1) Crear una galaxia
    2) Modificar una galaxia
    3) Consultar sobre las galaxias
    4) Jugar en una galaxia
    5) Salir de ChauCraft""")
    return fu.pedir_entero(1, 5)


def ranking_planetas(planetas):
    ranking = []
    # ((planeta, nombre galaxia), nombre planeta)
    for n_planeta in planetas.keys():
        ranking.append((planetas[n_planeta], n_planeta))
    '''As seen at https://python-course.eu/python3_lambda.php and
    https://docs.python.org/3/howto/sorting.html'''
    ranking.sort(key=lambda x: x[0][0].evolucion, reverse=True)
    mejores = deque(ranking[:5])
    n = 0
    print("Los mejores planetas son:")
    print()
    while len(mejores) > 0:
        n += 1
        tupla_planeta = mejores.popleft()
        planeta = tupla_planeta[0][0]
        print("{}) {}".format(n, tupla_planeta[1]), end=". ")
        print("de la galaxia: {}".format(tupla_planeta[0][1]))
        print("Nivel de evolución: {}".format(planeta.evolucion))
        print("Raza: {}".format(str(planeta.raza)))
        print()
    return


def menu_jugar():
    print("""¿Qué deseas hacer?
    1) Visitar un planeta
    2) Guardar cambios
    3) Volver atrás""")
    accion = fu.pedir_entero(1, 3)
    while accion == 3:
        print("No se conservarán cambios no guardados previamente")
        volver = input("Si desea seguir jugando digite 1, si desea continuar "
                       + "al menú principal pulse otra tecla: ")
        if volver == "1":
            print("""¿Qué deseas hacer?
            1) Visitar un planeta
            2) Guardar cambios
            3) Volver atrás""")
            accion = fu.pedir_entero(1, 3)
        else:
            return accion
    return accion


def planeta_conquistado():
    print("""¿Qué deseas hacer?
    1) Construir edificio
    2) Generar unidades
    3) Recolectar recursos
    4) Realizar Mejoras""")
    return fu.pedir_entero(1, 4)


def planeta_no_conquistado():
    print("""¿Qué deseas hacer?
    1) Invadir planeta
    2) Comprar el planeta""")
    return fu.pedir_entero(1, 2)


def realizar_mejoras(galaxia, planeta):
    accion = menu_mejoras()
    minerales = galaxia.reserva_mineral
    deuterio = galaxia.reserva_deuterio
    if accion == 1:
        if minerales < 1000:
            print("Mineral insuficiente ")
            return
        elif deuterio < 2000:
            print("Deuterio insuficente")
            return
        elif planeta.nivel_ataque == 3:
            print("Nivel ataque al máximo")
            return
        galaxia.reserva_deuterio -= 2000
        galaxia.reserva_mineral -= 1000
        planeta.nivel_ataque += 1
        print("Nivel de ataque mejorado")
        print("Nivel actual: {}".format(planeta.nivel_ataque))
    else:
        if minerales < 2000:
            print("Mineral insuficiente ")
            return
        elif deuterio < 4000:
            print("Deuterio insuficente")
            return
        elif planeta.nivel_economia == 3:
            print("Nivel economia al máximo")
            return
        galaxia.reserva_deuterio -= 4000
        galaxia.reserva_mineral -= 2000
        planeta.nivel_economia += 1
        print("Nivel de economia mejorado")
        print("Nivel actual: {}".format(planeta.nivel_economia))


def menu_mejoras():
    print("""¿Qué deseas mejorar?
    1) Nivel de ataque (1000 mineral/2000 deuterio)
    2) Nivel de economia (2000 mineral/4000 deuterio)""")
    return fu.pedir_entero(1, 2)


def comprar_planeta(galaxia, nombre_planeta):
    if galaxia.reserva_deuterio < 500000:
        print("Deuterio Insuficiente")
        return
    elif galaxia.reserva_mineral < 1000000:
        print("Mineral insuficiente")
        return
    print("Has conquistado pacíficamente este planeta")
    galaxia.reserva_mineral -= 1000000
    galaxia.reserva_deuterio -= 500000
    planeta = galaxia.planetas[nombre_planeta]
    planeta.conquistado = True
    galaxia.planetas_conquistados.add(nombre_planeta)


def boost(soldados, raza):
    Soldado = namedtuple("Soldier_type", ["ataque", "vida"])
    max_vida, max_ataque = maximos(str(raza))
    for n_soldado in range(len(soldados)):
        soldado = soldados[n_soldado]
        soldadovida = soldado.vida
        soldadoataque = soldado.ataque
        soldadoataque += 5
        if soldadoataque > max_ataque:
            soldadoataque = max_ataque
        soldadovida += 10
        if soldadovida > max_vida:
            soldadovida = max_vida
        soldados[n_soldado] = Soldado(soldadoataque, soldadovida)


def boost_magos(magos):
    Mago = namedtuple("Magician_type", ["ataque", "vida"])
    max_vida, max_ataque = 200, 120
    for n_mago in range(len(magos)):
        mago = magos[n_mago]
        magoataque = mago.ataque
        magovida = mago.vida
        magoataque += 5
        if magoataque > max_ataque:
            magoataque = max_ataque
        magovida += 10
        if magovida > max_vida:
            magovida = max_vida
        magos[n_mago] = Mago(magoataque, magovida)


def maximos(raza):
    if raza == "Maestro":
        return 250, 80
    elif raza == "Asesino":
        return 270, 45
    else:
        return 700, 60
