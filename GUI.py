from tkinter import *
from Movement import Trajectory
from World import World
import numpy as np
import time

class GUI:
    def __init__(self, size: int, debug: bool, agent: 'model' = None):
        self.debug     = debug
        self.size      = size
        self.squareNr  = 12 # Additional 2 to include horizontal and vertical walls
        self.world     = World(self.squareNr, debug, False)
        self.squareDim = self.size // self.squareNr
        self.gameSpeed = 200 if debug else 50
        self.createBoard()

        self.board.bind('<Left>', self.leftKey)
        self.board.bind('<Right>', self.rightKey)
        self.board.bind('<Up>', self.upKey)
        self.board.bind('<Down>', self.downKey)
        self.board.bind('<Escape>', self.exit)
        self.board.focus_set()
        self.board.pack()

        # AI related members
        self.agent = agent
        self.state = np.reshape(self.world.stateSpace, (1, 32))

    def createBoard(self) -> None:
        self.master = Tk()
        self.master.resizable(False, False)
        self.master.title("Falk: Snake")
        self.master.configure(background="black")
        self.board = Canvas(self.master, bg="white", highlightthickness=0, width = self.size, height = self.size)

    def draw(self) -> None:
        self.resetBoard()
        if(self.agent):
            action  = self.agent.playAction([self.state])
            state, _, _ = self.world.step(action)
            self.state = state
        else:
            self.world.updateWorld()

        currWorldState = self.world.worldState

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
                elif(currWorldState[row][col] == 9):
                    self.board.create_rectangle(x1, y1, x2, y2, fill="gray7")
                else:
                    self.board.create_rectangle(x1, y1, x2, y2, fill="gray15")

                if(self.debug):
                    if(currWorldState[row][col] == 8):
                        self.board.create_rectangle(x1, y1, x2, y2, fill="gray7")

        if(self.world.alive):
            self.board.after(self.gameSpeed, self.draw)
        else:
            print(self.world.gameState)
            self.gameOver()
            return

    def resetBoard(self) -> None:
        self.board.delete("all")

    def gameOver(self):
        l = Label(self.master, bg="salmon", text="You Lost!", font=("Helvetica", 30)) 
        l.place(relx = 0.5, rely = 0.5, anchor = 'center')
        l.config(width=self.size)


                    #####################
                    ## Keyboard inputs ##
                    #####################


    def leftKey(self, _) -> None:
        if(self.world.snake.head.trajectory == Trajectory.RIGHT):
            return
        self.world.trajectoryInput = Trajectory.LEFT

    def rightKey(self, _) -> None:
        if(self.world.snake.head.trajectory == Trajectory.LEFT):
            return
        self.world.trajectoryInput = Trajectory.RIGHT

    def upKey(self, _) -> None:
        if(self.world.snake.head.trajectory == Trajectory.DOWN):
            return
        self.world.trajectoryInput = Trajectory.UP

    def downKey(self, _) -> None:
        if(self.world.snake.head.trajectory == Trajectory.UP):
            return
        self.world.trajectoryInput = Trajectory.DOWN

    def exit(self, event) -> None:
        sys.exit()