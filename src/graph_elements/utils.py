from graph_elements.graph import Graph
from math import radians, cos, sin, asin, sqrt
from matplotlib.path import Path
from random import choice 

def insort_right(a, x, lo=0, hi=None, *, key=None):
    
    if key is None:
        lo = bisect_right(a, x, lo, hi)
    else:
        lo = bisect_right(a, key(x), lo, hi, key=key)
    a.insert(lo, x)

def bisect_right(a, x, lo=0, hi=None, *, key=None):
    
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if x < a[mid]:
                hi = mid
            else:
                lo = mid + 1
    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if x < key(a[mid]):
                hi = mid
            else:
                lo = mid + 1
    return lo

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

# This is just a mess... Don't look at it...
# All you need to know is that if you given it a
# list of nodes, it returns a list of edges for
# how you should connect them
def kruskal(nodes):

	new_node = []

	for i, node in enumerate(nodes):
		new_node.append((node, i))

	nodes = new_node

	def find(parent, i):
		if parent[i] == i:
			return i
		return find(parent, parent[i])

	def apply_union(parent, rank, x, y):
		xroot = find(parent,x)
		yroot = find(parent,y)
		if rank[xroot] < rank[yroot]:
			parent[xroot] = yroot
		elif rank[xroot] > rank[yroot]:
			parent[yroot] = xroot
		else:
			parent[yroot] = xroot
			rank[xroot] += 1

	result = []
	i,e = 0,0
	parent = []
	rank = []

	# 3-tuple (distance, n1, n2)
	edges = []

	for n1 in range(len(nodes)-1):
		for n2 in range(n1+1, len(nodes)):
			distance = haversine(nodes[n1][0].lat_lon, nodes[n2][0].lat_lon)
			edges.append((distance, nodes[n1], nodes[n2]))

	edges.sort(key=lambda x: x[0])

	for j in range(len(nodes)):
		parent.append(j)
		rank.append(0)

	while e < len(nodes)-1:
		(w,u,v) = edges[i]
		i = i+1
		x = find(parent, u[1])
		y = find(parent, v[1])
		if x != y:
			e = e + 1
			result.append((u[0],v[0]))
			apply_union(parent, rank, x, y)

	return result

# File is a .txt file that contains a list of coordinates as such
# (latitude, longitude)
# (latitude, longitude)
# ...
# (latitude, longitude)
# Nodes just a list of the nodes, ideally from Graph.nodes
def point_in_polygon(g, file):

	points = []
	
	fd = open(file)
	for line in fd:
		if line[0] != '(' or line[len(line)-2] != ')':
			raise Exception("File is not formatted properly!")

		line = line[1:len(line)-2]
		lat, lon = line.split(', ')
		points.append((float(lat), float(lon)))
	
	polygon = Path(points)

	# Returns a list of booleans
	is_in = polygon.contains_points([x.lat_lon for x in g.nodes])

	# Filter the original list
	nodes_in_poly = []
	for i in range(len(is_in)):
		if is_in[i]:
			nodes_in_poly.append(g.nodes[i])

	g.nodes = nodes_in_poly

	"""
	This bit of code will display the polygon if you want
	codes = [
	    Path.MOVETO,
	    Path.LINETO,
	    Path.LINETO,
	    Path.LINETO,
	    Path.CLOSEPOLY,
	]
	fig, ax = plt.subplots()
	patch = patches.PathPatch(polygon, facecolor='orange', lw=2)
	ax.add_patch(patch)
	ax.set_xlim(40.7, 40.9)
	ax.set_ylim(-76.9, -76.8)
	plt.show()
	"""

