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
    def __init__(self, SCREENWIDTH, SCREENHEIGHT, bgColour, wallColour, wallWidth, difficulty):
        super().__init__(SCREENWIDTH, SCREENHEIGHT, bgColour, [], [], [])

        assert SCREENWIDTH == SCREENHEIGHT, "Screen must be a square"

        self.SCREENWIDTH = SCREENWIDTH
        self.SCREENHEIGHT = SCREENHEIGHT
        self.wallColour = wallColour
        self.wallWidth = wallWidth
        self.difficulty = difficulty
        self.generated = False

    def drawMaze(self, offset):
        ## Draw the borders of the maze
        pygame.draw.line(self.image, self.wallColour, (0, 0), (self.SCREENWIDTH, 0), self.wallWidth)
        pygame.draw.line(self.image, self.wallColour, (self.SCREENWIDTH-self.wallWidth, 0), (self.SCREENWIDTH-self.wallWidth, self.SCREENHEIGHT), self.wallWidth)
        pygame.draw.line(self.image, self.wallColour, (0, 0), (0, self.SCREENHEIGHT), self.wallWidth)
        pygame.draw.line(self.image, self.wallColour, (0, self.SCREENHEIGHT-self.wallWidth), (self.SCREENWIDTH, self.SCREENHEIGHT-self.wallWidth), self.wallWidth)

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

    def generateMaze(self):
        self.cellWidth = int(self.SCREENWIDTH / (8 + (2 * self.difficulty)))
        self.cells = []
        for i in range(int(self.SCREENWIDTH / self.cellWidth)):
            for j in range(int(self.SCREENHEIGHT / self.cellWidth)):
                self.cells.append(cell.Cell(j, i))

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

        self.generated = True
        offset = (self.SCREENWIDTH - (self.cellWidth * (len(self.cells) ** 0.5))) / 2
        self.drawMaze(offset) ## Draw the maze to self.image

