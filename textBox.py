import pygame, button
pygame.init()

alphaNumeric = [x for x in range(pygame.K_a, pygame.K_z + 1)] + [y for y in range(pygame.K_0, pygame.K_9 + 1)]

class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, fontSize, textColour, activeBoxColour, passiveBoxColour, checkBoxColour, checkTextColour, variableToChange):
        super().__init__()

        self.fontSize = fontSize
        self.textFont = pygame.font.Font("Fonts/numberFont.ttf", self.fontSize)

        self.x = x
        self.y = y
        self.width = width
        self.height = self.textFont.size("A")[1]+6
        self.textColour = textColour
        self.activeBoxColour = activeBoxColour
        self.passiveBoxColour = passiveBoxColour
        self.checkBoxColour = checkBoxColour
        self.checkTextColour = checkTextColour
        self.variableToChange = variableToChange
        self.active = False

        self.rawText = ""
        self.renderedText = self.textFont.render(self.rawText, False, self.textColour)

        self.checkButton = pygame.sprite.GroupSingle()
        self.checkButton.add(button.EnterButton(self.textFont.size("ENTER")[0]+10, self.height, "ENTER", self.checkTextColour, self.checkBoxColour, self.fontSize, None))

        self.image = pygame.Surface([self.width + self.checkButton.sprite.width + 15, self.height])
        self.transparentColour = (1,1,1) if (self.activeBoxColour != (1,1,1) and self.passiveBoxColour != (1,1,1) and self.textColour != (1,1,1) and self.checkButton.sprite.boxColour != (1,1,1) and self.checkButton.sprite.textColour != (1,1,1)) else (2,2,2)
        self.image.set_colorkey(self.transparentColour)
        self.image.fill(self.transparentColour)

        pygame.draw.rect(self.image, self.passiveBoxColour, (0, 0, self.width, self.height))  ## Draw the main entry box
        self.image.blit(self.renderedText, (5, 2))
        self.checkButton.draw(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateBox(self):
        self.renderedText = self.textFont.render(self.rawText, False, self.textColour)
        
        pygame.draw.rect(self.image, self.activeBoxColour if self.active else self.passiveBoxColour, (0, 0, self.width, self.height))  ## Draw the main entry box
        self.image.blit(self.renderedText, (5, 2))
        self.checkButton.draw(self.image)
        

    def isClicked(self, mousex, mousey):
        if pygame.Rect(0, 0, self.width, self.height).collidepoint(mousex, mousey):
            self.active = True
        elif pygame.Rect(self.width + 10, 0, self.checkButton.sprite.width, self.checkButton.sprite.height).collidepoint(mousex, mousey):
            print("EE")
            self.active = False
            self.variableToChange = [self.rawText]
        else:
            self.active = False
        self.updateBox()

    def changeVariable(self):
        pass

    def enterText(self, char):
        if char == pygame.K_BACKSPACE:
            self.rawText = self.rawText[:-1]
        elif char in alphaNumeric:
            self.rawText += chr(char)
        self.updateBox()

