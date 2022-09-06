from classes.Enemy import Enemy
from classes.Room import Room   
from openal import *
from glob import glob
import json

class Loader:

    @staticmethod
    def load_sounds() -> dict[str, Source]:
        sounds = {}
        sound_path = glob("./sounds/*.wav")
        for s in sound_path:
            source = oalOpen(s)
            source.set_position([0.0, -1.0, -1.0])
            key = s[9:-4] #Erase the directory
            sounds[key] = source
        
        return sounds


    @staticmethod
    def load_enemies() -> dict[str, Enemy]:
        enemies = {}
        with open("./data/enemies.json", "r", encoding="utf-8") as file:
            enemies_data = json.load(file)
        for key in enemies_data:
            name = enemies_data[key]["name"]
            max_cringe = enemies_data[key]["max_cringe"]
            attack_msgs = enemies_data[key]["attack_msgs"]
            entry_track = enemies_data[key]["entry_track"]
            fight_track = enemies_data[key]["fight_track"]
            enemies[key] = Enemy(name, max_cringe, attack_msgs, entry_track, fight_track)

        return enemies
    

    @staticmethod
    def load_rooms() -> dict[str, Room]:
        rooms = {}
        with open("./data/rooms.json", 'r', encoding="utf-8") as file:
            rooms_data = json.load(file)
        for key in rooms_data:
            name = rooms_data[key]["name"]
            story = rooms_data[key]["story"]
            menu_text = rooms_data[key]["menu_text"]
            menu_action = rooms_data[key]["menu_action"]
            boss = rooms_data[key]["boss"]
            rooms[key] = Room(name, story, menu_text, menu_action, boss)
        
        return rooms