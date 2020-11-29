from GUI import GUI
from World import World
import argparse

SQUARE_NUMBER = 22 # The GUI states the square numbers. SO have to bypass this
    
parser = argparse.ArgumentParser()
parser.add_argument('--debug', help='Starts the game in debug mode if stated',
                    action='store_true')
parser.add_argument('--terminal', help='Starts the game in terminal mode',
                    action='store_true')
parser.add_argument('--size', help='Set the world size, should be divisible by 22 unless square count is changed',
                    default=660)
args = parser.parse_args()

# Implement Hamiltonian cycle to complete game
def startGame():
    size = args.size
    debug = args.debug
    terminal = args.terminal
    
    if debug and GUI : game = GUI(size, True)
    else: game = GUI(size, False)
    game.draw()
    game.master.mainloop()

if __name__ == "__main__":
    startGame()