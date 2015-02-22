#!/usr/bin/python

import networkx as nx



#Heatmap is an array of the board, with higher values being less safe.
#Headpos is the [column, row] of the snake head.
#Target is the [column, row] of the target.

#RETURNS a tuple: the position of our next move, the shortest path to the target
def ShortestPath(HeatMap, HeadPos, Target):
	Height = len(HeatMap[0])
	Width = len(HeatMap)
	G = nx.Graph()

	G.add_nodes_from(range(0, Height*Width))
	#print G.number_of_nodes()

	#Add vertical edges
	for column in range(0, Width):
		for row in range(0, Height-1):
			cur = column*Height + row
			next = cur + 1
			weight = HeatMap[column][row] + HeatMap[column][row+1]
			#print str(cur) + " Add edge between [" + str(column) + "][" + str(row) + "] and [" + str(column) + "][" + str(row+1) + "], weight=" + str(weight)
			G.add_edge(cur, next)
			G[cur][next]['weight'] = weight

	#Add horizontal edges
	for row in range(0, Height):
		for column in range(0, Width-1):
			cur = column*Height + row
			next = cur + Height
			weight = HeatMap[column][row] + HeatMap[column+1][row]
			#print str(next) + " Add edge between [" + str(column) + "][" + str(row) + "] and [" + str(column+1) + "][" + str(row) + "], weight=" + str(weight)
			G.add_edge(cur, next)
			G[cur][next]['weight'] = weight

	Path = nx.shortest_path(G, source = HeadPos[0]*Height+HeadPos[1], target=Target[0]*Height+Target[1], weight='weight')
	#print Path
	return [Path[1] // Height, Path[1] % Height], Path
			



#print ShortestPath([[0, 5], [1, 2], [3, 3]], [0,0], [2,1])
