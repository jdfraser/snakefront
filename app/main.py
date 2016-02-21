import bottle
import os
import json
import copy
import pathfinding
from heatmap import print_heatmap, gen_heatmap

name = 'Snakeoverflow'
snake_id = '2ca1ab89-620c-4fbe-b876-179013470205'
#snake_id = '99194a3a-985c-4423-9929-53235449f029' #delete-snake

#retrieve and parse data from REST API
@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
	head_url = '%s://%s/static/head.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
	)

	return {
	'color': '#00ff00',
	'head': head_url
	}


@bottle.post('/start')
def start():
	data = bottle.request.json

	return {
		'name': name,
		'color': '#1E90FF',
		'head_url': 'https://github.com/Nebual/snakefront/blob/master/snake.png?raw=true',
		'taunt': 'Online bookings for less!'
	}


@bottle.post('/move')
def move():
	data = bottle.request.json
	heatmap = gen_heatmap(data, snake_id)
	graph = pathfinding.graphify(heatmap)
	print_heatmap(heatmap)

	oursnake = None
	for snake in data['snakes']:
		if snake['id'] == snake_id:
			head = snake['coords'][0]
			oursnake = snake

	shortest = []
	move = [0,0]
	taunt = "Booking in progress"

	move = get_move(data, head, heatmap, graph)

	if move in oursnake['coords']:
		pass #TODO: WTF DON'T MOVE INTO OURSELF!!

	return {
		'move': get_direction_from_target_headpos(head, move),
		'taunt': 'battlesnake-python!'
	}

def get_move(data, head, heatmap, graph):
	# try different algorithms and pick our favourite one 
	idle_move, idle_cost = idle(data, head, heatmap, graph)
	food_move, food_cost = food(data, head, heatmap, graph)
	if(idle_move == False):
		return food_move
	smallest_cost = min(idle_cost, food_cost)
	if(idle_cost == smallest_cost):
		return idle_move
	elif(food_cost == smallest_cost):
		return food_move

def food(data, head, heatmap, graph):
	shortest = []
	shortestHeat = 99999
	for snack in data['food']:
		pathdata = pathfinding.cheapest_path(graph, len(heatmap[0]), head, snack)
		nextcoord = pathdata['nextPos']
		full_shortest_path = pathdata['path']
		heat = pathdata['cost']
		if heat < shortestHeat:
			shortest = full_shortest_path
			move = nextcoord
			shortestHeat = heat
	print "Recommend next move to " + str(move)
	return move, shortestHeat 

def idle(data, head, heatmap, graph):
	oursnake = []
	for snake in data['snakes']:
		if snake['id'] == snake_id:
			oursnake = snake['coords']
	if(len(oursnake) == 0):
		return False #didn't find our snake, bail
	target = oursnake[-1]
	if(target == head):
		return False, 99999

	pathdata = pathfinding.cheapest_path(graph, len(heatmap[0]), head, target)
	move = pathdata['nextPos']
	cost = pathdata['cost']
	return move, cost

def get_direction_from_target_headpos(head, move):
	if move[1] > head[1]:
	    nextmove = 'south'
	elif move[1] < head[1]:
	    nextmove = 'north'
	elif move[0] > head[0]:
	    nextmove = 'east'
	elif move[0] < head[0]:
	    nextmove = 'west'
	else:
	    print "UHHHH wat are you trying to move to yourself??"
	    nextmove = 'west'
	return nextmove

@bottle.post('/end')
def end():
	data = bottle.request.json

	# TODO: Do things with data

	return {
		'taunt': 'battlesnake-python!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
