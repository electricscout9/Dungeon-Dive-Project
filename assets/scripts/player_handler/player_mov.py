import pygame
from math import *

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
        speed = sqrt((speed**2)/2)
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
        
def enemy_move(enemy, player, entities, speed=2):
    
    move_unit_vect = [player.rect.x-enemy.rect.x, player.rect.y-enemy.rect.y]
    magnitude = sqrt(move_unit_vect[0]**2+move_unit_vect[1]**2)
    
    if magnitude == 0:
        magnitude = 1
    move_unit_vect = [move_unit_vect[0]/magnitude, move_unit_vect[1]/magnitude]
    
    move_vect = [move_unit_vect[0]*speed, move_unit_vect[1]*speed]
    
    for current in entities:
        enemy.rect.x += move_vect[0]
        enemy.rect.y += move_vect[1]
        if pygame.sprite.collide_mask(enemy, current):
            enemy.rect.x -= move_vect[0]
            enemy.rect.y -= move_vect[1]
            
            
    if magnitude <= 20:
        enemy.attack = True
    else:
        enemy.attack = False
    
    return enemy
            
        
    
    
        
def entity_direction(entity, entity_hand, entity_weapon):
    
    if entity.direction == 0:
        entity.image = pygame.transform.scale(pygame.image.load((str(entity.image_folder)[:-4]+"_up.png")), (entity.width, entity.height))
        entity_hand = [entity.rect.x + entity.hand[1][0], entity.rect.y + entity.hand[1][1]]
        if not entity_weapon.animation:
            entity_weapon = entity_weapon.image_at((0,0,99,99))
    if entity.direction == 90:
        entity.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load(entity.image_folder), True, False), (entity.width, entity.height))
        entity_hand = [entity.rect.x + (entity.width+1-entity.hand[0][0]), entity.rect.y + entity.hand[0][1]]
        if not entity_weapon.animation:
            entity_weapon.image = pygame.transform.rotate(entity_weapon.image_at((0,0,99,99)).image, 90)
    if entity.direction == 270:
        entity.image = pygame.transform.scale(pygame.image.load(entity.image_folder), (entity.width, entity.height))
        entity_hand = [entity.rect.x + entity.hand[0][0], entity.rect.y + entity.hand[0][1]]
        if not entity_weapon.animation:
            entity_weapon.image = pygame.transform.rotate(entity_weapon.image_at((0,0,99,99)).image, 270)
    if entity.direction == 180:
        entity.image = pygame.transform.scale(pygame.image.load((str(entity.image_folder)[:-4]+"_down.png")), (entity.width, entity.height))
        entity_hand = [entity.rect.x + entity.hand[2][0], entity.rect.y + entity.hand[2][1]]
        if not entity_weapon.animation:
            entity_weapon.image = pygame.transform.flip(entity_weapon.image_at((0,0,99,99)).image, False, True)
            
    return entity, entity_hand, entity_weapon