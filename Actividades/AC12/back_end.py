import os
import json
import pickle
from random import sample


ESTILO = (("label_principal", "background-image: url(gui/logo.png);"),
          ("boton_serializar", "background-image: url(gui/guantlet.png);"),
          ("boton_deserializar", "background-image: url(gui/dragon_balls.png);"),
          ("label_personas","background-color: rgba(30, 232, 204, 153);"),
          ("centralwidget", "#centralwidget{background-color: "
                            "qlineargradient(spread:repeat, x1:0,"
                            " y1:0,x2:1,y2:0,stop:0.197044 "
                            "rgba(179, 179, 179, 255), "
                            "stop:0.64532 rgba(204, 204, 204, 255), "
                            "stop:1 rgba(255, 255, 255, 255));}"),
          ("label_barra", "background-color: rgb(76, 76, 76);"),
          ("scrollArea", "#area{border: 3px solid black;} "
                         "QLabel{border: 1px solid grey; font-weight: bold}"))

class Persona():

    def __init__(self, nombre, apellido_paterno, apellido_materno, numero_alumno,
                 codigo_genetico, hermosura, inteligencia, velocidad):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.numero_alumno = numero_alumno
        self.codigo_genetico = codigo_genetico
        self.hermosura = hermosura
        self.inteligencia = inteligencia
        self.velocidad = velocidad
        self.serializado = False


    def __getstate__(self):
        ## rellenar método##
        #:return: dict
        copia = self.__dict__.copy()

        copia["ultimas_palabras"] = "Me están matando"
        return copia


    def __setstate__(self, state):
        ## rellenar método##
        #:state: dict
        state_ = state.copy()
        if "ultimas_palabras" in state_:
            del state_["ultimas_palabras"]
        self.__dict__ = state


#################################
#Espacio para JSONEncoder
class PersonaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Persona):
            return {"Nombre": obj.nombre,
                    "Apellido": obj.apellido_paterno,
                    "Numero de Alumno": obj.numero_alumno}
        return super().default(obj)




#FUNCIONES
##############################################################################
def filtrar_atributos(dict):
    new_dict = {}
    with open("caracteristicas.json", "r", encoding="utf-8") as file_:
        atributos = json.load(file_)
        for atributo in atributos:
            if atributo in dict:
                new_dict[atributo] = dict[atributo]
            else:
                new_dict[atributo] = None
    return new_dict

# Aca hay espacio para una funcion auxiliar, por ejemplo para algun object_hook



def agregar_estilo():
    """
    Retorna el estilo de la interfaz en formato json
    :return: str (formato json)
    """
    diccionario = dict(ESTILO)
    nuevo = json.dumps(diccionario)
    return nuevo

def cargar_personas():
    """
    Lee el archivo personas.json, deserializa cada persona en formato json y
    retorna una lista de Personas
    :return: list
    """
    with open("personas.json", "r", encoding="utf-8") as file:
        listirijilla = json.load(file, object_hook=filtrar_atributos)
    return listirijilla

def generar_personas(personas):
    """
    Crea la carpeta Personas que contiene a las personas serializadas con json
    :personas: lista de Personas
    """
    if personas is None:
        return
    template = "Personas/<{}>.json"
    if not os.path.exists("Personas"):
        os.mkdir("Personas")
    for dict_person in personas:
        person = Persona(**dict_person)
        path = template.format(person.codigo_genetico)
        with open(path, "w") as file:
            json.dump(person, file, cls=PersonaEncoder)

def serializar_personas(personas):
    """
    Crea la carpeta Serializados que contiene a las personas serializadas con pickle
    :personas: lista de Personas
    """
    largo = len(personas)
    mitad = int(largo/2)
    muestra = sample(personas, mitad)
    if not os.path.exists("Serializados"):
        os.mkdir("Serializados")
    for person_dict in muestra:
        persona = Persona(**person_dict)
        path = os.path.join("Serializados", persona.numero_alumno + ".rip")
        with open(path, "wb") as file:
            pickle.dump(persona, file)

##############################################################################
