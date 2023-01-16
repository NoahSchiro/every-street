"""
A simple way class. The method of storing ways in the osm
format is interesting. Say we have one street which connects
with 3 other streets via three intersections. In this case,
this will be represented as one "way" (one street) and then 
will have three child tags ("nd"). Each of these three children
represent one of the intersections in some order. For the purposes
of making a graph object out of this, this is important to remember.
We want to make sure we are generating multiple edges out of a 
single way, if there are > 2 nd tags. It's possible that these
nd tags are generated out of order, so we want to ensure that we are 
making edges that makes sense. For example, we don't want to generate
edges that go all the way from one intersection to another, skipping 
over intersections.

The best way to tackle this issue is to calculate the geodetic distance
between each of these nodes. For one given "way" we are really only 
generating a line, so for each node we only generate a connection that
is the two closest nodes.

For now, the way will just hold a list of ref ids to the nodes it is
connected to. The graph can handle making the actual edges, making
sure they are real nodes, etc.
"""

from xml.dom.minidom import parseString # This is primarily for testing

class Way():

	# Constructor that takes a minidom_element as a constructor
	def __init__(self, elem):

		# Get nd tags
		nd_tags = elem.getElementsByTagName("nd")
		iden = elem.getAttribute("id")

		# Make sure that this is a valid way
		if len(nd_tags) < 2:
			raise Exception("Error: Way must contain more than 2 nd tags")


		node_ids = []

		# For some reason, nd_tags is some weird iterator object. We
		# will just pull out the id numbers that we care about
		for i in range(nd_tags.length):
			node_ids.append(int(nd_tags.item(i).getAttribute("ref")))

		self.iden     = iden
		self.node_ids = node_ids

if __name__ == "__main__":

	document = """
	<way id="12051666">
	  <nd ref="108998219"/>
	  <nd ref="109022286"/>
	  <nd ref="109022288"/>
	  <nd ref="10312371294"/>
	  <nd ref="108982460"/>
	</way>
	"""

	dom = parseString(document)

	ways = dom.getElementsByTagName("way")

	way_objects = []

	for way in ways:
		way_objects.append(Way(way))

	for way in way_objects:
		print("Way id: {}".format(way.iden))
		print("Node ids: ", end="")
		for node in way.node_ids:
			print("{},".format(node), end=" ")
		print("")
