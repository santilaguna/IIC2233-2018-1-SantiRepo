# módulo destinado a ecribir las excepciones


class BadQuery(Exception):

    def __init__(self, consulta):
        super().__init__("BadQuery: {}".format(consulta))


class WrongInput(Exception):

    def __init__(self, consulta, parametro, valor):
        super().__init__("WrongInput: {}, {}, {}".format(consulta, parametro,
                                                         valor))


class MovieError(Exception):

    def __init__(self, consulta, pelicula, tipo_de_dato):
        super().__init__("MovieError: {}, {}, {}".format(consulta, pelicula,
                                                         tipo_de_dato))
