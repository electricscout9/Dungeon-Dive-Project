import pygame
from ...scripts.mask_handler.new_mask import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, height, width, img, scale, hand_pos):
        super().__init__()
        
        self.image_folder = img
        
        self.attack = False
        self.health = 0
        
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width*scale, height*scale))
        self.image.set_colorkey((255,255,255))
        
        self.width = width*scale
        self.height = height*scale
        self.hand = [[hand_pos[0][0]*scale, hand_pos[0][1]*scale], [hand_pos[1][0]*scale, hand_pos[1][1]*scale], [hand_pos[2][0]*scale, hand_pos[2][1]*scale]]
        
        self.rect = self.image.get_rect()
        self.direction = 270
        self.direction_last = 270
        
def make_player(path):
    player = Sprite(22, 30, path + "\\assets\\sprites\\player_assets\\crtlnd\\crtlnd.png", 2, [[28,14], [25,9], [23,19]])
    player = create_mask(player, (32,32,31,255))
    player.rect.x = 50
    player.rect.y = 50
    player.health = 3
    return player