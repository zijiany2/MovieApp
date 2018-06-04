import unittest
import network
import graph
class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.net = network.Network(network.init_graph())
        self.g = graph.Graph()

    def test_get_movie_gross(self):
        self.assertEqual(self.net.get_movie_gross('Lolita'), 1100000.0)

    def test_get_actor_age(self):
        self.assertEqual(self.net.get_actor_age('Marco Leonardi'), 46)

    def test_get_starred_movie(self):
        self.assertEqual(self.net.get_starred_movie('Marco Leonardi')[0].name, 'Once Upon a Time in Mexico')

    def test_get_starring_actors(self):
        self.assertTrue('Melanie Griffith' in [v.name for v in self.net.get_starring_actors('Lolita')])

    def test_get_most_grossing_movies(self):
        self.assertEqual(self.net.get_most_grossing_movies(1)[0].name, 'Titanic')

    def test_get_oldest_actors(self):
        self.assertEqual(self.net.get_oldest_actors(1)[0].name, 'Dick Van Dyke')

    def test_get_movies_for_a_year(self):
        self.assertEqual([v.name for v in self.net.get_movies_for_a_year('2000')],['Traffic'])

    def test_get_actors_of_an_age(self):
        self.assertEqual([v.name for v in self.net.get_actors_of_an_age(40)],['Chiwetel Ejiofor'])

    def test_get_degree(self):
        self.g.add_vertex(1,1)
        self.g.add_vertex(2,2)
        self.g.link_vertices(1,2)
        self.assertEqual(self.g.get_degree(1),1)


#if __name__ == '__main__':
#    unittest.main()


