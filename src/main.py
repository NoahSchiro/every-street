from xml.dom.minidom import parse 				# Parses .osm doc
from graph_elements.graph import Graph 			# Graph object
from parsing import filter_ways, filter_nodes	# Extra post processing on .osm
from graph_elements.utils import kruskal		# Extra post processing on .osm 
from visualization import display_graph			# Visualize the graph
from time import time							# Benchmarking
from math import floor							# Benchmarking

if __name__=="__main__":

	start = time()	
	# Move the xml file into DOM
	dom = parse("../data/selinsgrove.osm")
	stop = time()
	print("Parsed .osm in {} milliseconds".format(floor((stop - start)*1000.0)))

	# Gather all of the nodes and ways in the file
	way_elems = list(dom.getElementsByTagName("way"))
	node_elems = list(dom.getElementsByTagName("node"))

	# Filter the ways and nodes to the ones we care about
	way_elems = filter_ways(way_elems)
	node_elems = filter_nodes(node_elems, way_elems)

	# Create the graph
	g = Graph()

	start = time()	
	# Now that we have the data in a convenient form, parse it into the graph
	for elem in node_elems:
		g.add_node(elem)
	stop = time()
	print("Added {} nodes in {} milliseconds".format(len(g.nodes), floor((stop - start)*1000.0)))

	start = time()
	# Adding ways is a lot more complicated
	# For each way,
	for elem in way_elems:
		
		# Get the nd_tags
		nd_tags = list(elem.getElementsByTagName("nd"))
		
		# Get the IDs off of those tags
		node_ids = list(map(lambda x: int(x.getAttribute("ref")), nd_tags))
		
		# Collect the nodes in our graph
		# structure that pertain to this way
		nodes = []
		for i in range(len(g.nodes)):
			if g.nodes[i].iden in node_ids:
				nodes.append(g.nodes[i])

		# Run the minimum spanning tree algo to
		# figure out how they ought to be linked up
		connections = kruskal(nodes)

		# Add those edges
		for n1,n2 in connections:
			g.add_edge(n1, n2)

	stop = time()
	print("Added {} ways in {} milliseconds".format(len(g.edges), floor((stop - start)*1000.0)))
	display_graph(g)