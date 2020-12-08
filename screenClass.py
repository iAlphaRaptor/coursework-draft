import pygame, random, cell, player, mazeRoutines
pygame.init()

class Screen(pygame.sprite.Sprite):
    def __init__(self, SCREENWIDTH, SCREENHEIGHT, bgColour, rawButtons, rawTextBoxes, rawSliders):
        super().__init__()
        self.bgColour = bgColour
        self.rawButtons = rawButtons
        self.rawTextBoxes = rawTextBoxes
        self.rawSliders = rawSliders

        self.image = pygame.Surface([SCREENWIDTH, SCREENHEIGHT])
        self.image.fill(self.bgColour)

        self.rect = self.image.get_rect()

        self.buttons = pygame.sprite.Group()
        for r in self.rawButtons:
            self.buttons.add(r)

        self.textBoxes = pygame.sprite.Group()
        for t in self.rawTextBoxes:
            self.textBoxes.add(t)

        self.sliders = pygame.sprite.Group()
        for s in self.rawSliders:
            self.sliders.add(s)

class MazeScreen(Screen):
    def __init__(self, SCREENWIDTH, SCREENHEIGHT, bgColour, wallColour, wallWidth, difficulty):
        super().__init__(SCREENWIDTH, SCREENHEIGHT, bgColour, [], [], [])

        assert SCREENWIDTH == SCREENHEIGHT, "Screen must be a square"

        self.SCREENWIDTH = SCREENWIDTH
        self.SCREENHEIGHT = SCREENHEIGHT
        self.wallColour = wallColour
        self.wallWidth = wallWidth
        self.difficulty = difficulty
        self.generated = False

        self.players = pygame.sprite.Group()

    def getNeighbours(self, current):
        possibles = []

        n = mazeRoutines.index(self.cells, current.x, current.y+1)
        e = mazeRoutines.index(self.cells, current.x+1, current.y)
        s = mazeRoutines.index(self.cells, current.x, current.y-1)
        w = mazeRoutines.index(self.cells, current.x-1, current.y)

        if n != -1 and not self.cells[n].visited:
            possibles.append(n)
        if e != -1 and not self.cells[e].visited:
            possibles.append(e)
        if s != -1 and not self.cells[s].visited:
            possibles.append(s)
        if w != -1 and not self.cells[w].visited:
            possibles.append(w)

        return possibles

    def updateMaze(self):
        self.image.fill(self.bgColour)
        
        ## Draw the inner walls of the maze            
        for c in self.cells:
            i = c.x * self.cellWidth
            j = c.y * self.cellWidth
            if c.walls[0]:
                pygame.draw.line(self.image, self.wallColour, (i, j), (i+self.cellWidth, j), self.wallWidth)
            if c.walls[1]:
                pygame.draw.line(self.image, self.wallColour, (i+self.cellWidth, j), (i+self.cellWidth, j+self.cellWidth), self.wallWidth)
            if c.walls[2]:
                pygame.draw.line(self.image, self.wallColour, (i, j+self.cellWidth), (i+self.cellWidth, j+self.cellWidth), self.wallWidth)
            if c.walls[3]:
                pygame.draw.line(self.image, self.wallColour, (i, j), (i, j+self.cellWidth), self.wallWidth)

        for player in self.players:
            player.rect.x = (player.gridX * self.cellWidth) + 1
            player.rect.y = (player.gridY * self.cellWidth) + 1

        self.players.draw(self.image)

    def editWalls(self, current, nextCell):
        xDiff = nextCell.x - current.x;
        if xDiff == 1:
            current.walls[1] = 0
            nextCell.walls[3] = 0
        elif xDiff == -1:
            nextCell.walls[1] = 0
            current.walls[3] = 0

        yDiff = nextCell.y - current.y
        if yDiff == 1:
            current.walls[2] = 0
            nextCell.walls[0] = 0
        elif yDiff == -1:
            nextCell.walls[2] = 0
            current.walls[0] = 0

    def generatePlayers(self):
        user = player.Human(random.randint(0, self.dim-1), random.randint(0, self.dim-1), self.cellWidth)
        computerX = random.randint(0, self.dim-1)
        computerY = random.randint(0, self.dim-1)
        while computerX == user.gridX and computerY == user.gridY:
            computerX = random.randint(0, self.dim-1)
            computerY = random.randint(0, self.dim-1)
        computer = player.Computer(computerX, computerY, self.cellWidth)

        self.players.add(user, computer)

    def generateMaze(self):
        self.cellWidth = int(self.SCREENWIDTH / (8 + (2 * self.difficulty)))
        self.cells = []
        for i in range(int(self.SCREENWIDTH / self.cellWidth)):
            for j in range(int(self.SCREENHEIGHT / self.cellWidth)):
                self.cells.append(cell.Cell(j, i))
        self.dim = len(self.cells) ** 0.5

        stack = []
        current = self.cells[0]
        current.visited = True
        stack.append(current)

        while len(stack) > 0:
            possibles = self.getNeighbours(current)
            if len(possibles) == 0:
                current = stack.pop()
            else:
                nextIndex = random.choice(possibles)
                nextCell = self.cells[nextIndex]

                self.editWalls(current, nextCell)
                current = nextCell
                current.visited = True
                stack.append(current)

        self.generated = True
        
        offset = int((self.SCREENWIDTH - (self.cellWidth * (len(self.cells) ** 0.5))) / 2)
        self.image = pygame.transform.scale(self.image, (self.SCREENWIDTH-2*offset, self.SCREENHEIGHT-2*offset)) ## Resize self.image to fit the maze
        self.rect = self.image.get_rect()
        self.rect.x = offset ## Offset the screen so the maze is centered
        self.rect.y = offset

        self.generatePlayers() ## Create two player objects
        self.updateMaze() ## Draw the maze to self.image

    def cellIndex(self, x, y):
        return int((self.dim * y) + x)

    def moveUser(self, key):
        player = self.players.sprites()[0]
        gridX = player.gridX
        gridY = player.gridY

        if key == pygame.K_w:
            if not self.cells[self.cellIndex(gridX, gridY)].walls[0]:
                player.move("n")
        elif key == pygame.K_d:
            if not self.cells[self.cellIndex(gridX, gridY)].walls[1]:
                player.move("e")
        elif key == pygame.K_s:
            if not self.cells[self.cellIndex(gridX, gridY)].walls[2]:
                player.move("s")
        elif key == pygame.K_a:
            if not self.cells[self.cellIndex(gridX, gridY)].walls[3]:
                player.move("w")

    def moveComputer(self):
        pass

