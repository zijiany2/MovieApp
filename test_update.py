import unittest
from flask_testing import TestCase
from app import app
from analysis import Network
import json


class MyTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_actor(self):
        response = self.client.get("/network/api/actors/Bruce Willis")
        self.assertEquals(response.json['name'], 'Bruce Willis')

    def test_filter_actors(self):
        response = self.client.get("/network/api/actors?\'Bruce\'INname")
        self.assertTrue('Bruce Willis' in response.json)

    def test_get_movie(self):
        response = self.client.get("/network/api/actors/Bruce Willis")
        self.assertEquals(response.json['name'], 'Bruce Willis')

    def test_filter_movies(self):
        response = self.client.get("/network/api/movies?\'Verdict\'INnameANDyear=1982")
        self.assertTrue('The Verdict' in response.json)

    def test_update_actor(self):
        with app.test_client() as c:
            c.put("/network/api/actors/Bruce Willis", data=json.dumps(dict(age=62)),
                  content_type='application/json')
            response = c.get("/network/api/actors/Bruce Willis")
            self.assertEquals(response.json['age'], 62)

    def test_update_movie(self):
        with app.test_client() as c:
            c.put("/network/api/movies/The Verdict", data=json.dumps(dict(box_office=0)),
                  content_type='application/json')
            response = c.get("/network/api/movies/The Verdict")
            self.assertEquals(response.json['box_office'], 0)

    def test_add_actor(self):
        with app.test_client() as c:
            c.post("/network/api/actors", data=json.dumps(dict(name="Alice",age=0,total_gross=0)),
                   content_type='application/json')
            response = c.get("/network/api/actors/Alice")
            print(response)
            self.assertEquals(response.json['age'], 0)

    def test_add_movie(self):
        with app.test_client() as c:
            c.post("/network/api/movies", data=json.dumps(dict(name="XMan", year=2019)),
                   content_type='application/json')
            response = c.get("/network/api/movies/XMan")
            self.assertEquals(response.json['year'], 2019)

    def test_del_actor(self):
        with app.test_client() as c:
            c.post("/network/api/actors", data=json.dumps(dict(name="Alice", age=0, total_gross=0)),
                   content_type='application/json')
            response = c.delete("/network/api/actors/Alice",content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_del_movie(self):
        with app.test_client() as c:
            c.post("/network/api/movies", data=json.dumps(dict(name="XMan", year=2019)),
                   content_type='application/json')
            response = c.delete("/network/api/movies/XMan",content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_analysis(self):
        net = Network()
        hub_10 = net.get_hub_actors(10)
        names, _ = zip(*hub_10)
        self.assertTrue('Bruce Willis' in names)
        age_gross = net.get_age_average_gross_pairs()
        self.assertTrue(61 in age_gross)

if __name__ == '__main__':
    unittest.main()
