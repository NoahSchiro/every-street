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

	# Add the edges to the graph
	for edge in g.edges:
		nxg.add_edge(edge.n1.iden, edge.n2.iden)

	plt.rcParams['axes.facecolor'] = 'black'
	plt.rcParams['axes.edgecolor'] = 'black'
	nx.draw_networkx(nxg, node_pos, with_labels=False, edge_color='white', **options)
	plt.show()