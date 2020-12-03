import pygame
pygame.init()

alphaNumeric = [x for x in range(pygame.K_a, pygame.K_z + 1)] + [y for y in range(pygame.K_0, pygame.K_9 + 1)]

class Widget(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.Surface([width, height])

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button(Widget):
    def __init__(self, x, y, text, textColour, boxColour, fontSize):
        self.wordFont = pygame.font.Font("Fonts/numberFont.ttf", fontSize)

        textWidth, textHeight = self.wordFont.size(text)
        width = textWidth + 6
        height = textHeight + 10

        super().__init__(x, y, width, height)

        self.text = text
        self.textColour = textColour
        self.boxColour = boxColour

        self.renderedText = self.wordFont.render(self.text, False, self.textColour)

        self.image.fill(self.boxColour)
        self.image.blit(self.renderedText, (5, 2))


class ScreenButton(Button):
    def __init__(self, x, y, text, textColour, boxColour, fontSize, goTo):
        super().__init__(x, y, text, textColour, boxColour, fontSize)

        self.goTo = goTo

    def isClicked(self, mousex, mousey):
        if self.rect.collidepoint(mousex, mousey):
            return self.goTo


class EnterButton(Button):
    def __init__(self, x, y, text, textColour, boxColour, fontSize):
        super().__init__(x, y, text, textColour, boxColour, fontSize)

    def isClicked(self, mousex, mousey):
        return self.rect.collidepoint(mousex, mousey)
            

class TextBox(Widget):
    def __init__(self, x, y, width, fontSize, textColour, activeBoxColour, passiveBoxColour, checkBoxColour, checkTextColour, variableToChange, isInt=False):
        self.textFont = pygame.font.Font("Fonts/numberFont.ttf", fontSize)
        height = self.textFont.size("A")[1]+6

        super().__init__(x, y, width, height)

        self.fontSize = fontSize
        self.textColour = textColour
        self.activeBoxColour = activeBoxColour
        self.passiveBoxColour = passiveBoxColour
        self.checkBoxColour = checkBoxColour
        self.checkTextColour = checkTextColour
        self.variableToChange = variableToChange
        self.isInt = isInt
        self.active = False

        self.rawText = ""
        self.renderedText = self.textFont.render(str(self.rawText), False, self.textColour)

        self.checkButton = pygame.sprite.GroupSingle()
        self.checkButton.add(EnterButton(self.width+10, 0, "ENTER", self.checkTextColour, self.checkBoxColour, self.fontSize))

        self.image = pygame.Surface([self.width + self.checkButton.sprite.width + 15, self.height])
        self.transparentColour = (1,1,1) if (self.activeBoxColour != (1,1,1) and self.passiveBoxColour != (1,1,1) and self.textColour != (1,1,1) and self.checkButton.sprite.boxColour != (1,1,1) and self.checkButton.sprite.textColour != (1,1,1)) else (2,2,2)
        self.image.set_colorkey(self.transparentColour)
        self.image.fill(self.transparentColour)

        pygame.draw.rect(self.image, self.passiveBoxColour, (0, 0, self.width, self.height))  ## Draw the main entry box
        self.image.blit(self.renderedText, (5, 2))
        self.checkButton.draw(self.image)

    def updateBox(self):
        self.renderedText = self.textFont.render(str(self.rawText), False, self.textColour)

        self.image.fill(self.transparentColour)
        pygame.draw.rect(self.image, self.activeBoxColour if self.active else self.passiveBoxColour, (0, 0, self.width, self.height))  ## Draw the main entry box
        self.image.blit(self.renderedText, (5, 2))
        self.checkButton.draw(self.image)
        

    def isBoxClicked(self, mousex, mousey):
        relMouseX = mousex - self.x
        relMouseY = mousey - self.y

        if pygame.Rect(0, 0, self.width, self.height).collidepoint(relMouseX, relMouseY):
            self.active = True
        else:
            self.active = False
        self.updateBox()

    def isButtonClicked(self, mousex, mousey):
        if self.checkButton.sprite.isClicked(mousex, mousey):
            if self.isInt:
                try:
                    self.rawText = int(self.rawText)
                    return self.rawText
                except ValueError:
                    pass
            else:
                return self.rawText

    def enterText(self, char):
        self.rawText = str(self.rawText)
        if char == pygame.K_BACKSPACE:
            self.rawText = self.rawText[:-1]
        elif char in alphaNumeric:
            self.rawText += chr(char)
        self.updateBox()

class Slider(Widget):
    def __init__(self, x, y, width, height, minValue, maxValue, currentValue, bgColour, sliderColour, buttonColour, displayColour, variableToChange):
        super().__init__(x, y, width, height)

        self.minValue = minValue
        self.maxValue = maxValue
        self.currentValue = currentValue
        self.bgColour = bgColour
        self.sliderColour = sliderColour
        self.buttonColour = buttonColour
        self.displayColour = displayColour
        self.variableToChange = variableToChange
        self.active = False

        assert self.currentValue <= self.maxValue and self.currentValue >= self.minValue, "Current value not in given range of values"

        self.buttonRadius = int((self.height - 8) / 2)
        self.buttonPercentage = (self.currentValue - self.minValue) / (self.maxValue - self.minValue)
        self.sliderWidth = self.width - (2 * self.buttonRadius)
        self.sliderHeight = int(self.height * 0.2)

        self.textFont = pygame.font.Font("Fonts/numberFont.ttf", int(self.height / 1.4))
        self.renderedText = self.textFont.render(str(self.currentValue), False, self.displayColour)
        
        self.image = pygame.Surface([self.width + 12 + self.textFont.size("0" * len(str(self.maxValue)))[0], self.height])
        self.image.fill(self.bgColour)
        self.image.blit(self.renderedText, (self.width+6, 0))
        pygame.draw.rect(self.image, self.sliderColour, (self.buttonRadius, int((self.height / 2) - (self.height * 0.1)), self.sliderWidth, self.sliderHeight))
        self.buttonRect = pygame.draw.circle(self.image, self.buttonColour, (int(round(self.buttonPercentage*self.sliderWidth, 0)), int(round(self.height/2, 0))), self.buttonRadius)

    def isButtonClicked(self, mousex, mousey):
        relMouseX = mousex - self.x
        relMouseY = mousey - self.y
        if self.buttonRect.collidepoint(relMouseX, relMouseY):
            self.active = True
        else:
            self.active = False

    def changeValue(self, mousex):
        relMousex = mousex - self.x
        mousePercentage = (relMousex - self.buttonRadius) / self.sliderWidth
        self.buttonPercentage = mousePercentage

        if relMousex < self.buttonRadius:
            self.currentValue = self.minValue
        elif relMousex > self.sliderWidth + self.buttonRadius:
            self.currentValue = self.maxValue
        else:
            self.currentValue = int(round(mousePercentage * self.maxValue, 0)) + self.minValue

        self.renderedText = self.textFont.render(str(self.currentValue), False, self.displayColour)
        
        self.image.fill(self.bgColour)
        self.image.blit(self.renderedText, (self.width+6, 0))
        pygame.draw.rect(self.image, self.sliderColour, (self.buttonRadius, int((self.height / 2) - (self.height * 0.1)), self.sliderWidth, self.sliderHeight))
        self.buttonRect = pygame.draw.circle(self.image, self.buttonColour, (int(self.currentValue * (self.sliderWidth / (self.maxValue - self.minValue))) + self.buttonRadius, int(round(self.height / 2, 0))), self.buttonRadius)

class DifficultySlider(Slider):
    def __init__(self, x, y, width, height, minValue, maxValue, currentValue, bgColour, sliderColour, buttonColour, displayColour, mazeScreen):
        super().__init__(x, y, width, height, minValue, maxValue, currentValue, bgColour, sliderColour, buttonColour, displayColour, None)

        self.mazeScreen = mazeScreen

    def changeValue(self, mousex):
        relMousex = mousex - self.x
        mousePercentage = (relMousex - self.buttonRadius) / self.sliderWidth
        self.buttonPercentage = mousePercentage

        if relMousex < self.buttonRadius:
            self.currentValue = self.minValue
        elif relMousex > self.sliderWidth + self.buttonRadius:
            self.currentValue = self.maxValue
        else:
            self.currentValue = int(round(mousePercentage * self.maxValue, 0)) + self.minValue

        self.mazeScreen.difficulty = self.currentValue
        self.renderedText = self.textFont.render(str(self.currentValue), False, self.displayColour)
        
        self.image.fill(self.bgColour)
        self.image.blit(self.renderedText, (self.width+6, 0))
        pygame.draw.rect(self.image, self.sliderColour, (self.buttonRadius, int((self.height / 2) - (self.height * 0.1)), self.sliderWidth, self.sliderHeight))
        self.buttonRect = pygame.draw.circle(self.image, self.buttonColour, (int(self.currentValue * (self.sliderWidth / (self.maxValue - self.minValue))) + self.buttonRadius, int(round(self.height / 2, 0))), self.buttonRadius)