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
		data[x+coord[0]][y + coord[1]] += factor
		fractal_heat(data, [x+coord[0], y+coord[1]], coord, depth-1, factor/3)

def gen_heatmap(movedata, name='Snakefront-test'):
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


