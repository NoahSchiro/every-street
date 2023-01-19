from xml.dom.minidom import parse
from graph_elements.graph import Graph
from math import radians, cos, sin, asin, sqrt

###################### VISUALIZATION #########################
import networkx as nx
import matplotlib.pyplot as plt
###################### VISUALIZATION #########################

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

	# Adding ways is a lot more complicated
	# For each way,
	for elem in way_elems:
		
		# Get the nd_tags
		nd_tags = list(elem.getElementsByTagName("nd"))
		
		# Get the IDs off of those tags
		node_ids = list(map(lambda x: int(x.getAttribute("ref")), nd_tags))
		
		# Now we want to find where those nodes are in our
		# graph structure. We can store their indexes into a list
		node_indexes = []
		for i in range(len(g.nodes)):
			if g.nodes[i].iden in node_ids:
				node_indexes.append(i)

		# Now we loop through our list of nodes, and link them up one by one
		for i in range(len(node_indexes)):

			# If we are at the last index, no connection needs to be made
			if i == len(node_indexes)-1:
				pass
			else:
				g.add_edge(g.nodes[node_indexes[i]], g.nodes[node_indexes[i+1]])
				
	###################### VISUALIZATION #########################

	options = {
	    'node_color': 'black',
	    'node_size': 3,
	    'width': 1,
	}

	# NetworkX graph
	nxg = nx.Graph()

	# Create a dictionary of node IDs to their position
	node_pos = {}

	# Add the nodes to the dictionary 
	for node in g.nodes:
		node_pos[node.iden] = [node.lat_lon[0], node.lat_lon[1]]

	# Add nodes to the graph
	nxg.add_nodes_from([node.iden for node in g.nodes])

	# Add the edges to the graph
	for edge in g.edges:
		nxg.add_edge(edge.n1.iden, edge.n2.iden)


	nx.draw_networkx(nxg, node_pos, with_labels=False, **options)
	plt.show()


	###################### VISUALIZATION #########################