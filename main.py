from GUI import GUI

GAME_SIZE  = 720

# Implement Hamiltonian cycle to complete game

def startGame():
    game = GUI(GAME_SIZE)
    game.draw()
    game.master.mainloop()

if __name__ == "__main__":
    startGame()