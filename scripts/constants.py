import pygame
from pygame.constants import DOUBLEBUF, HWSURFACE

#General
WINDOW_SIZE = (900, 700)
SCREEN = pygame.display.set_mode((WINDOW_SIZE))
CLOCK = pygame.time.Clock()
ZOOM = 4

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
