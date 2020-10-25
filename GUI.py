from tkinter import *
from Movement import Trajectory
from World import World
import time

GAME_SPEED = 50
DEBUG = False

class GUI:
    def __init__(self, size: int):
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

    def createBoard(self) -> None:
        self.master = Tk()
        self.master.resizable(False, False)
        self.master.title("Falk: Snake")
        self.master.configure(background="black")
        self.board = Canvas(self.master, bg="white", highlightthickness=0, width = self.size, height = self.size)

    def draw(self) -> None:
        self.resetBoard()
        self.world.updateWorld()
        currWorldState = self.world.state

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
            l = Label(self.master, bg="salmon", text="You Lost!", font=("Helvetica", 30)) 
            l.place(relx = 0.5, rely = 0.5, anchor = 'center')
            l.config(width=self.size)
            return

    def resetBoard(self) -> None:
        self.board.delete("all")


                    #####################
                    ## Keyboard inputs ##
                    #####################


    def leftKey(self, _) -> None:
        if(self.world.snake.head.trajectory == Trajectory.RIGHT):
            return
        self.world.setTrajectoryInput(Trajectory.LEFT)

    def rightKey(self, _) -> None:
        if(self.world.snake.head.trajectory == Trajectory.LEFT):
            return
        self.world.setTrajectoryInput(Trajectory.RIGHT)

    def upKey(self, _) -> None:
        if(self.world.snake.head.trajectory == Trajectory.DOWN):
            return
        self.world.setTrajectoryInput(Trajectory.UP)

    def downKey(self, _) -> None:
        if(self.world.snake.head.trajectory == Trajectory.UP):
            return
        self.world.setTrajectoryInput(Trajectory.DOWN)

    def exit(self, event) -> None:
        sys.exit()