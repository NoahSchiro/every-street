"""
For the graph object, we will want to create our own edge object so
that we can create the concept of a weight. For nodes, we really
only care about the id, lat, and lon, so we can just use the same
node that is generated from the osm file.
"""
from graph_elements.node import Node
from graph_elements.edge import Edge

class Graph():

	# A graph is going to just be a list of nodes and edges
	def __init__(self):

		self.nodes = []
		self.edges = []

	def add_node(self, elem):
		self.nodes.append(Node(elem))
		
	def add_edge(self, n1, n2):
		if n1 in self.nodes and n2 in self.nodes:
			self.edges.append(Edge(n1, n2))
		else:
			raise Exception("Error: node does not exist in graph")

	def to_dictionary(self):

		d = {}
		for i in range(len(self.nodes)):
			d[i] = []

		edges_as_tuple = []
		for i in range(len(self.edges)):
			n1 = self.edges[i].n1
			n2 = self.edges[i].n2
			n1_idx = -1
			n2_idx = -1

			for i in range(len(self.nodes)):
				if self.nodes[i] == n1:
					n1_idx = i
				if self.nodes[i] == n2:
					n2_idx = i

			edges_as_tuple.append((n1_idx, n2_idx, self.edges[i].weight))

		for edge in edges_as_tuple:
			d[edge[0]].append((edge[1], edge[2]))
			d[edge[1]].append((edge[0], edge[2]))

		return d

	# A dictionary, but only with nodes referencing other nodes
	def to_node_dictionary(self):
	
		d = {}
		for node in self.nodes:
			d[node] = []

		for edge in self.edges:
			d[edge.n1].append(edge.n2)	
			d[edge.n2].append(edge.n1)

		return d

	# Compute the length of every street
	def get_length(self):

		accumulator = 0
		for edge in self.edges:
			accumulator += edge.compute_distance()

		return accumulator

	def __str__(self):
		return "({}, {})".format(len(self.nodes), len(self.edges))
