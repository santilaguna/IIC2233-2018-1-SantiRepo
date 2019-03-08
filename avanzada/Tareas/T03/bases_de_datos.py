# Este módulo esta destinado para las funciones encargadas de leer y editar
# las bases de datos

# Importar como bdd

from collections import namedtuple
import csv
from itertools import groupby

Movie = namedtuple("Movie_type", ["id", "title", "rating_imdb",
                                  "rating_metacritic", "rating_rt",
                                  "box_office", "date"])


def juntar(mini_generador):
    return {value for k, value in mini_generador}


def unir(mini_generador):
    return [value for k, value in mini_generador]


def become_movie(line):
    return Movie(line["id"], line["title"], line["rating_imdb"],
                 line["rating_metacritic"], line["rating_rt"],
                 line["box_office"], line["date"])


def cargar_movies(path="TestingDatabase/movies.csv"):
    with open(path, "r", encoding="utf-8", newline="") as file:
        movies = csv.DictReader(file, skipinitialspace=True)
        return tuple(become_movie(movie_dict) for movie_dict in movies)


def cargar_generos(path="TestingDatabase/genres.csv", movies=0):
    """As seen at: https://stackoverflow.com/questions/13883549/
    group-by-aggregate-functions-with-dictionary-comprehensions"""
    with open(path, "r", encoding="utf-8", newline="") as file:
        dict_lines = csv.DictReader(file, skipinitialspace=True)
        lines = [(line["genre"], line["id"]) for line in dict_lines]
        if movies != 0:
            lines = list(filter(lambda x: x[1] in movies, lines))
        lines.sort(key=lambda x: x[0])
        genres = {k: juntar(v) for k, v in groupby(lines, key=lambda x: x[0])}
    return genres


def cargar_actores(path="TestingDatabase/actors.csv", movies=0):
    with open(path, "r", encoding="utf-8", newline="") as file:
        dict_lines = csv.DictReader(file, skipinitialspace=True)
        lines = [(line["actor"], line["id"]) for line in dict_lines]
        if movies != 0:
            lines = list(filter(lambda x: x[1] in movies, lines))
        lines.sort(key=lambda x: x[0])
        actors = {k: juntar(v) for k, v in groupby(lines, key=lambda x: x[0])}
    return actors


def cargar_actores_inv(path="TestingDatabase/actors.csv", movies=0):
    with open(path, "r", encoding="utf-8", newline="") as file:
        dict_lines = csv.DictReader(file, skipinitialspace=True)
        lines = [(line["id"], line["actor"]) for line in dict_lines]
        if movies != 0:
            lines = list(filter(lambda x: x[0] in movies, lines))
        lines.sort(key=lambda x: x[0])
        actors = {k: juntar(v) for k, v in groupby(lines, key=lambda x: x[0])}
    return actors


def cargar_comentarios(path="clean_reviews.csv"):
    """As seen at: https://stackoverflow.com/questions/3420122/
    filter-dict-to-contain-only-certain-keys"""
    with open(path, "r", encoding="utf-8", newline="") as file:
        dict_lines = csv.DictReader(file, skipinitialspace=True)
        lines = [(line["id"], line["review"]) for line in dict_lines]
        lines.sort(key=lambda x: x[0])
        reviews = {k: unir(v) for k, v in groupby(lines, key=lambda x: x[0])}
    return reviews


def words():
    with open("words.csv", "r", encoding="utf-8", newline="") as file:
        dict_lines = csv.DictReader(file, skipinitialspace=True)
        return list(dict_lines)


def pertenece(palabra, _words):
    repeticiones = list(filter(lambda x: x in palabra, _words))
    if repeticiones:
        return True
    else:
        return False


def clasificar_review(review, good_words, bad_words):
    words_review = review.split(" ")
    goods = list(filter(lambda x: pertenece(x, good_words), words_review))
    bads = list(filter(lambda x: pertenece(x, bad_words), words_review))
    return clasificar_comentario(len(goods), len(bads), len(words_review))


def clasificar_comentario(goods, bads, review):
    if goods / review >= 0.6 or (
            goods / review >= 0.4 and bads / review <= 0.2):
        return 1  # positive
    elif goods / review >= 0.6 or (
            goods / review >= 0.4 and bads / review <= 0.2):
        return -1  # negative
    else:
        return 0  # neutral


def opiniones_movie(reviews, goods, bads):
    opinions = (clasificar_review(review, goods, bads) for review in reviews)
    rating_people = sum(opinions)
    return rating_people


def clasificar_movies(movies):
    palabras = words()
    palabras = [(x["word"], x["type"]) for x in palabras]
    goods = filter(lambda x: x[1] == "positive", palabras)
    goods = [x[0] for x in goods]
    bads = filter(lambda x: x[1] == "negative", palabras)
    bads = [x[0] for x in bads]
    all_reviews = cargar_comentarios()
    movies = list(movies)
    movies.sort(key=lambda x: opiniones_movie(all_reviews[x.id], goods, bads))
    return movies
