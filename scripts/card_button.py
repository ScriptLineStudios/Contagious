import pygame
import numpy as np
from scripts.framework import *

class CardButton:
    def __init__(self, x, y, image, offset, text):
        self.x = x
        self.y = y
        self.image = image
        self.offset = offset
        self.start_y = self.y + self.offset
        self.sin = 0
        self.font = pygame.font.SysFont("Arial", 18)
        self.text = text
        self.ability = self.font.render(self.text, False, (255,255,255))
        self.played_sound = False

        
    def draw(self, display, clicking):
        display.blit(self.image, (self.x, self.start_y+np.sin(self.sin)*5))

        mx, my = pygame.mouse.get_pos()
        mx, my = mx/4, my/4

        if self.start_y > self.y:
            if not self.played_sound:
                play_sound("card.wav")
                self.played_sound = True
            self.start_y -= 3
            