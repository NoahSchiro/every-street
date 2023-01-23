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
			print("Error: node does not exist in graph")

	# Compute the length of every street
	def get_length(self):

		accumulator = 0
		for edge in self.edges:
			accumulator += edge.compute_distance()

		return accumulator

	def __str__(self):
		return "({}, {})".format(len(self.nodes), len(self.edges))
