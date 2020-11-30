import pygame
pygame.init()

class Slider(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, minValue, maxValue, currentValue, bgColour, sliderColour, buttonColour, displayColour):
		super().__init__()

		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.minValue = minValue
		self.maxValue = maxValue
		self.currentValue = currentValue
		self.bgColour = bgColour
		self.sliderColour = sliderColour
		self.buttonColour = buttonColour
		self.displayColour = displayColour
		self.active = False

		self.buttonRadius = int((self.height - 8) / 2)
		self.buttonPercentage = (self.currentValue - self.minValue) / (self.maxValue - self.minValue)
		self.sliderWidth = self.width - (2 * self.buttonRadius)
		self.sliderHeight = int(self.height * 0.2)

		self.textFont = pygame.font.Font("Fonts/numberFont.ttf", int(self.height / 1.4))
		self.renderedText = self.textFont.render(str(self.currentValue), False, self.displayColour)

		self.image = pygame.Surface([self.width + 8 + self.textFont.size("0" * len(str(self.maxValue)))[0], self.height])
		self.image.fill(self.bgColour)
		self.image.blit(self.renderedText, (self.width+6, 0))
		pygame.draw.rect(self.image, self.sliderColour, (self.buttonRadius, int((self.height / 2) - (self.height * 0.1)), self.sliderWidth, self.sliderHeight))
		pygame.draw.circle(self.image, self.buttonColour, (int(round(self.buttonPercentage*self.sliderWidth, 0)), int(round(self.height/2, 0))), self.buttonRadius)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def isButtonClicked(self, mousex, mousey):
		buttonRect = pygame.Rect(self.x+int(self.buttonPercentage*self.sliderWidth)-self.buttonRadius, self.y+int(self.height/2)-self.buttonRadius, self.buttonRadius*2, self.buttonRadius*2)
		if buttonRect.collidepoint(mousex, mousey):
			self.active = True
		else:
			self.active = False

	def changeValue(self, mousex):
		print("buttonx: ", int(self.buttonPercentage*self.sliderWidth))
		relMousex = mousex - self.x
		print("relmousex: ", relMousex)

		if relMousex < self.buttonRadius:
			self.currentValue = self.minValue
		elif relMousex > self.width - self.buttonRadius:
			self.currentValue = self.maxValue
		else:
			self.currentValue = relMousex // (self.maxValue - self.minValue) + self.minValue
		print(self.currentValue)

		self.buttonPercentage = (self.currentValue - self.minValue) / (self.maxValue - self.minValue)
		self.renderedText = self.textFont.render(str(self.currentValue), False, self.displayColour)

		self.image = pygame.Surface([self.width + 8 + self.textFont.size("0" * len(str(self.maxValue)))[0], self.height])
		self.image.fill(self.bgColour)
		self.image.blit(self.renderedText, (self.width+6, 0))
		pygame.draw.rect(self.image, self.sliderColour, (self.buttonRadius, int((self.height / 2) - (self.height * 0.1)), self.sliderWidth, self.sliderHeight))
		pygame.draw.circle(self.image, self.buttonColour, (int(round(self.buttonPercentage*self.sliderWidth, 0)), int(round(self.height/2, 0))), self.buttonRadius)
