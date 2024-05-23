#Importing libraries
import pygame
import sqlite3 as sql
import pathlib
import math

#Importing relevant functions
from assets.scripts.player_handler.player_start import *
from assets.scripts.player_handler.player_mov import *
from assets.scripts.mask_handler.new_mask import *
from assets.scripts.menus.main_start.main_menu import *
from assets.scripts.room_handler.room_start import *
from assets.scripts.database.database_start import *
from assets.scripts.button import *
from assets.scripts.weapons import *
from assets.scripts.text_entry import *

#Initialising pygame
pygame.init()
clock = pygame.time.Clock()

#Creating sprite groups
allSprites = pygame.sprite.Group()
weapons = pygame.sprite.Group()
buttons = pygame.sprite.Group()
entities = pygame.sprite.Group()
textboxes = []


#Declaring variables
FPS = 60
a=ord("a") #Character ascii codes
s=ord("s")
d=ord("d")
w=ord("w")
speed = 2  #Player speed
player_hand = [0,0]  #Player hand location
vect_move = [0,0]  #Player movement vector
button_hover = False  #Mouse hovering button
mouse_left_down = 0  #Left mouse button down
running = True
player_free = False
startup = True
background = "White"
current_time = 0
animation_time = 0.05
current_frame = 0

#Starting the database
db = database_initialise()

#Finding location of 'project' folder
path = str(pathlib.Path.cwd())

#Creating the Screen
mainScene = pygame.display.set_mode((800, 600))

#Intitiallising the player character
player = make_player(path)

#Initiallising the first room
room = Room(300, 400, path + "\\assets\\sprites\\rooms\\test_background.png", 2)
room = create_mask(room, (0,0,0,255))

#Initiallising the players weapon
player_weapon = melee_weapon(path + "\\assets\\sprites\\weapons\\sword.png")
player_weapon = player_weapon.image_at(player_weapon.current_rect)

#Initiallising the start screen
play = Button(50, 100, path + "\\assets\\sprites\\start.png", 2)
play.rect.x = 600
play.rect.y = 500
buttons.add(play)
username = Textbox(20, 110, [100,100], (20,20,20), (255,255,255))
textboxes.append(username)
textbox_active = False
active_box = None

notusername = Textbox(20, 110, [100,200], (20,20,20), (255,255,255))
textboxes.append(notusername)


