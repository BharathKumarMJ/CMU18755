import networkx as nx
import random
import csv
from random import random
# Generates a graph in two formats, gml and gexf. gexf format is used for
# dynamic network analysis. Outputs are in test.gml and test.gxml
G = nx.DiGraph()

with open('users.csv', 'rb') as user_names:
	users = csv.reader(user_names)
	for row in users:		
		G.add_node(row[0])

with open('connections.csv', 'rb') as user_names:
	users = csv.reader(user_names)
	for row in users:
		user1 = row[0]
		print user1
		user2 = row[1]
		start = row[2].split(".")	
		start[0] = start[0][-7:]
		G.add_edge(user1, user2,start=int(start[0]))

nx.write_gml(G, "test.gml")
nx.write_gexf(G, "test.gexf")

"""
for i in range(nodes):
	G.add_edge(i, (i+1)%nodes)
	G.add_edge(i, (i+2)%nodes)
	if (i-1) < 0:
		G.add_edge(i, (nodes+(i-1))%nodes)
	else:
		G.add_edge(i, (i-1)%nodes)
	if (i-2) < 0:
		G.add_edge(i, (nodes+(i-2))%nodes)
	else:
		G.add_edge(i, (i-2)%nodes)

for i in range(nodes):
	G1 = G.copy()
	for neighbor in G1.neighbors_iter(i):
		if random.randrange(rand_value) == 0:
			new_node = random.randrange(nodes)
			if new_node == i:
				continue
			G.remove_edge(i, neighbor)
			G.add_edge(i, new_node)


nx.write_gml(G, "test.gml")
"""