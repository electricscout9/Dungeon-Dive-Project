import pygame

class Label(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        
        self.text = text
        self.pos = pos
        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 16)
        
        
def draw_label(labels, screen):
    
    for label in labels:
        
        text = label.font.render(label.text, True, (255,255,255))
        screen.blit(text, label.pos)
        