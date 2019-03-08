import unittest
import library as lib

class ChequearLibreria(unittest.TestCase):

    def setUp(self):
        self.likes = "120"
        self.dislikes = "240"
        self.publish_date = "18.04.12"
        self.trending_date = "18.10.12"

    def test_trending(self):
        self.assertEqual(lib.tiempo_trending(self.publish_date,
                                             self.trending_date), 6)
    def test_likes(self):
        self.assertEqual(lib.like_dislike_ratio(self.likes, self.dislikes),
                         0.5)

    def test_trending_exceptions(self):
        self.assertRaises(ValueError, lib.tiempo_trending, "18/12/02",
                                                            "19.10.11")

    def test_likes_exceptions(self):
        self.assertRaises(TypeError, lib.like_dislike_ratio, "23dsf", "1")


suite = unittest.TestLoader().loadTestsFromTestCase(ChequearLibreria)
unittest.TextTestRunner().run(suite)
