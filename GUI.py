from tkinter import *
from World import World
import time

GAME_SPEED = 0.5

class GUI:
    def __init__(self, size):
        self.size = size
        self.squareNr = 30
        self.world = World(self.squareNr)
        self.squareDim = self.size // self.squareNr

        self.createBoard()

        self.board.bind('<Left>', self.leftKey)
        self.board.bind('<Right>', self.rightKey)
        self.board.bind('<Up>', self.upKey)
        self.board.bind('<Down>', self.downKey)
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
        currWorldState = self.world.getWorld()

        for row in range(self.squareNr):
            for col in range(self.squareNr):
                x1 = self.squareDim*col
                y1 = self.squareDim*row
                x2 = self.squareDim*(col+1)
                y2 = self.squareDim*(row+1)

                if(currWorldState[row][col] == 1):
                    self.board.create_rectangle(x1, y1, x2, y2, fill="white")
                elif(currWorldState[row][col] == 2):
                    self.board.create_rectangle(x1, y1, x2, y2, fill="green")
                else:
                    self.board.create_rectangle(x1, y1, x2, y2, fill="black")

        if(self.world.isAlive()):
            self.board.after(500, self.draw)
        else:
            return

    def resetBoard(self):
        self.board.delete("all")

    def leftKey(self, _):
        print("Left Key Pressed")
        self.world.snake.setHeadTrajectory([0, -1])

    def rightKey(self, _):
        print("Right Key Pressed")
        self.world.snake.setHeadTrajectory([0, 1])

    def upKey(self, _):
        print("Up Key Pressed")
        self.world.snake.setHeadTrajectory([-1, 0])

    def downKey(self, _):
        print("Down Key Pressed")
        self.world.snake.setHeadTrajectory([1, 0])