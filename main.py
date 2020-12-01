import pygame, screenClass, widget
pygame.init()

SCREENWIDTH = 1000
SCREENHEIGHT = 650
size = (SCREENWIDTH, SCREENHEIGHT)
clock = pygame.time.Clock()
FPS = [60]

carryOn = True

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Game")

screens = pygame.sprite.Group()
screens.add(screenClass.Screen(SCREENWIDTH, SCREENHEIGHT, (255, 0, 0), [widget.ScreenButton(125, 200, "Play Game", (0, 0, 0), (255, 255, 255), 50, 1),
                                                                        widget.ScreenButton(100, 300, "High Scores", (0, 0, 0), (255, 255, 255), 50, 2),
                                                                        widget.ScreenButton(140, 500, "Settings", (0, 0, 0), (255, 255, 255), 50, 3),
                                                                        widget.ScreenButton(200, 550, "Quit", (0, 0, 0), (255, 255, 255), 50, -1)],
                                                                       [widget.TextBox(10, 10, 250, 40, (0, 0, 0), (225, 225, 225), (255, 255, 255), (0, 163, 7), (255, 255, 255), FPS)],
                                                                       [widget.Slider(20, 600, 750, 50, 0, 50, 2, (0, 0, 0), (0, 0, 255), (10, 240, 10), (133, 43, 209))]),
            screenClass.Screen(SCREENWIDTH, SCREENHEIGHT, (0, 255, 0), [widget.ScreenButton(100, 100, "Screen 1", (100, 0, 100), (230, 230, 230), 85, None),
                                                                        widget.ScreenButton(500, 200, "Back", (100, 0, 100), (230, 230, 230), 76, 0)], [], []),
            screenClass.Screen(SCREENWIDTH, SCREENHEIGHT, (0, 0, 255), [widget.ScreenButton(100, 100, "Screen 2", (0, 200, 200), (250, 250, 250), 25, None),
                                                                        widget.ScreenButton(100, 500, "Back", (0, 200, 200), (250, 250, 250), 48, 0)], [], []),
            screenClass.Screen(SCREENWIDTH, SCREENHEIGHT, (250 , 100, 255), [widget.ScreenButton(150, 200, "Screen 3", (0, 200, 200), (250, 250, 250), 14, None),
                                                                             widget.ScreenButton(750, 450, "Back", (200, 200, 200), (12, 130, 250), 72, 0)], [], []))

currentScreen = pygame.sprite.GroupSingle()
currentScreen.add(screens.sprites()[0])

while carryOn:
    ##print(FPS[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mousex, mousey = pygame.mouse.get_pos()
            for button in currentScreen.sprite.buttons:
                index = button.isClicked(mousex, mousey)
                if index != -1 and index is not None:
                    currentScreen.add(screens.sprites()[index])
                elif index == -1:
                    carryOn = False
            for box in currentScreen.sprite.textBoxes:
                box.isClicked(mousex, mousey)
            for slider in currentScreen.sprite.sliders:
                slider.active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            for slider in currentScreen.sprite.sliders:
                slider.isButtonClicked(mousex, mousey)
        elif event.type == pygame.MOUSEMOTION:
            mousex = pygame.mouse.get_pos()[0]
            for slider in currentScreen.sprite.sliders:
                if slider.active:
                    slider.changeValue(mousex)
        elif event.type == pygame.KEYDOWN:
            for box in currentScreen.sprite.textBoxes:
                if box.active:
                    box.enterText(event.key)

    currentScreen.draw(screen)
    currentScreen.sprite.buttons.draw(screen)
    currentScreen.sprite.textBoxes.draw(screen)
    currentScreen.sprite.sliders.draw(screen)

    pygame.display.flip()
    clock.tick(FPS[0])

pygame.quit()
