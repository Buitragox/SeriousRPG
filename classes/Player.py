from random import randint

class Player:
    def __init__(self, name = "", hp = 3) -> None:
        self.name = name
        self.hp = hp
        self.max_hp = 3
    
    def insult(self, chance = 10) -> bool:
        return randint(1, 100) <= chance
    
    def joke(self, chance = 50) -> bool:
        return randint(1, 100) <= chance

    def set_name(self, name = "") -> bool:
        valid = True
        if len(name) == 0:
            valid = False
        
        if valid:
            self.name = name
        
        return valid
