from GUI import GUI
from World import World

GAME_SIZE  = 660

# Implement Hamiltonian cycle to complete game

def startGame():
    game = GUI(GAME_SIZE)
    game.draw()
    game.master.mainloop()

if __name__ == "__main__":
    startGame()
    #world = World(20, True)
    #print(world.state)