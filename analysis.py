import json
import graph
from collections import defaultdict

class Actor:
    def __init__(self, name, age, gross):
        self.name = name
        self.age = age
        self.gross = gross

    def __gt__(self, actor):
        '''compare two actors according to their gross'''
        return self.gross > actor.gross


def init_graph():
    '''
    load the data file and build the actor network graph
    :return: the actor network graph
    '''
    g = graph.Graph()
    with open("data.json") as f:
        data = json.load(f)
    actors = {k: Actor(v["name"], v["age"], v["total_gross"]) \
              for (k, v) in data[0].items()}
    g.add_vertices(actors)

    actor_names = list(actors.keys())

    for i, name1 in enumerate(actor_names):
        for j in range(i+1, len(actors)):
            name2 = actor_names[j]
            actor1 = data[0][name1]
            actor2 = data[0][name2]
            # if the movies lists of two actors joint, then add an adge
            if not set(actor1["movies"]).isdisjoint(actor2["movies"]):
                    g.link_vertices(name1, name2)
    return g

class Network:
    def __init__(self):
        self.g = init_graph()

    def get_hub_actors(self, num):
        '''
        get the actors with most connections with other actors
        :param num: the number of actors
        :return: a list of top-num actor, degree pairs
        '''
        return [(v.content.name, v.get_degree()) for v in self.g.max_degree_vertices(num)]

    def get_age_average_gross_pairs(self):
        '''
        get the average gross of actors of the same age
        :return: a dictionary with key = age and value = average gross
        '''
        def age_gross_pair(vertex):
            return (vertex.content.age, vertex.content.gross)

        pairs =  self.g.traverse(self.g.bfs, age_gross_pair)
        merged_gross = defaultdict(list)
        for k, v in pairs:
            merged_gross[k].append(v)
        for age in merged_gross:
            l = merged_gross[age]
            merged_gross[age] = sum(l)/len(l)
        
        return merged_gross



