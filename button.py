import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, textColour, boxColour, fontSize, fitBox=True, width=False, height=False):
        super().__init__()
        
        self.x = x
        self.y = y
        self.text = text
        self.textColour = textColour
        self.boxColour = boxColour
        self.fontSize = fontSize
        self.fitBox = fitBox

        wordFont = pygame.font.Font("Fonts/numberFont.ttf", self.fontSize)

        self.renderedText = wordFont.render(self.text, False, self.textColour)

        if self.fitBox:
            textWidth, textHeight = wordFont.size(self.text)
            self.width = textWidth + 6
            self.height = textHeight + 10
        else:
            self.width = width
            self.height = height

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.boxColour)
        self.image.blit(self.renderedText, (5, 2))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

class ScreenButton(Button):
    def __init__(self, x, y, text, textColour, boxColour, fontSize, goTo, fitBox=True, width=False, height=False):
        super().__init__(x, y, text, textColour, boxColour, fontSize, fitBox, width, height)

        self.goTo = goTo

    def isClicked(self, mousex, mousey):
        if self.rect.collidepoint(mousex, mousey):
            return self.goTo


class EnterButton(Button):
    def __init__(self, x, y, text, textColour, boxColour, fontSize, fitBox=True, width=False, height=False):
        super().__init__(x, y, text, textColour, boxColour, fontSize, fitBox, width, height)

    def isClicked(self, mousex, mousey):
        if self.rect.collidepoint(mousex, mousey):
            return self.goTo
