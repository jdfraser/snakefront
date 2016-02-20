import copy, math

def print_heatmap(heatmap):
	text = "heatmap:\n"
	for y in range(len(heatmap[0])):
		for xs in heatmap:
			text += "%4d, " % min(int(xs[y]), 9999)
		text += "\n"
	print text, "end heatmap"

def default_heatmap(width, height):
	heatmap = []
	for x in range(width):
		heatmap.append([1]*height)
	return heatmap

def fractal_heat(data, coord, neck, depth, factor):
	if depth <= 0: return
	for x,y in [[0,1],[0,-1],[1,0],[-1,0]]:
		if [x + coord[0], y + coord[1]] == neck: continue # not backwards
		try:
			data[x+coord[0]][y + coord[1]] += factor
		except IndexError:
			continue
		fractal_heat(data, [x+coord[0], y+coord[1]], coord, depth-1, factor/3)

def gen_heatmap(requestdata, our_id='2ca1ab89-620c-4fbe-b876-179013470205', maxturns=6, use_rings=True):
	state = copy.deepcopy(requestdata)
	width = state['width']
	height = state['height']
	final = default_heatmap(width, height)
	for snake in state['snakes']:
		if snake['id'] == our_id:
			oursnake = snake
			break
	oursnakeHead = oursnake['coords'][0]
	oursnakeNeck = oursnake['coords'][1]
	oursnakeLength = len(oursnake['coords'])
	for turn in range(1, maxturns+1):
		heatmap = default_heatmap(width, height)
		snakes = copy.deepcopy(state['snakes'])
		for snake in snakes:
			coords = snake['coords']
			if snake['id'] != our_id:
				# parse heat around the head
				we_are_bigger = (len(coords) < oursnakeLength)
				fractal_heat(heatmap, coords[0], coords[1], turn - we_are_bigger, (turn == 1 and 100 or 33.0))
			# todo: what if they ate food?
			# Now parse the body
			try:
				for i in range(turn): coords.pop()
			except IndexError: pass
			for x,y in coords:
				heatmap[x][y] += 8000
		for x, col in enumerate(heatmap):
			for y, heat in enumerate(col):
				if heat != 1:
					if not use_rings or ((abs(x-oursnakeHead[0]) + abs(y-oursnakeHead[1])) == turn):
						final[x][y] += heat
		final[oursnakeHead[0]][oursnakeHead[1]] = 9998
		final[oursnakeNeck[0]][oursnakeNeck[1]] = 9998

	return final