while running:
    
    #Updating the clock and relevant variables
    dt = clock.tick(FPS)/1000
    current_time += dt
    speed = 200*dt
    
    
    #Resetting mouse inputs
    button_hover = False
    mouse_left_down = False
    
    
    #Aquiring mouse states
    mouse_state = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    
    
    #Finding the active text boxes cursor location
    if active_box != None:
        if len(active_box.text) > 10:
            cursor_pos = (active_box.cursor.rect.x-active_box.rect.x+5)//10-11+len(active_box.text)+active_box.text_pos
        else:
            cursor_pos = (active_box.cursor.rect.x-active_box.rect.x+5)//10-1+active_box.text_pos
    
    #Collecting all events since last call
    for event in pygame.event.get():
        
        #Detecting key presses
        if not textbox_active:
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key in [w,a,s,d]:
                    aDown, sDown, dDown, wDown, player = player_input(event, player, current_frame)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active_box.cursor.rect.x-10 > active_box.rect.x:
                        active_box.cursor.rect.x -= 10
                    active_box.text = active_box.text[:-1]
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
                        if len(active_box.text) > 10 and cursor_next:
                            active_box.cursor.rect.x -= 10
                        
        #Detecting exit button pressed
        if event.type == pygame.QUIT:
            running=False
            
        #Detecting mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_left_down = True
                
    
    #Stopping player inputs unless freed    
    if player_free:
        vect_move = vect_set(aDown, sDown, dDown, wDown, speed, player, room, vect_move)
        player_move(player, vect_move, entities)
        
    
    #Detecting if start button pressed
    if play.mouse_click():
        if play in buttons:
            
            #Updating relevant variables and groups on start
            player_free = True
            allSprites.add(player)
            entities.add(room)
            buttons.remove(play)
            weapons.add(player_weapon)
    
    if mouse_left_down:
        
        if active_box != None:
            if len(active_box.text) > 10:
                print((active_box.cursor.rect.x-active_box.rect.x+5)//10-11+active_box.text_pos+len(active_box.text))
            else:
                print((active_box.cursor.rect.x-active_box.rect.x+5)//10-1+active_box.text_pos)
        
        for box in textboxes:
            if textbox_press(mouse_position, box):
                active_box = box
                textbox_active = True
                active_box.active = True
                break
            else:
                if active_box != None:
                    active_box.active = False
                active_box = None
                textbox_active = False
    
    if active_box != None:
        
        if active_box.text_pos > 0:
            active_box.text_pos = 0
        if abs(active_box.text_pos)+10 > len(active_box.text) and len(active_box.text) > 10:
            active_box.text_pos = -len(active_box.text)+10
            
    
    
    #Detecting if mouse cursor is hovering over any active button
    for button in buttons:
        if button.rect.collidepoint(mouse_position):
            button_hover = True
            
    
    #Detecting if player clicked on gameplay area
    if (not button_hover) and mouse_left_down and player_free:
        
        #Creating a vector from the players hand position to the mouse cursor
        hit_direction = [mouse_position[0]-player_hand[0], mouse_position[1]-player_hand[1]]
        
        player.direction_last = player.direction

        #Starting the first frame of players attack animation
        if not player_weapon.animation:
            
            #Updating players direction to follow the previously made vector
            if (hit_direction[0]>0 and hit_direction[0]**2 >= hit_direction[1]**2):
                player.direction = 270
            if (hit_direction[0]<0 and hit_direction[0]**2 >= hit_direction[1]**2):
                player.direction = 90
            if (hit_direction[1]<0 and hit_direction[0]**2 < hit_direction[1]**2):
                player.direction = 0
            if (hit_direction[1]>0 and hit_direction[0]**2 < hit_direction[1]**2):
                player.direction = 180
            
            #Updates the active weapons image to be the second frame of the spritesheet
            player_weapon.current_rect = [player_weapon.current_rect[0] + 100, 0, player_weapon.current_rect[2] + 100, 99]
            player_weapon = player_weapon.image_at(player_weapon.current_rect)
            player_weapon.image = pygame.transform.rotate(player_weapon.image, player.direction)
            player_weapon.rect = player_weapon.image.get_rect()
            
            #Setting time since last animation to 0
            current_time = 0
    
    #Detecting if next frame in the weapons animation is ready to play   
    if current_time >= animation_time and player_weapon.current_rect[0] != 0:
        
        #Detecting if weapons active frame is in range of spritesheet
        if player_weapon.current_rect[2] <= player_weapon.spritesheet.get_width():
            
            #Updates the active weapons image to be the next frame of the spritesheet
            player_weapon.current_rect = [player_weapon.current_rect[0] + 100, 0, player_weapon.current_rect[2] + 100, 99]
            player_weapon = player_weapon.image_at(player_weapon.current_rect)
            player_weapon.image = pygame.transform.rotate(player_weapon.image, player.direction)
            
            #Setting time since last animation to 0
            current_time = 0
        else:
            #Reseting weapons animation if finished
            player_weapon.current_rect = [0,0,99,99]
            
            
    #Detecting if weapon animation is player
    if (current_time >= animation_time) and (player_weapon.current_rect[0] == 0):
        player_weapon.animation = False
    else:
        player_weapon.animation = True
        
    #Sets the player and weapon to the correct orientation
    player, player_hand, player_weapon = player_direction(player, player_hand, player_weapon, path)
    if player.direction == 90  or player.direction == 270:
        player.mask = pygame.mask.from_surface(pygame.Surface((player.image.get_width(), player.image.get_height())))

    #Setting the weapons coordinates to the location of the players hand
    player_weapon.rect.x = player_hand[0]-50
    player_weapon.rect.y = player_hand[1]-50
    
    
    #Reseting scene to background colour
    mainScene.fill(background)
    
    #Updating all sprite groups
    entities.update()
    allSprites.update()
    weapons.update()
    
    #Drawing all sprites groups in relevant order
    entities.draw(mainScene)
    if player.direction != 180:
        weapons.draw(mainScene)
    allSprites.draw(mainScene)
    if player.direction == 180:
        weapons.draw(mainScene)
    buttons.draw(mainScene)
    draw_textbox(textboxes, mainScene)
    
    
    
    #Updates the screen
    pygame.display.flip()

    #Sets the framerate
    clock.tick(FPS)

pygame.quit()
exit()
