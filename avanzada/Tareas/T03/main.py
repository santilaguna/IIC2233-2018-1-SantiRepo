from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
import preprocesamiento
import libreria as lib
from excepciones import BadQuery, WrongInput, MovieError


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()

    def process_query(self, queries):
        # Agrega en pantalla la solucion.
        results = [self.obtener_resultado(x) for x in queries]
        for n in range(len(results)):
            self.add_answer("Consulta {} \n".format(n + 1))
            for element in results[n]:
                if isinstance(results[n], list):
                    self.add_answer(element + "\n")
                else:
                    self.add_answer(self.str_movie(element))
            self.add_answer("\n")

    @staticmethod
    def str_movie(movie):
        text = 'id: {}, title: {}, rating_imdb: {}, rating_metacritic: {}, ' \
               'rating_rt: {}, box_office: {}, date: {} \n'\
            .format(movie.id, movie.title, movie.rating_imdb,
                    movie.rating_metacritic, movie.rating_rt,
                    movie.box_office, movie.date)
        return text

    @staticmethod
    def obtener_resultado(query):
        try:
            result = lib.procesar_queries(query)
        except (BadQuery, WrongInput, MovieError) as err:
            result = err
        return result

    def save_file(self, queries):
        queries_answers = [self.obtener_resultado(x) for x in queries]
        with open("resultados.txt", "w", encoding="utf-8") as file:
            for n in range(len(queries_answers)):
                file.write("Consulta {} \n".format(n + 1))
                for element in queries_answers[n]:
                    if isinstance(queries_answers[n], list):
                        file.write(element + "\n")
                    else:
                        file.write(self.str_movie(element))


if __name__ == '__main__':
    preprocesamiento.reviews_writer()

    def hook(_type, value, traceback):
        print(_type)
        print(value)
        print(traceback)

    sys.__excepthook__ = hook

    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
