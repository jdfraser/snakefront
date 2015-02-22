import bottle
import json
import copy
from pathfinding import ShortestPath

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

def simulate(state):
	#modify state
	pass

def print_heatmap(heatmap):
	text = "heatmap:\n"
	for y in range(len(heatmap[0])):
		for xs in heatmap:
			text += str(xs[y]) + ", "
		text += "\n"
	print text, "end heatmap"

def default_heatmap(width, height):
	heatmap = []
	for x in range(width):
		heatmap.append([1]*height)
	return heatmap

def fractal_heat(data, coord, neck, depth, factor):
	if depth == 0: return
	for x,y in [[0,1],[0,-1],[1,0],[-1,0]]:
		if [x + coord[0], y + coord[1]] == neck: continue # not backwards
		data[x+coord[0]][y + coord[1]] += factor
		fractal_heat(data, [x+coord[0], y+coord[1]], coord, depth-1, factor/3)

def gen_heatmap(movedata):
	global name
	state = copy.deepcopy(movedata)
	width = len(state['board'])
	height = len(state['board'][0])
	final = default_heatmap(width, height)

	for turn in range(4):
		heatmap = default_heatmap(width, height)
		snakes = copy.deepcopy(state['snakes'])
		oursnake = None
		oursnakeHead = [0,0]
		for snake in snakes:
			coords = snake['coords']
			if snake['name'] != name:
				headpos = coords[0]
				# parse heat around the head
				fractal_heat(heatmap, headpos, coords[1], turn+1, 33.0)
			else:
				oursnake = snake
				oursnakeHead = snake['coords'][0]
			# todo: what if they ate food?
			# Now parse the body
			try: 
				for i in range(turn+1): coords.pop()
			except IndexError: pass
			for x,y in snake['coords']:
				heatmap[x][y] += 100	
		#ring = []
		#for x in range(-(turn+1), (turn+1)+1):
		#	for y in range(-(turn+1), (turn+1)+1):
		#		if (x + y) == (turn+1): ring.append([x + oursnakeHead,y + oursnakeHead]) # add any combination thats distance == our turn #
		for x, col in enumerate(heatmap):
			for y, heat in enumerate(col):
				#if heat != 1 and ((x-oursnakeHead[0]) + (y-oursnakeHead[1])) == (turn+1): 
				final[x][y] += heat

	return final


@bottle.post('/move')
def move():
	data = bottle.request.json # {'game_id': 'hairy-cheese', 'turn': 1, 'board': <boarddata>, 'snakes': <snakedatas>, 'food': [[1,2],[4,1]]} 
	# <boarddata>: 2d array [x][y] = {'state': 'empty' or 'food' or 'head' or 'body', 'snake': None or 'badsnake'}
	# <snakedata>: [{'url':'http://...', 'color': '#ffffff', 'headurl': 'http://....png', 'name': 'badsnake', 'taunt': 'Hey'}]
	# Do things here!!


	text = "heatmap:\n"
	heatmap = gen_heatmap(data)
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
