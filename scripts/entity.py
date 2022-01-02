import pygame
import random
import numpy as np

class Entity:
    def __init__(self, x, y, image, alpha, function, radius, color):
        self.x = x
        self.y = y
        self.color = color
        try:
            self.image = image.copy()
        except:
            self.image = None
        self.alpha = alpha
        self.function = function

        self.radius = radius
        self.sine = random.randrange(-100, 100)
    
    def draw(self, display, scroll):
        self.sine += 1
        self.function(self)


        pygame.draw.circle(display, self.color, ((self.x-scroll[0]), (self.y-scroll[1])), self.radius)