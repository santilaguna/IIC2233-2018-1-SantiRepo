# Módulo destinado a implementar el backend

textos = {}
def procesar_texto(texto):
    if texto in textos.values():
        return texto, False
    elif not texto or texto == "":
        return texto, False
    elif len(texto) > 140:
        return texto, False
    if len(textos) >= 9:
        return texto, False
    else:
        return texto, True

def agregar_texto(texto, n):
    textos[n] = texto

def borrar_label(n):
    del textos[n]
