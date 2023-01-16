from xml.dom.minidom import parse

def looking_at_tags(dom):

	# Gather all of the node objects
	nodes = dom.getElementsByTagName("node")

	# For now, I just want to see what kind of "keys" are
	# in nodes, so we will create a set to gather them
	key_values = set()

	# Go through all of the nodes
	for node in nodes:

		# Go through all of the tags in the nodes
		tags = node.getElementsByTagName("tag")

		for tag in tags:

			key_values.add(tag.getAttribute("k"))

	# Print the set of keys
	for key in key_values:
		print(key)

def looking_at_ways(dom):

	ways = dom.getElementsByTagName("way")

	nodes = dom.getElementsByTagName("node")

	# For now, let's look at the connection of one way.
	# The tag "nd" will generate the nodes that this way is connected to
	node_list = None

	# This will just find North Market Street
	for way in ways:
		if way.getAttribute("id") == "477217061":
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

# The documentation noted that all ways should have >= 2 nd tags. Let's make sure.
def check_valid_ways(dom):

	ways = dom.getElementsByTagName("way")

	for way in ways:
		iden = way.getAttribute("id")
		nds  = way.getElementsByTagName("nd")

		if len(nds) < 2:
			print("Error. Check out way {}".format(iden))


if __name__ == "__main__":

	data = parse("../data/selinsgrove.osm")
	check_valid_ways(data)
