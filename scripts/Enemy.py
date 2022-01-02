import pygame
import numpy as np
import random
import math

from scripts.framework import *
from scripts.images import explosion_imgs

class Enemy:
    def __init__(self, x, y, image, white_image, bullet_pattern, health):
        self.x = x
        self.y = y
        self.image = image
        self.time = 0
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.bullet_pattern = bullet_pattern
        self.white_image = white_image
        self.bullet_cooldown = random.randrange(70, 140)
        self.hit = False
        self.health = health

    def draw(self, display, scroll):
        self.time += 0.3
        alpha_img = self.image.copy()
        alpha_img.set_alpha(128)
        if self.hit:
            display.blit(self.white_image, (self.x-scroll[0], self.y-scroll[1]+np.sin(self.time)))
        else:
            display.blit(alpha_img, (self.x-scroll[0], self.y-scroll[1]+np.sin(self.time)+2))
            display.blit(self.image, (self.x-scroll[0], self.y-scroll[1]+np.sin(self.time)))

        self.hit = False



class BasicEnemy(Enemy):
    def __init__(self, x, y, image, white_image, bullet_pattern, health):
        super().__init__(x, y, image, white_image, bullet_pattern, health)

    def move_towards_player(self, player_rect, scroll):
        self.rect = pygame.Rect(self.x-scroll[0], self.y-scroll[1], 16, 16)
        player_vector = pygame.Vector2(player_rect.center)
        vector = pygame.Vector2(self.rect.center)

        try:
            self.towards = (vector - player_vector).normalize() /4

            self.x -= self.towards[0]
            self.y -= self.towards[1]
        except:
            pass

    def release_bullets(self, enemy_bullets):

        if self.bullet_cooldown <= 0:
            for bullet in self.bullet_pattern:
                enemy_bullets.append([[self.x, self.y], bullet, 100, 0])
            self.bullet_cooldown = random.randrange(70, 120)
        else:
            self.bullet_cooldown -= 1

    def main(self, display, scroll, enemy_bullets, player_rect, screen_shake):
        self.release_bullets(enemy_bullets)
        self.move_towards_player(pygame.Rect(player_rect.x-scroll[0], player_rect.y-scroll[1], 16, 16), scroll)
        self.draw(display, scroll)

class ShooterEnemy(Enemy):
    def __init__(self, x, y, image, white_image, bullet_pattern, health):
        super().__init__(x, y, image, white_image, bullet_pattern, health)
        

    def release_bullets(self, enemy_bullets, player_rect, scroll):
        self.rect = pygame.Rect(self.x-scroll[0], self.y-scroll[1], 16, 16)
        if self.bullet_cooldown <= 0:
            for x in range(5):
                target_x = player_rect.x-scroll[0]
                target_y = player_rect.y-scroll[1]
                angle = math.atan2((self.y-scroll[1])-target_y, (self.x-scroll[0])-target_x)
                x_vel = math.cos(angle) * 3
                y_vel = math.sin(angle) * 3

                bullet = [-x_vel+random.random(), -y_vel+random.random()]

                enemy_bullets.append([[self.x, self.y], bullet, 100, 0])

            self.bullet_cooldown = 130
        else:
            self.bullet_cooldown -= 1
    
    def main(self, display, scroll, enemy_bullets, player_rect, screen_shake):
        self.release_bullets(enemy_bullets, player_rect, scroll)
        #self.move_towards_player(pygame.Rect(player_rect.x-scroll[0], player_rect.y-scroll[1], 16, 16), scroll)
        self.draw(display, scroll)


