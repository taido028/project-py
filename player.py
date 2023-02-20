import time

import pygame, math, random

import rect
import importlib
from constants import *
import constants
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        This defines the Player class, which inherits from pygame.sprite.Sprite. 
        The player images (walk_imgs, walk_back_imgs, walk_red_imgs) are defined, and the initial image and rect of the player are set.
        The anim_counter and anim_speed are used for animation, and angle is the angle between the player and the mouse pointer. 
        
        The upgrades dictionary contains the current level of each upgrade, as well as the maximum level and step size for each upgrade. 
        
        Diagonal_speed is the speed of the player when moving diagonally. 
        Shot_inaccuracy is the degree of inaccuracy when shooting. 
        hp is the player's health points. damaged_count and immune are used for controlling when the player can be damaged. 
        last_time_shot is the time when the player last shot.
        """
        pygame.sprite.Sprite.__init__(self)
        
        # create animation and set the position of the player at the center 
        self.walk_imgs = player_walk
        self.walk_back_imgs = player_walk_back
        self.walk_red_imgs = player_walk_red
        self.image = self.walk_imgs[0]
        self.rect_p = self.image.get_rect()
        self.rect = rect.Rect(self.rect_p)
        self.rect.set_center((WIN_X / 2, WIN_Y / 2))

        # init variables
        self.anim_counter = 0
        self.anim_speed = 5
        self.angle = 0
        self.walking_direction = 0
        self.walking = False
        
        self.shot_inaccuracy = 20
        self.hp = 1
        self.damaged_count = 0
        self.immune = False
        self.last_time_shot = 0
        
        # (actual, max, step)
        self.upgrades = {
            'bullet_speed': [15, 100, 5],
            'bullet_count': [5, 50, 5],
            'walk_speed': [3, 10, 1],
            'hp': [1, 10, 1],
            'reload_time': [1, 0.2, -0.1]  # s
        }
        
        self.diagonal_speed = ((self.upgrades['walk_speed'][0] ** 2) / 2) ** (1 / 2)
        
        
    def update(self):
        
        mouse = pygame.mouse.get_pos()
        # vector from player center to mouse pos
        vec1 = (mouse[0] - self.rect.center[0], mouse[1] - self.rect.center[1]) 
        
        # vertical vector from player center to the top 
        vec2 = (0, 1 - self.rect.center[1])  

        # get the angle between these two vectors (https://mathsathome.com/wp-content/uploads/2021/12/how-to-find-the-angle-between-two-vectors.png)
        try:
            self.angle = math.degrees(math.acos((vec1[0] * vec2[0] + vec1[1] * vec2[1]) / ((vec1[0] ** 2 + vec1[1] ** 2) ** (1 / 2) * (vec2[0] ** 2 + vec2[1] ** 2) ** (1 / 2))))
        except ZeroDivisionError:
            self.angle = 0

        # If the mouse is to the right of the player, the angle is negated. This ensures that the player always faces the mouse.
        if self.rect.center[0] < mouse[0]:  
            self.angle = - self.angle

        # movement
        pos_before = str(self.rect)  # saving the previous position 

        events = pygame.key.get_pressed()  # get pressed keys
        # so that the diagonal movement has the same speed as horizontal and vertical.
        
        #if 'w' and 'a' keys are pressed , the player's walking direction is set to 45 degrees.
        if events[pygame.K_w] and events[pygame.K_a] and self.rect.y > 0 and self.rect.x > 0:  
            self.rect.set_y(self.rect.y - self.diagonal_speed)
            self.rect.set_x(self.rect.x - self.diagonal_speed)
            self.walking_direction = 45
        #if 'w' and 'd' keys are pressed , the player's walking direction is set to -45 degrees.    
        elif events[pygame.K_w] and events[pygame.K_d] and self.rect.y > 0 and self.rect.x < WIN_X - self.rect.width:
            self.rect.set_y(self.rect.y - self.diagonal_speed)
            self.rect.set_x(self.rect.x + self.diagonal_speed)
            self.walking_direction = - 45
        #if 's' and 'a' keys are pressed , the player's walking direction is set to 135 degrees.
        elif events[pygame.K_s] and events[pygame.K_a] and self.rect.y < WIN_Y - self.rect.height and self.rect.x > 0:
            self.rect.set_y(self.rect.y + self.diagonal_speed)
            self.rect.set_x(self.rect.x - self.diagonal_speed)
            self.walking_direction = 45 + 90
        #if 's' and 'd' keys are pressed , the player's walking direction is set to -135 degrees.
        elif events[pygame.K_s] and events[pygame.K_d] and self.rect.y < WIN_Y - self.rect.height and self.rect.x < WIN_X - self.rect.width:
            self.rect.set_y(self.rect.y + self.diagonal_speed)
            self.rect.set_x(self.rect.x + self.diagonal_speed)
            self.walking_direction = - 45 - 90
        else:
            if events[pygame.K_w] and self.rect.y > 0:  
                self.rect.set_y(self.rect.y - self.upgrades['walk_speed'][0])
                self.walking_direction = 0
            elif events[pygame.K_s] and self.rect.y < WIN_Y - self.rect.height:
                self.rect.set_y(self.rect.y + self.upgrades['walk_speed'][0])
                self.walking_direction = 180
            elif events[pygame.K_a] and self.rect.x > 0:
                self.rect.set_x(self.rect.x - self.upgrades['walk_speed'][0])
                self.walking_direction = 90
            elif events[pygame.K_d] and self.rect.x < WIN_X - self.rect.width:
                self.rect.set_x(self.rect.x + self.upgrades['walk_speed'][0])
                self.walking_direction = - 90

        if pos_before != str(self.rect):  # if position changed
            self.walking = True
        else:
            self.walking = False

        # walk animation
        if self.walking:
            if self.walking_direction == 180:  
                if self.angle < 0:
                    if self.walking_direction + self.angle > 90 + 30:
                        self.image = self.walk_back_imgs[self.anim_counter // self.anim_speed]
                    else:
                        self.image = self.walk_imgs[self.anim_counter // self.anim_speed]
                else:
                    if self.walking_direction - self.angle > 90 + 30:
                        self.image = self.walk_back_imgs[self.anim_counter // self.anim_speed]
                    else:
                        self.image = self.walk_imgs[self.anim_counter // self.anim_speed]

            # the idea is that it decides if the player is moving forwards or backwards by calculating the angle between walking direction and the mouse
            # if its bigger than 120° you go backwards, else you go forward
            # if the player looks the oposite direction from walking direction, he will walk backwards.
            
            elif math.fabs(self.angle - self.walking_direction) > 90 + 30:  
                self.image = self.walk_back_imgs[self.anim_counter // self.anim_speed]
            else:
                self.image = self.walk_imgs[self.anim_counter // self.anim_speed]

            self.counter_plus()  # increase the counter by one (the counter determinates the frame of the animation 1-6)
        else:
            self.image = self.walk_imgs[0]

        if self.immune:  # delay between taking dmg again
            self.damaged_count += 1
            if self.damaged_count >= 60:  # 1s
                self.immune = False
                self.damaged_count = 0

            if 1 < self.damaged_count <= 20:
                self.image = self.walk_red_imgs[self.anim_counter // self.anim_speed]

    def draw(self): 
        # Function handeling render to screen
        surf = pygame.Surface((self.rect.width, gun_img.get_rect().height + 5 * PX), pygame.SRCALPHA, 32).convert_alpha()
        surf.blit(self.image, (0, 5 * PX))
        surf.blit(gun_img, (0, 0))

        rotated_img = pygame.transform.rotate(surf, self.angle)  # rotate the image
        rotated_rect = rect.Rect(rotated_img.get_rect())  # get the size and pos
        rotated_rect.set_center(self.rect.center)  # position it into the center
        sc.blit(pygame.transform.rotate(surf, self.angle), rotated_rect.get())  # draw to screen

    def counter_plus(self):
        """
        This function updates the anim_counter attribute, which is used to cycle through the images in the walk_imgs and hit_imgs lists.
        """
        if self.anim_counter == 6 * self.anim_speed - 1:
            self.anim_counter = 0
        else:
            self.anim_counter += 1

    def shoot(self, bullets):
        if time.time() - self.last_time_shot >= self.upgrades['reload_time'][0]:
            for _ in range(self.upgrades['bullet_count'][0]):
                bullets.add(
                    Bullet(self.rect.center[0], self.rect.center[1], random.randint(self.upgrades['bullet_speed'][0] * 0.8, self.upgrades['bullet_speed'][0] * 1.2), self.shot_inaccuracy))
            self.last_time_shot = time.time()

    def restore_hp(self):
        self.hp = self.upgrades['hp'][0]