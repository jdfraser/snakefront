import bottle
import json
import copy
from pathfinding import ShortestPath
from heatmap import print_heatmap, gen_heatmap

name = 'Snakefront'

def neighbours(c):
	return [[c[0]+1,c[1]],[c[0]-1,c[1]],[c[0],c[1]+1],[c[0],c[1]-1]]

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
	oursnake = None
	for snake in data['snakes']:
		if snake['name'] == name:
			head = snake['coords'][0]
			oursnake = snake

	shortest = []
	move = [0,0]
	for snack in data['food']:
		nextcoord, full_shortest_path = ShortestPath(heatmap, head, snack)
		print full_shortest_path, nextcoord
		if shortest == [] or len(full_shortest_path) < len(shortest):
			shortest = full_shortest_path
			move = nextcoord
	print "Recommend next move to " + str(move)
	taunt = "Booking in progress"
	try: #this was done at 6:20pm okay I was scared
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
	except Exception: 
		pass	
	if move in oursnake['coords']:
		return json.dumps({})
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
		'taunt': taunt
	})


@bottle.post('/end')
def end():
	data = bottle.request.json # {'game_id': 'hairy_cheese'}
	# Flush game state info    


	return json.dumps({}) # Server ignores our response


# Expose WSGI app
application = bottle.default_app()
