import pygame
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, gridX, gridY, width):
        super().__init__()

        self.x = (gridX * width)
        self.y = (gridY * width)
        self.gridX = gridX
        self.gridY = gridY
        self.width = width - 1

        self.image = pygame.Surface([self.width, self.width])

        self.rect = self.image.get_rect()

    def move(self, direction):
        if direction == "n":
            self.gridY -= 1
        elif direction == "e":
            self.gridX += 1
        elif direction == "w":
            self.gridX -= 1
        elif direction == "s":
            self.gridY += 1


class Human(Player):
    def __init__(self, gridX, gridY, width):
        super().__init__(gridX, gridY, width)
        
        self.COLOUR = (255, 200, 0)

        self.image.fill(self.COLOUR)


class Computer(Player):
    def __init__(self, gridX, gridY, width):
        super().__init__(gridX, gridY, width)
        
        self.COLOUR = (0, 200, 255)

        self.image.fill(self.COLOUR)
