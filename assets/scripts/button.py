import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, height, width, img, scale):
        super().__init__()
        
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*scale, self.image.get_height()*scale))
        self.image.set_colorkey((255,255,255))
        
        self.rect = self.image.get_rect()
        
        self.height = height
        self.width = width
        self.state = False
        
    def mouse_click(self):
        
        
        mouse_position = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.state == False:
                self.state = True
                return True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.state = False