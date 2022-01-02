"""WARNING: The code you are about to read is complete and utter garbage, during this jam I was under 
quite a lot of time pressue and ended up writing a ton of 'game jam spaghetti'"""

import pygame
from opensimplex import OpenSimplex
import random
import math

from pygame import font

from scripts.constants import *
from scripts.Player import Player as Player
from scripts.images import *
from scripts.Enemy import BasicEnemy, ShooterEnemy, Boss
from scripts.entity import Entity
from scripts.framework import *
from scripts.card_button import CardButton
import pygame.gfxdraw


display = pygame.Surface((WINDOW_SIZE[0]/ZOOM, WINDOW_SIZE[1]/ZOOM)).convert()
lighting =  pygame.Surface((WINDOW_SIZE[0]/ZOOM, WINDOW_SIZE[1]/ZOOM))
player = Player(100, 150, 1)

simplex = OpenSimplex(seed=random.randrange(-1000000, 1000000))

tile_rects = []

scroll = [0, 0]

attacks = []

enemies = []

enemy_bullets = []

punch_attacks = []

can_dash = 0

entities = []

screen_shake = 0

pygame.mouse.set_visible(False)

#Cards
dash_card = CardButton(60, 76, dash_card_img,100, "Dash Time +1")
speed_card = CardButton(100, 76, speed_card_img,100,"Speed +1")
bullet_damage_card = CardButton(180, 76, bullet_damage_card_img,100, "Bullet Damage +1")
double_bullets_card = CardButton(180, 76, double_bullet_card_img,100, "Double Bullets")
hearts_card = CardButton(180, 76, hearts_card_img,100, "Hearts +1")

cards = [dash_card, speed_card, bullet_damage_card, double_bullets_card, hearts_card]



card_buttons = []

difficulty_progression = [3,3,3, 4, 5, 6, 6, 1]

enemy_icon = pygame.image.load("assets/images/enemy_1.png")
enemy_icon.set_colorkey(WHITE)
pygame.display.set_icon(enemy_icon)


pygame.display.set_caption("Contagious")


