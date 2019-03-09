# módulo destinado a implementar las funciones de procesamiento

# importar como lib
import bases_de_datos as bdd
from excepciones import BadQuery, WrongInput, MovieError
from types import GeneratorType

rating_types = {"All", "IMDb", "RT", "MC", "Internet Movie Database",
                "Rotten Tomatoes", "Metacritic"}
symbols = {">", "<", "==", "!="}
columns = {"RT": "rating_rt", "Rotten Tomatoes": "rating_rt",
           "IMDb": "rating_imdb", "Internet Movie Database": "rating_imdb",
           "Metacritic": "rating_metacritic", "MC": "rating_metacritic",
           "date": "date", "box_office": "box_office"}


def revisar_generador(query, nombre_dato, dato):
    """Esta función sólo aplica para este programa, porque son los tipos
    de datos utilizados. La razón de su existencia, es que no existe un
    GeneratorType que considere filter, ziped, map, reduce, etc. objects"""
    if isinstance(dato, list) or isinstance(dato, tuple) or \
            isinstance(dato, str) or isinstance(dato, int) or \
            isinstance(dato, dict):
        raise WrongInput(query, nombre_dato, dato)


def revisar_input(query, nombre_dato, dato, tipo, opciones=None,
                  condition=None):
    if tipo is GeneratorType:
        return revisar_generador(query, nombre_dato, dato)
    if not isinstance(dato, tipo):
        raise WrongInput(query, nombre_dato, dato)
    if opciones:
        if dato not in opciones:
            raise WrongInput(query, nombre_dato, dato)
    if condition == "+":
        if dato < 0:
            raise WrongInput(query, nombre_dato, dato)
    elif condition == "-":
        if dato > 0:
            raise WrongInput(query, nombre_dato, dato)


def revisar_data(query, movie, nombre_dato, dato):
    if "N/A" in dato:
        raise MovieError(query, movie.title, nombre_dato)
    return movie


def calcular_rating(query, movie, r_type):
    if r_type == "All":
        return (calcular_rating(query, movie, "IMDb") + calcular_rating(
            query, movie, "RT") + calcular_rating(query, movie, "MC")) / 3
    if r_type == "IMDb" or r_type == "Internet Movie Database":
        revisar_data(query, movie, "rating_imdb", movie.rating_imdb)
        return float(movie.rating_imdb[:3]) * 10
    if r_type == "RT" or r_type == "Rotten Tomatoes":
        revisar_data(query, movie, "rating_rt", movie.rating_rt)
        return int(movie.rating_rt.replace("%", ""))
    if r_type == "MC" or r_type == "Metacritic":
        revisar_data(query, movie, "rating_metacritic",
                     movie.rating_metacritic)
        return int(movie.rating_metacritic.split("/")[0])


def evaluar_rating(query, movie, r_min, r_max, r_type):
    if calcular_rating(query, movie, r_type) in range(r_min, r_max + 1):
        return True
    else:
        return False


def compare(movie_value, symbol, value):
    if symbol == ">":
        if movie_value > value:
            return True
    if symbol == "<":
        if movie_value < value:
            return True
    if symbol == "==":
        if movie_value == value:
            return True
    if symbol == "!=":
        if movie_value != value:
            return True
    return False


def obtener_dato(query, movie, column):
    dato_csv = getattr(movie, columns[column])
    revisar_data(query, movie, columns[column], dato_csv)
    if column in rating_types:
        return calcular_rating(query, movie, column)
    elif column == "date":
        return int(dato_csv)
    else:
        dato = dato_csv[1:].replace(".", "")
        return int(dato)


def juntar_string(actor, pelis):
    movies = filter(lambda x: x.id in pelis, bdd.cargar_movies())
    titles = (movie.title for movie in movies)
    ret = ", ".join(titles)
    return actor + ", " + ret


def prom(ids, movies_ratings):
    return sum((movies_ratings[y] for y in ids)) / max(len(ids), 1)


def largo_values(_id, movies_dict):
    return max(len(movies_dict[_id]), 1)


def paga_actor(ids, movies):
    movies_dict = bdd.cargar_actores_inv(movies=ids)
    actor_movies = filter(lambda x: x.id in ids, movies)
    movies_box = (obtener_dato("highest_paid_actors", x, "box_office") /
                  largo_values(x.id, movies_dict) for x in actor_movies)
    return sum(movies_box)


def filtrar_ratings(movies):
    movies = filter(lambda x: 50 < calcular_rating(
        "successful_actors", x, "MC"), movies)
    movies = filter(lambda x: 50 < calcular_rating(
        "successful_actors", x, "RT"), movies)
    movies = filter(lambda x: 50 < calcular_rating(
        "successful_actors", x, "IMDb"), movies)
    return movies


def all_good(actor, actors, movies_ids):
    actor_movies = actors[actor]
    if actor_movies - movies_ids:
        return False
    else:
        return True


def transformar_en_lista(query, tipo_dato, generador):
    revisar_input(query, tipo_dato, generador, GeneratorType)
    return list(generador)


def load_database():
    movies = bdd.cargar_movies()
    return (movie for movie in movies)  # evitamos I/O operation


def filter_by_date(movies, date, lower=True):
    revisar_input("filter_by_date", "date", date, int)
    revisar_input("filter_by_date", "lower", lower, bool)
    movies = procesar_queries(movies)
    revisar_input("filter_by_date", "movies", movies, GeneratorType)
    movies_revisadas = (revisar_data("filter_by_date", x, "date", x.date)
                        for x in movies)
    if lower:
        return filter(lambda x: int(x.date) < date, movies_revisadas)
    else:
        return filter(lambda x: int(x.date) >= date, movies_revisadas)


