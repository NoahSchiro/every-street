"""
For the graph object, we will want to create our own edge object so
that we can create the concept of a weight. For nodes, we really
only care about the id, lat, and lon, so we can just use the same
node that is generated from the osm file.
"""
import node
import edge

class Graph():

	# A graph is going to just be a list of nodes and edges
	def __init__(self):

		self.nodes = []
		self.edges = []

	def add_node(self, elem):
		nodes.append(Node(elem))
		
	def add_node(self, node):
		nodes.append(node)

	def add_edge(self, n1, n2):
		edges.append(Edge(n1, n2))

	def add_edge(self, edge):
		edges.append(edge)
