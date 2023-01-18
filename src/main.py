from xml.dom.minidom import parse

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



if __name__=="__main__":

	# Move the xml file into DOM
	dom = parse("../data/selinsgrove.osm")

	# Gather all of the nodes and ways in the file
	way_elems = list(dom.getElementsByTagName("way"))
	node_elems = list(dom.getElementsByTagName("node"))

	num_ways_before  = len(way_elems)
	num_nodes_before = len(node_elems)

	# Filter the ways and nodes to the ones we care about
	way_elems = filter_ways(way_elems)
	node_elems = filter_nodes(node_elems, way_elems)

	num_ways_after  = len(way_elems)
	num_nodes_after = len(node_elems)

	print("Ways before: {}\nWays after: {}".format(num_ways_before, num_ways_after))
	print("Nodes before: {}\nNodes after: {}".format(num_nodes_before, num_nodes_after))

"""
# With each way, we want to gather
# nodes associated with those ways
# We can collect them in a set
node_ids = set()

# For each way
for elem in way_elems:

	# Get the nodes connected to this way
	way_nds = elem.getElementsByTagName("nd")

	# For each one of those nodes, get the id, find where that node is in the xml file
	for way_nd in way_nds:

		node_ids.add(int(way_nd.getAttribute("ref")))

# Now that we have all the ways we care about and a reference
# ID to the nodes we care about, let's go collect the node elements
print(len(node_elems))
node_elems = list(filter(lambda x: x.getAttribute("id") not in node_ids, node_elems))
print(len(node_elems))
"""