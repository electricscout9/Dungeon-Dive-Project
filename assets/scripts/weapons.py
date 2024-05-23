import pygame

class melee_weapon(pygame.sprite.Sprite):
    def __init__(self, spritesheet):
        super().__init__()
        
        self.spritesheet = pygame.image.load(spritesheet)
        self.frames = int(self.spritesheet.get_width()/100)
        self.current_rect = [0,0,99,99]
        self.animation = False
        
    def image_at(self, location, colourkey = None):
        
        image = pygame.Surface((100,100), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0,0), location)
        self.image = image
        self.rect = self.image.get_rect()
        
        return self