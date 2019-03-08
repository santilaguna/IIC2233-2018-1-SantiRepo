# Módulo destinado a correr el programa

from chaucraft import ChauCraft
from galaxia import Galaxia
from planeta import Planeta
from clases import Aprendiz, Asesino, Maestro, Edificio
from datetime import datetime


game = ChauCraft()
try:
    with open("galaxias.csv", "r", encoding="utf-8") as galaxias_file:
        primera = galaxias_file.readline()
        orden = (dato.strip("\n").split(": ") for dato in primera.split(","))
        orden = tuple(dato.strip() for [dato, tipo] in orden)
        nueva_galaxia = {}
        for line in galaxias_file:
            datos_galaxia = (dato.strip() for dato in
                             line.strip("\n").split(","))
            for dato in orden:
                nueva_galaxia[dato] = datos_galaxia.__next__()
            galaxia = Galaxia(nueva_galaxia["nombre"])
            galaxia.reserva_mineral = int(nueva_galaxia["minerales"])
            galaxia.reserva_deuterio = int(nueva_galaxia["deuterio"])
            game.galaxias[nueva_galaxia["nombre"]] = galaxia

    with open("planetas.csv", "r", encoding="utf-8") as planetas_file:
        primera = planetas_file.readline()
        orden = (dato.split(": ") for dato in primera.strip("\n").split(","))
        orden = tuple(dato.strip() for [dato, tipo_dato] in orden)
        nuevo_planeta = {}
        for line in planetas_file:
            datos_planeta = (dato.strip() for dato in
                             line.strip("\n").split(","))
            for dato in orden:
                nuevo_planeta[dato] = datos_planeta.__next__()
            if nuevo_planeta["raza"] == "Aprendiz":
                raza = Aprendiz()
            elif nuevo_planeta["raza"] == "Maestro":
                raza = Maestro()
            elif nuevo_planeta["raza"] == "Asesino":
                raza = Asesino()
            else:
                raise ValueError
            galaxia = game.galaxias[nuevo_planeta["galaxia"]]
            galaxia.planetas[nuevo_planeta["nombre"]] = Planeta(raza)
            planeta = galaxia.planetas[nuevo_planeta["nombre"]]
            planeta.magos = int(nuevo_planeta["magos"])
            planeta.soldados = int(nuevo_planeta["soldados"])
            planeta.tasa_minerales = int(nuevo_planeta["tasa_minerales"])
            planeta.tasa_deuterio = int(nuevo_planeta["tasa_deuterio"])
            planeta.nivel_ataque = int(nuevo_planeta["nivel_ataque"])
            planeta.nivel_economia = int(nuevo_planeta["nivel_economia"])
            if nuevo_planeta["conquistado"] == "True":
                planeta.conquistado = True
                galaxia.planetas_conquistados.add(nuevo_planeta["nombre"])
            if nuevo_planeta["torre"] == "True":
                planeta.torre = Edificio(150, 300, 1000, 2000)
            if nuevo_planeta["cuartel"] == "True":
                planeta.cuartel = Edificio(200, 500, 0, 5000)
            recoleccion = nuevo_planeta["ultima_recoleccion"]
            '''As seen at https://stackoverflow.com/questions/466345
            /converting-string-into-datetime'''
            modo_datetime = datetime.strptime(recoleccion, '%Y-%m-%d %H:%M:%S')
            planeta.ultima_recoleccion = modo_datetime
            nombre_planeta = nuevo_planeta["nombre"]
            nombre_galaxia = nuevo_planeta["galaxia"]
            Galaxia.planetas[nombre_planeta] = (planeta, nombre_galaxia)
except FileNotFoundError:
    print("No hay archivos para cargar o estos no tienen el header")
    print("Se comenzará el juego desde cero")
game.run()
