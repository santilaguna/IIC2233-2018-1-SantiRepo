# móduo destinado a crear la función que suma los tiempos


def sumar_tiempo(tiempo_inical, tiempo_agregado):
    """tiempo_inical: (int, int)
    tiempo_agregado: (int, int)
    retorna suma de tiempos: (int, int)"""
    tiempo = (tiempo_inical[0] + tiempo_agregado[0],
              tiempo_inical[1] + tiempo_agregado[1])
    while tiempo[1] >= 60:
        tiempo = (tiempo[0] + 1, tiempo[1] - 60)
    if tiempo[0] > 23:
        tiempo = (tiempo[0] - 24, tiempo[1])
    return tiempo


def comparar_tiempo(tiempo_uno, tiempo_dos):
    """tiempo_inical: (int, int) , tiempo_agregado: (int, int)
    retorna int:  1 si tiempo_uno > tiempo_dos, 2 si tiempo_dos > tiempo_uno
    o 0 si tiempo_uno == tiempo_dos
    """
    if tiempo_uno[0] > tiempo_dos[0]:
        return 1
    elif tiempo_dos[0] > tiempo_uno[0]:
        return 2
    elif tiempo_uno[1] > tiempo_dos[1]:
        return 1
    elif tiempo_dos[1] > tiempo_uno[1]:
        return 2
    return 0


def diferencia(tiempo_final, tiempo_inicial):
    """tiempo_final: (int, int) , tiempo_inicial: (int, int)
    retorna la diferencia en minutos entre ambos tiempos"""
    minutos = tiempo_final[1] - tiempo_inicial[1]
    minutos += ((tiempo_final[0] - tiempo_inicial[0]) * 60)

    if minutos < -1:  # le dimos un segundo al operador para colación
        raise ValueError("cambio de dia")
    return minutos
