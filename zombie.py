import math
import random

import pygame
from constants import *
import rect


class Zombie(pygame.sprite.Sprite):
    def __init__(self, hp, speed):
        """
        This function defines the zombie 
        - Input: hp, speed
        - The method initializes the sprite by calling the constructor of the parent class and setting the initial image of the zombie 
        to the first image in a list of zombie_walk images.
        - The method also sets the position of the zombie randomly on one of the four sides of the game window.
        """
        pygame.sprite.Sprite.__init__(self)
        self.walk_imgs = zombie_walk
        self.hit_imgs = zombie_walk_red
        self.image = self.walk_imgs[0]
        self.rect_p = self.image.get_rect()
        self.rect = rect.Rect(self.rect_p)

        side = random.randint(1, 4)
        if side == 1:
            self.rect.set_center((-self.rect.width / 2, random.randint(-self.rect.height, WIN_Y + self.rect.height)))
        elif side == 2:
            self.rect.set_center((WIN_X + self.rect.width / 2, random.randint(-self.rect.height, WIN_Y + self.rect.height)))
        elif side == 3:
            self.rect.set_center((random.randint(-self.rect.width, WIN_X + self.rect.width), -self.rect.width / 2))
        elif side == 4:
            self.rect.set_center((random.randint(-self.rect.width, WIN_X + self.rect.width), WIN_Y + self.rect.width / 2))
            
        # init variables
        self.anim_counter = 0
        self.anim_speed = 5
        self.angle = 0
        self.speed = speed
        self.diagonal_speed = ((self.speed ** 2) / 2) ** (1 / 2)
        self.vector = (0, 0)
        self.hp = hp
        self.hit_count = 0

        self.knockback = 5

    def update(self, target):
        mouse = pygame.mouse.get_pos()
        vec1 = (target.rect.center[0] - self.rect.center[0], target.rect.center[1] - self.rect.center[1])  # vector from player center to zombie
        vec2 = (0, 1 - self.rect.center[1])  # vertical vector from player center to the top

        # get the angle between these two vectors 
        try:
            self.angle = math.degrees(math.acos((vec1[0] * vec2[0] + vec1[1] * vec2[1]) / ((vec1[0] ** 2 + vec1[1] ** 2) ** (1 / 2) * (vec2[0] ** 2 + vec2[1] ** 2) ** (1 / 2))))
        except ZeroDivisionError:
            self.angle = 0
            
        # If the player is to the right of the zombie, the angle is negated so that the zombie faces towards the player.
        if target.rect.center[0] > self.rect.center[0]:  
            self.angle = - self.angle

        self.vector = vec1
        try:
            # calculate the vector towards player with length of speed
            # https://math.stackexchange.com/questions/897723/how-to-resize-a-vector-to-a-specific-length
            self.vector = (self.vector[0] * (self.speed / ((self.vector[0] ** 2 + self.vector[1] ** 2) ** (1 / 2))),
                           self.vector[1] * (self.speed / ((self.vector[0] ** 2 + self.vector[1] ** 2) ** (1 / 2))))  
        except ZeroDivisionError:
            self.vector = (0, 0)

        # moves the zombie towards the player by adding the vector to its rect (x,y) and then checks if the counter that counts frames of the knockback animation.
        self.rect.set_center((self.rect.center[0] + self.vector[0], self.rect.center[1] + self.vector[1]))
        if pygame.Rect(self.rect.get()).colliderect(pygame.Rect((target.rect.x + 20 , target.rect.y + 20, target.rect.width -10, target.rect.height - 10))):
            self.rect.set_center((self.rect.center[0] - self.vector[0], self.rect.center[1] - self.vector[1]))
            if not target.immune:
                target.hp -= 1
                target.immune = True
        # knockback
        if self.hit_count != 0:
            self.rect.set_center((self.rect.center[0] - self.vector[0]*1.5, self.rect.center[1] - self.vector[1]*1.5))
            self.image = self.hit_imgs[self.anim_counter // self.anim_speed]
            self.hit_count -= 1
        else:
            self.image = self.walk_imgs[self.anim_counter // self.anim_speed]
        self.counter_plus()

    def draw(self):
        rotated_img = pygame.transform.rotate(self.image, self.angle)  # rotate the image
        rotated_rect = rect.Rect(rotated_img.get_rect())  # get the size and pos
        rotated_rect.set_center(self.rect.center)  # position it into the center
        sc.blit(rotated_img, rotated_rect.get())  # draw to screen

    def counter_plus(self):
        """
        This function updates the anim_counter attribute, which is used to cycle through the images in the walk_imgs and hit_imgs lists.
        """
        if self.anim_counter == 6 * self.anim_speed - 1:
            self.anim_counter = 0
        else:
            self.anim_counter += 1

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            return 1
        self.hit_count = 6  # frames for how long the zombie should be red
        return 0

