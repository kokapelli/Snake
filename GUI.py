from tkinter import *
from World import World
import time

GAME_SPEED = 200
DEBUG = False

class GUI:
    def __init__(self, size):
        self.size = size
        self.squareNr = 20
        self.world = World(self.squareNr, DEBUG)
        self.squareDim = self.size // self.squareNr

        self.createBoard()

        self.board.bind('<Left>', self.leftKey)
        self.board.bind('<Right>', self.rightKey)
        self.board.bind('<Up>', self.upKey)
        self.board.bind('<Down>', self.downKey)
        self.board.bind('<Escape>', self.exit)
        self.board.focus_set()
        self.board.pack()

    def createBoard(self):
        self.master = Tk()
        self.master.resizable(False, False)
        self.master.title("Falk: Snake")
        self.master.configure(background="black")
        self.board = Canvas(self.master, bg="white", highlightthickness=0, width = self.size, height = self.size)

    def draw(self):
        self.resetBoard()
        self.world.updateWorld()
        currWorldState = self.world.world

        for row in range(self.squareNr):
            for col in range(self.squareNr):
                x1 = self.squareDim*col
                y1 = self.squareDim*row
                x2 = self.squareDim*(col+1)
                y2 = self.squareDim*(row+1)

                if(currWorldState[row][col] == 1):
                    self.board.create_rectangle(x1, y1, x2, y2, fill="AntiqueWhite1")
                elif(currWorldState[row][col] == 2):
                    self.board.create_rectangle(x1, y1, x2, y2, fill="pale green")
                else:
                    self.board.create_rectangle(x1, y1, x2, y2, fill="gray15")

        if(self.world.alive):
            self.board.after(GAME_SPEED, self.draw)
        else:
            return

    def resetBoard(self):
        self.board.delete("all")


                    #####################
                    ## Keyboard inputs ##
                    #####################

    def leftKey(self, _):
        print("Left Key Pressed")
        if(self.world.snake.getHeadTrajectory() == [0, 1]):
            return
        #self.world.snake.setHeadTrajectory([0, -1])
        self.world.setTrajectoryInput([0, -1])

    def rightKey(self, _):
        print("Right Key Pressed")
        if(self.world.snake.getHeadTrajectory() == [0, -1]):
            return
        #self.world.snake.setHeadTrajectory([0, 1])
        self.world.setTrajectoryInput([0, 1])


    def upKey(self, _):
        print("Up Key Pressed")
        if(self.world.snake.getHeadTrajectory() == [1, 0]):
            return
        #self.world.snake.setHeadTrajectory([-1, 0])
        self.world.setTrajectoryInput([-1, 0])

    def downKey(self, _):
        print("Down Key Pressed")
        if(self.world.snake.getHeadTrajectory() == [-1, 0]):
            return
        #self.world.snake.setHeadTrajectory([1, 0])
        self.world.setTrajectoryInput([1, 0])

    def exit(self, event):
        sys.exit()