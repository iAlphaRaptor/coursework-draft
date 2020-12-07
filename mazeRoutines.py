def index(data, x, y):
		if x < 0 or y < 0 or x > (len(data) ** 0.5) - 1 or y > (len(data) ** 0.5) - 1:
			return -1
		return int(x + y * (len(data) ** 0.5))

def getNeighbours(current, cells):
		possibles = []

		n = index(cells, current.x, current.y+1)
		e = index(cells, current.x+1, current.y)
		s = index(cells, current.x, current.y-1)
		w = index(cells, current.x-1, current.y)

		if n != -1 and not cells[n].visited:
			possibles.append(n)
		if e != -1 and not cells[e].visited:
			possibles.append(e)
		if s != -1 and not cells[s].visited:
			possibles.append(s)
		if w != -1 and not cells[w].visited:
			possibles.append(w)

		return possibles

def h(n, goal):
	""" Estimates the cost to reach a goal node from node n using Pythagoras' Theorem.
	Used as the heuristic in the below A* algorithm.
	'n' and 'goal' are tuples of co-ordinates (x,y). """

	b = abs(n[0] - goal[0])
	c = abs(n[1] - goal[1])

	a = ((b ** 2) + (c ** 2)) ** 0.5   ## Pythagoras
	return a


def aStar(maze, start, goal):
	""" Returns a list of directions to get from 'start' to 'end'.
	'start' and 'goal' are tuples of co-ordinates (x,y). """

	openSet = [start]
	cameFrom = [None for x in range(len(maze))]

	fScore = [0 for x in range(len(maze))]
	gScore = [0 for x in range(len(maze))]

	fScore[index(maze, start[0], start[1])] = h(start, goal)
	gScore[index(maze, start[0], start[1])] = 0

	while openSet:
		current = openSet[fScore.index(min(fScore))]
		if current == goal:
			return True

		openSet.pop(current)
		neighbours = getNeighbours(current, maze)
		for neighbour in neighbours:
			mazeIndex = maze.index(neighbour)
			if gScore[maze.index(current)] < gScore[mazeIndex]:
				cameFrom[mazeIndex] = current
				gScore[mazeIndex] = gScore[maze.index(current)]
				fScore[mazeIndex] = gScore[mazeIndex] + h("XXX", goal)
				### Need to work out the (i, j), given the current index of neighbour

aStar([1,1,1,1,1,1,1], (1,2), (1, 2))
