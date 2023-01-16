"""
For the graph object, we will want to create our own edge object so
that we can create the concept of a weight. For nodes, we really
only care about the id, lat, and lon, so we can just use the same
node that is generated from the osm file.
"""
import node
import edge

class Graph():

	# A graph is always just a list of nodes and edges
	def __init__(self):

		self.nodes = []
		self.edges = []