from xml.dom.minidom import parse
	
# Move the xml file into DOM
dom = parse("../data/selinsgrove.osm")

# Gather all of the nodes and ways in the file
way_elems = dom.getElementsByTagName("way")
node_elems = list(dom.getElementsByTagName("node"))

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