def popular_movies(movies, r_min, r_max, r_type="All"):
    revisar_input("popular_movies", "r_min", r_min, int)
    revisar_input("popular_movies", "r_max", r_max, int)
    revisar_input("popular_movies", "r_type", r_type, str, rating_types)
    movies = procesar_queries(movies)
    revisar_input("filter_by_date", "movies", movies, GeneratorType)
    return filter(lambda x: evaluar_rating("popular_movies", x, r_min, r_max,
                                           r_type), movies)


def best_comments(movies, n):
    revisar_input("best_comments", "n", n, int)
    if n == 0:
        raise WrongInput("best_comments", "n", n)
    movies = procesar_queries(movies)
    revisar_input("filter_by_date", "movies", movies, GeneratorType)
    movies = bdd.clasificar_movies(movies)
    if n > 0:
        movies = movies[::-1]
    while movies:
        for i in range(abs(n)):
            yield movies[i]
        break


def take_movie_while(movies, column, symbol, value):
    revisar_input("take_movie_while", "column", column, str, columns)
    revisar_input("take_movie_while", "symbol", symbol, str, symbols)
    revisar_input("take_movie_while", "value", value, int)
    movies = procesar_queries(movies)
    revisar_input("filter_by_date", "movies", movies, GeneratorType)
    while movies:
        movie = next(movies)
        dato = obtener_dato("take_movie_while", movie, column)
        if compare(dato, symbol, value):
            yield movie
        else:
            break


def popular_genre(movies, r_type="All"):
    revisar_input("popular_genre", "r_type", r_type, str, rating_types)
    movies = transformar_en_lista("popular_genre", "movies",
                                  procesar_queries(movies))
    movies_rating = {x.id: calcular_rating("popular_genre", x, r_type)
                     for x in movies}
    genres = bdd.cargar_generos(movies={x.id for x in movies})
    if "N/A" in genres.keys():
        movie = next((x.title for x in movies if x.id in genres["N/A"]))
        raise MovieError("popular_actors", movie, "genre")
    rating_genres = [(k, prom(v, movies_rating)) for k, v in genres.items()]
    rating_genres.sort(key=lambda x: x[1], reverse=True)
    mejores_generos = rating_genres[:4]
    return [genre for genre, promedio in mejores_generos]


def popular_actors(movies, k_actors, n_movies, r_type="All"):
    revisar_input("popular_actors", "k_actors", k_actors, int, condition="+")
    revisar_input("popular_actors", "n_movies", n_movies, int, condition="+")
    revisar_input("popular_actors", "r_type", r_type, str, rating_types)
    movies = transformar_en_lista("popular_actors", "movies",
                                  procesar_queries(movies))
    movies.sort(key=lambda x: calcular_rating("popular_actors", x, r_type),
                reverse=True)
    movies = movies[:n_movies]
    actors = bdd.cargar_actores(movies={x.id for x in movies})
    if "N/A" in actors.keys():
        movie = next((x.title for x in movies if x.id in actors["N/A"]))
        raise MovieError("popular_actors", movie, "actor")
    actors = sorted(actors.items(), key=lambda x: len(x[1]), reverse=True)
    return [juntar_string(actor, pelis) for actor, pelis in actors[:k_actors]]


def highest_paid_actors(movies, k_actors=1):
    revisar_input("highest_paid_actors", "k_actors", k_actors, int,
                  condition="+")
    movies = transformar_en_lista("highest_paid_actors", "movies",
                                  procesar_queries(movies))
    actors = bdd.cargar_actores(movies={x.id for x in movies})
    if "N/A" in actors.keys():
        movie = next((x.title for x in movies if x.id in actors["N/A"]))
        raise MovieError("highest_paid_actors", movie, "actor")
    actors = sorted(actors.items(), key=lambda x: paga_actor(x[1], movies),
                    reverse=True)
    return [juntar_string(actor, pelis) for actor, pelis in actors[:k_actors]]


def successful_actors(movies):
    movies = procesar_queries(movies)
    revisar_input("successful_actors", "movies", movies, GeneratorType)
    movies_ids = {x.id for x in filtrar_ratings(movies)}
    actors = list({actor for k, v in
                   bdd.cargar_actores_inv(movies=movies_ids).items()
                   for actor in v})
    if "N/A" in actors:
        movie = next((x.title for x in movies if x.id in
                      bdd.cargar_actores()["N/A"]))
        raise MovieError("successful_actors", movie, "actor")
    all_actors = bdd.cargar_actores()  # con todas las movies
    return list(filter(lambda x: all_good(x, all_actors, movies_ids), actors))


consultas_posibles = {"load_database": (load_database, {0}),
                      "filter_by_date": (filter_by_date, {2, 3}),
                      "popular_movies": (popular_movies, {3, 4}),
                      "best_comments": (best_comments, {2}),
                      "take_movie_while": (take_movie_while, {4}),
                      "popular_genre": (popular_genre, {1, 2}),
                      "popular_actors": (popular_actors, {3, 4}),
                      "highest_paid_actors": (highest_paid_actors, {1, 2}),
                      "successful_actors": (successful_actors, {1})
                      }


def procesar_queries(query):
    if (not query) or (query[0] not in consultas_posibles):
        raise BadQuery(query)
    f, cantidad_argumentos = consultas_posibles[query[0]]
    args = query[1:]
    if len(args) not in cantidad_argumentos:
        raise BadQuery(query)
    return f(*args)
