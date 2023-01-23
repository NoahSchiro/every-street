"""
Simple edge element
"""
from xml.dom.minidom import parseString # This is primarily for testing
from math import sin, cos, sqrt, atan2, radians
from graph_elements.node import Node

class Edge():

	def __init__(self, n1, n2):
		
		# Add nodes
		self.n1 = n1
		self.n2 = n2

		self.weight = self.compute_distance()

	# Basic haversine computation for two given lat and lons
	# All units in meters
	def compute_distance(self):

		# Earth radius (roughly) 
		R = 6373.0

		# Extract data from the tuples
		lat1 = radians(self.n1.lat_lon[0])
		lon1 = radians(self.n1.lat_lon[1])
		lat2 = radians(self.n2.lat_lon[0])
		lon2 = radians(self.n2.lat_lon[1])

		# Compute the delta on the lats and lon
		dlat = lat2 - lat1
		dlon = lon2 - lon1

		# For more info on haversine: https://en.wikipedia.org/wiki/Haversine_formula
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		distance = (R * c) * 1000

		return distance


if __name__ == "__main__":

	document = """
	<osm>
	  <node id="1" lat="52.2296756" lon="21.0122287"/>
	  <node id="2" lat="52.406374" lon="16.9251681"/>
	  <node id="3" lat="0" lon="0"/>
	</osm>
	"""
	dom = parseString(document)
	nodes_as_elem = dom.getElementsByTagName("node")

	nodes = []
	for node in nodes_as_elem:
		nodes.append(Node(node))
