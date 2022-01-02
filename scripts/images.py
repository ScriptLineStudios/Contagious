import pygame
from scripts.constants import *
import os

def load_img(img):
    image = pygame.image.load("assets/images/" + img + ".png").convert()
    image.set_colorkey(WHITE)
    return image

player_img = load_img("player")
attack_img = load_img("attack")
enemy_1_img = load_img("enemy_1")
enemy_1_white_img = load_img("enemy_1_white")

enemy_2_image = load_img("enemy_2")

enemy_bullet_img = load_img("enemy_bullet")

speed_card_img = load_img("speed_card_sprite")
dash_card_img = load_img("dash_card_sprite")
punch_card_img = load_img("punch_card_sprite")
bullet_damage_card_img = load_img("bullet_damage_card_sprite")
double_bullet_card_img = load_img("double_bullet_card_sprite")
hearts_card_img = load_img("heart_card_sprite")

entrance_img = load_img("entrance")

heart_img = load_img("heart")

explosion_imgs = []

for i in range(64):
    if i < 10:
        img = pygame.image.load(f"assets/images/explosion/frame000{i}.png")
        explosion_imgs.append(img)
    else:
        img = pygame.image.load(f"assets/images/explosion/frame00{i}.png")
        explosion_imgs.append(img)

bomb_img = load_img("bomb")

sqaure_img = load_img("square")

boss_img = load_img("BOSS")
boss_white_img = load_img("boss_white")

cursor_img = load_img("cursor")

