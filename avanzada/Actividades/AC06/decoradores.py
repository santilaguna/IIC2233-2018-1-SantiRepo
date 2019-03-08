"""
-- decoradores.py --

Escriba, en este archivo, todos sus decoradores.
"""

FILENAME = 'registro.txt'


from functools import wraps
from time import time


def registar(f):
    @wraps(f)
    def registrar_dec(*args, **kwargs):
        retorno = f(*args, **kwargs)
        with open(FILENAME, "a", encoding="utf-8") as file:
            file.write("Funcion: " + f.__name__ + "Args: " + str(args) +
                       "Kwargs: " + str(kwargs) + "Retorno: " + str(retorno) +
                       "\n")
        return retorno
    return registrar_dec

def verificar_tipos(*argumentos):
    def verificar_tipos_(f):
        def verificar_dec(*args, **kwargs):
            if len(args) != (len(argumentos)+1):
                raise TypeError("La cantidad de argumentos de la función "
                                "no coincide con la cantidad de argumentos"
                                " entregados")
            for i in range(len(argumentos)):
                if not isinstance(args[i+1], argumentos[i]):
                    raise TypeError("El argumento {} no es del tipo {}"
                                    .format(args[i], argumentos[i]))
            return f(*args, **kwargs)
        return verificar_dec
    return verificar_tipos_

def invertir_string(f):
    def invertir_dec(*args, **kwargs):
        retorno = f(*args, **kwargs)
        newarg = retorno[0][::-1]
        return [newarg] + retorno[1:]

    return invertir_dec


def temporizador(limite=3):
    """As seen at: https://github.com/IIC2233/contenidos/blob/master/
    semana-06/03-Ejemplos-decoradores.ipynb"""
    def revisar_tiempo(f):
        @wraps(f)
        def temporizador_dec(*args, **kwargs):
            inicio = time()
            retorno = f(*args, **kwargs)
            final = time()
            dif = final-inicio
            print("La función tardó {} segundos".format(dif))
            if final-inicio > limite:
                print("Funcíon excede tiempo esperado", "Función:",
                      f.__name__, "Tiempo límite: ", limite, "Tiempo de "
                    "ejecución: {} segundos".format(dif))
            return retorno
        return temporizador_dec
    return revisar_tiempo