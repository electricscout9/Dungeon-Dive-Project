#Importing libraries
import pygame
import sqlite3 as sql
import pathlib
import random as r
import datetime
import os.path
from math import *


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
            if pygame.mouse.get_pressed()[0] == 1 :
                return True
            
def draw_labels(labels, screen):
    for label in labels:
        
        pygame.draw.rect(screen, label.colour, label.rect)
        
        text = label.font.render(label.text, True, (255,255,255))
        
        screen.blit(text, label.rect)
        
def multipend(list1, list2):
    for i in list2:
        list1.append(i)
    return list1

class Room(pygame.sprite.Sprite):
    def __init__(self, height, width, img, path, scale, db):
        super().__init__()
        
        self.image = pygame.image.load(path+img)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image.set_colorkey((255,255,255))
        self.enemies = int(db.execute("SELECT enemies FROM room_table WHERE sprite ='" + img + "'").fetchone()[0])
        self.width = width
        self.height = height
        
        self.rect = self.image.get_rect()
        
        
def room_change(player, map_coordinate, room):
    
    changed = False
    
    if player.rect.x > room.width:
        if (map_coordinate[1]+1>=0 and map_coordinate[1]+1<=2):
            map_coordinate[1] += 1
            player.rect.x = 0
            changed = True
    if player.rect.x < 0:
        if (map_coordinate[1]-1>=0 and map_coordinate[1]-1<=2):
            map_coordinate[1] -= 1
            player.rect.x = room.width - player.width
            changed = True
    if player.rect.y > room.height:
        if (map_coordinate[0]+1>=0 and map_coordinate[0]+1<=2):
            map_coordinate[0] += 1
            player.rect.y = 0
            changed = True
    if player.rect.y < 0:
        if (map_coordinate[0]-1>=0 and map_coordinate[0]-1<=2):
            map_coordinate[0] -= 1
            player.rect.y = room.height - player.height
            changed = True
        
    
    
    return player, map_coordinate, changed

def map_rooms(room_map, db):
    
    all_rooms = db.execute("SELECT sprite FROM room_table").fetchall()
    
    temp = all_rooms
    for row in range(len(room_map)):
        for column in range(len(room_map[row])):
            if len(temp) == 0:
                temp = db.execute("SELECT sprite FROM room_table").fetchall()
            room_map[row][column] = temp.pop(r.randint(0,len(temp)-1))[0]
    return room_map

class Textbox(pygame.sprite.Sprite):
    def __init__(self, height, width, pos, colour, text_colour, label):
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
        
        self.label = label
    
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
            
            if box.label != None:
                
                label = box.font.render(box.label, True, (0,0,0))
                label_length = len(box.label) * 10 + 5
                screen.blit(label, (box.rect.x-label_length, box.rect.y))
        
        
        
        
        
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

def database_initialise():
    
        
    if not pathlib.Path("dungeon_dive_DB.db").is_file():
        add_data = True
    else:
        add_data = False
        
    db = sql.connect("dungeon_dive_DB.db")
        
    if add_data:
        db.execute("""CREATE TABLE player_table(
                player_ID TEXT PRIMARY KEY,
                username TEXT,
                password TEXT,
                email TEXT)""")
        
        db.execute("""CREATE TABLE weapon_table(
                weapon_ID TEXT PRIMARY KEY,
                spritesheet TEXT,
                damage TEXT,
                frame_time TEXT)""")
        db.execute("""CREATE TABLE room_table(
                room_ID TEXT PRIMARY KEY,
                sprite TEXT,
                enemies TEXT)""")
        db.execute("""CREATE TABLE enemy_table(
                enemy_ID TEXT PRIMARY KEY,
                sprite TEXT,
                health TEXT)""")
        db.execute("""CREATE TABLE runs_table(
                run_ID TEXT PRIMARY KEY,
                player_ID TEXT,
                score TEXT,
                date TEXT)""")
        
        db.commit()
        
        
        
    return db

def create_mask(obj, mask_colour):
    
    obj.mask = pygame.mask.from_threshold(obj.image, mask_colour, (1, 1, 1,255))
    return obj

aDown = False
sDown = False
dDown = False
wDown = False

def player_input(event, player, current_frame):

    global aDown
    global sDown
    global dDown
    global wDown
    if event.type == pygame.KEYDOWN:
        if chr(event.key) == "a":
            aDown = True

        if chr(event.key) == "w":
            wDown = True

        if chr(event.key) == "s":
            sDown = True

        if chr(event.key) == "d":
             dDown = True

    if event.type == pygame.KEYUP:
        if chr(event.key) == "a":
            aDown = False
        if chr(event.key) == "w":
            wDown = False
        if chr(event.key) == "s":
            sDown = False
        if chr(event.key) == "d":
            dDown = False

    if current_frame == 0:    
        if aDown:
            player.direction = 90
        if dDown:
            player.direction = 270
    
    return aDown, sDown, dDown, wDown, player
        
def vect_set(aDown, sDown, dDown, wDown, speed, player_sprite, room, vect_move):

    if wDown and (aDown or dDown) or sDown and (aDown or dDown):
        speed = sqrt((speed**2)/2)
    if vect_move[0]**2 <= speed**2:
        if aDown:
            vect_move[0] -= speed
        if dDown:
            vect_move[0] += speed
    if vect_move[1]**2 <= speed**2:
        if sDown:
            vect_move[1] += speed
        if wDown:
            vect_move[1] -= speed
            

    return vect_move
        
