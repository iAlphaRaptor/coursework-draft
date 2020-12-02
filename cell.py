class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.walls = [1,1,1,1]
		self.visited = False

	def index(self, data, x, y):
		if x < 0 or y < 0 or x > (len(data) ** 0.5) - 1 or y > (len(data) ** 0.5) - 1:
			return -1
		return int(x + y * (len(data) ** 0.5))

	def getPossibles(self, cells):
		possibles = []

		n = self.index(cells, self.x, self.y+1)
		e = self.index(cells, self.x+1, self.y)
		s = self.index(cells, self.x, self.y-1)
		w = self.index(cells, self.x-1, self.y)

		if n != -1 and not cells[n].visited:
			possibles.append(n)
		if e != -1 and not cells[e].visited:
			possibles.append(e)
		if s != -1 and not cells[s].visited:
			possibles.append(s)
		if w != -1 and not cells[w].visited:
			possibles.append(w)

		return possibles
