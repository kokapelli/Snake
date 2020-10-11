from GUI import GUI

GAME_SIZE  = 540

def startGame():
    game = GUI(GAME_SIZE)
    game.draw()
    game.master.mainloop()
    #game.master.update_idletasks()
    #game.master.update()

if __name__ == "__main__":
    startGame()