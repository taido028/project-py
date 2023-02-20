import random
import time

import pygame, sys

import constants
import end
from constants import *
from player import Player
from zombie import Zombie
import upgrade_menu

# Init varianbles
score = 0
wave = 1

# Init player
p = Player()


def draw(start_time):
    """
    The draw function updates the display by blitting the background, the player, the bullets, the zombies, the player's health and the score. 
    It also displays the current wave for the first three seconds of each wave.
    """
    sc.blit(background, (0, 0))
    # draw bullets
    for b in bullets:
        b.draw()
        
    # draw zombie
    for z in zombies:
        z.draw()
        
    # draw the hearts that represent the player's health on the screen.
    for i in range(p.upgrades['hp'][0]):
        if i < p.hp:
            sc.blit(heart, (10 + i * 35, 10))
        else:
            sc.blit(no_heart, (10 + i * 35, 10))

    p.draw()
    
    # show Wave 'X' for 3 seconds
    if time.time() - start_time <= 3:  
        wave_text = MENU_FONT.render('Wave ' + str(wave), True, (255, 255, 255))
        sc.blit(wave_text, (WIN_X / 2 - wave_text.get_width() / 2 + 4, WIN_Y / 2 - wave_text.get_height() / 2 - 100))

    score_text = MENU_BTN_FONT.render(str(score), True, (255, 255, 255))
    sc.blit(score_text, (WIN_X - score_text.get_width() - 20 + 4, 20))

    pygame.display.update()


def start():
    """
    - This function is the main loop of the game. 
    - It updates the player, the bullets and the zombies, checks for collisions between bullets and zombies, 
    and handles events such as mouse clicks and key presses. 
    - It also updates the current wave and the player's score, and displays an upgrade menu at the end of each wave. 
    """
    global score, wave, p, zombies, bullets
    pygame.display.set_caption(CAPTION)

    start_time = time.time()
    running = True
    # game loop that checks for Pygame events such as mouse clicks and key presses, and updates the player's state accordingly
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                p.shoot(bullets)

        # update the player, bullets, and zombies based on current states.
        p.update()
        bullets.update()
        zombies.update(p)

        # This loop checks for collisions between bullets and zombies, and removes the bullet and updates the score if there is a hit.
        for b in bullets:
            for z in zombies:
                if pygame.Rect(z.rect.get()).collidepoint(b.rect.center):
                    b.kill()
                    score += z.hit()

        draw(start_time)
        
        # if it ends of wave and there are no zombies left 
        # then display the upgrade menu, updates the wave number, and restores the player's health.
        if time.time() - start_time >= WAVE_LENGTH + 3 and len(zombies) == 0: 
            time.sleep(0.3)
            upgrade_menu.start(wave, p)
            start_time = time.time()
            wave += 1
            p.restore_hp()
            
        # if the title Wave X has disappeared 
        elif WAVE_LENGTH + 3 > time.time() - start_time >= 3:  
            if random.randint(1, int(250 - wave * 10)) == 1:  # chance of spawning zombie
                zombies.add(Zombie(10 + (wave-1) * 2, 2 + wave/20))
                
        # if player has 0 hp, reset player's HP, score, wave , the upgrade of bullets,..
        if p.hp <= 0: 
            again = end.start(score)
            if again:
                score = 0
                p = Player()
                wave = 1
                bullets = pygame.sprite.Group()
                zombies = pygame.sprite.Group()
                return True

            else:
                running = False


    pygame.quit()
    return True
