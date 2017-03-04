import bottle
import os
import json
import copy
import random
import time

import pathfinding
from heatmap import print_heatmap, gen_heatmap
import util

name = 'camel_Snake'
snake_id = ''

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
		'head_url': 'https://demo.checkfront.com/images/checky.png',
		'head_type': 'smile',
		'tail_type': 'fat-rattle',
		'taunt': taunt
	}


@bottle.post('/move')
def move():
	print "\n\n"
	time_start_request = time.clock()
	data = bottle.request.json

	find_our_snake(data)
	# print(data) # Uncomment this to save a full game state

	with util.TimerPrint("Heatmap Time"):
		heatmap = gen_heatmap(data)
	with util.TimerPrint("Graph Time"):
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

	print "\nFull Request Time:", str(round((time.clock() - time_start_request) * 1000, 3)) + "ms"
	return response

def get_move(data, head, heatmap, graph):
	# try different algorithms and pick our favourite one

	idle_move, idle_cost = idle(data, head, heatmap, graph)
	food_move, food_cost = food(data, head, heatmap, graph)
	follow_move, follow_cost = follow(data, head, heatmap, graph)
	print "follow", follow_cost, "idle", idle_cost, "food", food_cost

	longestSnakeID = ''
	longestSnakeLength = 0
	for snake in data['snakes']:
		if snake['id'] != snake_id and len(snake['coords']) > longestSnakeLength:
			longestSnakeLength = len(snake['coords'])
			longestSnakeID = snake['id']

	move_name = ''

	if(int(data['oursnake']['health_points']) < 25 and food_cost < 100):
		move = food_move
		move_name = 'food'
	elif(int(data['oursnake']['health_points']) < 50 and food_cost < 70):
		move = food_move
		move_name = 'food'
	elif((longestSnakeLength + 2) >= len(data['oursnake']['coords']) and food_cost < 40):
		move = food_move
		move_name = 'food'
	elif(follow_cost < 9000):
		move = follow_move
		move_name = 'follow'
	elif(idle_cost < 100):
		move = idle_move
		move_name = 'idle'
	else:
		move = move_idle_dumb(data, head, heatmap, graph)
		move_name = 'default'

	print "Recommend next move", move_name, get_direction_from_target_headpos(head, move), str(move)

	return move

	# Running out of options... find the longest path

	# Worst case scenario: Go 1 square in a direction that doesn't immediately kill it

def food(data, head, heatmap, graph):
	move = [0,0]
	shortest = []
	cost = 9995
	for snack in data['food']:
		pathdata = pathfinding.cheapest_path(graph, heatmap, head, snack)
		print "Food idea: ", pathdata
		nextcoord = pathdata['nextPos']
		full_shortest_path = pathdata['path']
		heat = pathdata['cost']
		if heat < cost:
			shortest = full_shortest_path
			move = nextcoord
			cost = heat
	return move, cost

def idle(data, head, heatmap, graph):
	oursnake = data['oursnake']['coords']
	if(len(oursnake) == 0):
		return False, 9995 #didn't find our snake, bail

	target = oursnake[-1]
	if(target == head):
		return False, 9995

	pathdata = pathfinding.cheapest_path(graph, heatmap, head, target)
	move = pathdata['nextPos']
	cost = pathdata['cost']
	return move, cost

# Follow other snakes' tails if we're right next to one
def follow(data, head, heatmap, graph):
	target = False

	for snake in data['snakes']:
		snake_tail = snake['coords'][-1]
		if dist(head, snake_tail) == 1:
			target = snake_tail

	if not target:
		#No tails nearby
		return False, 9995

	pathdata = pathfinding.cheapest_path(graph, heatmap, head, target)
	move = pathdata['nextPos']
	cost = pathdata['cost']
	return move, cost

def move_idle_dumb(data, head, heatmap, graph):
	left_pathdata = pathfinding.cheapest_path(graph, heatmap, head, [max(0, head[0] - 1), head[1]])
	right_pathdata = pathfinding.cheapest_path(graph, heatmap, head, [min(len(heatmap)-1, head[0] + 1), head[1]])
	up_pathdata = pathfinding.cheapest_path(graph, heatmap, head, [head[0], max(0, head[1] - 1)])
	down_pathdata = pathfinding.cheapest_path(graph, heatmap, head, [head[0], min(len(heatmap[0])-1, head[1] + 1)])

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
		nextmove = 'down'
	elif move[1] < head[1]:
		nextmove = 'up'
	elif move[0] > head[0]:
		nextmove = 'right'
	elif move[0] < head[0]:
		nextmove = 'left'
	else:
		print "UHHHH wat are you trying to move to yourself??"
		nextmove = 'left'
	return nextmove

def find_our_snake(request_data):
	global snake_id
	snake_id = request_data['you']
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

def dist(a, b):
	return abs(b[0] - a[0]) + abs(b[1] - a[1])

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