# Accepts a graph, a starting node, and a
# set of nodes to attempt to reach
def bfs(G, start, targets):

	new_targets = [x for x in targets if x != start]

	# Queue of nodes to explore
	queue = []

	# Start the node with the root
	queue.append((start, 0))

	# Nodes we have already explored
	explored = set()
	explored.add(start)

	# For each node, a reference to the "parent" node
	node_parents = {}
	node_parents[start] = None

	# Last node we looked at
	node = (None, 0)

	# While the queue is not empty
	while queue:

		# Grab the node to be explored and
		# the distance it took to get there so far
		node, distance = queue.pop(0)

		# If node happens to
		# be what we are looking for
		if node in new_targets:
			break

		# [(Node, Absolute weight it takes to get there from start)]
		adjacent_nodes = []

		for edge in G.edges:
			if edge.n1 == node:
				adjacent_nodes.append((edge.n2, distance + edge.weight))
			if edge.n2 == node:
				adjacent_nodes.append((edge.n1, distance + edge.weight))

		# Go through adjacent nodes
		for next_node, weight in adjacent_nodes:
			# If we have not seen them
			if next_node not in explored:
				# Mark them as seen
				explored.add(next_node)
				# Mark the parent node as the node before it
				node_parents[next_node] = node
				# Insert the node into our queue IN ORDER
				insort_right(queue, (next_node, weight), key=lambda x: x[1])

	# When this while loop breaks, we should
	# be able to use the dictionary to
	# reconstruct the path back
	path = []
	path.append(node)
	while node_parents[node] != None:
		path.append(node_parents[node])
		node = node_parents[node]

	return path

def make_graph_eulerian(g):

	# First we need to collect the odd vertices	
	node_connections = []

	# For each node
	for node in g.nodes:
		
		# Accumulate the number of connections it has
		connections = 0
		for edge in g.edges:
			if edge.n1 == node or edge.n2 == node:
				connections += 1

		# Add to list
		node_connections.append((node, connections))
	
	# Filter the node connections that are odd, remove the 
	# number of connections they have, and put them into a set
	odd_nodes = list(map(lambda x: x[0], filter(lambda x: x[1]%2==1, node_connections)))

	# While their are intersections that are non-eulerian
	while len(odd_nodes) > 0:

		# Select a node at random
		start_node = choice(odd_nodes)
		path = bfs(g, start_node, odd_nodes)
		end_node = path[0]
		path_back = bfs(g, end_node, odd_nodes)

		# If they both agree that they are the shortest node to each other
		if start_node == path_back[0]:

			# Now, for every connection in that path, we need to add it to
			# the graph. This is effectively duplicating some edges
			for i in range(len(path)-1):
				n1 = path[i]
				n2 = path[i+1]
				g.add_edge(n1, n2)

			odd_nodes.remove(start_node)
			odd_nodes.remove(end_node)

"""	
	# (starting_node, ending_node, path itself, length of path)
	paths_between_nodes = []

	# Compute shortest paths for each odd_node
	for node in odd_nodes:
		path = bfs(g, node, odd_nodes)
		paths_between_nodes.append((node, path[len(path)-1])) 	


	# Now we can iterate through this set, and make new connections.
	# Once a new connection is made, remove from set
	while len(odd_nodes) > 0:
		
		# Get a random node from the set (and remove this node from the set)
		start_node = odd_nodes.pop()
		path_to_target = bfs(g, start_node, odd_nodes)

		# The node at the beginning of the path is the one
		# we are connection to, so remove that from the set as well
		odd_nodes.remove(path_to_target[0])

		# Now, for every connection in that path, we need to add it to
		# the graph. This is effectively duplicating some edges
		for i in range(len(path_to_target)-1):
			n1 = path_to_target[i]
			n2 = path_to_target[i+1]
			g.add_edge(n1, n2)

	# Graph is now eulerian
"""

# Takes a graph (as a dictionary) and generates the
# Eulerian route (a list of nodes)
def hierholzer(gd, start_node):

	# Keep a stack of nodes we are searching through
	stack = [start_node]

	# Path we will generate and return
	path = []
	
	# While we still have nodes to process
	while len(stack) > 0:

		# Get a node from the stack
		node =  stack[-1]

		# If the node is not in our graph or it has no
		# outgoing edges, than we have already discovered
		# it and we need to backtrack, add it to the list
		# and continue processing the node that came before it
		if node not in gd or len(gd[node]) == 0:
			path.append(node)
			stack.pop()
		
		# If we have not seen this node before, add one of it's
		# connections to the stack and remove this connection from
		# our graph dictionary. We have "discovered" this connection
		# and we don't want to rewalk it.
		else:
			stack.append(gd[node][-1])

			# We have to remove the connection from
			# both parts of the graph!
			other_node = gd[node].pop()
			gd[other_node].remove(node)

	# It's possible that this does not need to be done
	return path

	