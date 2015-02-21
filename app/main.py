import bottle
import json


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
		'name': 'Snakefront',
		'color': '#1E90FF',
		'head_url': 'http://snakefront.herokuapp.com',
		'taunt': 'Online bookings for less!'
	})

def simulate(state):
	#modify state
	pass

def gen_heatmap(movedata):
	state = movedata.clone()
	heatmap = []
	height = len(state['board'][0])
	for x in range(len(state['board']):
		heatmap.append([1]*height)
	simulate(state)


@bottle.post('/move')
def move():
	data = bottle.request.json # {'game_id': 'hairy-cheese', 'turn': 1, 'board': <boarddata>, 'snakes': <snakedatas>, 'food': [[1,2],[4,1]]} 
	# <boarddata>: 2d array [x][y] = {'state': 'empty' or 'food' or 'head' or 'body', 'snake': None or 'badsnake'}
	# <snakedata>: [{'url':'http://...', 'color': '#ffffff', 'headurl': 'http://....png', 'name': 'badsnake', 'taunt': 'Hey'}]
	# Do things here!!

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
