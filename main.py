from classes.Game import Game
from openal import oalQuit

if __name__ == "__main__":
	game = Game()
	game.start()
	oalQuit()
