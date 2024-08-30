import pygame
import sqlite3
import random as r
#from assets.scripts.mask_handler.new_mask import *


class Room(pygame.sprite.Sprite):
    def __init__(self, height, width, img, scale):
        super().__init__()
        
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image.set_colorkey((255,255,255))
        
        self.width = width
        self.height = height
        
        self.rect = self.image.get_rect()
        
        
def room_change(player, map_coordinate, room):
    
    changed = False
    
    if player.rect.x > room.width:
        if (map_coordinate[1]+1>=0 and map_coordinate[1]+1<=2):
            map_coordinate[1] += 1
            player.rect.x = 0
            changed = True
    if player.rect.x < 0:
        if (map_coordinate[1]-1>=0 and map_coordinate[1]-1<=2):
            map_coordinate[1] -= 1
            player.rect.x = room.width - player.width
            changed = True
    if player.rect.y > room.height:
        if (map_coordinate[0]+1>=0 and map_coordinate[0]+1<=2):
            map_coordinate[0] += 1
            player.rect.y = 0
            changed = True
    if player.rect.y < 0:
        if (map_coordinate[0]-1>=0 and map_coordinate[0]-1<=2):
            map_coordinate[0] -= 1
            player.rect.y = room.height - player.height
            changed = True
        
    
    
    return player, map_coordinate, changed

def map_rooms(room_map, db):
    
    all_rooms = db.execute("SELECT sprite FROM room_table").fetchall()
    
    temp = all_rooms
    for row in range(len(room_map)):
        for column in range(len(room_map[row])):
            if len(temp) == 0:
                temp = db.execute("SELECT sprite FROM room_table").fetchall()
            room_map[row][column] = temp.pop(r.randint(0,len(temp)-1))[0]
    return room_map