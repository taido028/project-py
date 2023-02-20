import pygame, sys
from constants import *
from button import Button

pygame.init()

pygame.display.set_caption(CAPTION + ' - Game Over')

buttons = pygame.sprite.Group()


def draw():
    sc.fill((0, 0, 0))
    
    
    # render text
    text = MENU_BTN_FONT.render('Instruction', True, (255, 255, 255))
    text1 = MENU_BTN_FONT.render('Press W, A, S, D to move', True, (255, 255, 255))
    text2 = MENU_BTN_FONT.render('Right click to shoot', True, (255, 255, 255))
    text3 = MENU_BTN_FONT.render('Survive the zombies as long as you can', True, (255, 255, 255))
    
    # draw text to screen
    sc.blit(text, (WIN_X / 2 - text.get_width() / 2 , 60))
    sc.blit(text1, (WIN_X / 2- text1.get_width() /2 , 150))
    sc.blit(text2, (WIN_X / 2- text1.get_width() /2 , 250))
    sc.blit(text3, (WIN_X / 2- text1.get_width() /2 -150 , 350))
    
    
    buttons.update()

    pygame.display.update()


def start():
    # Create "back" button
    buttons.add(Button((CENTER_X, 600), (250, 120), 'Back'))

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
                        running = False
                        break

        draw()