def player_move(player, vect_move, entities, map_coordinates):
    
    if vect_move[0]**2 < 1:
        vect_move[0] = 0
    if vect_move[1]**2 <1:
        vect_move[1] = 0
        
    for entity in entities:
        player.rect.x += vect_move[0]
        if pygame.sprite.collide_mask(player, entity):
            if ((vect_move[1]==0 and vect_move[0] != 0) or (vect_move[1]!=0 and vect_move[0]==0)) and (player.rect.x <= 790 and player.rect.x >= 10) and (player.rect.y >=10 and player.rect.y <= 590):
                for displace in range(5):
                    player.rect.y += displace
                    if not pygame.sprite.collide_mask(player, entity):
                        break
                    player.rect.y -= displace
                for displace in range(5):
                    player.rect.y -= displace
                    if not pygame.sprite.collide_mask(player, entity):
                        break
                    player.rect.y += displace
            #if pygame.sprite.collide_mask(player, entity):
            #    player.rect.x -= vect_move[0]
            #    vect_move[0] = 0
        player.rect.y += vect_move[1]
        if pygame.sprite.collide_mask(player, entity):
            if ((vect_move[1]==0 and vect_move[0] != 0) or (vect_move[1]!=0 and vect_move[0]==0)) and (player.rect.x <= 790 and player.rect.x >= 10) and (player.rect.y >=10 and player.rect.y <= 590):
                for displace in range(5):
                    player.rect.x += displace
                    if not pygame.sprite.collide_mask(player, entity):
                        break
                    player.rect.x -= displace
                for displace in range(5):
                    player.rect.x -= displace
                    if not pygame.sprite.collide_mask(player, entity):
                        break
                    player.rect.x += displace
            #if pygame.sprite.collide_mask(player, entity):
            #    player.rect.y -= vect_move[1]
            #    vect_move[1] = 0
    
    if player.rect.x < 0:
        if map_coordinates[1] == 0:
            player.rect.x = 1
    if player.rect.y < 0:
        if map_coordinates[0] == 0:
            player.rect.y = 1
    if player.rect.x + player.width > 800:
        if map_coordinates[1] == 2:
            player.rect.x = 799-player.width
    if player.rect.y + player.height > 600:
        if map_coordinates[0] == 2:
            player.rect.y = 599-player.height
    
    
    
    if vect_move[0] < 0:
        vect_move[0] += 1
    elif vect_move[0] >0:
        vect_move[0] -= 1
    if vect_move[1] < 0 :
        vect_move[1] += 1
    elif vect_move[1] >0:
        vect_move[1] -= 1
        
def enemy_move(enemy, player, entities, speed=2):
    
    move_unit_vect = [player.rect.x-enemy.rect.x, player.rect.y-enemy.rect.y]
    magnitude = sqrt(move_unit_vect[0]**2+move_unit_vect[1]**2)
    
    if magnitude == 0:
        magnitude = 1
    move_unit_vect = [move_unit_vect[0]/magnitude, move_unit_vect[1]/magnitude]
    
    move_vect = [move_unit_vect[0]*speed, move_unit_vect[1]*speed]
    
    for current in entities:
        enemy.rect.x += move_vect[0]
        enemy.rect.y += move_vect[1]
        if pygame.sprite.collide_mask(enemy, current):
            enemy.rect.x -= move_vect[0]
            enemy.rect.y -= move_vect[1]
            
            
    if magnitude <= 20:
        enemy.attack = True
    else:
        enemy.attack = False
    
    return enemy
            
        
    
    
        
def entity_direction(entity, entity_hand, entity_weapon):
    
    if entity.direction == 0:
        entity.image = pygame.transform.scale(pygame.image.load((str(entity.image_folder)[:-4]+"_up.png")), (entity.width, entity.height))
        entity_hand = [entity.rect.x + entity.hand[1][0], entity.rect.y + entity.hand[1][1]]
        if not entity_weapon.animation:
            entity_weapon = entity_weapon.image_at((0,0,99,99))
    if entity.direction == 90:
        entity.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load(entity.image_folder), True, False), (entity.width, entity.height))
        entity_hand = [entity.rect.x + (entity.width+1-entity.hand[0][0]), entity.rect.y + entity.hand[0][1]]
        if not entity_weapon.animation:
            entity_weapon.image = pygame.transform.rotate(entity_weapon.image_at((0,0,99,99)).image, 90)
    if entity.direction == 270:
        entity.image = pygame.transform.scale(pygame.image.load(entity.image_folder), (entity.width, entity.height))
        entity_hand = [entity.rect.x + entity.hand[0][0], entity.rect.y + entity.hand[0][1]]
        if not entity_weapon.animation:
            entity_weapon.image = pygame.transform.rotate(entity_weapon.image_at((0,0,99,99)).image, 270)
    if entity.direction == 180:
        entity.image = pygame.transform.scale(pygame.image.load((str(entity.image_folder)[:-4]+"_down.png")), (entity.width, entity.height))
        entity_hand = [entity.rect.x + entity.hand[2][0], entity.rect.y + entity.hand[2][1]]
        if not entity_weapon.animation:
            entity_weapon.image = pygame.transform.flip(entity_weapon.image_at((0,0,99,99)).image, False, True)
            
    return entity, entity_hand, entity_weapon

class Sprite(pygame.sprite.Sprite):
    def __init__(self, height, width, img, scale, hand_pos):
        super().__init__()
        
        self.image_folder = img
        
        self.attack = False
        self.health = 0
        
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width*scale, height*scale))
        self.image.set_colorkey((255,255,255))
        
        self.width = width*scale
        self.height = height*scale
        self.hand = [[hand_pos[0][0]*scale, hand_pos[0][1]*scale], [hand_pos[1][0]*scale, hand_pos[1][1]*scale], [hand_pos[2][0]*scale, hand_pos[2][1]*scale]]
        
        self.rect = self.image.get_rect()
        self.direction = 270
        self.direction_last = 270
        

        
def make_player(path):
    player = Sprite(22, 30, path + "\\assets\\sprites\\player_assets\\crtlnd\\crtlnd.png", 2, [[28,14], [25,9], [23,19]])
    player = create_mask(player, (32,32,31,255))
    player.rect.x = 50
    player.rect.y = 50
    player.health = 3
    return player

#Initialising pygame
pygame.init()
clock = pygame.time.Clock()

