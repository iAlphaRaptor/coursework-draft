import pygame, button
pygame.init()

class Screen(pygame.sprite.Sprite):
    def __init__(self, bgColour, rawButtons):
        super().__init__()
        self.bgColour = bgColour
        self.rawButtons = rawButtons

        self.image = pygame.Surface([950,950])
        self.image.fill(self.bgColour)

        self.rect = self.image.get_rect()

        self.buttons = pygame.sprite.Group()
        for r in rawButtons:
        	self.buttons.add(r)
