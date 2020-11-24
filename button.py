import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, goTo):
        super().__init__()

        self.image = pygame.Surface([100, 100])
        self.image.fill((100, 100, 100))

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

        self.goTo = goTo

    def isClicked(self, mousex, mousey):
        if self.rect.collidepoint(mousex, mousey):
            return self.goTo
        return False
