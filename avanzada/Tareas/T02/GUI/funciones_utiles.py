# Este módulo contiene funciones útiles genericas que pueden ser utilizadas en \
# futuros programas.
# Contiene funciones para facilitar el diálogo con el usuario y otras
# funcionalidades del sistema

# Importar como fu


from random import randint
from math import inf


# Probabilidad de que ocurra una acción, enteros del 1 al 100
def probabilidad(numero):
    n = randint(1, 100)
    if n <= numero:
        return True
    return False


# Pedir un número entero en un rango sin caida del programa
def pedir_entero(limite_inferior=(-inf), limite_superior=inf):
    number = input()
    while not number.isdigit() or not int(number) >= limite_inferior or not\
            int(number) <= limite_superior:
        number = input("Error al ingresar datos, debe ingresar un número "
                       + "válido: ")
    number = int(number)
    print()
    return number


# Pedir un número decimal en un rango sin caida del programa
def pedir_decimal(limite_inferior=(-inf), limite_superior=inf):
    number = input()
    while not number.isdecimal() or not float(number) >= limite_inferior \
            or not float(number) <= limite_superior:
        number = input("Error al ingresar datos, debe ingresar un número"
                       + " válido: ")
    number = float(number)
    print()
    return number


# Pedir un string de largo específico
def pedir_string(limite_inferior=(-inf), limite_superior=inf):
    palabra = input()
    while not len(palabra) >= limite_inferior or not \
            len(palabra) <= limite_superior:
        palabra = input("Ha ingresado un largo equivocado, por favor ingrese"
                        + " datos nuevamente: ")
    print()
    return palabra


# Revisar cuantos elementos de cierto tipo hay en una clase, retorna un entero
def contar_tipo(lista, ejemplo_de_tipo):
    tipo = type(ejemplo_de_tipo)
    if not lista:
        return 0
    cuenta = 0
    for elemento in lista:
        if isinstance(elemento, tipo):
            cuenta += 1
    return cuenta


def tomar_decision(lista_datos):
    # Preguntar que se desea hacer antes
    n = 1
    for dato in lista_datos:
        print("{}) {}".format(n, dato))
        n += 1
    numero_dato_escogido = pedir_entero(1, len(lista_datos))
    dato_escogido = lista_datos[numero_dato_escogido - 1]
    # retornamos el dato
    return dato_escogido
