import pygame
from scripts.constants import *
from scripts.images import *
from scripts.framework import *
import numpy as np
from functools import lru_cache
import numpy as np

time = np.arange(-5, 1, 0.1)
amplitude   = np.sin(time)

class Player:
    def __init__(self, x, y, movement_speed):
        self.x = x
        self.y = y
        self.player_rect = pygame.Rect(self.x,self.y, 10, 16)
        self.player_movement = [0,0]
        self.moving_left = False
        self.moving_right = False
        self.movement_speed = movement_speed
        self.scroll = [0,0]
        self.vertical_momentum = 0
        self.air_timer = 0
        self.animation_index = 0
        self.flipped = False
        self.rotation = 0
        self.jumping = False
        self.scale = [18, 27]
        self.time = 0

        



    
    def get_input(self, dt):
        self.player_movement = [0,0]
        self.air_timer += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_movement[0] -= self.movement_speed
        if keys[pygame.K_d]:
            self.player_movement[0] += self.movement_speed


        if keys[pygame.K_w]:
            self.player_movement[1] -= self.movement_speed
        if keys[pygame.K_s]:
            self.player_movement[1] += self.movement_speed


        if self.player_movement[0] > 0:
            self.flipped = False
        elif self.player_movement[0] < 0:
            self.flipped = True



    def check_collisions(self, display, tile_rects, scroll):
        hit_list = []
        for tile in tile_rects:
            if pygame.Rect(self.player_rect.x-scroll[0], self.player_rect.y-scroll[1], self.player_rect.width, self.player_rect.height).colliderect(pygame.Rect(tile[0]-scroll[0], tile[1]-scroll[1], tile[2], tile[3])):
                hit_list.append(pygame.Rect(tile[0], tile[1], 8, 8))
        return hit_list



    def move(self, display, tile_rects, scroll):
        collisions = {"top": False,
                    "bottom": False, 
                    "left": False,
                    "right": False}
        self.player_rect.x += self.player_movement[0]
        hit_list = self.check_collisions(display, tile_rects, scroll)
        for tile in hit_list:
            if self.player_movement[0] > 0:
                self.player_rect.right = tile.left
                collisions["right"] = True
            elif self.player_movement[0] < 0:
                self.player_rect.left = tile.right
                collisions["left"] = True


        self.player_rect.y += self.player_movement[1]
        hit_list = self.check_collisions(display, tile_rects, scroll)
        for tile in hit_list:
            if self.player_movement[1] > 0:
                self.player_rect.bottom = tile.top 
                collisions["bottom"] = True
            elif self.player_movement[1] < 0:
                self.player_rect.top = tile.bottom
                collisions["top"] = True

        
        return self.player_rect, collisions




    def calculate_scroll(self):
        self.scroll[0] += (self.player_rect.x-self.scroll[0]-150)/10
        self.scroll[1] += (self.player_rect.y-self.scroll[1]-150)/10


    def draw(self, display, scroll):
        self.time += 0.3
        #pygame.draw.rect(display, (0,0,0), (self.player_rect.x-scroll[0], self.player_rect.y-scroll[1], self.player_rect.width, self.player_rect.height))
        
        image = player_img
        #image = pygame.transform.rotate(image, self.rotation)

        alpha_img = image.copy()
        alpha_img.set_alpha(128)
        display.blit(pygame.transform.flip(pygame.transform.rotate(alpha_img, self.rotation), self.flipped, False), (self.player_rect.x-scroll[0], self.player_rect.y-scroll[1]-np.sin(self.time)+2))
        display.blit(pygame.transform.flip(pygame.transform.rotate(image, self.rotation), self.flipped, False), (self.player_rect.x-scroll[0], self.player_rect.y-scroll[1]-np.sin(self.time)))



        #display.blit(pygame.transform.rotate(bow_img, angle), (self.player_rect.x-scroll[0]+image.get_width()/2, self.player_rect.y-scroll[1]))





    def main(self, display, dt, tile_rects, scroll):
        self.get_input(dt)
        self.rect, collisions = self.move(display, tile_rects, scroll)

        #self.calculate_scroll()
        self.draw(display, scroll)


