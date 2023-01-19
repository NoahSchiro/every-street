"""
For the graph object, we will want to create our own edge object so
that we can create the concept of a weight. For nodes, we really
only care about the id, lat, and lon, so we can just use the same
node that is generated from the osm file.
"""

class Graph():

	# A graph is going to just be a list of nodes and edges
	def __init__(self):

		self.nodes = set()
		self.edges = set()

	def add_node(self, elem):
		self.nodes.add(Node(elem))
		
	def add_node(self, node):
		self.nodes.add(node)

	def add_edge(self, n1, n2):
		if n1 in self.nodes and n2 in self.nodes:
			self.edges.add(Edge(n1, n2))
		else:
			print("Error: node does not exist in graph")

	def __str__(self):
		return "({}, {})".format(len(self.nodes), len(self.edges))
