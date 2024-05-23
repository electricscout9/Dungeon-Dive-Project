import pygame

class Room(pygame.sprite.Sprite):
    def __init__(self, height, width, img, scale):
        super().__init__()
        
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width*scale, height*scale))
        self.image.set_colorkey((255,255,255))
        
        self.width = width*scale
        self.height = height*scale
        
        self.rect = self.image.get_rect()