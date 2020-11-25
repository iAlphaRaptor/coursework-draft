import pygame, screenClass, button, textBox
pygame.init()

SCREENWIDTH = 950
SCREENHEIGHT = 950
size = (SCREENWIDTH, SCREENHEIGHT)
clock = pygame.time.Clock()
FPS = 60

carryOn = True

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Game")

screens = pygame.sprite.Group()
screens.add(screenClass.Screen((255,0,0), [button.Button(325, 200, "Play Game", (0, 0, 0), (255, 255, 255), 50, 1),
                                           button.Button(300, 300, "High Scores", (0, 0, 0), (255, 255, 255), 50, 2),
                                           button.Button(340, 500, "Settings", (0, 0, 0), (255, 255, 255), 50, 3)],
                                          [textBox.TextBox(10, 10, 250, 40, (0, 0, 0), (225, 225, 225), (255, 255, 255), (0, 163, 7), (255, 255, 255))]),
            screenClass.Screen((0,255,0), [button.Button(100, 100, "Screen 1", (100, 0, 100), (230, 230, 230), 85, -1),
                                           button.Button(500, 200, "Back", (100, 0, 100), (230, 230, 230), 76, 0)], []),
            screenClass.Screen((0,0,255), [button.Button(100, 100, "Screen 2", (0, 200, 200), (250, 250, 250), 25, -1),
                                           button.Button(100, 500, "Back", (0, 200, 200), (250, 250, 250), 48, 0)], []),
            screenClass.Screen((250,100,255), [button.Button(150, 200, "Screen 3", (0, 200, 200), (250, 250, 250), 14, -1),
                                           button.Button(750, 450, "Back", (200, 200, 200), (12, 130, 250), 72, 0)], []))

currentScreen = pygame.sprite.GroupSingle()
currentScreen.add(screens.sprites()[0])

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn=False
        if event.type == pygame.MOUSEBUTTONUP:
            mousex, mousey = pygame.mouse.get_pos()
            for button in currentScreen.sprite.buttons:
                index = button.isClicked(mousex, mousey)
                if index != None and index != -1:
                    currentScreen.add(screens.sprites()[index])
            for box in currentScreen.sprite.textBoxes:
                box.isClicked(mousex, mousey)
        elif event.type == pygame.KEYDOWN:
            for box in currentScreen.sprite.textBoxes:
                if box.active:
                    box.enterText(event.key)

    currentScreen.draw(screen)
    currentScreen.sprite.buttons.draw(screen)
    currentScreen.sprite.textBoxes.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
