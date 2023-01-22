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

def check_a_way(dom, way_id):

	ways = dom.getElementsByTagName("way")

	nodes = dom.getElementsByTagName("node")

	# For now, let's look at the connection of one way.
	# The tag "nd" will generate the nodes that this way is connected to
	node_list = None

	for way in ways:
		if way.getAttribute("id") == way_id:
			node_list = way.getElementsByTagName("nd")

	# Collect the nodes that this way is associated with
	node_ids = []
	for i in range(node_list.length):
		node_ids.append(node_list.item(i).getAttribute("ref"))

	# Now, loop through all of the 
	# nodes and find the ones we care about
	nodes_connected = []
	for node in nodes:
		for i in node_ids:
			if node.getAttribute("id") == i:
				nodes_connected.append(node)

	# Now we want to fetch 
	# the lat and lon of each of these nodes
	lat_lon = []
	for node in nodes_connected:
		lat = float(node.getAttribute("lat"))
		lon = float(node.getAttribute("lon"))
		lat_lon.append((lat,lon))

	for i in lat_lon:
		print(i)
if __name__ == "__main__":

	data = parse("../data/selinsgrove.osm")
	check_a_way(data, "918721924")

	# check_way_tag_types(data)

""" 
primary_link	-> Save
secondary		-> Save
motorway_link	-> Save
service 		-> Save
residential		-> Save
motorway 		-> Save
footway			-> Don't save
unclassified	-> Save, but could cause problems later on
primary 		-> Save
raceway			-> Don't save
path			-> Don't save
tertiary		-> Save
"""