import pygame

class Image_Button(pygame.sprite.Sprite):
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
            
class Label(pygame.sprite.Sprite):
    def __init__(self, height, width, text, pos, bg_colour):
        super().__init__()
        
        self.height = height
        self.width = width
    
        self.text = text
        self.colour = bg_colour
        self.text_width = (width-10)//10
        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 16)
        
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        
    def mouse_click(self):
        
        
        mouse_position = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.state == False:
                self.state = True
                return True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.state = False
            
def draw_labels(labels, screen):
    for label in labels:
        
        pygame.draw.rect(screen, label.colour, label.rect)
        
        text = label.font.render(label.text, True, (255,255,255))
        
        screen.blit(text, label.rect)