class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.walls = [1,1,1,1]
		self.visited = False
