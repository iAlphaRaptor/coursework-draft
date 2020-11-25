import pygame
pygame.init()

class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, fontSize, textColour, activeBoxColour, passiveBoxColour):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.fontSize = fontSize
        self.textColour = textColour
        self.activeBoxColour = activeBoxColour
        self.passiveBoxColour = passiveBoxColour
        self.active = False

        self.textFont = pygame.font.Font("Fonts/numberFont.ttf", self.fontSize)
        self.rawText = ""
        self.renderedText = self.textFont.render(self.rawText, False, self.textColour)

        self.image = pygame.Surface([self.width, self.textFont.size("A")[0]+6])
        self.image.fill(self.passiveBoxColour)
        self.image.blit(self.renderedText, (5, 2))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateBox(self):
        self.renderedText = self.textFont.render(self.rawText, False, self.textColour)
        
        self.image.fill(self.activeBoxColour if self.active else self.passiveBoxColour)
        self.image.blit(self.renderedText, (5, 2))
        

    def isClicked(self, mousex, mousey):
        if self.rect.collidepoint(mousex, mousey):
            self.active = True
        else:
            self.active = False
        self.updateBox()

    def enterText(self, char):
        if char == pygame.K_BACKSPACE:
            self.rawText = self.rawText[:-1]
        else:
            self.rawText += chr(char)
        self.updateBox()