#Creating sprite groups
allSprites = pygame.sprite.Group()
weapons = pygame.sprite.Group()
buttons = pygame.sprite.Group()
entities = pygame.sprite.Group()
textboxes = []
labels = []
enemies = pygame.sprite.Group()

#Starting the database
db = database_initialise()


#Declaring variables
FPS = 60
a=ord("a") #Character ascii codes
s=ord("s")
d=ord("d")
w=ord("w")
speed = 5 #Player speed
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
start_type = ""
player_data = ()
devmode = True
first = True
player_invulnerable = 0
score = 0
current_floor = []
total_rooms_visited = 0
changed_room = True
last_room = []

room_width = 800
room_height = 600

room_map = [[None,None,None],
            [None,None,None],
            [None,None,None]]
room_map = map_rooms(room_map, db)
map_coordinate = [1,1]


#Finding location of 'project' folder
path = str(pathlib.Path.cwd())

#Creating the Screen
mainScene = pygame.display.set_mode((800, 600))

#Intitiallising the player character
player = make_player(path)

room = Room(room_height, room_width, room_map[map_coordinate[0]][map_coordinate[1]],path, 2, db)
room = create_mask(room, (0,0,0,255))



#Initiallising the players weapon
player_weapon_data = db.execute("SELECT * FROM weapon_table WHERE weapon_ID ='001'").fetchone()
player_weapon = melee_weapon(path, player_weapon_data)

#Initiallising the start screen
login = Label(20,60,"Log In", (400,200), (0,0,0))

signup = Label(20, 70, "Sign Up", (400,300), (0,0,0))

enter = Label(20, 50, "Enter", (600, 500), (0,0,0))

health = Label(20, 90, ("Health:" + str(player.health)), (710, 0), (0,0,0))

rooms_visited = Label(20, 100, ("Rooms:" + str(total_rooms_visited)), (80, 0), (0,0,0))

floors = Label(20, 80, ("Floor: 1"), (0, 0), (0,0,0))


labels.append(login)
labels.append(signup)



username = Textbox(20, 110, [100,100], (20,20,20), (255,255,255), "Username:")

textbox_active = False
active_box = None

password = Textbox(20, 110, [100,130], (20,20,20), (255,255,255), "Password:")

email = Textbox(20, 110, [100,160], (20,20,20), (255,255,255), "Email:")


