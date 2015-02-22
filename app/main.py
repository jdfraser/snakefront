import bottle
import json
import copy
from pathfinding import ShortestPath
from heatmap import print_heatmap, gen_heatmap

name = 'Snakefront-test'

@bottle.get('/')
def index():
	return """
		<a href="https://github.com/sendwithus/battlesnake-python">
			gonna leave this default for now, don't want people spying :D
		</a>
	"""
@bottle.post('/start')
def start():
	data = bottle.request.json

	return json.dumps({
		'name': name,
		'color': '#1E90FF',
		'head_url': 'https://github.com/Nebual/snakefront/blob/master/snake.png?raw=true',
		'taunt': 'Online bookings for less!'
	})

@bottle.post('/move')
def move():
	data = bottle.request.json # {'game_id': 'hairy-cheese', 'turn': 1, 'board': <boarddata>, 'snakes': <snakedatas>, 'food': [[1,2],[4,1]]} 
	# <boarddata>: 2d array [x][y] = {'state': 'empty' or 'food' or 'head' or 'body', 'snake': None or 'badsnake'}
	# <snakedata>: [{'url':'http://...', 'color': '#ffffff', 'headurl': 'http://....png', 'name': 'badsnake', 'taunt': 'Hey'}]
	# Do things here!!


	text = "heatmap:\n"
	heatmap = gen_heatmap(data, name)
	for y in range(len(heatmap[0])):
		for xs in heatmap:
			text += str(xs[y]) + ", "
		text += "\n"
	print text, "end heatmap"
	
	for snake in data['snakes']:
		if snake['name'] == name:
			head = snake['coords'][0]
	move = ShortestPath(heatmap, head, [0,0])
	#move = [0,0]
	print "Recommend next move to " + str(move)


	#move = getpath()
	move = [head[0] +1, head[1]]
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
	
	return json.dumps({
		'move': nextmove,
		'taunt': 'Booking in progress'
	})


@bottle.post('/end')
def end():
	data = bottle.request.json # {'game_id': 'hairy_cheese'}
	# Flush game state info    


	return json.dumps({}) # Server ignores our response


# Expose WSGI app
application = bottle.default_app()
