import pygame

class melee_weapon(pygame.sprite.Sprite):
    def __init__(self, path, weapon_data):
        super().__init__()
        
        self.spritesheet = pygame.image.load(path + weapon_data[1])
        self.frames = int(self.spritesheet.get_width()/100)
        self.current_rect = [0,0,99,99]
        self.animation = False
        
        self.damage = float(weapon_data[2])
        
        self.animation_speed = float(weapon_data[3])
                
        self = self.image_at(self.current_rect)
            
    def image_at(self, location, colourkey = None):
        
        image = pygame.Surface((100,100), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0,0), location)
        self.image = image
        self.image = pygame.transform.scale(self.image,(200, 200))
        self.rect = self.image.get_rect()
        
        return self