class Boss(Enemy):
    def __init__(self, x, y, image, white_image, bullet_pattern, health, start_y):
        super().__init__(x, y, image, white_image, bullet_pattern, health)
        self.start_y = start_y
        self.animation = 0
        self.completed_intro = False
        self.played_thud = False
        self.sin = 0
        self.moving_left = True
        self.bullet_cooldown = 0
        self.teleport_cooldown = 50
        self.index = 0
        self.switch_attacks = random.randrange(100, 300)
        self.current_attack = None
        self.degree = 0

    def intro(self, display, scroll, screen_shake):
        if not self.completed_intro:
            if self.y < self.start_y:
                self.y += 3
            else:
                if not self.played_thud:
                    play_sound("thud.wav")
                    self.played_thud = True
                self.animation = animate(explosion_imgs, self.animation, 1)
                display.blit(explosion_imgs[self.animation//1], (self.x-scroll[0]-32, self.y-scroll[1]))
                if self.animation > 62:
                    self.completed_intro = True

    def attack1(self, scroll, player_rect, enemy_bullets): #Move up and down firing attacks
        if self.moving_left:
            self.x -= 2
            if self.x <= 0:
                self.moving_left = False
        else:
            self.x += 2
            if self.x >= 200:
                self.moving_left = True
        if self.bullet_cooldown <= 0:
            try:
                bullet = [0, (player_rect.y-self.y)/abs(player_rect.y-self.y)]
                enemy_bullets.append([[self.x, self.y], bullet, 100, 0])
                self.bullet_cooldown = 20
            except ZeroDivisionError:
                pass



        else:
            self.bullet_cooldown -= 1

    def attack2(self, scroll, player_rect, enemy_bullets): #Teleport in a triangle formation sparying bullets
        points = [[0,0], [200, 0], [100, 150]]

        self.x = points[self.index][0]
        self.y = points[self.index][1]
        if self.bullet_cooldown <= 0:
            for x in range(random.randrange(1, 3)):
                target_x = player_rect.x-scroll[0]
                target_y = player_rect.y-scroll[1]
                angle = math.atan2((self.y-scroll[1])-target_y, (self.x-scroll[0])-target_x)
                x_vel = math.cos(angle) * 3
                y_vel = math.sin(angle) * 3

                bullet = [-x_vel+random.random(), -y_vel+random.random()]

                enemy_bullets.append([[self.x, self.y], bullet, 100, 0])
            self.bullet_cooldown = 20
        else:
            self.bullet_cooldown -= 1

        if self.teleport_cooldown <= 0:
            if self.index == 2:
                self.index = 0

            else:
                self.index += 1


            self.teleport_cooldown = 50
        else:
            self.teleport_cooldown -= 1

    def attack3(self,scroll, player_rect, enemy_bullets): #Stand in the middle and launch a mega attack :)
        self.x = 100
        self.y = 100

        xradius = 200
        yradius = 100
        x1 = int(math.cos(self.degree*2*math.pi/360)*xradius)+300
        y1 = int(math.sin(self.degree*2*math.pi/360)*xradius)+150
        #pygame.draw.circle(display, RED, (x1-scroll[0]-100,y1-scroll[1]), 5)
        target_x = x1-scroll[0]-100
        target_y = y1-scroll[1]
        angle = math.atan2((self.y-scroll[1])-target_y, (self.x-scroll[0])-target_x)
        x_vel = math.cos(angle) * 3
        y_vel = math.sin(angle) * 3
        
        bullet = [x_vel, y_vel]

        enemy_bullets.append([[self.x, self.y], bullet, 100, 0])

        bullet = [-x_vel, -y_vel]

        enemy_bullets.append([[self.x, self.y], bullet, 100, 0])
        self.degree+=1

        #print(self.angle)



    def main(self, display, scroll, enemy_bullets, player_rect, screen_shake):
        self.rect = pygame.Rect(self.x-scroll[0], self.y-scroll[1], 32, 32)
        attacks = (self.attack1, self.attack2, self.attack3)

        if not self.completed_intro:
            self.intro(display, scroll, screen_shake)
            self.current_attack = random.choice(attacks)
        else:
            #print(self.current_attack)
            self.current_attack(scroll, player_rect, enemy_bullets)
            if self.switch_attacks <= 0:
                self.current_attack = random.choice(attacks)
                self.switch_attacks = random.randrange(100, 300)
            else:
                self.switch_attacks -= 1
        #self.release_bullets(enemy_bullets, player_rect, scroll)
        #self.move_towards_player(pygame.Rect(player_rect.x-scroll[0], player_rect.y-scroll[1], 16, 16), scroll)
        self.draw(display, scroll)




    
        



