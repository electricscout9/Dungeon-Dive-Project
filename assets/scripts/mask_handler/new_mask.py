import pygame

def create_mask(obj, mask_colour):
    
    obj.mask = pygame.mask.from_threshold(obj.image, mask_colour, (1, 1, 1,255))
    return obj