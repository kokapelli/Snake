from GUI import GUI
from World import World
from Train import Train
from file_processing import *
import argparse
import numpy as np

SQUARE_NUMBER = 22 # The GUI states the square numbers. SO have to bypass this
    
parser = argparse.ArgumentParser()
parser.add_argument('--debug', help='Starts the game in debug mode if stated',
                    action='store_true')
parser.add_argument('--terminal', help='Starts the game in terminal mode',
                    action='store_true')
parser.add_argument('--ai', help='Starts the game in AI mode',
                    action='store_true')
parser.add_argument('--size', help='Set the world size, should be divisible by 22 unless square count is changed',
                    default=660)
args = parser.parse_args()

SIZE     = args.size
DEBUG    = args.debug
TERMINAL = args.terminal
AI       = args.ai

# Implement Hamiltonian cycle to complete game
def startGame():
    
    game = GUI(SIZE, True)
    game.draw()
    game.master.mainloop()

def AIGame():
    params    = loadParams()
    config    = loadGameConfig()
    worldSize = config["square_number"]
    agent     = Train(params, True)
    game      = GUI(SIZE, False, agent)

    game.draw()
    game.master.mainloop()

if __name__ == "__main__":
    #AIGame()
    startGame()