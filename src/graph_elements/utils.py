from graph_elements.graph import Graph
from math import radians, cos, sin, asin, sqrt

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