while running:
    
    while player.health > 0:
    
        #Updating the clock and relevant variables
        dt = clock.tick(FPS)/1000
        current_time += dt
        speed = 500*dt
        player_invulnerable -= dt
        
        
        animation_time = player_weapon.animation_speed
        
        
        #Resetting mouse inputs
        button_hover = False
        mouse_left_down = False
            
        
        if len(current_floor) == 9 and len(enemies) == 0:
            score += 50
            room_map = [[None,None,None],
                        [None,None,None],
                        [None,None,None]]
            room_map = map_rooms(room_map, db)
            map_coordinate = [1,1]
            current_floor = []
            changed_room = True
            last_room = []
            floors.text = "Floor:" +str(((total_rooms_visited)//9)+1)
        
        
        if changed_room and player_free:
            
            if enemies:
                all_killed = False
            else:
                all_killed = True
            entities.remove(room)
            room = Room(room_height, room_width, room_map[map_coordinate[0]][map_coordinate[1]],path, 2, db)
            entities.add(room)
            changed_room = False
            room = create_mask(room, (0,0,0,255))
            

            enemies = pygame.sprite.Group()
            
            if (last_room not in current_floor) and all_killed and last_room != []:
                score += 25
                total_rooms_visited += 1
                current_floor.append(last_room)
                
            if not (map_coordinate in current_floor):
                
                for i in range(room.enemies):
                    enemy_data = db.execute("SELECT * FROM enemy_table ORDER BY RANDOM() LIMIT 1").fetchone()
                    i = Sprite(16,16, path + enemy_data[1], 3, [[10,10],[10,10],[10,10]])
                    i.health = int(enemy_data[2])
                    
                    enemy_colliding = True
                    
                    while enemy_colliding:
                        enemy_colliding = False
                        i.rect.x = r.randint(0,800)
                        i.rect.y = r.randint(0,600)
                        for current in entities:
                            if pygame.sprite.collide_mask(i, current):
                                enemy_colliding = True
                    
                    enemies.add(i)
        if player_free:  
            last_room = list(map_coordinate)
            player, map_coordinate, changed_room = room_change(player, map_coordinate, room)
            
                
        rooms_visited.text = str("Rooms:" + str(total_rooms_visited))
        
        

        for enemy in enemies:
            enemy = enemy_move(enemy, player, entities)
            if enemy.attack and player_invulnerable <= 0 and enemy.alive:
                player_invulnerable = 0.7
                player.health -= 1
        
        #Aquiring mouse states
        mouse_state = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        
        
        #Finding the active text boxes cursor location
        if active_box != None:
            if len(active_box.text) > active_box.text_width:
                cursor_pos = (active_box.cursor.rect.x-active_box.rect.x+5)//10-(active_box.text_width+1)+len(active_box.text)+active_box.text_pos
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
                    character_entry(event, active_box, cursor_pos)    
                            
            #Detecting exit button pressed
            if event.type == pygame.QUIT:
                running = False
                player.health = 0
                
                
            #Detecting mouse button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_left_down = True
                    
                    for enemy in enemies:
                        magnitude = sqrt((player.rect.x-enemy.rect.x)**2 + (player.rect.y-enemy.rect.y)**2)
                        if magnitude <= 100:
                            enemy.health -= 1
                            if enemy.health == 0:
                                score += 10
                                enemies.remove(enemy)


        #Stopping player inputs unless freed    
        if player_free:
            vect_move = vect_set(aDown, sDown, dDown, wDown, speed, player, room, vect_move)
            player_move(player, vect_move, entities, map_coordinate)


        #Detecting if start button pressed
        if signup.mouse_click():
            if signup in labels:
                start_type = "signup"
                labels = []
                labels.append(enter)
                textboxes.append(username)
                textboxes.append(password)
                textboxes.append(email)
                
                    
        if login.mouse_click():
            if login in labels:
                start_type = "login"
                labels = []
                labels.append(enter)
                textboxes.append(username)
                textboxes.append(password)

        if enter.mouse_click():
            if enter in labels:
                if start_type == "signup":
                    #Adding user entry to database
                    user_ID = str(r.randint(0,9)) + str(r.randint(0,9)) + chr(r.randint(65, 90)) + chr(r.randint(65, 90))
                    player_data = (user_ID, username.text, password.text, email.text)
                    db.execute("INSERT INTO player_table VALUES(?,?,?,?)", player_data)
                    db.commit()
                    
                    #Updating relevant variables and groups on start
                    textboxes = []
                    player_free = True
                    allSprites.add(player)
                    entities.add(room)
                    labels = []
                    labels.append(health)
                    labels.append(floors)
                    labels.append(rooms_visited)
                    weapons.add(player_weapon)
                    
                if start_type == "login":
                    test_data = db.execute("SELECT * FROM player_table").fetchall()
                    for current in test_data:
                        if username.text in current and password.text in current:
                            #Updating relevant variables and groups on start
                            textboxes = []
                            player_free = True
                            allSprites.add(player)
                            entities.add(room)
                            
                            labels = []
                            labels.append(health)
                            labels.append(floors)
                            labels.append(rooms_visited)
                            weapons.add(player_weapon)
                            player_data = current
                            break
                        else:
                            warning = Label(20, 230, "Wrong Username/Password", (550, 460), (60,0,0))
                            labels.append(warning)
                            warning_2 = Label(20,230, "Please Try Again", (550, 480), (60,0,0))
                            labels.append(warning_2)
                
                active_box = None
                textbox_active = False
                    
        if mouse_left_down:
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
            if abs(active_box.text_pos)+active_box.text_width > len(active_box.text) and len(active_box.text) > active_box.text_width:
                active_box.text_pos = -len(active_box.text)+active_box.text_width
                
        
        
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
        player, player_hand, player_weapon = entity_direction(player, player_hand, player_weapon)
        if player.direction == 90  or player.direction == 270:
            player.mask = pygame.mask.from_surface(pygame.Surface((player.image.get_width(), player.image.get_height())))

        #Setting the weapons coordinates to the location of the players hand
        player_weapon.rect.x = player_hand[0]-100
        player_weapon.rect.y = player_hand[1]-100
        
        health.text = "Health: " + str(player.health)
        
        #Reseting scene to background colour
        mainScene.fill(background)
        
        #Updating all sprite groups
        entities.update()
        allSprites.update()
        weapons.update()
        enemies.update()
        
        #Drawing all sprites groups in relevant order
        entities.draw(mainScene)
        enemies.draw(mainScene)
        if player.direction != 180:
            weapons.draw(mainScene)
        allSprites.draw(mainScene)
        if player.direction == 180:
            weapons.draw(mainScene)
        buttons.draw(mainScene)
        draw_labels(labels, mainScene)
        draw_textbox(textboxes, mainScene)
        
        
        
        #Updates the screen
        pygame.display.flip()
        
        #Sets the framerate
        clock.tick(FPS)
    
    if not running:
        break
    
    allSprites = pygame.sprite.Group()
    weapons = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    textboxes = []
    labels = []
    enemies = pygame.sprite.Group()
    player.rect.x = 50
    player.rect.y = 50
    current_floor = []
    total_rooms_visited = 0
    changed_room = True
    last_room = []
    
    entities.update()
    allSprites.update()
    weapons.update()
    enemies.update()
    
    cont = Label(20,90,"Continue?", (355,420), (0,0,0))
    
    player_ID = db.execute("SELECT player_ID FROM player_table WHERE username ='" + username.text + "'").fetchone()
    
    player_scores = db.execute("SELECT score FROM runs_table WHERE player_ID ='" + player_ID[0] + "'").fetchall()

    
    if len(player_scores) == 1:
        highscore = player_scores[0][0]
    elif len(player_scores) == 0:
        highscore = str(0)
    else:
        highscore = sorted(player_scores)[-1][0]


    score_label = Label(20,70+(10 * len(str(score))),("Score: " + str(score)), (375,260), (0,0,0))
    highscore_label = Label(20,110+(10*len(str(highscore))),("Highscore: " + str(highscore)), (355,280), (0,0,0))
    
    labels.append(cont)
    labels.append(highscore_label)
    labels.append(score_label)
    
    mainScene.fill((255,255,255))
    draw_labels(labels, mainScene)
    pygame.display.flip()
    
    total_runs = len(db.execute("SELECT run_ID FROM runs_table").fetchall())
    
    run_ID = str(total_runs+1)
    while len(run_ID) < 3:
        run_ID = "0" + run_ID

    date = str(datetime.datetime.now())
    
    db.execute("INSERT INTO runs_table VALUES(?,?,?,?)", [run_ID, player_ID[0], str(score), date[0:10]])
    db.commit()
    
    play_again = False
    while not play_again:
        
        for event in pygame.event.get():
            #Detecting exit button pressed
            if event.type == pygame.QUIT:
                running = False
                play_again= True
                player.health = 0
                
        if cont.mouse_click():
            play_again = True
            player.health = 3
        
    textboxes = []
    player_free = True
    allSprites.add(player)
    entities.add(room)
    labels = []
    labels.append(health)
    labels.append(floors)
    labels.append(rooms_visited)
    weapons.add(player_weapon)
    score = 0
        
    
    
pygame.quit()

def dev_initialise():
    
    print("\n\n================================================================================")
    print("Please choose a table to manage:")
    print("================================================================================")
    print("1-Player Table")
    print("2-Weapon Table")
    print("3-Room Table")
    print("4-Enemy Table")
    print("5-Runs Table")
    
    selection = input("Option: ")
    return selection


def verify(text, cases):
    if cases == 1:
        try:
            text = int(text) / 1
        except:
            return False
        else:
            return True
    if cases == "":
        try:
            text = text + ""
        except:
            return False
        else:
            return True
    if cases == []:
        try:
            temp_path = path + text
        except:
            return False
        else:
            if os.path.isfile(temp_path):
                return True
            else:
                return False


def input_row(row):
    
    new = []
    
    print("\n\n================================================================================")
    for thing in row:
        next = input("Please enter the "+ str(thing[0]) + ":")
        while not verify(next, thing[1]):
            print("Invalid Input")
            next = input("Please enter the "+ str(thing[0]) + ":")
        new.append(next)
    
    return new
    

def print_player_table(table_data):
    
    username_max = len(table_data[0][1])
    password_max = len(table_data[0][2])
    email_max = len(table_data[0][3])
    
    if not isinstance(table_data[0], str):
        for row in table_data:
            
            if len(row[1]) > username_max:
                username_max = len(row[1])
            if len(row[2]) > password_max:
                password_max = len(row[2])
            if len(row[3]) > email_max:
                email_max = len(row[3])
    else:
        if len(table_data[1]) > username_max:
            username_max = len(table_data[1])
        if len(table_data[2]) > password_max:
            password_max = len(table_data[2])
        if len(table_data[3]) > email_max:
            email_max = len(table_data[3])
            
    if username_max >= 9:
        username_max -= 8
    if password_max >= 8:
        password_max -= 8
    if email_max >= 5:
        email_max -= 5
        
    
    print("\n\n================================================================================")
    print("Player_ID|Username"+username_max*" "+"|Password"+password_max*" "+"|Email"+email_max*" "+"|")
    print("---------|--------"+username_max*"-"+"|--------"+password_max*"-"+"|-----"+email_max*"-"+"|")
        
    if not isinstance(table_data[0], str):
        for row in table_data:
            print(""+row[0]+"     |", end="")
            print(row[1]+(username_max-len(row[1])+8)*" "+"|", end="")
            print(row[2]+(password_max-len(row[2])+8)*" "+"|", end="")
            print(row[3]+(email_max-len(row[3])+5)*" "+"|")
    else:
        print(""+table_data[0]+"     |", end="")
        print(table_data[1]+(username_max-len(table_data[1])+8)*" "+"|", end="")
        print(table_data[2]+(password_max-len(table_data[2])+8)*" "+"|", end="")
        print(table_data[3]+(email_max-len(table_data[3])+5)*" "+"|")

def player_table(player_table_active):

    player_table_data = db.execute("SELECT * FROM player_table").fetchall()

    print("\n\n================================================================================")
    print("Please choose an action to perform on the player table:")
    print("================================================================================")
    print("1-View All Data")
    print("2-Add New Row")
    print("3-Edit Existing Row")
    print("4-Delete Row")
    print("5-Exit To Tables Viewer")
    
    selection = input("Option: ")
    
    if selection == "1":
        
        print_player_table(player_table_data)
    
    elif selection == "2":
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:
            
            new_row = [str(r.randint(0,9)) + str(r.randint(0,9)) + chr(r.randint(65, 90)) + chr(r.randint(65, 90))] + input_row([["Username", ""], ["Password",""], ["Email",""]])

            print_player_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
            db.execute("INSERT INTO player_table VALUES(?,?,?,?)", new_row)
            db.commit()
            
            print("\n================================================================================")
            print("Row Successfully Added!")
            print("================================================================================")
    
    elif selection == "3":
            
        print("\n\n================================================================================")
        print("Choose a row to edit:")
        print("================================================================================")
        
        print_player_table(player_table_data)
            
        selected_ID = input("Enter ID: ").upper()
        
        selected_row = db.execute(f"SELECT * FROM player_table WHERE player_ID='{selected_ID}'").fetchone()
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:
            
            new_row = [selected_row[0]] + input_row([["Username", ""], ["Password",""], ["Email",""]])

            print_player_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
            db.execute(f"DELETE FROM player_table WHERE player_ID='{new_row[0]}'")
            db.execute(f"INSERT INTO player_table VALUES(?,?,?,?)", new_row)
            db.commit()
            
            print("================================================================================")
            print("Row Successfully Changed!")
            print("================================================================================")
        
    elif selection == "4":
        
        print("\n\n================================================================================")
        print("Choose a row to delete:")
        print("================================================================================")
        
        print_player_table(player_table_data)
            
        selected_ID = input_row([["User ID", ""]]).upper()
        
        selected_row = db.execute(f"SELECT * FROM player_table WHERE player_ID='{selected_ID}'").fetchone()
        
        confirmation = input(f"\nAre you sure you wish to delete the row with ID {selected_ID}(Y/N): ")
        
        confirmed_valid = False
        
        while not confirmed_valid:
                if confirmation.upper() == "Y":
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
        db.execute(f"DELETE FROM player_table WHERE player_ID='{selected_ID}'")
        db.commit()
            
        print("================================================================================")
        print("Row Successfully Deleted!")
        print("================================================================================")
    elif selection == "5":
        
        player_table_active = False
    return player_table_active

def print_weapon_table(table_data):
    
    if not isinstance(table_data[0], str):
        
        spritesheet_max = len(table_data[0][1])
        damage_max = len(table_data[0][2])
        frame_time_max = len(table_data[0][3])
        
        for row in table_data:
            
            if len(row[1]) > spritesheet_max:
                spritesheet_max = len(row[1])
            if len(row[2]) > damage_max:
                damage_max = len(row[2])
            if len(row[3]) > frame_time_max:
                frame_time_max = len(row[3])
    else:
        
        spritesheet_max = len(table_data[1])
        damage_max = len(table_data[2])
        frame_time_max = len(table_data[3])
        
        if len(table_data[1]) > spritesheet_max:
            spritesheet_max = len(table_data[1])
        if len(table_data[2]) > damage_max:
            damage_max = len(table_data[2])
        if len(table_data[3]) > frame_time_max:
            frame_time_max = len(table_data[3])
            
    if spritesheet_max >= 12:
        spritesheet_max -= 11
    if damage_max >= 6:
        damage_max -= 6
    if frame_time_max >= 10:
        frame_time_max -= 10
        
    
    print("\n\n================================================================================")
    print("Weapon_ID|Spritesheet"+spritesheet_max*" "+"|Damage"+damage_max*" "+"|Frame Time"+frame_time_max*" "+"|")
    print("---------|-----------"+spritesheet_max*"-"+"|------"+damage_max*"-"+"|----------"+frame_time_max*"-"+"|")
        
    if not isinstance(table_data[0], str):
        for row in table_data:
            print(""+row[0]+"      |", end="")
            print(row[1]+(spritesheet_max-len(row[1])+11)*" "+"|", end="")
            print(row[2]+(damage_max-len(row[2])+6)*" "+"|", end="")
            print(row[3]+(frame_time_max-len(row[3])+10)*" "+"|")
    else:
        print(""+table_data[0]+"      |", end="")
        print(table_data[1]+(spritesheet_max-len(table_data[1])+11)*" "+"|", end="")
        print(table_data[2]+(damage_max-len(table_data[2])+6)*" "+"|", end="")
        print(table_data[3]+(frame_time_max-len(table_data[3])+10)*" "+"|")

def weapon_table(weapon_table_active):
      
    weapon_table_data = db.execute("SELECT * FROM weapon_table").fetchall()

    print("\n\n================================================================================")
    print("Please choose an action to perform on the weapon table:")
    print("================================================================================")
    print("1-View All Data")
    print("2-Add New Row")
    print("3-Edit Existing Row")
    print("4-Delete Row")
    print("5-Exit To Tables Viewer")
    
    selection = input("Option: ")
    
    
    if selection == "1":
        
        print_weapon_table(weapon_table_data)
    
    elif selection == "2":
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:
            
            new_row = input_row([["ID", ""],["Spritesheet",[]], ["Damage",1], ["Frame Time",1]])
            
            print_weapon_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
        db.execute("INSERT INTO weapon_table VALUES(?,?,?,?)", new_row)
        db.commit()
            
        print("\n================================================================================")
        print("Row Successfully Added!")
        print("================================================================================")
    
    elif selection == "3":
            
        print("\n\n================================================================================")
        print("Choose a row to edit:")
        print("================================================================================")
        
        print_weapon_table(weapon_table_data)
            
        selected_ID = input("Enter ID: ").upper()
        
        selected_row = db.execute(f"SELECT * FROM weapon_table WHERE weapon_ID='{selected_ID}'").fetchone()
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:
          
            
            new_row = [selected_row[0]] + input_row([["Spritesheet",[]], ["Damage",1], ["Frame Time",1]])

            print_weapon_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
            db.execute(f"DELETE FROM weapon_table WHERE weapon_ID='{new_row[0]}'")
            db.execute(f"INSERT INTO weapon_table VALUES(?,?,?,?)", new_row)
            db.commit()
            
            print("================================================================================")
            print("Row Successfully Changed!")
            print("================================================================================")
        
    elif selection == "4":
        
        print("\n\n================================================================================")
        print("Choose a row to delete:")
        print("================================================================================")
        
        print_weapon_table(weapon_table_data)
            
        selected_ID = input_row([["ID", ""]]).upper()
        
        selected_row = db.execute(f"SELECT * FROM weapon_table WHERE weapon_ID='{selected_ID}'").fetchone()
        
        confirmation = input(f"\nAre you sure you wish to delete the row with ID {selected_ID}(Y/N): ")
        
        confirmed_valid = False
        
        while not confirmed_valid:
                if confirmation.upper() == "Y":
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
        db.execute(f"DELETE FROM weapon_table WHERE weapon_ID='{selected_ID}'")
        db.commit()
            
        print("================================================================================")
        print("Row Successfully Deleted!")
        print("================================================================================")
    elif selection == "5":
        
        weapon_table_active = False
    return weapon_table_active


def print_room_table(table_data):
    
    if not isinstance(table_data[0], str):
        
        sprite_max = len(table_data[0][1])
        enemies_max = len(table_data[0][2])
        
        for row in table_data:
            
            if len(row[1]) > sprite_max:
                sprite_max = len(row[1])
            if len(row[2]) > enemies_max:
                enemies_max = len(row[2])

    else:
        
        sprite_max = len(table_data[1])
        enemies_max = len(table_data[2])
        
        if len(table_data[1]) > sprite_max:
            sprite_max = len(table_data[1])
        if len(table_data[2]) > enemies_max:
            enemies_max = len(table_data[2])

    if sprite_max >= 7:
        sprite_max -= 6
    if enemies_max >= 7:
        enemies_max -= 7

        
    
    print("\n\n================================================================================")
    print("Room_ID|Sprite"+sprite_max*" "+"|Enemies"+enemies_max*" "+"|")
    print("-------|------"+sprite_max*"-"+"|-------"+enemies_max*"-"+"|")
        
    if not isinstance(table_data[0], str):
        for row in table_data:
            print(""+row[0]+"    |", end="")
            print(row[1]+(sprite_max-len(row[1])+6)*" "+"|", end="")
            print(row[2]+(enemies_max-len(row[2])+7)*" "+"|")

    else:
        print(""+table_data[0]+"    |", end="")
        print(table_data[1]+(sprite_max-len(table_data[1])+6)*" "+"|", end="")
        print(table_data[2]+(enemies_max-len(table_data[2])+7)*" "+"|")
 
def room_table(room_table_active):
      
    room_table_data = db.execute("SELECT * FROM room_table").fetchall()

    print("\n\n================================================================================")
    print("Please choose an action to perform on the room table:")
    print("================================================================================")
    print("1-View All Data")
    print("2-Add New Row")
    print("3-Edit Existing Row")
    print("4-Delete Row")
    print("5-Exit To Tables Viewer")
    
    selection = input("Option: ")
    
    if selection == "1":
        
        print_room_table(room_table_data)
    
    elif selection == "2":
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:
            
            new_row = input_row([["ID",""], ["Sprite",[]], ["# Enemies",1]])
            print_room_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
        db.execute("INSERT INTO room_table VALUES(?,?,?)", new_row)
        db.commit()
            
        print("\n================================================================================")
        print("Row Successfully Added!")
        print("================================================================================")
    
    elif selection == "3":
            
        print("\n\n================================================================================")
        print("Choose a row to edit:")
        print("================================================================================")
        
        print_room_table(room_table_data)
            
        selected_ID = input("Enter ID: ").upper()
        
        selected_row = db.execute(f"SELECT * FROM room_table WHERE room_ID='{selected_ID}'").fetchone()
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:

            new_row = [selected_row[0]] + input_row(["ID", "Sprite", "# Enemies"])

            print_room_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
            db.execute(f"DELETE FROM room_table WHERE room_ID='{new_row[0]}'")
            db.execute(f"INSERT INTO room_table VALUES(?,?,?,?)", new_row)
            db.commit()
            
            print("================================================================================")
            print("Row Successfully Changed!")
            print("================================================================================")
        
    elif selection == "4":
        
        print("\n\n================================================================================")
        print("Choose a row to delete:")
        print("================================================================================")
        
        print_room_table(room_table_data)
            
        selected_ID = input("Enter ID: ").upper()
        
        selected_row = db.execute(f"SELECT * FROM room_table WHERE room_ID='{selected_ID}'").fetchone()
        
        confirmation = input(f"\nAre you sure you wish to delete the row with ID {selected_ID}(Y/N): ")
        
        confirmed_valid = False
        
        while not confirmed_valid:
                if confirmation.upper() == "Y":
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
        db.execute(f"DELETE FROM room_table WHERE room_ID='{selected_ID}'")
        db.commit()
            
        print("================================================================================")
        print("Row Successfully Deleted!")
        print("================================================================================")
    elif selection == "5":
        
        room_table_active = False
    return room_table_active       


def print_enemy_table(table_data):
    
    if not isinstance(table_data[0], str):
        
        sprite_max = len(table_data[0][1])
        health_max = len(table_data[0][2])
        
        for row in table_data:
            
            if len(row[1]) > sprite_max:
                sprite_max = len(row[1])
            if len(row[2]) > health_max:
                health_max = len(row[2])

    else:
        
        sprite_max = len(table_data[1])
        health_max = len(table_data[2])
        
        if len(table_data[1]) > sprite_max:
            sprite_max = len(table_data[1])
        if len(table_data[2]) > health_max:
            health_max = len(table_data[2])

    if sprite_max >= 7:
        sprite_max -= 6
    if health_max >= 7:
        health_max -= 6
    
    print("\n\n================================================================================")
    print("Enemy_ID|Sprite"+sprite_max*" "+"|Health|")
    print("--------|------"+sprite_max*"-"+"|------|")
        
    if not isinstance(table_data[0], str):
        for row in table_data:
            print(""+row[0]+"     |", end="")
            print(row[1]+(sprite_max-len(row[1])+6)*" "+"|", end="")
            print(row[2]+(health_max-len(row[2])+4)*" "+"|")
            
    else:
        print(""+table_data[0]+"    |", end="")
        print(table_data[1]+(sprite_max-len(table_data[1])+6)*" "+"|", end="")
        print(table_data[2]+(health_max-len(table_data[2])+4)*" "+"|")
 
def enemy_table(enemy_table_active):
      
    enemy_table_data = db.execute("SELECT * FROM enemy_table").fetchall()

    print("\n\n================================================================================")
    print("Please choose an action to perform on the enemy table:")
    print("================================================================================")
    print("1-View All Data")
    print("2-Add New Row")
    print("3-Edit Existing Row")
    print("4-Delete Row")
    print("5-Exit To Tables Viewer")
    
    selection = input("Option: ")
    
    if selection == "1":
        
        print_enemy_table(enemy_table_data)
    
    elif selection == "2":
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:
            
            new_row = input_row([["ID",""], ["Sprite",[]], ["Health",1]])
            print_enemy_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
        db.execute("INSERT INTO enemy_table VALUES(?,?,?)", new_row)
        db.commit()
            
        print("\n================================================================================")
        print("Row Successfully Added!")
        print("================================================================================")
    
    elif selection == "3":
            
        print("\n\n================================================================================")
        print("Choose a row to edit:")
        print("================================================================================")
        
        print_enemy_table(enemy_table_data)
            
        selected_ID = input("Enter ID: ").upper()
        
        selected_row = db.execute(f"SELECT * FROM enemy_table WHERE enemy_ID='{selected_ID}'").fetchone()
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:

            new_row = [selected_row[0]] + input_row(["ID", "Sprite", "Health"])

            print_enemy_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
            db.execute(f"DELETE FROM enemy_table WHERE enemy_ID='{new_row[0]}'")
            db.execute(f"INSERT INTO enemy_table VALUES(?,?,?,?)", new_row)
            db.commit()
            
            print("================================================================================")
            print("Row Successfully Changed!")
            print("================================================================================")
        
    elif selection == "4":
        
        print("\n\n================================================================================")
        print("Choose a row to delete:")
        print("================================================================================")
        
        print_enemy_table(enemy_table_data)
            
        selected_ID = input("Enter ID: ").upper()
        
        selected_row = db.execute(f"SELECT * FROM enemy_table WHERE enemy_ID='{selected_ID}'").fetchone()
        
        confirmation = input(f"\nAre you sure you wish to delete the row with ID {selected_ID}(Y/N): ")
        
        confirmed_valid = False
        
        while not confirmed_valid:
                if confirmation.upper() == "Y":
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
        db.execute(f"DELETE FROM enemy_table WHERE enemy_ID='{selected_ID}'")
        db.commit()
            
        print("================================================================================")
        print("Row Successfully Deleted!")
        print("================================================================================")
    elif selection == "5":
        
        enemy_table_active = False
    return enemy_table_active

#############

def print_runs_table(table_data):
    
    player_ID_max = len(table_data[0][1])
    score_max = len(table_data[0][2])
    date_max = len(table_data[0][3])
    
    if not isinstance(table_data[0], str):
        for row in table_data:
            
            if len(row[1]) > player_ID_max:
                player_ID_max = len(row[1])
            if len(row[2]) > score_max:
                score_max = len(row[2])
            if len(row[3]) > date_max:
                date_max = len(row[3])
    else:
        if len(table_data[1]) > player_ID_max:
            player_ID_max = len(table_data[1])
        if len(table_data[2]) > score_max:
            score_max = len(table_data[2])
        if len(table_data[3]) > date_max:
            date_max = len(table_data[3])
            
    if player_ID_max >= 9:
        player_ID_max -= 8
    if score_max >= 8:
        score_max -= 8
    if date_max >= 5:
        date_max -= 5
        
    
    print("\n\n================================================================================")
    print("Run_ID|Player_ID"+player_ID_max*" "+"|Score"+score_max*" "+"|Date"+date_max*" "+"|")
    print("------|--------"+player_ID_max*"-"+"|--------"+score_max*"-"+"|-----"+date_max*"-"+"|")
        
    if not isinstance(table_data[0], str):
        for row in table_data:
            print(""+row[0]+"     |", end="")
            print(row[1]+(player_ID_max-len(row[1])+8)*" "+"|", end="")
            print(row[2]+(score_max-len(row[2])+8)*" "+"|", end="")
            print(row[3]+(date_max-len(row[3])+5)*" "+"|")
    else:
        print(""+table_data[0]+"     |", end="")
        print(table_data[1]+(player_ID_max-len(table_data[1])+8)*" "+"|", end="")
        print(table_data[2]+(score_max-len(table_data[2])+8)*" "+"|", end="")
        print(table_data[3]+(date_max-len(table_data[3])+5)*" "+"|")

def runs_table(runs_table_active):

    runs_table_data = db.execute("SELECT * FROM runs_table").fetchall()

    print("\n\n================================================================================")
    print("Please choose an action to perform on the runs table:")
    print("================================================================================")
    print("1-View All Data")
    print("2-Add New Row")
    print("3-Edit Existing Row")
    print("4-Delete Row")
    print("5-Exit To Tables Viewer")
    
    selection = input("Option: ")
    
    if selection == "1":
        
        print_runs_table(runs_table_data)
    
    elif selection == "2":
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:
            
            new_row = [str(r.randint(0,9)) + str(r.randint(0,9)) + chr(r.randint(65, 90)) + chr(r.randint(65, 90))] + input_row(["Player_ID", "Score", "Date"])

            print_runs_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
            db.execute("INSERT INTO runs_table VALUES(?,?,?,?)", new_row)
            db.commit()
            
            print("\n================================================================================")
            print("Row Successfully Added!")
            print("================================================================================")
    
    elif selection == "3":
            
        print("\n\n================================================================================")
        print("Choose a row to edit:")
        print("================================================================================")
        
        print_runs_table(runs_table_data)
            
        selected_ID = input("Enter ID: ").upper()
        
        selected_row = db.execute(f"SELECT * FROM runs_table WHERE runs_ID='{selected_ID}'").fetchone()
        
        data_correct = False
        confirmed_valid = False
        
        while not data_correct:
            
            new_row = [selected_row[0]] + input_row(["Player_ID", "Score", "Date"])

            print_runs_table(new_row)
            
            confirmation = input("\nY/N: ")
            
            while not confirmed_valid:
                if confirmation.upper() == "Y":
                    data_correct = True
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    data_correct = False
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
            db.execute(f"DELETE FROM runs_table WHERE runs_ID='{new_row[0]}'")
            db.execute(f"INSERT INTO runs_table VALUES(?,?,?,?)", new_row)
            db.commit()
            
            print("================================================================================")
            print("Row Successfully Changed!")
            print("================================================================================")
        
    elif selection == "4":
        
        print("\n\n================================================================================")
        print("Choose a row to delete:")
        print("================================================================================")
        
        print_runs_table(runs_table_data)
            
        selected_ID = input("Enter ID: ").upper()
        
        selected_row = db.execute(f"SELECT * FROM runs_table WHERE runs_ID='{selected_ID}'").fetchone()
        
        confirmation = input(f"\nAre you sure you wish to delete the row with ID {selected_ID}(Y/N): ")
        
        confirmed_valid = False
        
        while not confirmed_valid:
                if confirmation.upper() == "Y":
                    confirmed_valid = True
                elif confirmation.upper() == "N":
                    confirmed_valid = True
                else:
                    confirmation = input("\nY/N")
                    
        db.execute(f"DELETE FROM runs_table WHERE runs_ID='{selected_ID}'")
        db.commit()
            
        print("================================================================================")
        print("Row Successfully Deleted!")
        print("================================================================================")
    elif selection == "5":
        
        runs_table_active = False
    return runs_table_active      

  
if devmode:
    running = True
    while running:
        player_table_active = True
        weapon_table_active = True
        enemy_table_active = True
        runs_table_active = True
        room_table_active = True
        choice = dev_initialise()
        
        if choice == "1":
            while player_table_active:
                player_table_active = player_table(player_table_active)
        elif choice == "2":
            while weapon_table_active:
                weapon_table_active = weapon_table(weapon_table_active)
        elif choice == "3":
            while room_table_active:
                room_table_active = room_table(room_table_active)
        elif choice == "4":
            while enemy_table_active:
                enemy_table_active = enemy_table(enemy_table_active)
        elif choice == "5":
            while runs_table_active:
                runs_table_active = runs_table(runs_table_active)