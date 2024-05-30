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
        
        self.text_width = (width-10)//10
        
        self.active = False
        
        self.cursor = Textbox_cursor(self)
    
class Textbox_cursor(pygame.sprite.Sprite):
    def __init__(self, textbox):
        super().__init__()
        
        self.rect = pygame.Rect(textbox.rect.x + 5, textbox.rect.y,2, 20)
        
def draw_textbox(boxes, screen):
    
    for box in boxes:
            pygame.draw.rect(screen, box.colour, box.rect)
            
            if len(box.text) > box.text_width:
                if box.text_pos == 0:
                    text = box.text[-box.text_width+box.text_pos:]
                else:
                    text = box.text[-box.text_width+box.text_pos:box.text_pos]
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

def character_entry(event, active_box, cursor_pos):
    cursor_next = False
    if event.key == pygame.K_BACKSPACE:
        if active_box.cursor.rect.x-10 > active_box.rect.x:
            active_box.cursor.rect.x -= 10
            cursor_next = True
        if cursor_pos == len(active_box.text):
            active_box.text = active_box.text[:-1]
            if len(active_box.text) > active_box.text_width and cursor_next:
                active_box.cursor.rect.x += 10
                cursor_next = False
        else:
            active_box.text = active_box.text[:cursor_pos-1] + active_box.text[cursor_pos:]
            if len(active_box.text) > active_box.text_width and cursor_next:
                active_box.cursor.rect.x += 10
    elif event.key == pygame.K_RIGHT:
        if active_box.cursor.rect.x+10 < active_box.rect.x+active_box.width and active_box.cursor.rect.x+10 < len(active_box.text)*10+active_box.rect.x+15: 
            active_box.cursor.rect.x += 10
        else:
            active_box.text_pos += 1
    elif event.key == pygame.K_LEFT:
                    
        if active_box.cursor.rect.x-10 > active_box.rect.x:
            active_box.cursor.rect.x -= 10
        else:
            active_box.text_pos -= 1
    else:
        if active_box.cursor.rect.x+10 < active_box.rect.x+active_box.width and active_box.cursor.rect.x+10 < len(active_box.text)*10+active_box.rect.x+25:
            cursor_next = True
            active_box.cursor.rect.x += 10
        if cursor_pos == len(active_box.text):
            active_box.text += event.unicode
        else:
            active_box.text = active_box.text[:cursor_pos] + event.unicode + active_box.text[cursor_pos:]
            if len(active_box.text) > active_box.text_width and cursor_next:
                active_box.cursor.rect.x -= 10
                cursor_next = False