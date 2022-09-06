from openal import oalOpen
from random import randint

class Enemy:
    cringe = 0
    def __init__(self, name = "", max_cringe = 3, attack_msgs = [], 
                entry_track = "", fight_track = "") -> None:
        self.name = name
        self.max_cringe = max_cringe
        self.attack_msgs = attack_msgs
        self.entry_track = entry_track
        self.fight_track = fight_track
    
    
    def select_msg(self) -> str:
        i = randint(0, len(self.attack_msgs) - 1)
        return self.attack_msgs[i]

    
    def __str__(self) -> str:
        return self.name