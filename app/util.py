import time


class Timer:
	def __enter__(self):
		self.start = time.clock()
		return self

	def __exit__(self, *args):
		self.end = time.clock()
		self.interval = self.end - self.start


class TimerPrint(Timer):
	def __init__(self, msg="Timer"):
		self.msg = msg

	def __exit__(self, *args):
		Timer.__exit__(self)
		print self.msg + ":", str(round(self.interval * 1000, 3)) + "ms"


def is_valid_move(possible_move, data):

	if possible_move == data['oursnake']['coords'][-1]:
		#it's fine to chase our tail
		return True

	if possible_move in data['oursnake']['coords']:
		return False

	valid_move = False
	for x in range(data['width']):
		for y in range(data['height']):
			if possible_move[0] == x and possible_move[1] == y:
				valid_move = True

	return valid_move

def dist(a, b):
	return abs(b[0] - a[0]) + abs(b[1] - a[1])


def bad_move():
	return False, 9995
