instancias = True
try :
    from main import chaobug
    print("chaobug creado exitosamente")
except Exception as err:
    print("No se instancio bien chaobug")
    instancias = False

try :
    from main import billis
    print("billis creado exitosamente")
except Exception as err:
    print("No se instancio bien billis")
    instancias = False

try :
    from main import popa
    print("popa creado exitosamente")
except Exception as err:
    print("No se instancio bien popa")
    instancias = False

try :
    from main import johnny
    print("johnny creado exitosamente")
except Exception as err:
    print("No se instancio bien johnny")
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

instances = (johnny, popa, billis, chaobug)

if instancias:
    print("----------------------------------------------")
    try:
        johnny()
    except Exception as err:
        print("Un Supersaiyayin tuvo un problema con su practica (__call__)")

    try:
        chaobug()
    except Exception as err:
        print("Un Supersaiyayin tuvo un problema con su practica (__call__)")

    print("----------------------------------------------")
    try:
        billis.agregar_bola(bola2)
        billis.agregar_bola(bola3)
        billis.agregar_bola(bola1)

    except Exception as err:
        print("El villano tuvo un problema con agregar_bola")
    try:
        billis.usar_bolas()

    except Exception as err:
        print("El villano tuvo un problema con usar_bolas")

    print("----------------------------------------------")

    print("Ha comenzado la batalla!")
    try:
        billis.atacar(chaobug)
    except Exception as err:
        print("El villano a tenido un problema con su ataque")

    try:
        chaobug.atacar(billis)
    except Exception as err:
        print("El Supersaiyayin ha tenido un problema con su ataque")

    try:
        chaobug.obtener_ki_externo(johnny, popa)
    except Exception as err:
        print("El Supersaiyayin ha tenido problemas recolectando Ki")

    try:
        popa.atacar(johnny)
    except Exception as err:
        print("El villano ha tenido un problema con su ataque")

    try:
        johnny.perder_cola()
    except Exception as e:
        print("El Supersaiyayin ha tenido problemas con perder cola")





else:
    print("La batalla termina por bocover (faltaron instancias)")