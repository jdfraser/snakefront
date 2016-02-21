#!/usr/bin/python

import networkx as nx


#HOW TO USE:
#	Graph = pathfinding.graphify(HeatMap)
#Then run:
#	pathfinding.cheapest_path(Graph, HeightOfPlayArea, HeadPos, TargetPos)
#This returns a dict, see below for names/details



#Heatmap is an array of the board, with higher values being less safe.
#Headpos is the [column, row] of the snake head.

#RETURNS a networkx graph
def graphify(HeatMap):
	Height = len(HeatMap[0])
	Width = len(HeatMap)
	G = nx.Graph()

	G.add_nodes_from(range(0, Height*Width))
	print "Num nodes: " + str(G.number_of_nodes())

	#Add vertical edges
	for column in range(0, Width):
		for row in range(0, Height-1):
			cur = column*Height + row
			next = cur + 1
			weight = HeatMap[column][row] + HeatMap[column][row+1]
			print str(cur) + " Add edge between [" + str(column) + "][" + str(row) + "] and [" + str(column) + "][" + str(row+1) + "], weight=" + str(weight)
			G.add_edge(cur, next)
			G[cur][next]['weight'] = weight

	#Add horizontal edges
	for row in range(0, Height):
		for column in range(0, Width-1):
			cur = column*Height + row
			next = cur + Height
			weight = HeatMap[column][row] + HeatMap[column+1][row]
			print str(next) + " Add edge between [" + str(column) + "][" + str(row) + "] and [" + str(column+1) + "][" + str(row) + "], weight=" + str(weight)
			G.add_edge(cur, next)
			G[cur][next]['weight'] = weight
	print G.edges()

	return G




def cheapest_path(G, Height, HeadPos, TargetPos):
	Path = nx.shortest_path(G, source = HeadPos[0]*Height+HeadPos[1], target=TargetPos[0]*Height+TargetPos[1], weight='weight')
	PosOfNextMove = [Path[1] // Height, Path[1] % Height]
	weight = 0
	for i in range(1, len(Path)-1): #TODO: make sure short paths won't break
		weight += G[Path[i]][Path[i+1]]['weight'] #Get weight of move
	return {
		"path" : Path,
		"length" : len(Path),
		"nextPos" : PosOfNextMove,
		"cost" : weight
	}



G = graphify([[0, 5], [1, 2], [3, 3]])
#print cheapest_path(G, [0,0], [2,1])
