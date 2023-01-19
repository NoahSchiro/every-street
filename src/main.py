from xml.dom.minidom import parse
from graph_elements.graph import Graph
from math import radians, cos, sin, asin, sqrt

# Ways is passed in as the [minidom.Element] 
# Returns a list of way elements we care about [minidom.Element]
def filter_ways(ways):

	# These are tag values which are either
	# 1. Not a road
	# 2. Illegal to ride a bike on
	bad_highway_values = ["footway", "raceway", "path"]
	bad_service_vales = ["parking_aisle", "driveway", "emergency_access"]

	# Accumulator for the ways that we care about
	good_ways = []

	# Eliminate ways which are not related to streets.
	for way in ways:

		# Flag
		keep = False
		tags = way.getElementsByTagName("tag")

		# For each tag, make sure that it:
		for tag in tags:
			
			key   = tag.getAttribute("k")
			value = tag.getAttribute("v")

			# 1. Has a highway tag (but doesn't have bad values of highway)
			if key == "highway" and value not in bad_highway_values:
				keep = True

			# 2. Is not a private drive
			if key == "access" and value == "private":
				keep = False
				break

			# 3. Does not have a service tag that has bad values
			if key == "service" and value in bad_service_vales:
				keep = False
				break

		# Add to our list if the flag is still true
		if keep:
			good_ways.append(way)

	# Return accumulator
	return good_ways

def filter_nodes(node_elems, way_elems):

	# Accumulator for the nodes of interest
	node_ids = set()

	# Go through all of the ways
	for way in way_elems:

		# Go through all the references to nodes
		# and add the IDs to the accumulator
		nds = way.getElementsByTagName("nd")

		for nd in nds:
			node_ids.add(int(nd.getAttribute("ref")))

	# Now we can go through all the nodes and only return the ones in the set
	return list(filter(lambda x : int(x.getAttribute("id")) in node_ids, node_elems))

# Compute the distance between two coordinates
def haversine(lat_lon1, lat_lon2):

	# Radius of the earth
    R = 6372.8

    # Delta on the lat / lon
    dLat = radians(lat_lon2[0] - lat_lon1[0])
    dLon = radians(lat_lon2[1] - lat_lon1[1])

    lat1 = radians(lat_lon1[0])
    lat2 = radians(lat_lon2[0])

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c * 1000

if __name__=="__main__":

	# Move the xml file into DOM
	dom = parse("../data/selinsgrove.osm")

	# Gather all of the nodes and ways in the file
	way_elems = list(dom.getElementsByTagName("way"))
	node_elems = list(dom.getElementsByTagName("node"))

	# Filter the ways and nodes to the ones we care about
	way_elems = filter_ways(way_elems)
	node_elems = filter_nodes(node_elems, way_elems)

	# Create the graph
	g = Graph()

	# Now that we have the data in a convenient form, parse it into the graph
	for elem in node_elems:
		g.add_node(elem)

	n1 = g.nodes[0].lat_lon
	n2 = g.nodes[1].lat_lon

	print(n1)
	print(n2)
	print(haversine(n1,n2))
