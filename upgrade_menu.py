import random

import pygame, sys

from button import Button
from constants import *
from player import Player
from zombie import Zombie

buttons = pygame.sprite.Group()


def draw(wave):
    #draw the background, text when pass 1 wave
    sc.blit(background, (0, 0))

    text = MENU_BTN_FONT.render("You've passed wave " + str(wave), True, (255, 255, 255))
    sc.blit(text, (WIN_X / 2 - text.get_width() / 2 + 4, 20))

    text2 = MENU_BTN_FONT.render("Choose one upgrade!", True, (255, 255, 255))
    sc.blit(text2, (WIN_X / 2 - text2.get_width() / 2 + 4, 100))

    buttons.update()

    pygame.display.update()


def start(wave, p):
    gap = 30
    btn_size = 180
    all_size = (len(p.upgrades) - 1) * (btn_size + gap) - gap
    buttons.add(
        Button((WIN_X / 2 - all_size / 2, 300), (btn_size, btn_size), 'Bullet Speed', text2='Maxed out' if p.upgrades['bullet_speed'][0] == p.upgrades['bullet_speed'][1] else None,
               font=UPGRADE_FONT, func='bullet_speed'))
    buttons.add(Button((WIN_X / 2 - all_size / 2 + btn_size + gap, 300), (btn_size, btn_size), 'Bullet Count', text2='Maxed out' if p.upgrades['bullet_count'][0] ==
                                                                                                                                    p.upgrades['bullet_count'][1] else None,
                       font=UPGRADE_FONT,
                       func='bullet_count'))
    buttons.add(Button((WIN_X / 2 - all_size / 2 + (btn_size + gap) * 2, 300), (btn_size, btn_size), 'Walk Speed', text2='Maxed out' if p.upgrades['walk_speed'][0] ==
                                                                                                                                        p.upgrades['walk_speed'][1] else None,
                       font=UPGRADE_FONT,
                       func='walk_speed'))
    buttons.add(Button((WIN_X / 2 - all_size / 2 + (btn_size + gap) * 3, 300), (btn_size, btn_size), 'Lives + 1', text2='Maxed out' if p.upgrades['hp'][0] ==
                                                                                                                                       p.upgrades['hp'][1] else None,
                       font=UPGRADE_FONT,
                       func='hp'))
    buttons.add(Button((WIN_X / 2 - all_size / 2 + (btn_size + gap) * 4, 300), (btn_size, btn_size), 'Reload Time', text2='Maxed out' if p.upgrades['reload_time'][0] ==
                                                                                                                                         p.upgrades['reload_time'][1] else None,
                       font=UPGRADE_FONT,
                       func='reload_time'))

    pygame.display.set_caption(CAPTION + ' - Choose an upgrade')

    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if p.upgrades[button.func][0] != p.upgrades[button.func][1]:  # if not maxed out
                            p.upgrades[button.func][0] += p.upgrades[button.func][2]
                            p.diagonal_speed = ((p.upgrades['walk_speed'][0] ** 2) / 2) ** (1 / 2)
                            running = False
                        break

        draw(wave)
