"""
The node class is fairly simple. There is only a
couple aspects of the data that we care about
for now, this is just the id number, the
latitude and longitude (which is normally
represented as a 2-tuple). 
"""

from xml.dom.minidom import parseString # This is primarily for testing

class Node():

	# Constructor that takes a minidom element as argument
	def __init__(self, elem):

		# Collect items of interest
		iden = elem.getAttribute("id") 
		lat  = elem.getAttribute("lat")
		lon  = elem.getAttribute("lon")

		# Make sure everything worked	
		if iden == None:
			raise Exception("Error: Node did not have id number")
		if lat == None:
			raise Exception("Error: Node did not have latitude")
		if lon == None:
			raise Exception("Error: Node did not have longitude")
		
		# Form two tuple
		lat_lon = (lat, lon)

		self.iden    = iden		# Identification
		self.lat_lon = lat_lon 	# Longitude


if __name__ == "__main__":

	document = """
	<node id="26514338" visible="true" version="1" changeset="235448" timestamp="2007-03-13T14:50:07Z" user="Adam Killian" uid="5473" lat="40.8102044" lon="-76.8551536">
	 <tag k="created_by" v="YahooApplet 1.0"/>
	</node>
	"""

	# Parse and get node	
	dom = parseString(document)
	nodes = dom.getElementsByTagName("node")

	# Create node
	my_node = Node(nodes[0])

	print("Node id: {}".format(my_node.iden))
	print("Node lat: {}".format(my_node.lat_lon[0]))
	print("Node lon: {}".format(my_node.lat_lon[1]))
