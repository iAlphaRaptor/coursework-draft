import pygame, button
pygame.init()

class Screen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([950,950])
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()

        self.buttons = pygame.sprite.Group()
        self.buttons.add(button.Button(2))
