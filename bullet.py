import pygame, math, random

import rect
from constants import *


class Bullet(pygame.sprite.Sprite):
    """
    This class defines 'x' and 'y', which specify the starting position of the bullet, 'speed' specifies the speed at which the bullet moves,
    and 'acc' specifies the accuracy of the bullet 
    
    This class creates bullets that move in a straight line from their starting position to the current mouse position,
    with some random deviation in their trajectory
    """
    def __init__(self, x, y, speed, acc):
        pygame.sprite.Sprite.__init__(self)
        self.rect_p = pygame.Rect(x, y, PX, PX)
        self.rect = rect.Rect(self.rect_p)
        self.speed = speed
        
        # get the vector between the starting position of the bullet and the mouse position.
        target = list(pygame.mouse.get_pos())
        self.vector = (target[0] - x, target[1] - y)
        
        try:
            """ 
            # calculate the vector towards target with length of speed
            # https://math.stackexchange.com/questions/897723/how-to-resize-a-vector-to-a-specific-length
            
            # This line normalizes the self.vector to a unit vector and scales it to the desired speed.
            # This ensures that the bullet moves at a constant speed, regardless of the distance between the starting position and the mouse position.
            """
            self.vector = (self.vector[0] * (self.speed / ((self.vector[0] ** 2 + self.vector[1] ** 2) ** (1 / 2))),
                           self.vector[1] * (self.speed / ((self.vector[0] ** 2 + self.vector[1] ** 2) ** (1 / 2))))  
            self.invalid = False
            
        except ZeroDivisionError:
            self.invalid = True
            
        # make the bullets not precise
        deviation = math.radians((random.random() - 0.5) * acc)  
         
        
        # This line applies the random deviation to the bullet trajectory, by rotating the self.vector by the deviation angle
        self.vector = (self.vector[0] * math.cos(deviation) - self.vector[1] * math.sin(deviation), 
                       self.vector[0] * math.sin(deviation) + self.vector[1] * math.cos(deviation))
        
        
    def update(self):
        """
        This method updates the position of the bullet each time it is called.
        It moves the bullet by the vector vector and updates the position of the bullet's rectangle accordingly using the set_x and set_y methods.
        """
        self.rect.set_x(self.rect.x + self.vector[0])
        self.rect.set_y(self.rect.y + self.vector[1])

        # if the bullet is out of the screen then delete the bullet
        if self.rect.x < 0 or self.rect.x > WIN_X or self.rect.y < 0 or self.rect.y > WIN_Y or self.invalid:  
            self.kill()

    def draw(self):
        pygame.draw.rect(sc, (196, 72, 10), self.rect.get())
