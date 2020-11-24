import pygame, screenClass, button
pygame.init()

SCREENWIDTH = 950
SCREENHEIGHT = 950
size = (SCREENWIDTH, SCREENHEIGHT)
clock = pygame.time.Clock()
FPS = 30

carryOn = True

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Game")

screens = pygame.sprite.Group()
screens.add(screenClass.Screen((255,0,0), [button.Button(325, 200, "Play Game", (0,0,0), (255,255,255), 50, 0),
                                           button.Button(300, 300, "High Scores", (0,0,0), (255,255,255), 50, 1),
                                           button.Button(340, 500, "Settings", (0,0,0), (255,255,255), 50, 2)]),
            screenClass.Screen((0,255,0), [button.Button(100, 100, "Screen 1", (100, 0, 100), (230, 230, 230), 100, 0)]),
            screenClass.Screen((0,0,255), [button.Button(100, 100, "Screen 2", (0, 200, 200), (250, 250, 250), 25, 0)]))

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
                if index != None:
                    currentScreen.add(screens.sprites()[index])

    currentScreen.draw(screen)
    currentScreen.sprite.buttons.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

###### Refactor so we have currentScreen as sprite.Single() thing, then only update that
