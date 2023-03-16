import networkx as nx
import matplotlib.pyplot as plt
from graph_elements.graph import Graph

def display_graph(g, heatmap=False):

	# Make it dark mode
	plt.rcParams['axes.facecolor'] = 'black'
	plt.rcParams['axes.edgecolor'] = 'black'

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

	if heatmap:
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

	# If heatmap = False
	else:
		
		# Add the edges to the graph
		for edge in g.edges:
			nxg.add_edge(edge.n1.iden, edge.n2.iden)
		
		# Make it dark
		plt.rcParams['axes.facecolor'] = 'black'
		plt.rcParams['axes.edgecolor'] = 'black'

		# Draw
		nx.draw_networkx(nxg, node_pos, with_labels=False, edge_color='white', **options)

	plt.show()

def animate_walk(path, speed):

	# Imports needed for this
	import numpy as np
	from matplotlib.animation import FuncAnimation

	# Output we will draw too
	fig, ax = plt.subplots()
	xdata, ydata = [], []

	# This "line" will be used to plot our route
	ln, = ax.plot([], [])

	# I am setting these to the maximum coordinates of our route
	def init():

		# Determine the min and max coordinates of the animation
		lat_min = 360
		lat_max = -360
		lon_min = 360
		lon_max = -360
		for node in path:
			lat_min = min(lat_min, node.lat_lon[0])
			lat_max = max(lat_max, node.lat_lon[0])
			lon_min = min(lon_min, node.lat_lon[1])
			lon_max = max(lon_max, node.lat_lon[1])
		
		print("{}, {}".format(lat_min, lat_max))
		print("{}, {}".format(lon_min, lon_max))

		ax.set_xlim(lon_min, lon_max)
		ax.set_ylim(lat_min, lat_max)

		return ln,

	def update(frame):
		ydata.append(path[frame].lat_lon[0])
		xdata.append(path[frame].lat_lon[1])
		ln.set_data(xdata, ydata)
		return ln,

	ani = FuncAnimation(fig, update, interval=speed, frames=range(len(path)), init_func=init, blit=True)

	plt.show()

