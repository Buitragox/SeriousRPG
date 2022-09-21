from classes.Enemy import Enemy
from classes.Loader import Loader
from classes.Player import Player
from classes.Room import Room
from classes.Room import RoomAction
from sys import stdout
import time
from pynput import keyboard as kb
from random import random
from openal import *
from colorama import Fore, Back, Style

MIN_PLAY_TIME = 2.5
MAX_PLAY_TIME = 5.0
VALID_DODGE_TIME = 1.0
START_ROOM = "victoria"

class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.sounds = Loader.load_sounds()
        self.enemies = Loader.load_enemies()
        self.rooms = Loader.load_rooms()
        self.current_room = ""
        self.pressed_dodge = False
        stdout.reconfigure(encoding='utf-8')
   

    def start(self) -> None:
        """Start of the game, ask for player name and call game_loop"""
        try:
            self.slow_print("BIENVENIDO A", "")
            self.slow_print(" ...", delay=0.5)
            self.slow_print("UN RPG MUY ", "", mods=Back.YELLOW)
            self.slow_print("COLOM", "", mods=Back.BLUE)
            self.slow_print("BIANO", mods=Back.RED)
            valid_name = False
            while not valid_name:
                self.slow_print("Ingresa tu nombre: ", "", mods=Fore.RED)
                name = input()
                valid_name = self.player.set_name(name)
                if not valid_name:
                    self.slow_print("¿Se le olvido como escribir?")
            self.current_room = START_ROOM
            self.game_loop()
            self.slow_print("Gracias por jugar!", mods=Fore.GREEN)
            self.slow_print("Presiona Enter para salir...",  mods=Fore.GREEN)
            input()

        except KeyboardInterrupt:
            print("\nEjecución detenida\n") 

        except Exception as e:
            print("Ha ocurrido un error:", e)       
            

    @staticmethod
    def slow_print(text="", end="\n", delay=0.01, mods="") -> None:
        """Personalized print function, adds per char delay and color functionality"""
        stdout.write(mods)
        for c in text: 
            stdout.write(c) 
            stdout.flush()
            time.sleep(delay)
        stdout.write(Style.RESET_ALL + end) 
        stdout.flush()


    def play_story(self, room_key: str) -> None:
        """Prints the story of a room"""

        room = self.rooms[room_key]
        for text, sound in room.story:
            if sound != "" and sound in self.sounds:
                self.sounds[sound].play()
            
            self.slow_print(text, "")
            input()


    def option_menu(self, question = "", options = [], cheats = []) -> int:
        """Prints the menu of a room"""

        if len(options) == 0:
            raise RuntimeError("Menu de opciones vacío")
        valid_option = False
        opc = 0
        while not valid_option:
            self.slow_print(question, mods=Fore.LIGHTCYAN_EX)
            for i, text in enumerate(options):
                print(f"{i}. ", end="")
                self.slow_print(text)

            try:
                opc = int(input("> "))
                if opc >= 0 and opc < len(options) or opc in cheats:
                    valid_option = True
                else:
                    raise ValueError("Opción invalida")
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except Exception:
                self.slow_print("Ingresa una opción valida, no es tan difícil...")
        print()
        return opc


    def press(self, key):
        """Function used by the keyboard listener to register when the keyboard is pressed"""
        self.pressed_dodge = True

    
    def dodge(self) -> bool:
        """Does all the logistics regarding the dodge mechanic."""

        play_time = MIN_PLAY_TIME + (random() * (MAX_PLAY_TIME - MIN_PLAY_TIME))
        success = False
        sound = self.sounds["sonidoAtaque"]
        sound_played = False
        sound_time = 0 #Start time of playing the sound
        pressed_time = 0 #Start time of pressing the key
        start_time = time.time() #Start time of event
        self.pressed_dodge = False
        with kb.Listener(self.press) as listener:
            while not self.pressed_dodge:
                if time.time() - start_time > play_time and not sound_played:
                    sound_played = True
                    sound_time = time.time()
                    sound.set_gain(0.7)
                    sound.play()
            pressed_time = time.time()
            listener.stop()
        
        if not sound_played:
            self.slow_print("Demasiado rápido", mods=Fore.YELLOW)
        elif pressed_time - sound_time <= VALID_DODGE_TIME:
            self.slow_print("Perfecto", mods=Fore.GREEN)
            success = True
        else:
            self.slow_print("Demasiado tarde", mods=Fore.YELLOW)

        return success

    def slow_stop(self, sound_key: str, fade_time = 1.0) -> None:
        """Slowly stops a sound with a fade over a specified time"""
        sound = self.sounds[sound_key]
        og_vol = sound.gain #original volume
        if sound.get_state() == AL_PLAYING:
            start_time = time.time()
            t = time.time()
            while t - start_time < fade_time:
                vol = og_vol * (1 - (t - start_time)/fade_time)
                sound.set_gain(vol)
                t = time.time()
            
            self.sounds[sound_key].set_looping(False)
            sound.set_gain(og_vol)
            self.sounds[sound_key].stop()


    def stop_all_sounds(self):
        """Stops all sounds"""
        for key in self.sounds:
            self.slow_stop(key)
                
                
    def battle(self, enemy_key: str) -> bool:
        """Handles both the player's and the enemy's turn"""
        enemy = self.enemies[enemy_key]
        
        victory = False
        question = "¿Cuál es tu movimiento?"
        options = ["Insultar", "Chiste", "Suplicar", "Nada"]
        
        self.slow_print(f"{self.player.name}", "", mods=Fore.LIGHTBLUE_EX)
        self.slow_print(f" vs ", "")
        self.slow_print(f"{enemy.name}", mods=Fore.LIGHTRED_EX)

        self.stop_all_sounds()
        
        self.sounds[enemy.fight_track].set_looping(True)
        self.sounds[enemy.fight_track].play()
            
        while self.player.hp > 0 and not victory:
            self.slow_print(f"\nVida {self.player.hp}/{self.player.max_hp}", mods=Fore.RED)
            opc = self.option_menu(question, options, [420])

            if opc == 0:
                if self.player.insult():
                    self.slow_print("Tu insulto ha hecho llorar el enemigo...")
                    self.slow_print("Se resbala con sus lagrimas y es derrotado.")
                    self.slow_print("Te sientes como una mala persona.")
                    victory = True
                    break
                else:
                    self.slow_print("Tu enemigo esta furioso, maravillosa jugada")

            elif opc == 1:
                if self.player.joke():
                    enemy.cringe += 1
                    if enemy.cringe == enemy.max_cringe:
                        self.slow_print("Tu enemigo ha muerto del cringe... victoria?")
                        victory = True
                        break
                    else:
                        self.slow_print("Tu chiste fue tan malo que le dolio a tu enemigo")
                else:
                    self.slow_print("¿Andas cómo comediante no?")
            
            elif opc == 2:
                if enemy.name == "Uribito":
                    victory = 1
                    break
                else:
                    self.slow_print("Has suplicado piedad... No ha funcionado")
            
            elif opc == 3:
                self.player.hp = 0
                self.slow_print("Como no haces nada te vuelves policía, perdiste")
                break
            
            elif opc == 420:
                victory = True
                print("Ha bajado diosito ha salvarte, has ganado")
                break

            self.slow_print("El enemigo se esta preparando para atacar")
            self.slow_print(enemy.select_msg())

            self.slow_print("Presiona ESPACIO cuando suene el ataque.\nPresiona Enter cuando estes listo ...")
            input()
            self.slow_print("ATENTO!", delay=0, mods=Back.YELLOW)
            success = self.dodge()
            if not success:
                self.player.hp -= 1
                self.sounds["dano"].play()
                if self.player.hp == 0:
                    self.slow_print("Te mataron, mucha loca no sabe pelear")


        self.slow_stop(enemy.fight_track)

        enemy.cringe = 0

        return victory


    def game_loop(self) -> None:
        """Main function of the class, handles the game loop"""

        self.slow_print("========================")
        victory = False
        new_room = True
        while self.player.hp > 0 and not victory:
            if new_room:
                self.play_story(self.current_room)
                new_room = False

            if self.rooms[self.current_room].name == "victoria":
                break

            options = self.rooms[self.current_room].menu_text
            opc = self.option_menu("\n¿Qué deseas hacer?", options)

            action = self.rooms[self.current_room].menu_action[opc]
            
            if action[0] == RoomAction.NOTYPE.name:
                print("Nothing")

            elif action[0] == RoomAction.HEAL.name:
                self.slow_print("Te has recuperado")
                self.player.hp = self.player.max_hp

            elif action[0] == RoomAction.MOVE.name:
                next_room = action[1]
                if next_room not in self.rooms: #Room must exist
                    raise ValueError("Sala inexistente")
                self.current_room = next_room
                new_room = True

            elif action[0] == RoomAction.FIGHT.name:
                enemy_key = self.rooms[self.current_room].boss
                if enemy_key not in self.enemies:
                    raise ValueError("Enemigo inexistente")
                next_room = action[1]
                if next_room not in self.rooms:
                    raise ValueError("Sala inexistente")
                
                battle_win = self.battle(enemy_key)
                if battle_win:
                    self.current_room = next_room
                    new_room = True
            
            elif action[0] == RoomAction.NOTHING.name:
                self.player.hp = 0
                self.slow_print("Como no haces nada te vuelves policía, perdiste")
            
            elif action[0] == RoomAction.DEAD.name:
                self.player.hp = 0
                self.slow_print("Has muerto, ¿quién come eso?")
            
            elif action[0] == RoomAction.VICTORY.name:
                victory = True
        
             
