import datetime
import random


class Persona:
    rut = 1
    def __init__(self, nombre, nacimiento, **kwargs):
        self.nombre = nombre
        self.nacimiento = nacimiento # datetime
        hoy = datetime.date.today()
        self.edad = (hoy - self.nacimiento) // datetime.timedelta(days=365.2425)
        # fuente: https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
        self.rut = Persona.rut
        Persona.rut += 1
        super().__init__()

    def __repr__(self):
        return "{},({})".format(self.nombre, self.rut)


class Alumno(Persona):

    def __init__(self, ramos, **kwargs):
        self.__conocimiento = 10
        self.ramos = ramos
        super().__init__(**kwargs)

    @property
    def conocimiento(self):
        return self.__conocimiento

    @conocimiento.setter
    def conocimiento(self, value):
        if value > 100:
            self.__conocimiento = 100
        elif value < 1:
            self.__conocimiento = 1
        else:
            self.__conocimiento = value
        if not isinstance(self, Ayudante):
            if self.conocimiento < 60:
                print("Si sigo así, me voy a hechar el ramo D:")
            else:
                print("¡Qué chévere Python! Voy a postular a TPd para \
                      aprender más.")

    def estudiar(self):
        self.conocimiento += random.randint(5,10)

    def __str__(self):
        aux = "{}, Rut: {}, Edad: {}, Ramos: {},Nivel de conocimiento: {}".\
              format(self.nombre, self.rut, self.edad, self.ramos,
                     self.conocimiento)
        return aux


class Ayudante(Alumno):

    def __init__(self, seccion, **kwargs):
        self.seccion = seccion
        super().__init__(**kwargs)
        self.conocimiento += 65

    def ensennar(self, al):
        al.conocimiento += random.randint(5,15)
        pass

        def __str__(self):
            aux = "{}, Rut: {}, Edad: {}, Sección: {}, Ramos: {},\
                  Nivel de conocimiento: {}".format(self.nombre,
                  self.rut, self.edad, self.seccion,
                  self.ramos, self.conocimiento)
            return aux


class Profesor(Persona):

    def __init__(self, seccion, **kwargs):
        super().__init__(**kwargs)
        self.seccion = seccion

    def ensennar(self, student):
        student.conocimiento += random.randint(10,25)

    def __str__(self):
        aux = "{}, Rut: {}, Edad: {}, Sección: {}".format(self.nombre,
                                    self.rut, self.edad, self.seccion)
        return aux


if __name__ == "__main__":
    elprofe = Profesor(seccion = "1", nombre = "Pedro", nacimiento = datetime.date(1980,5,8))
    elayudante = Ayudante(seccion = "1", nombre = "José", nacimiento = datetime.date(1994,6,12), ramos = ["IIC9999", "IMAT9998"])
    otroayudante = Ayudante(seccion = "1", nombre = "Pablo", nacimiento = datetime.date(1995,8,12), ramos = ["IIC9998", "MAT9999"])
    alumno1 = Alumno(nombre = "Pablo", nacimiento = datetime.date(1998,9,3), ramos = ["IIC2233", "MAT1640"])
    alumno2 = Alumno(nombre = "Pablo", nacimiento = datetime.date(2000,10,4), ramos = ["IIC2233", "MAT1000"])
    sección1 = [elprofe,elayudante,otroayudante,alumno1,alumno2]
    print(sección1)
    for persona in sección1:
        print(persona)