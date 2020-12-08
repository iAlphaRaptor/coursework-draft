import pygame, screenClass, widget, random, mazeRoutines
pygame.init()

SCREENWIDTH = SCREENHEIGHT = 800
size = (SCREENWIDTH, SCREENHEIGHT)
clock = pygame.time.Clock()
FPS = 60
difficulty = 5

carryOn = True

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Game")

screens = pygame.sprite.Group()
screens.add(screenClass.Screen(SCREENWIDTH, SCREENHEIGHT, (255, 0, 0), [widget.ScreenButton(50, 100, "Play Game", (0, 0, 0), (255, 255, 255), 50, 1),
                                                                        widget.ScreenButton(50, 200, "High Scores", (0, 0, 0), (255, 255, 255), 50, 3),
                                                                        widget.ScreenButton(50, 300, "Settings", (0, 0, 0), (255, 255, 255), 50, 4),
                                                                        widget.ScreenButton(50, 500, "Quit", (0, 0, 0), (255, 255, 255), 50, -1)],
                                                                       [widget.TextBox(10, 10, 400, 40, (0, 0, 0), (225, 225, 225), (255, 255, 255), (0, 163, 7), (255, 255, 255), "FPS", True)],
                                                                       [widget.Slider(20, 400, 500, 60, 3, 10, 3, (0, 0, 255), (10, 240, 10), (133, 43, 209),  (133, 43, 209), "x")]),
            screenClass.Screen(SCREENWIDTH, SCREENHEIGHT, (255, 0, 0), [widget.ScreenButton(300, 300, "Start", (0, 0, 0), (255, 255, 255), 50, 2),
                                                                        widget.ScreenButton(300, 100, "BACK", (123, 231, 132), (81, 102, 229), 50, 0)], [],
                                                                       [widget.DifficultySlider(10, 200, 500, 50, 0, 20, difficulty, (255, 0, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0), None)]),
            screenClass.MazeScreen(SCREENWIDTH, SCREENHEIGHT, (200, 200, 200), (0, 0, 0), 1, difficulty),
            screenClass.Screen(SCREENWIDTH, SCREENHEIGHT, (0, 0, 255), [widget.ScreenButton(100, 100, "Screen 2", (0, 200, 200), (250, 250, 250), 25, None),
                                                                        widget.ScreenButton(100, 500, "Back", (0, 200, 200), (250, 250, 250), 48, 0)], [], []),
            screenClass.Screen(SCREENWIDTH, SCREENHEIGHT, (250 , 100, 255), [widget.ScreenButton(150, 200, "Screen 3", (0, 200, 200), (250, 250, 250), 14, None),
                                                                             widget.ScreenButton(350, 450, "Back", (200, 200, 200), (12, 130, 250), 72, 0)], [], []))
screens.sprites()[1].sliders.sprites()[0].mazeScreen = screens.sprites()[2]

currentScreen = pygame.sprite.GroupSingle()
currentScreen.add(screens.sprites()[1])

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.MOUSEBUTTONUP:
            for slider in currentScreen.sprite.sliders:
                slider.active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            for button in currentScreen.sprite.buttons:
                index = button.isClicked(mousex, mousey)
                if index != -1 and index is not None:
                    currentScreen.add(screens.sprites()[index])
                elif index == -1:
                    carryOn = False
            for box in currentScreen.sprite.textBoxes:
                box.isBoxClicked(mousex, mousey)
                boxValue = box.isButtonClicked(mousex, mousey)
                if boxValue is not None:
                    globals()[box.variableToChange] = boxValue
            for slider in currentScreen.sprite.sliders:
                slider.isButtonClicked(mousex, mousey)
        elif event.type == pygame.MOUSEMOTION:
            mousex = pygame.mouse.get_pos()[0]
            for slider in currentScreen.sprite.sliders:
                if slider.active:
                    slider.changeValue(mousex)
                    globals()[slider.variableToChange] = slider.currentValue
        elif event.type == pygame.KEYDOWN:
            for box in currentScreen.sprite.textBoxes:
                if box.active:
                    box.enterText(event.key)
            if currentScreen.sprite.__class__.__name__ == "MazeScreen":
                if event.key == pygame.K_z:
                    currentScreen.add(screens.sprites()[1])
                elif event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    currentScreen.sprite.moveUser(event.key)

    if currentScreen.sprite.__class__.__name__ == "MazeScreen":
        if not currentScreen.sprite.generated:
            currentScreen.sprite.generateMaze()
            astar = mazeRoutines.aStar(screens.sprites()[2].cells, (0,0), (2,2))
            print(astar)
            screen.fill(currentScreen.sprite.wallColour)
        else:
            currentScreen.sprite.updateMaze()
            currentScreen.sprite.moveComputer()

    currentScreen.draw(screen)
    currentScreen.sprite.buttons.draw(screen)
    currentScreen.sprite.textBoxes.draw(screen)
    currentScreen.sprite.sliders.draw(screen)
    #if currentScreen.sprite.__class__.__name__ == "MazeScreen":
        #for a in astar:
            #if a != 0:
                #pygame.draw.rect(screen, (0,0,255), (a[0]*currentScreen.sprite.cellWidth+1, a[1]*currentScreen.sprite.cellWidth+1, currentScreen.sprite.cellWidth-1, currentScreen.sprite.cellWidth-1))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
