# módulo destinado a importar los tests


import libreria as lib
import unittest
import os
import preprocesamiento

RESULT1 = {x for x in range(19)}
RESULT2 = {0, 1, 4, 6, 8, 9, 10, 11, 14, 15, 17, 18}
RESULT3 = {0, 1, 4, 6, 7, 8, 9, 10, 11, 14, 15, 17, 18}
RESULT4 = {0}
RESULT5 = {0, 1}
RESULT6 = ['Musical', 'Comedia', 'Ciencia ficción', 'Acción']
RESULT7 = ['Belén Saldías, Piratas del caribe, Matrix']
RESULT81 = ['Jaime Castro, Braveheart, Pulp fiction']
RESULT82 = ['Ignacio Hermosilla, Titanic, El exorcista',
            'Fernando Pieressa, El exorcista']
RESULT91 = ['Hernán Valdivieso']
RESULT92 = ['Enzo Tamburini']


class TestearLibreria(unittest.TestCase):
    """As seen at: https://github.com/IIC2233/contenidos/blob/master/
    semana-04/03-testing.ipynb"""

    def setUp(self):
        self.results = {"load_database": RESULT1,
                        "filter_by_date": RESULT2,
                        "popular_movies": RESULT3,
                        "best_comments": RESULT4,
                        "take_movie_while": RESULT5,
                        "popular_genre": RESULT6,
                        "popular_actors": RESULT7,
                        "highest_paid_actors1": RESULT81,
                        "highest_paid_actors2": RESULT82,
                        "successful_actors1": RESULT91,
                        "successful_actors2": RESULT92
                        }

    def tearDown(self):
        if os.path.isfile("clean_reviews.csv"):
            os.remove("clean_reviews.csv")

    def test_load_database(self):
        result = lib.procesar_queries(["load_database"])
        movies = {int(movie.id) for movie in result}
        self.assertEqual(movies, self.results["load_database"])

    def test_filter_by_date(self):
        result = lib.procesar_queries(["filter_by_date", ["popular_movies",
                                                          ["load_database"],
                                                          50, 100, "RT"],
                                       2009])
        movies = {int(movie.id) for movie in result}
        self.assertEqual(movies, self.results["filter_by_date"])

    def test_popular_movies(self):
        result = lib.procesar_queries(["popular_movies", ["load_database"],
                                       50, 100, "RT"])
        movies = {int(movie.id) for movie in result}
        self.assertEqual(movies, self.results["popular_movies"])

    def test_best_comments(self):
        preprocesamiento.reviews_writer("clean_reviews.csv",
                                        "TestingDatabase/reviews.csv")
        result = lib.procesar_queries(["best_comments", ["take_movie_while",
                                                         ["load_database"],
                                                         "RT", ">", 30], 1])
        movies = {int(movie.id) for movie in result}
        self.assertEqual(movies, self.results["best_comments"])

    def test_take_movie_while(self):
        result = lib.procesar_queries(["take_movie_while", ["load_database"],
                                       "date", "<", 2005])
        movies = {int(movie.id) for movie in result}
        self.assertEqual(movies, self.results["take_movie_while"])

    def test_popular_genre(self):
        result = lib.procesar_queries(["popular_genre", ["filter_by_date",
                                                         ["popular_movies",
                                                          ["load_database"],
                                                          50, 100, "RT"],
                                                         2000, False], "RT"])
        self.assertIsInstance(result, list)
        self.assertEqual(result, self.results["popular_genre"])

    def test_popular_actors(self):
        result = lib.procesar_queries(["popular_actors", ["load_database"], 1,
                                       10, "RT"])
        self.assertIsInstance(result, list)
        self.assertEqual(result, self.results["popular_actors"])

    def test_highest_paid_actors1(self):
        result = lib.procesar_queries(["highest_paid_actors",
                                       ["filter_by_date", ["popular_movies",
                                                           ["load_database"],
                                                           50, 100, "RT"],
                                        2000]])
        self.assertIsInstance(result, list)
        self.assertEqual(result, self.results["highest_paid_actors1"])

    def test_highest_paid_actors2(self):
        result = lib.procesar_queries(["highest_paid_actors",
                                       ["filter_by_date", ["popular_movies",
                                                           ["load_database"],
                                                           55, 95, "RT"],
                                        2002], 2])
        self.assertIsInstance(result, list)
        self.assertEqual(result, self.results["highest_paid_actors2"])

    def test_successfulll_actors1(self):
        result = lib.procesar_queries(
            ["successful_actors", ["filter_by_date", ["popular_movies",
                                                      ["load_database"], 70,
                                                      90, "RT"], 2010, True]])
        self.assertIsInstance(result, list)
        self.assertEqual(result, self.results["successful_actors1"])

    def test_successfulll_actors2(self):
        result = lib.procesar_queries(
            ["successful_actors", ["filter_by_date", ["popular_movies",
                                                      ["load_database"], 60,
                                                      100, "RT"], 2001]])
        self.assertIsInstance(result, list)
        self.assertEqual(result, self.results["successful_actors2"])


suite = unittest.TestLoader().loadTestsFromTestCase(TestearLibreria)
unittest.TextTestRunner().run(suite)
