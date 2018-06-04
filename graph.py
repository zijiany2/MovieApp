from asyncio import Queue
import heapq

# a processing function of vertex
def print_content(v):
	print(v.content)
	return None


class Vertex:
	# Vertex class
	# Each vertex has a unique id, a content field and an edge list
	def __init__(self,content, id):
		self.id = id
		self.content = content
		self.edges = []

	def get_degree(self):
		return len(self.edges)

	def __gt__(self, other):
		return self.get_degree() > other.get_degree()

	def get_all_neighbors(self):
		'''get the neighbors of a vertex refered by id'''
		neighbors = []
		for e in self.edges:
			neighbor = e.vertices[1] if e.vertices[0] == self \
					else e.vertices[0]
			neighbors.append(neighbor.content)
		return neighbors

class Edge:
	#Edge class
	#Each edge has a vertices list (of length 2) and a weight (default to 0)
    def __init__(self, vertices, weight = 0):
    	self.vertices = vertices
    	self.weight = weight
    
class Graph:
	'''The generic graph class'''
	def __init__(self):
		'''maintaining a vertices dictionary {id:vertex}'''
		self.vdict = {}
	
	def add_vertex(self,v,id):
		'''add a single vertex with content =v and identity = id'''
		vertex = Vertex(v,id)
		self.vdict[id] = vertex
	
	def add_vertices(self,vdict):
		'''add multiple vertices from vdict of the form {id:content}'''
		for id in vdict.keys():
			vdict[id] = Vertex(vdict[id], id)
		self.vdict.update(vdict) 

	def link_vertices(self, id1, id2, weight = 0):
		'''link two vertices referred by id1 and id2'''
		vl = [self.vdict[id1], self.vdict[id2]]
		e = Edge(vl, weight)
		vl[0].edges.append(e)
		vl[1].edges.append(e)

	def max_degree_vertices(self, num):
		return heapq.nlargest(num, self.vdict.values())


	def traverse(self, search_fun, processing = print_content):
		'''traverse the graph
		search fun: the way of traversal, bfs or dfs
		processing: a function to process a vertex and return a value
		return collection, which is a list of the values returned by processing
		'''
		collection = []
		visited = dict(zip(self.vdict.keys(), [0] * len(self.vdict)))
		source = self.find_first_unvisited(visited)
		while source is not None: 
			search_fun(source, visited, processing, collection)
			source = self.find_first_unvisited(visited)
		return collection

	def find_first_unvisited(self,visited):
		'''return a vertex that has not been visited in traversal'''
		for id in visited:
			if visited[id] == 0:
				return self.vdict[id]
		return None

	def bfs(self, vertex, visited, processing, collection):
		'''breadth-first search
		vertex: current vertex to be visited
		visited: recording of vistied vertices
		procesing: a function to process a vertex and return a value
		collection: a list of the values returned by processing
		'''
		q = Queue()
		visited[vertex.id] = 1
		collection.append(processing(vertex))
		q.put(vertex)
		while(not q.empty()):
			v0 = q.get()
			for e in v0.edges:
				v1 = e.vertices[1] if e.vertices[0] == v0 \
					else e.vertices[0]

				if visited[v1.id] == 0:
					visited[v1.id] = 1
					collection.append(processing(v1))
					q.put(v1)


	def dfs(self, vertex, visited, processing, collection):
		'''depth-first search
				vertex: current vertex to be visited
				visited: recording of vistied vertices
				procesing: a function to process a vertex and return a value
				collection: a list of the values returned by processing
		'''
		visited[vertex.id] = 1
		collection.append(processing(vertex))
		for e in vertex.edges:
			v1 = e.vertices[1] if e.vertices[0] == vertex \
				else e.vertices[0]
			if visited[v1.id] == 0:
				self.dfs(v1, visited, processing, collection)










