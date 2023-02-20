import pygame, sys
from constants import *
import game
from button import Button
import help

pygame.init()

pygame.display.set_caption(CAPTION + ' - Menu')

buttons = pygame.sprite.Group()


def draw():
    sc.fill((0, 0, 0))

    # render text
    text = MENU_FONT.render('Zombies', True, (255, 255, 255)) 
    
    # draw text
    sc.blit(text, (WIN_X / 2 - text.get_width() / 2 + 4, 20)) 

    buttons.update()

    pygame.display.update()


def start():
    # Create buttons in main menu
    buttons.add(Button((CENTER_X, 250), (250, 120), 'Play', func=game.start))
    buttons.add(Button((CENTER_X, 400), (350, 120), 'Instruction', func=help.start))
    buttons.add(Button((CENTER_X, 550), (250, 120), 'Quit', func=sys.exit))

    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if button.func():
                            running = False
                            return True
                        break

        if not running:
            break

        draw()

    return False
