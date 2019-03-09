# módulo destinado a la ejecución del programa


import os
import string


cwd = os.getcwd()


def encontrar_64():
    for root, dirs, files in os.walk(cwd):
        if "marciano64.png" in files:
            return root


def encontrar_zurdo():
    for root, dirs, files in os.walk(cwd):
        if "marcianozurdo.pep" in files:
            return root


PATH_64 = encontrar_64()
PATH_ZURDO = encontrar_zurdo()

mis_letras = string.ascii_uppercase + string.ascii_lowercase\
             + string.digits +  "+/"
dict_letras = {mis_letras[i]: i for i in range(len(mis_letras))}

def algoritmo_base_64():
    with open(PATH_64 + os.sep + "marciano64.png", "rb") as file:
        marciano_chr = [chr(byte) for byte in file.read()]
        base = [dict_letras[x] for x in marciano_chr]
        binarios = [str(bin(x)[2:].zfill(6)) for x in base]
        unidos = "".join(binarios)
        i = 0
        cadena = []
        while i < len(unidos):
            cadena.append(unidos[i: i + 8])
            i += 8
        return [int(binario, 2) for binario in cadena]


def rotar(chunk):
    nuevo = chunk[1:]
    nuevo.append(chunk[0])
    return nuevo


def generador_size():
    """As seen at:
    https://stackoverflow.com/questions/3953749/python-fibonacci-generator"""
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def juntar():
    base_64 = algoritmo_base_64()
    with open(PATH_ZURDO + os.sep + "marcianozurdo.pep", "rb") as file:
        zurdo = file.read()

    array = bytearray()
    fib = generador_size()
    inico = 0
    fin = len(base_64) + len(zurdo)
    while inico < fin:
        size = next(fib)
        chunk = rotar(bytearray(zurdo[:size]))
        zurdo = zurdo[size:]
        array.extend(chunk)
        inico += size

        size = next(fib)
        chunk = base_64[:size]
        base_64 = base_64[size:]
        array.extend(chunk)
        inico += size
    return array


def escribir(text):
    with open("resultado.png", "wb") as file:
        file.write(text)

escribir(juntar())
