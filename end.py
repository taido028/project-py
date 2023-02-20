import pygame, sys
from constants import *
from button import Button

pygame.init()

pygame.display.set_caption(CAPTION + ' - Game Over')

buttons = pygame.sprite.Group()

# Update and draw text, score in the game over menu.
def draw(score, new):
    sc.fill((0, 0, 0))

    text = MENU_FONT.render('Game Over', True, (255, 255, 255))
    sc.blit(text, (WIN_X / 2 - text.get_width() / 2 + 4, 60))
    text2 = MENU_BTN_FONT.render('Your score is ' + str(score), True, (255, 255, 255))
    sc.blit(text2, (WIN_X / 2 - text2.get_width() / 2 + 4, 180))
    text3 = MENU_BTN_FONT.render('New highscore is ' + str(get_highscore()) if new else 'Highscore is ' + str(get_highscore()), True, (255, 255, 255))
    sc.blit(text3, (WIN_X / 2 - text3.get_width() / 2 + 4, 240))

    buttons.update()

    pygame.display.update()


def start(score):
    buttons.add(Button((CENTER_X, 600), (250, 120), 'Quit', func=sys.exit))
    buttons.add(Button((CENTER_X, 440), (350, 120), 'Play again', func=None))
    
    # check if we got new high score
    if get_highscore() < score: 
        save_highscore(score)
        new = True
    else: new = False
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
                        # play again
                        if button.func is None:  
                            return True
                        else:
                            button.func()

        draw(score, new)
