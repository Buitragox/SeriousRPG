from enum import Enum

class RoomAction(Enum):
    NOTYPE = 0
    MOVE = 1
    HEAL = 2
    FIGHT = 3
    NOTHING = 4
    VICTORY = 5
    DEAD = 6

class Room:
    def __init__(self, name = "", story = [], menu_text = [], menu_action = [], 
                boss = "") -> None:
        self.name = name
        self.story = story
        self.menu_text = menu_text
        self.menu_action = menu_action
        self.boss = boss
