import sqlite3 as sql
import pathlib


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
        
        db.commit()
        
        
        
    return db