import pygame

class Textbox(pygame.sprite.Sprite):
    def __init__(self, height, width, pos, colour, text_colour):
        super().__init__()
        
        self.height = height
        self.width = width
        
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        
        self.colour = colour
        
        self.text = ""
        self.text_pos = 0
        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 16)
        self.text_colour = text_colour
        
        self.active = False
        
        self.cursor = Textbox_cursor(self)
    
class Textbox_cursor(pygame.sprite.Sprite):
    def __init__(self, textbox):
        super().__init__()
        
        self.rect = pygame.Rect(textbox.rect.x + 5, textbox.rect.y,2, 20)
        
def draw_textbox(boxes, screen):
    
    for box in boxes:
            pygame.draw.rect(screen, box.colour, box.rect)
            
            if len(box.text) > 10:
                if box.text_pos == 0:
                    text = box.text[-10+box.text_pos:]
                else:
                    text = box.text[-10+box.text_pos:box.text_pos]
            else:
                text = box.text
            text = box.font.render(text, True, (255,255,255))
            screen.blit(text, (box.rect.x+5, box.rect.y))
            
            if box.active:
                pygame.draw.rect(screen, (150, 150, 150), box.cursor.rect)
        
        
        
        
        
def textbox_press(mouse_location, box):
    
    box_pressed = False
    
    if box.rect.collidepoint(mouse_location):
            box_pressed = True
            
    return box_pressed
    