import pygame, screenClass
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
screens.add(screenClass.Screen())

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn=False
        if event.type == pygame.MOUSEBUTTONUP:
            mousex, mousey = pygame.mouse.get_pos()
            for s in screens.sprites():
                for b in s.buttons.sprites():
                    print(b.isClicked(mousex, mousey))

    screens.draw(screen)
    for s in screens.sprites():
        s.buttons.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

###### Refactor so we have currentScreen as sprite.Single() thing, then only update that
