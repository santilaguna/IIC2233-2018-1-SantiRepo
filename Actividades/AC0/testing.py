from main import (Humano, Extraterrestre, Supersaiyayin, Villano)
import abc

if isinstance(Humano,abc.ABCMeta):
    print("Humano es ABC")
else:
    print("Humano no es ABC")
try:
    print(Humano.vida)
    if isinstance(Humano.vida, property):
        print("Ok property vida Humano")
except Exception as err:
    print("Problema checkeando property vida Humano")


if isinstance(Extraterrestre,abc.ABCMeta):
    print("Extraterrestre es ABC")
else:
    print("Extraterrestre no es ABC")

try:
    if isinstance(Extraterrestre.vida, property):
        print("Ok property vida Extraterrestre")
except Exception as err:
    print("Problema checkeando property vida Extraterrestre")


if Supersaiyayin.__bases__ == (Humano,Extraterrestre):
    print("Multieherencia ok con Supersaiyayin")
else:
    print("Supersaiyayin no cumple con la multiherencia")

instancias = True
try :
    from main import supersaiyayin1
    print("supersaiyayin1 creado exitosamente")
except Exception as err:
    print("No se instancio bien supersaiyayin1")
    instancias = False

try :
    from main import villano1
    print("villano1 creado exitosamente")
except Exception as err:
    print("No se instancio bien villano1")
    instancias = False

try :
    from main import villano2
    print("villano2 creado exitosamente")
except Exception as err:
    print("No se instancio bien villano2")
    instancias = False

try :
    from main import supersaiyayin2
    print("supersaiyayin2 creado exitosamente")
except Exception as err:
    print("No se instancio bien supersaiyayin2")
    instancias = False

try :
    from main import bola1
    print("bola1 creado exitosamente")
except Exception as err:
    print("No se instancio bien bola1")
    instancias = False

try :
    from main import bola2
    print("bola2 creado exitosamente")
except Exception as err:
    print("No se instancio bien bola2")
    instancias = False

try :
    from main import bola3
    print("bola3 creado exitosamente")
except Exception as err:
    print("No se instancio bien bola3")
    instancias = False

instances = (supersaiyayin2, villano2, villano1, supersaiyayin1)

if instancias:
    print("----------------------------------------------")
    try:
        supersaiyayin2()
    except Exception as err:
        print("Un Supersaiyayin tuvo un problema con su practica (__call__)")

    try:
        supersaiyayin1()
    except Exception as err:
        print("Un Supersaiyayin tuvo un problema con su practica (__call__)")

    print("----------------------------------------------")
    try:
        villano1.agregar_bola(bola2)
        villano1.agregar_bola(bola3)
        villano1.agregar_bola(bola1)

    except Exception as err:
        print("El villano tuvo un problema con agregar_bola")
    try:
        villano1.usar_bolas()


    except Exception as err:
        print("El villano tuvo un problema con usar_bolas")

    print("----------------------------------------------")

    print("Ha comenzado la batalla!")
    try:
        villano1.atacar(supersaiyayin1)
    except Exception as err:
        print("El villano a tenido un problema con su ataque")

    try:
        supersaiyayin1.atacar(villano1)
    except Exception as err:
        print("El Supersaiyayin ha tenido un problema con su ataque")

    try:
        supersaiyayin1.obtener_ki_externo(supersaiyayin2, villano2)
    except Exception as err:
        print("El Supersaiyayin ha tenido problemas recolectando Ki")

    try:
        villano2.atacar(supersaiyayin2)
    except Exception as err:
        print("El villano ha tenido un problema con su ataque")

    try:
        supersaiyayin2.perder_cola()
    except Exception as e:
        print("El Supersaiyayin ha tenido problemas con perder cola")





else:
    print("La batalla termina por bocover (faltaron instancias)")