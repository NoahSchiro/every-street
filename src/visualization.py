import networkx as nx
import matplotlib.pyplot as plt
from graph_elements.graph import Graph

def display_graph(g):

	options = {
	    'node_color': 'white',
	    'node_size': 5,
	    'width': 2,
	}

	# NetworkX graph
	nxg = nx.Graph()

	# Create a dictionary of node IDs to their position
	node_pos = {}

	# Add the nodes to the dictionary 
	for node in g.nodes:
		node_pos[node.iden] = [node.lat_lon[1], node.lat_lon[0]]

	# Add nodes to the graph
	nxg.add_nodes_from([node.iden for node in g.nodes])
	nx.draw_networkx_nodes(nxg, node_pos, node_size=2, node_color='black')

	# Now we want to split the edges into buckets. Here, the index of
	edges_copy = g.edges
	edges_count = []

	for edge in edges_copy: 
		n1 = edge.n1
		n2 = edge.n2
		count = 1
		for edge2 in edges_copy:
			if edge2.n1 == n1 and edge2.n2 == n2 and edge2 != edge:
				count += 1
				edges_copy.remove(edge2)
		edges_count.append((edge,count))

	count_color = {
		1: "blue",
		2: "green",
		3: "orange",
		4: "red",
	}
	for edge in edges_count:
		nx.draw_networkx_edges(nxg, node_pos,
							   edgelist=[(edge[0].n1.iden, edge[0].n2.iden)], 
							   edge_color=count_color[edge[1]])



	# Make it dark
	plt.rcParams['axes.facecolor'] = 'black'
	plt.rcParams['axes.edgecolor'] = 'black'
	plt.show()