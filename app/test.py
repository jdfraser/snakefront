#!/usr/bin/python

import heatmap as hm

#heatmap = hm.default_heatmap(20,20)
#main.fractal_heat(heatmap, [5,6], [5,7], 4, 33)


data = {'snakes': [
	{'name': 'Snakefront-test', 'coords': [[4,5],[4,6],[4,7]]},
	{'name': 'boop', 'coords': [[14,7],[14,6],[14,5],[14,4]]},
	{'name': 'test', 'coords': [[5,6],[5,7],[5,8],[6,8],[7,8]]}
], 'board': []}
data['board'] = [[0]*20]*20

heatmap = hm.gen_heatmap(data, use_rings=False)
hm.print_heatmap(heatmap)



print "k"
