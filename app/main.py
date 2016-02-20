import bottle
import json
import copy
from pathfinding import shortest_path
from heatmap import print_heatmap, gen_heatmap

#retrieve and parse data from REST API
state = get_state()
heatmap = gen_heatmap(movedata)

if state == 'food':
	get_food()
elif state == 'idle':

elif state == 'aggressive':

def get_state():
	return 'food'
	
def get_food():
	#determine target here
	nextcoord, full_shortest_path = shortest_path(heatmap, headpos, target)
