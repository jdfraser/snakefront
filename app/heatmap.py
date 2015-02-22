import copy

def print_heatmap(heatmap):
	text = "heatmap:\n"
	for y in range(len(heatmap[0])):
		for xs in heatmap:
			text += "%3d, " % int(xs[y])
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
		try:
			data[x+coord[0]][y + coord[1]] += factor
		except IndexError:
			continue
		fractal_heat(data, [x+coord[0], y+coord[1]], coord, depth-1, factor/3)

def gen_heatmap(movedata, name='Snakefront-test', maxturns=7, userings=True):
	state = copy.deepcopy(movedata)
	width = len(state['board'])
	height = len(state['board'][0])
	final = default_heatmap(width, height)
	for snake in state['snakes']:
		if snake['name'] == name:
			oursnake = snake
			break
	oursnakeHead = oursnake['coords'][0]
	oursnakeNeck = oursnake['coords'][1]
	oursnakeLength = len(oursnake['coords'])
	for turn in range(1, maxturns):
		heatmap = default_heatmap(width, height)
		snakes = copy.deepcopy(state['snakes'])
		for snake in snakes:
			coords = snake['coords']
			if snake['name'] != name and len(coords) >= oursnakeLength:
				# parse heat around the head
				fractal_heat(heatmap, coords[0], coords[1], turn, 33.0)
			# todo: what if they ate food?
			# Now parse the body
			try: 
				for i in range(turn): coords.pop()
			except IndexError: pass
			for x,y in snake['coords']:
				heatmap[x][y] += 10000
		for x, col in enumerate(heatmap):
			for y, heat in enumerate(col):
				if heat != 1:
					if not userings or (((x-oursnakeHead[0]) + (y-oursnakeHead[1])) == turn): 
						final[x][y] += heat
		final[oursnakeHead[0]][oursnakeHead[1]] = 99999
		final[oursnakeNeck[0]][oursnakeNeck[1]] = 99999

	return final


