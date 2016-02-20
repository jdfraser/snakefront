import bottle
import os
import json
import copy
from pathfinding import shortest_path
from heatmap import print_heatmap, gen_heatmap

name = 'Snakeoverflow'
snake_id = '2ca1ab89-620c-4fbe-b876-179013470205'

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

	state = get_state()
	heatmap = gen_heatmap(data, snake_id)
	print_heatmap(heatmap)

	oursnake = None
	for snake in data['snakes']:
		if snake['id'] == snake_id:
			head = snake['coords'][0]
			oursnake = snake

	shortest = []
	move = [0,0]
	taunt = "Booking in progress"

	if state == 'food':
		for snack in data['food']:
			nextcoord, full_shortest_path = ShortestPath(heatmap, head, snack)
			print full_shortest_path, nextcoord
			if shortest == [] or len(full_shortest_path) < len(shortest):
				shortest = full_shortest_path
				move = nextcoord
		print "Recommend next move to " + str(move)
	elif state == 'aggressive':
	    pass
	elif state == 'idle':
	    pass

	"""
	#this was done at 6:20pm okay I was scared
	for snake in data['snakes']:
	    if snake['name'] != name and move in neighbours(snake['coords'][0]):
	        taunt = "Get booked!"
	        if len(snake['coords']) >= len(oursnake['coords']):
	            #ahh they're bigger run away
	            taunt = "RUN"
	            if move[1] > head[1]:
	                move[1] = head[1]
	                move[0] = head[0] - 1
	            elif move[1] < head[1]:
	                move[1] = head[1]
	                move[0] = head[0] + 1
	            elif move[0] < head[0]:
	                move[0] = head[0]
	                move[1] = head[1] + 1
	            elif move[0] > head[0]:
	                move[0] = head[0]
	                move[1] = head[1] - 1
	        break
	"""

	if move in oursnake['coords']:
	    pass #TODO: WTF DON'T MOVE INTO OURSELF!!

	return {
		'move': get_direction_from_target_headpos(head, move),
		'taunt': 'battlesnake-python!'
	}

def get_state():
	return 'food'

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
