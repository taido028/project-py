import pygame

"""
* This is a class that create just to replace the existing pygame.Rect type which only supports ints and not floats.
* That resulted in inconsistent movement of zombies and player.

* Using a this class that supports float values 
  can make movement appear smoother and more natural, especially when moving by small amounts.
"""

class Rect:
    def __init__(self, pygame_rect):
        """
        This funtion sets the x, y, width, height, and center attributes of the new Rect object
        based on the corresponding attributes of the given pygame Rect object.
        """
        self.x = pygame_rect.x
        self.y = pygame_rect.y

        self.width = pygame_rect.width
        self.height = pygame_rect.height

        self.center = (self.x + self.width / 2, self.y + self.height / 2)

    def set_center(self, pos):
        """
        This is a function that sets the center of the rectangle to the given position
        and update the x, y, and center attributes of the Rect object based on the new center position.
        """
        self.center = (pos[0], pos[1])
        self.x = pos[0] - self.width / 2
        self.y = pos[1] - self.height / 2

    def get(self):
        return tuple((self.x, self.y, self.width, self.height))

    def set_y(self, y):
        """
        This is a function that sets the y position of the rectangle to the given value 
        and update the y position and center attributes of the Rect object based on the new y value.
        """
        self.y = y
        self.center = self.center = (self.x + self.width / 2, self.y + self.height / 2)

    def set_x(self, x):
        # similar to set_y funtion but for x position 
        self.x = x
        self.center = self.center = (self.x + self.width / 2, self.y + self.height / 2)

    def __str__(self):
        return str(self.get())

