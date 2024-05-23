import pygame
import math

from assets.scripts.weapons import *

aDown = False
sDown = False
dDown = False
wDown = False

def player_input(event, player, current_frame):

    global aDown
    global sDown
    global dDown
    global wDown
    if event.type == pygame.KEYDOWN:
        if chr(event.key) == "a":
            aDown = True

        if chr(event.key) == "w":
            wDown = True

        if chr(event.key) == "s":
            sDown = True

        if chr(event.key) == "d":
             dDown = True

    if event.type == pygame.KEYUP:
        if chr(event.key) == "a":
            aDown = False
        if chr(event.key) == "w":
            wDown = False
        if chr(event.key) == "s":
            sDown = False
        if chr(event.key) == "d":
            dDown = False

    if current_frame == 0:    
        if aDown:
            player.direction = 90
        if dDown:
            player.direction = 270
    
    return aDown, sDown, dDown, wDown, player
        
def vect_set(aDown, sDown, dDown, wDown, speed, player_sprite, room, vect_move):

    if wDown and (aDown or dDown) or sDown and (aDown or dDown):
        speed = math.sqrt((speed**2)/2)
    if vect_move[0]**2 <= speed**2:
        if aDown:
            vect_move[0] -= speed
        if dDown:
            vect_move[0] += speed
    if vect_move[1]**2 <= speed**2:
        if sDown:
            vect_move[1] += speed
        if wDown:
            vect_move[1] -= speed
            

    return vect_move
        
def player_move(player, vect_move, entities):
    
    if vect_move[0]**2 < 1:
        vect_move[0] = 0
    if vect_move[1]**2 <1:
        vect_move[1] = 0
        
    for entity in entities:
        player.rect.x += vect_move[0]
        if pygame.sprite.collide_mask(player, entity):
            if ((vect_move[1]==0 and vect_move[0] != 0) or (vect_move[1]!=0 and vect_move[0]==0)) and (player.rect.x <= 790 and player.rect.x >= 10) and (player.rect.y >=10 and player.rect.y <= 590):
                for displace in range(5):
                    player.rect.y += displace
                    if not pygame.sprite.collide_mask(player, entity):
                        break
                    player.rect.y -= displace
                for displace in range(5):
                    player.rect.y -= displace
                    if not pygame.sprite.collide_mask(player, entity):
                        break
                    player.rect.y += displace
            if pygame.sprite.collide_mask(player, entity):
                player.rect.x -= vect_move[0]
                vect_move[0] = 0
        player.rect.y += vect_move[1]
        if pygame.sprite.collide_mask(player, entity):
            if ((vect_move[1]==0 and vect_move[0] != 0) or (vect_move[1]!=0 and vect_move[0]==0)) and (player.rect.x <= 790 and player.rect.x >= 10) and (player.rect.y >=10 and player.rect.y <= 590):
                for displace in range(5):
                    player.rect.x += displace
                    if not pygame.sprite.collide_mask(player, entity):
                        break
                    player.rect.x -= displace
                for displace in range(5):
                    player.rect.x -= displace
                    if not pygame.sprite.collide_mask(player, entity):
                        break
                    player.rect.x += displace
            if pygame.sprite.collide_mask(player, entity):
                player.rect.y -= vect_move[1]
                vect_move[1] = 0
    
    
    if vect_move[0] < 0:
        vect_move[0] += 1
    elif vect_move[0] >0:
        vect_move[0] -= 1
    if vect_move[1] < 0 :
        vect_move[1] += 1
    elif vect_move[1] >0:
        vect_move[1] -= 1
        
def player_direction(player, player_hand, player_weapon, path):
    
    if player.direction == 0:
        player.image = pygame.transform.scale(pygame.image.load(path + "\\assets\\sprites\\player_assets\\crtlnd\\crtlnd_up.png"), (player.width, player.height))
        player_hand = [player.rect.x + player.hand[1][0], player.rect.y + player.hand[1][1]]
        if not player_weapon.animation:
            player_weapon = player_weapon.image_at((0,0,99,99))
    if player.direction == 90:
        player.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load(path + "\\assets\\sprites\\player_assets\\crtlnd\\crtlnd.png"), True, False), (player.width, player.height))
        player_hand = [player.rect.x + (player.width+1-player.hand[0][0]), player.rect.y + player.hand[0][1]]
        if not player_weapon.animation:
            player_weapon.image = pygame.transform.rotate(player_weapon.image_at((0,0,99,99)).image, 90)
    if player.direction == 270:
        player.image = pygame.transform.scale(pygame.image.load(path + "\\assets\\sprites\\player_assets\\crtlnd\\crtlnd.png"), (player.width, player.height))
        player_hand = [player.rect.x + player.hand[0][0], player.rect.y + player.hand[0][1]]
        if not player_weapon.animation:
            player_weapon.image = pygame.transform.rotate(player_weapon.image_at((0,0,99,99)).image, 270)
    if player.direction == 180:
        player.image = pygame.transform.scale(pygame.image.load(path + "\\assets\\sprites\\player_assets\\crtlnd\\crtlnd_down.png"), (player.width, player.height))
        player_hand = [player.rect.x + player.hand[2][0], player.rect.y + player.hand[2][1]]
        if not player_weapon.animation:
            player_weapon.image = pygame.transform.flip(player_weapon.image_at((0,0,99,99)).image, False, True)
            
    return player, player_hand, player_weapon