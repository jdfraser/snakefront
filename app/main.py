import bottle
import os
import json
import copy
import random
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
	rand = random.randint(0, 2)
	taunts = ['0xA9FF33', '0xFFFFFF', '0xA28F3C']
	taunt = taunts[rand]
	return {
		'name': name,
		'color': '#1E90FF',
		'head_url': 'https://github.com/Nebual/snakefront/blob/master/snake.png?raw=true',
		'taunt': taunt
	}


@bottle.post('/move')
def move():
	data = bottle.request.json

	find_our_snake(data)

	heatmap = gen_heatmap(data, snake_id)
	graph = pathfinding.graphify(heatmap)
	print_heatmap(heatmap)

	shortest = []
	move = [0,0]

	rand = random.randint(0, 2)
	taunts = ['0xA9FF33', '0xFFFFFF', '0xA28F3C']
	taunt = taunts[rand]

	move = get_move(data, data['ourhead'], heatmap, graph)

	if move in data['oursnake']['coords']:
		pass #TODO: WTF DON'T MOVE INTO OURSELF!!

	response = {
		'move': get_direction_from_target_headpos(data['ourhead'], move)
	}
	if random.randint(0, 10) == 0:
		response['taunt'] = taunt
	return response

def get_move(data, head, heatmap, graph):
	# try different algorithms and pick our favourite one

	coin_move, coin_cost = move_coin(data, head, heatmap, graph)
	idle_move, idle_cost = idle(data, head, heatmap, graph)
	food_move, food_cost = food(data, head, heatmap, graph)
	print "coin", coin_cost, "idle", idle_cost, "food", food_cost

	longestSnakeID = ''
	longestSnakeLength = 0
	for snake in data['snakes']:
		if snake['id'] != snake_id and len(snake['coords']) > longestSnakeLength:
			longestSnakeLength = len(snake['coords'])
			longestSnakeID = snake['id']

	if coin_cost < 50 and int(data['oursnake']['health']) > 25:
		return coin_move
	if(int(data['oursnake']['health']) < 25 and food_cost < 100):
		return food_move
	if(int(data['oursnake']['health']) < 50 and food_cost < 70):
		return food_move
	if((longestSnakeLength + 2) >= len(data['oursnake']['coords']) and food_cost < 40):
		return food_move
	if(idle_cost < 100):
		return idle_move

	# Running out of options... find the longest path


	# Worst case scenario: Go 1 square in a direction that doesn't immediately kill it
	return move_idle_dumb(data, head, heatmap, graph)

def move_coin(data, head, heatmap, graph):
	if 'gold' in data and len(data['gold']):
		nextcoord, full_shortest_path, cost = pathfinding.cheapest_path(graph, len(heatmap[0]), head, data['gold'][0])
		min_coin_distance = (5 + data['oursnake'].get('gold', 0)*2) # Allow further distances as our bank account increases
		if len(full_shortest_path) < min_coin_distance:
			return nextcoord, cost
	return False, 9995

def food(data, head, heatmap, graph):
	move = [0,0]
	shortest = []
	shortestHeat = 9995
	for snack in data['food']:
		pathdata = pathfinding.cheapest_path(graph, len(heatmap[0]), head, snack)
		print "Food idea: ", pathdata
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
	oursnake = data['oursnake']['coords']
	if(len(oursnake) == 0):
		return False, 9995 #didn't find our snake, bail
	target = oursnake[-1]
	if(target == head):
		return False, 9995

	pathdata = pathfinding.cheapest_path(graph, len(heatmap[0]), head, target)
	move = pathdata['nextPos']
	cost = pathdata['cost']
	return move, cost

def move_idle_dumb(data, head, heatmap, graph):
	left_pathdata = pathfinding.cheapest_path(graph, len(heatmap[0]), head, [head[0] - 1, head[1]])
	right_pathdata = pathfinding.cheapest_path(graph, len(heatmap[0]), head, [head[0] + 1, head[1]])
	up_pathdata = pathfinding.cheapest_path(graph, len(heatmap[0]), head, [head[0], head[1] - 1])
	down_pathdata = pathfinding.cheapest_path(graph, len(heatmap[0]), head, [head[0], head[1] + 1])

	smallest = min(left_pathdata['cost'], right_pathdata['cost'], up_pathdata['cost'], down_pathdata['cost'])
	if smallest == left_pathdata['cost']:
		return left_pathdata['nextPos']
	if smallest == right_pathdata['cost']:
		return right_pathdata['nextPos']
	if smallest == up_pathdata['cost']:
		return up_pathdata['nextPos']
	if smallest == down_pathdata['cost']:
		return down_pathdata['nextPos']

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

def find_our_snake(request_data):
	request_data['oursnake'] = dict()
	request_data['ourhead'] = [0, 0]
	for snake in request_data['snakes']:
		if snake['id'] == snake_id:
			request_data['ourhead'] = snake['coords'][0]
			request_data['oursnake'] = snake

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