game_map = [['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
           ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
           ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

boss_map = [['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
           ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
           ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]
                
menu = True

title_font = pygame.font.Font("assets/SplineSans-Regular.ttf", 24)
font_small = pygame.font.Font("assets/SplineSans-Regular.ttf", 15)

title_text = title_font.render("Contagious", False, WHITE)
title_text_rect = title_text.get_rect(center=(115, 15))

clicking = False

spawned_tutorial_enemy = False

bullet_count = 15

generated_cards = False

damage_bomb = 20

levels = -1 #-1 because of the tutorial level

menu_sin = 0

def start_game():
    global menu
    menu = False
    pygame.mixer.music.load("assets/soundeffects/main_soundtrack.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def quit_():
    pygame.quit()


player_health = 5
player_damage_cooldown = 0

squares = []

dash_cooldown = 0

def rot_center(image, angle, x, y, scale):
    rotated_image = pygame.transform.scale(image, (scale,scale))
    rotated_image = pygame.transform.rotate(rotated_image, angle)

    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

sqaure_cooldown = 0

while menu:
    mx, my = pygame.mouse.get_pos()
    mx, my = mx/ZOOM, my/ZOOM
    display.fill((20, 20, 20))
    for s in squares:
        s[1] -= 1
        s[2] += 1
        if s[3] < 0.2:
            squares.remove(s)
        s[3] -= 0.1
        img, rect = rot_center(sqaure_img, s[2], s[0], s[1], s[3])
        display.blit(img, rect)
    display.blit(title_text, title_text_rect)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = True

    render_button(display, "Play", title_font, False, WHITE, (90, 60), clicking, start_game)
    render_button(display, "Quit", title_font, False, WHITE, (90, 90), clicking, quit_)

    if sqaure_cooldown <= 0:
        squares.append([random.randrange(-10, 300), 180, 0, 32])
        sqaure_cooldown = 30
    else:
        sqaure_cooldown -=1

    display.blit(cursor_img, (mx-8, my-8))

    clicking = False
    SCREEN.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    #SCREEN.blit(pygame.transform.scale(lighting, WINDOW_SIZE), (0,0))


    CLOCK.tick(60)
    pygame.display.update()

    
tutorial = True

dead_enemies = []

level_complete = False

enemy_count = 0

bullet_regen = 0

game_clicking = False


#Variables for cards to modify
dash_time = 10
default_player_speed = 1
double_bullets = False
default_hearts = 5
bullet_damage = 1


enemy_types = ["enemy1", "enemy2"]

boss_intro = False

def next_level():
    global level_complete, tutorial, enemy_count, card_buttons, dead_enemies, generated_cards, levels, difficulty_progression, enemies
    global enemy_types    #Global variables... :(
    global simplex
    global player_damage_cooldown
    global player_health
    global player
    global boss_intro
    global screen_shake
    player.player_rect.x = 178
    player.player_rect.y = 143
    levels +=1
    enemies = []
    level_complete = False
    player_damage_cooldown = 50
    player_health = default_hearts
    simplex = OpenSimplex(seed=random.randrange(-1000000, 1000000))
    for x in range(difficulty_progression[levels]):
        if levels != 7:
            if difficulty_progression[levels] > 3:
                choice = random.choice(enemy_types)
                if choice == "enemy1":
            
                    enemies.append(BasicEnemy(random.randrange(0, 448), random.randrange(0, 200), enemy_1_img, enemy_1_white_img, [[1, 0], [-1, 0], 
                    [0, 1], [0, -1], 
                
                    [0.8, 0.8], [-0.8, 0.8], 
                    [-0.8, -0.8], [0.8, -0.8]], 7))

                if choice == "enemy2":
                
                    enemies.append(ShooterEnemy(random.randrange(0, 448), random.randrange(0, 200), enemy_2_image, enemy_1_white_img, [], 10))
            else:
                enemies.append(BasicEnemy(random.randrange(0, 448), random.randrange(0, 200), enemy_1_img, enemy_1_white_img, [[1, 0], [-1, 0], 
                    [0, 1], [0, -1], 
                
                    [0.8, 0.8], [-0.8, 0.8], 
                    [-0.8, -0.8], [0.8, -0.8]], 7))
        else: #Boss fight time!
            pygame.mixer.music.unload()
            pygame.mixer.music.load("assets/soundeffects/boss_fight.mp3")
            pygame.mixer.music.play()
            enemies.append(Boss(100, -150, boss_img, boss_white_img, [], 200, 50))
            boss_intro = True



    card_buttons = []
    dead_enemies = []

    generated_cards = False

    enemy_count = difficulty_progression[levels]
    tutorial = False


def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

sin = 0

def restart():
    global level_complete, tutorial, enemy_count, card_buttons, dead_enemies, generated_cards, levels, difficulty_progression, enemies
    global enemy_types    #Global variables... :(
    global simplex
    global player_damage_cooldown
    global player_health
    global player
    global boss_intro
    global screen_shake
    global enemy_bullets
    global enemy_count
    enemy_bullets = []
    player.player_rect.x = 178
    player.player_rect.y = 143
    enemies = []
    level_complete = False
    player_damage_cooldown = 50
    player_health = default_hearts
    simplex = OpenSimplex(seed=random.randrange(-1000000, 1000000))
    enemy_count = difficulty_progression[levels]
    for x in range(difficulty_progression[levels]):
        if levels != 7:
            if difficulty_progression[levels] > 3:
                choice = random.choice(enemy_types)
                if choice == "enemy1":
            
                    enemies.append(BasicEnemy(random.randrange(0, 448), random.randrange(0, 200), enemy_1_img, enemy_1_white_img, [[1, 0], [-1, 0], 
                    [0, 1], [0, -1], 
                
                    [0.8, 0.8], [-0.8, 0.8], 
                    [-0.8, -0.8], [0.8, -0.8]], 7))

                if choice == "enemy2":
                
                    enemies.append(ShooterEnemy(random.randrange(0, 448), random.randrange(0, 200), enemy_2_image, enemy_1_white_img, [], 10))
            else:
                enemies.append(BasicEnemy(random.randrange(0, 448), random.randrange(0, 200), enemy_1_img, enemy_1_white_img, [[1, 0], [-1, 0], 
                    [0, 1], [0, -1], 
                
                    [0.8, 0.8], [-0.8, 0.8], 
                    [-0.8, -0.8], [0.8, -0.8]], 7))
        else: #Boss fight time!
            pygame.mixer.music.unload()
            pygame.mixer.music.load("assets/soundeffects/boss_fight.mp3")
            pygame.mixer.music.play()
            enemies.append(Boss(100, -150, boss_img, boss_white_img, [], 200, 50))
            boss_intro = True


def generate_map():
    global levels

    if levels != 7:
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    pygame.draw.rect(display, BLACK, (x*16-scroll[0], y*16-scroll[1], 16, 16))
                    tile_rects.append([x*16, y*16, 8, 8])
                x += 1
            y += 1
    else:
        y = 0
        for layer in boss_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    pygame.draw.rect(display, BLACK, (x*16-scroll[0], y*16-scroll[1], 16, 16))
                    tile_rects.append([x*16, y*16, 8, 8])
                x += 1
            y += 1

shoot_cooldown = 0

shooting = False

bombs = []

game_complete = False

endx = 0
endy = 0

animation = 0

while not menu:

    display.fill(BLACK)
    #lighting.fill(BLACK)



    if bullet_regen <= 0 and bullet_count < 15:
        bullet_count += 1
        bullet_regen = 40
    else:
        bullet_regen -= 1

    if player_damage_cooldown > 0:
        player_damage_cooldown -= 1

    tile_rects = []

    mx, my = pygame.mouse.get_pos()
    mx, my = mx/ZOOM, my/ZOOM



    if not game_complete:
        if not boss_intro:
            scroll[0] += (player.player_rect.x-scroll[0]-100+mx/10)/10
            scroll[1] += (player.player_rect.y-scroll[1]-75+my/10)/10
        else:
            scroll[0] = 20
            scroll[1] = 10
            screen_shake = 10

            if enemies[0].completed_intro == True:
                boss_intro = False

    else:
        scroll[0] = endx-100
        scroll[1] = endy-100


    sin += 0.1

    if levels != 7:
        pygame.draw.rect(display, (20, 20, 20), (0-scroll[0], 0-scroll[1], 430, 270))
    else:
        pygame.draw.rect(display, (20, 20, 20), (0-scroll[0], 0-scroll[1], 215, 270))


    #pygame.draw.circle(display, RED, (100, 100), 10+np.sin(sin)*5)

    generate_map()

    

    if not tutorial:
        if levels != 7:
            for y in range(0, 100, 8):

                for x in range(50, 300, 8):
                    value = simplex.noise2d(x/100 , y/100)
                    _x = x-scroll[0]
                    _y = y-scroll[1]
                    dist = math.hypot((player.player_rect.x-scroll[0])-_x, (player.player_rect.y-scroll[1])-_y)
                    if dist < 200:
                        if value > 0.01:
                            tile_rects.append([x, y, 8, 8])
                            pygame.draw.rect(display, (100, 100,100), (x-scroll[0], y-scroll[1], 8, 8))

            for y in range(200, 300, 8):

                for x in range(50, 300, 8):
                    value = simplex.noise2d(x/100 , y/100)
                    _x = x-scroll[0]
                    _y = y-scroll[1]
                    dist = math.hypot((player.player_rect.x-scroll[0])-_x, (player.player_rect.y-scroll[1])-_y)
                    if dist < 200:
                        if value > 0.01:
                            tile_rects.append([x, y, 8, 8])
                            pygame.draw.rect(display, (100, 100,100), (x-scroll[0], y-scroll[1], 8, 8))

    else:

        text = font_small.render("Left Mouse to Shoot", False, WHITE)
        display.blit(text, (30-scroll[0], 100-scroll[1]))

        text2 = font_small.render("Shift to dash and avoid bullets", False, WHITE)
        display.blit(text2, (200-scroll[0], 100-scroll[1]))


        if player.player_rect.x > 205:
            if not spawned_tutorial_enemy:
                enemies.append(BasicEnemy(300, 100, enemy_1_img, enemy_1_white_img, [[1, 0], [-1, 0], 
                                                [0, 1], [0, -1], 
                                                
                                                [0.8, 0.8], [-0.8, 0.8], 
                                                [-0.8, -0.8], [0.8, -0.8]], 10))

                spawned_tutorial_enemy = True
                enemy_count = 1


    if shoot_cooldown > 0:
        shoot_cooldown -= 1
    
    if can_dash > 0:
        can_dash -= 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                if can_dash <= 0:
                    play_sound("dash.flac")
                    dash_cooldown = dash_time
                    can_dash = 30

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                game_clicking = True
                shooting = True

    

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                shooting = False

    for bomb in bombs:
        angle = math.atan2((bomb[1]-scroll[1])-bomb[3], (bomb[0]-scroll[0])-bomb[2])
        x_vel = math.cos(angle) * 3
        y_vel = math.sin(angle) * 3
        bomb[4] -= 1

        if bomb[4] > 0:
            bomb[0] -= x_vel
            bomb[1] -= y_vel
            display.blit(bomb_img, (bomb[0]-scroll[0], bomb[1]-scroll[1]))
            #pygame.draw.circle(display, RED, (bomb[0]-scroll[0], bomb[1]-scroll[1]), 5)
        else:
            bomb[5] = animate(explosion_imgs, bomb[5], 1)
            display.blit(explosion_imgs[bomb[5]//1], (bomb[0]-scroll[0]-50, bomb[1]-scroll[1]-50))
            if bomb[5] == 5:
                screen_shake += 10
            if bomb[5] == 69:
                bombs.remove(bomb)

            for enemy in enemies:
                if enemy.rect.colliderect(bomb[0]-scroll[0]-30, bomb[1]-scroll[1]-30, 60, 60):
                    
                    enemy.hit = True
                    enemy.health -= 10
                    try:
                        enemy.x += enemy.towards[0]*50
                        enemy.y += enemy.towards[1]*50
                    except AttributeError: #Got no clue why this happens, but ive got no time to fix it lol EDIT: This was before I added the shooter enemy
                        pass
                    screen_shake = 1
                    

                    for x in range(10):
                        particles.append(Particle(bomb[0], bomb[1]+random.randrange(-3, 3), random.randrange(-5, 5), random.randrange(-5, 5), 3, (172, 50, 50), 0, 50, True))
                #pygame.draw.rect(display, RED, (), 1)


    if shooting:
        if shoot_cooldown <= 0:
            play_sound("shoot.wav")
            screen_shake = 3
            mouse_x = pygame.mouse.get_pos()[0]/ZOOM
            mouse_y = pygame.mouse.get_pos()[1]/ZOOM
            angle = math.atan2((player.player_rect.y-scroll[1])-mouse_y, (player.player_rect.x-scroll[0])-mouse_x)
            x_vel = math.cos(angle) * 3
            y_vel = math.sin(angle) * 3

            rel_x, rel_y = mouse_x - (player.player_rect.x-scroll[0]), mouse_y - (player.player_rect.y-scroll[1])
            angle_rot = ((180 / math.pi) * -math.atan2(rel_y, rel_x))

            if not double_bullets:
                attacks.append([player.player_rect.x-8, player.player_rect.y-8, x_vel, y_vel, angle, angle_rot, 100])
            else:
                
                attacks.append([player.player_rect.x-8, player.player_rect.y-8, x_vel+1, y_vel+1, angle, angle_rot, 100])
                attacks.append([player.player_rect.x-8, player.player_rect.y-8, x_vel, y_vel, angle, angle_rot, 100])

            shoot_cooldown = 27


    if dash_cooldown > 0:
        player.movement_speed = 3
        dash_cooldown -= 1
        entities.append(Entity(player.player_rect.x+8, player.player_rect.y+8, None, 255, radius_decrease, 10, WHITE))
        if dash_cooldown == 1:
            player_damage_cooldown = 30
    else:
        player.movement_speed = default_player_speed

    for punch in punch_attacks:
        punch[2] += 1
        if punch[3] > 1:
            punch[3] -= 1
        else:
            
            punch_attacks.remove(punch)
        pygame.draw.circle(display, (200, 200, 200), (punch[0]-scroll[0], punch[1]-scroll[1]), punch[2], punch[3])


    for attack in attacks:
        attack[0] -= attack[2]*3
        attack[1] -= attack[3]*3

        attack[6] -= 1

        if attack[6] <= 0:
            attacks.remove(attack)

    


        for enemy in enemies:
            if enemy.rect.colliderect(attack[0]-scroll[0]+4, attack[1]-scroll[1]+4, 8, 8):
                
                enemy.hit = True
                enemy.health -= bullet_damage
                if damage_bomb != 20:
                    damage_bomb += 1
                try:
                    enemy.x += enemy.towards[0]*50
                    enemy.y += enemy.towards[1]*50
                except AttributeError: #Got no clue why this happens, but ive got no time to fix it lol EDIT: This was before I added the shooter enemy
                    pass
                screen_shake = 1
                try:
                    attacks.remove(attack)
                except:
                    pass

                for x in range(10):
                    particles.append(Particle(attack[0]+8, attack[1]+random.randrange(-3, 3), random.randrange(-5, 5), random.randrange(-5, 5), 3, (172, 50, 50), 0, 50, True))

        display.blit(pygame.transform.rotate(attack_img, attack[5]), (attack[0]-scroll[0], attack[1]-scroll[1]))

    player.main(display, 1, tile_rects, scroll)


    for entity in entities:
        if entity.radius <= 0:
            entities.remove(entity)
        entity.draw(display, scroll)
        
    if screen_shake:
        scroll[0] += random.randint(0, 8) - 4
        scroll[1] += random.randint(0, 8) - 4


    handle_particles(display, scroll)

    if screen_shake > 0:
        screen_shake -= 1

    for enemy in enemies:
        if enemy.health > 0:
            enemy.main(display, scroll, enemy_bullets, player.player_rect, screen_shake)
        else: 
            #IMAGE, X, Y, ROT, TOWARDS
            enemy_count -= 1
            try:
                if enemy.moving_left or not enemy.moving_left:
                    endx = enemy.x 
                    endy = enemy.y
            except:
                pass
            dead_enemies.append([enemy.image,enemy.x, enemy.y, 0])
            enemies.remove(enemy)

    if enemy_count <= 0 and spawned_tutorial_enemy:
        if levels != 7:
            level_complete = True
        else:
            game_complete = True

    for enemy in dead_enemies:
        if enemy[3] < 90:
            enemy[3] += 4

        display.blit(pygame.transform.rotate(enemy[0], enemy[3]), (enemy[1]-scroll[0], enemy[2]-scroll[1]))

    for bullet in enemy_bullets:
        bullet[0][0] += bullet[1][0]
        bullet[0][1] += bullet[1][1]
        bullet[2] -= 1
        bullet[3] += 0.1

        display.blit(enemy_bullet_img, (bullet[0][0]-scroll[0]+8, bullet[0][1]-scroll[1]+8))

        if pygame.Rect(player.player_rect.x-scroll[0], player.player_rect.y-scroll[1], 16, 16).colliderect(pygame.Rect(bullet[0][0]-scroll[0]+8, bullet[0][1]-scroll[1]+8, 10, 10)):
            if player_damage_cooldown <= 0 and dash_cooldown <= 0:
                for x in range(20):
                    particles.append(Particle(10+player_health*16+scroll[0], 12+scroll[1], random.randrange(-5, 5), random.randrange(-5, 5), 3, (221, 65, 65), 0, 20, True))
               
                screen_shake += 15
                player_health -= 1
                play_sound("hit.wav")
                player_damage_cooldown = 25

                
                
        pygame.gfxdraw.filled_circle(display, int(bullet[0][0]-scroll[0]+16), int(bullet[0][1]-scroll[1]+16), int(10+np.sin(bullet[3])*3), (182, 60, 60, 60))
        #display.blit(circle_surf(8+np.sin(bullet[3])*2, (172, 50, 50)), (bullet[0][0]-scroll[0]+8-np.sin(bullet[3]), bullet[0][1]-scroll[1]+8-np.sin(bullet[3])), special_flags=pygame.BLEND_RGB_ADD)
        if bullet[2] <= 0:
            enemy_bullets.remove(bullet)

    for i in range(player_health):
        image = heart_img.copy()
        image.set_alpha(128)
        display.blit(image, (10+i*16, 13))
        display.blit(heart_img, (10+i*16, 10+np.sin(sin)*2))

    if levels == 7:
        if len(enemies) >0:
            pygame.draw.rect(display, (117, 89, 99), (50, 150, 120, 10))
            pygame.draw.rect(display, (172, 50, 50), (50, 150, enemies[0].health*0.6, 10))

    if game_complete:
        text = title_font.render("Game Complete!", False, WHITE)
        display.blit(text, (35, 50))

    if player_health <= 0:
        pygame.draw.rect(display, BLACK, (0,0,500,500))
        title_text = title_font.render("You Failed!", False, WHITE)
        text_rect = text.get_rect(center=(119, 15))
        display.blit(title_text, text_rect)
        render_button(display, "Try Again", title_font, False, WHITE, (70, 60), game_clicking, restart)


    display.blit(cursor_img, (mx-8, my-8))
    #pygame.draw.rect(display, RED, (100, 40,  bullet_count*3, 10))
    SCREEN.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    if level_complete:
    
        if not generated_cards:
            card_selection = cards.copy()
            for i in range(3):
                choice = random.choice(card_selection)
                choice.x = 60 + i*40
                choice.offset = 100 + i*100
                choice.start_y = choice.y + choice.offset
                card_buttons.append(choice)
                card_selection.remove(choice)
            generated_cards = True
        lighting.fill(BLACK)
        lighting.blit(cursor_img, (mx-8, my-8))
        title_text = title_font.render("Level Complete", False, WHITE)
        if levels % 2 == 0:
            text_rect = text.get_rect(center=(104, 15))
            lighting.blit(title_text, text_rect)
            for card in card_buttons:
                card.draw(lighting, game_clicking)

                if pygame.Rect(card.x, card.y, 32, 40).collidepoint((mx, my)):
                    card.sin += 0.1
                    lighting.blit(card.ability, (110-card.ability.get_rect().width/2, 130))
                    if game_clicking:
                        if card.text == "Dash Time +1":
                            dash_time += 2

                            next_level()

                        if card.text == "Speed +1":
                            default_player_speed += 0.5

                            next_level()

                        if card.text == "Double Bullets":
                            cards.remove(card)
                            double_bullets = True
                            next_level()
                        
                        if card.text == "Bullet Damage +1":
                            bullet_damage += 1
                            next_level()

                        if card.text == "Hearts +1":
                            default_hearts += 1
                            next_level()

                else:
                    card.sin = 0
        
        else:
            text_rect = text.get_rect(center=(104, 15))
            lighting.blit(title_text, text_rect)
            render_button(lighting, "Continue", title_font, False, WHITE, (70, 60), game_clicking, next_level)

        SCREEN.blit(pygame.transform.scale(lighting, WINDOW_SIZE), (0,0))


    game_clicking = False
    CLOCK.tick(60)
    pygame.display.update()