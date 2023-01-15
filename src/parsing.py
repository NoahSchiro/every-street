from xml.dom.minidom import parse

# Parse into Document object
data = parse("../data/selinsgrove.osm")

# Gather all of the node objects
nodes = data.getElementsByTagName("nodes")

# For now, I just want to see what kind of "keys" are
# in nodes, so we will create a set to gather them
key_values = set()

# Go through all of the nodes
for node in nodes:

	# Go through all of the tags in the nodes
	tags = node.getElementsByTagName("tag")

	for tag in tags:

		# Get the key and add it to the set
		key = tag.getAttribute("k")

		key_values.add(key)

# Print the set of keys
for key in key_values:
	print(key)
