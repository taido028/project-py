import pygame
from constants import *

# button sprite
class Button(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple, size: tuple, text: str, text2: str = None, func=None, font=MENU_BTN_FONT):
        """
	This function define the button, which initializes the button's rectangular area using the pygame.Rect class 
    and takes the center position, size, text, optional second text, function, and font as parameters.
	   """
        pygame.sprite.Sprite.__init__(self)
        
        # calculating the left top corner coordinates from the center
        self.rect = pygame.Rect(center_pos[0] - size[0] / 2, center_pos[1] - size[1] / 2, size[0], size[1]) 
        self.text = text
        self.text2 = text2
        self.center_pos = center_pos
        self.func = func
        self.font = font

# update and draw buttons
    def update(self):
        """
        This method updates the button's appearance based on whether the mouse pointer is over the button or not, 
        and blits the button's text onto the screen using the render() method of the font.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(sc, BTN_HOVER_COLOR, self.rect, border_radius=BTN_BORDER_RADIUS)
        else:
            pygame.draw.rect(sc, BTN_COLOR, self.rect, border_radius=BTN_BORDER_RADIUS)

        text = self.font.render(self.text, True, (0, 0, 0))
        if self.text2 is not None:
            sc.blit(text, (self.center_pos[0] - text.get_width() / 2 + 4, self.center_pos[1] - text.get_height() / 2 - 30))
            text2 = self.font.render(self.text2, True, (0, 0, 0))
            sc.blit(text2, (self.center_pos[0] - text2.get_width() / 2 + 4, self.center_pos[1] - text2.get_height() / 2 + 30))
        else:
            sc.blit(text, (self.center_pos[0] - text.get_width() / 2 + 4, self.center_pos[1] - text.get_height() / 2))