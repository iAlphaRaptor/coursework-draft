import pygame, random, cell
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
    def __init__(self, SCREENWIDTH, SCREENHEIGHT, bgColour, wallColour, wallWidth, cellWidth):
        super().__init__(SCREENWIDTH, SCREENHEIGHT, bgColour, [], [], [])

        self.wallColour = wallColour
        self.wallWidth = wallWidth
        self.cellWidth = cellWidth
        assert SCREENWIDTH % self.cellWidth == 0, "Cell width must be a factor of SCREENWIDTH"
        assert SCREENHEIGHT % self.cellWidth == 0, "Cell width must be a factor of SCREENHEIGHT"

        self.cells = []
        for i in range(int(SCREENWIDTH / self.cellWidth)):
            for j in range(int(SCREENHEIGHT / self.cellWidth)):
                self.cells.append(cell.Cell(j, i))

        self.createMaze()

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

    def createMaze(self):
        stack = []
        current = self.cells[0]
        current.visited = True
        stack.append(current)

        while len(stack) > 0:
            possibles = current.getPossibles(self.cells)
            if len(possibles) == 0:
                current = stack.pop()
            else:
                nextIndex = random.choice(possibles)
                nextCell = self.cells[nextIndex]

                self.editWalls(current, nextCell)
                current = nextCell
                current.visited = True
                stack.append(current)

