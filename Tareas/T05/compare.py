# módulo destinado a funciones de comparación por pixeles (backend).

from random import choice
from parameters import DISTANCIA_MINIMA, MAPA_SIZE, N


def in_range(coordenada, inferior, superior):
    if coordenada > inferior:
        if coordenada < superior:
            return True
    return False


def colision(object_a, object_b):
    ax = object_a.x
    ay = object_a.y
    asx = object_a.sizex
    asy = object_a.sizey
    bx = object_b.x
    by = object_b.y
    bsx = object_b.sizex
    bsy = object_b.sizey
    # choque por la izquierda
    if (bx + bsx) > ax > bx:
        # por arriba
        if (by + bsy) > ay > by:
            return True
        # por abajo
        elif by < (ay + asy) < (by + bsy):
            return True
    # choque por la derecha
    elif bx < (ax + asx) < (bx + bsx):
        # por arriba
        if (by + bsy) > ay > by:
            return True
        # por abajo
        elif by < (ay + asy) < (by + bsy):
            return True
    return False


def colisiones(player, objects):
    for object_ in objects:
        if colision(player, object_):
            return True
    return False


def specific_colision(player, objects):
    for object_ in objects:
        if colision(player, object_):
            return object_
    return False


def kick_bomb(player, bombs):
    for bomb in bombs:
        if colision(player, bomb):
            return bomb
    return False


def move_way(player, bomb):
    return player.moving, bomb.id_


def bomb_space(bomb, spaces):
    for space in spaces:
        if colision(bomb, space):
            if not space.ocupado:
                space.ocupado = True
                return space
    return False


def centrar(x, y):
    cuadro_size = N/MAPA_SIZE
    cant_x = x//cuadro_size
    real_x = cant_x * cuadro_size
    real_x += cuadro_size/2
    cant_y = y//cuadro_size
    real_y = cant_y * cuadro_size
    real_y += cuadro_size/2
    return real_x, real_y


def casillas_afectadas(event, spaces, walls):
    casillas = []
    left_casillas = []
    right_casillas = []
    up_casillas = []
    down_casillas = []
    opciones = spaces + walls
    event_x, event_y = centrar(event.x, event.y)
    for cuadro in opciones:
        x, y = cuadro.pos
        if event_y == y and event_x > x >= event_x - event.rango:
            left_casillas.append(cuadro)
        elif event_y == y and event_x < x <= event_x + event.rango:
            right_casillas.append(cuadro)
        elif event_x == x and event_y < y <= event_y + event.rango:
            down_casillas.append(cuadro)
        elif event_x == x and event_y > y >= event_y - event.rango:
            up_casillas.append(cuadro)
        elif event_x == x and event_y == y:
            casillas.append(cuadro)
    left_casillas.sort(key=lambda cuadro: cuadro.x)
    while left_casillas:
        cuadro = left_casillas.pop()
        if cuadro.stop_explosion:
            if cuadro.destructible:
                casillas.append(cuadro)
            break
        casillas.append(cuadro)
    right_casillas.sort(key=lambda cuadro: cuadro.x)
    while right_casillas:
        cuadro = right_casillas.pop(0)
        if cuadro.stop_explosion:
            if cuadro.destructible:
                casillas.append(cuadro)
                break
            break
        casillas.append(cuadro)
    up_casillas.sort(key=lambda cuadro: cuadro.y)
    while up_casillas:
        cuadro = up_casillas.pop()
        if cuadro.stop_explosion:
            if cuadro.destructible:
                casillas.append(cuadro)
                break
            break
        casillas.append(cuadro)
    down_casillas.sort(key=lambda cuadro: cuadro.y)
    while down_casillas:
        cuadro = down_casillas.pop(0)
        if cuadro.stop_explosion:
            if cuadro.destructible:
                casillas.append(cuadro)
                break
            break
        casillas.append(cuadro)
    return casillas


def find_label(labels, size, x, y):
    pos_vertical = int(y // size)
    pos_horizontal = int(x // size)
    return labels[pos_vertical][pos_horizontal]


def revisar_hostilidad(e, player_one, player_two):
    playerx = player_one.x + player_one.sizex/2
    playery = player_one.y + player_one.sizey/2
    if (e.y - playery) ** 2 + (e.x - playerx) ** 2 <= e.rango ** 2:
        return 1
    if player_two is not None:
        playerx = player_two.x + player_two.sizex/2
        playery = player_two.y + player_two.sizey/2
        if (e.y - playery) ** 2 + (e.x - playerx) ** 2 <= e.rango ** 2:
            return 2
    return False


def hostil_way(x, y, player, last_side):
    playerx = player.x + player.sizex/2
    playery = player.y + player.sizey/2
    difx = playerx - x
    dify = playery - y
    if last_side is not None:
        if last_side in {"up", "down"}:
            if difx < 0:
                return "left"
            else:
                return "right"
        else:
            if dify < 0:
                return "up"
            else:
                return "down"
    elif abs(difx) < abs(dify):
        if difx < 0:
            return "left"
        else:
            return "right"
    else:
        if dify < 0:
            return "up"
        else:
            return "down"


def distancia_minima(espacio, player):
    x, y = espacio.pos
    player_x = player.x + player.sizex/2
    player_y = player.y + player.sizey/2
    if ((player_x - x) ** 2) + ((player_y - y) ** 2) > DISTANCIA_MINIMA ** 2:
        return True
    return False


def pedir_celdas(espacios, enemigos, player_one, player_two):
    posibles = filter(lambda x: x.ocupado is False, espacios)
    posibles = filter(lambda x: not colisiones(x, enemigos), posibles)
    posibles = filter(lambda x: distancia_minima(x, player_one), posibles)
    if player_two is not None:
        posibles = filter(lambda x: distancia_minima(x, player_two), posibles)
    posibles = list(posibles)
    if not posibles:
        return False, False
    chosen_one = choice(posibles)
    return chosen_one.pos
