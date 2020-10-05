import numpy as np
import Snake as Snake
from os import system, name 

class World:
    def __init__(self):
        self.wSize = 20
        self.worldMat = self.createWorld()
        self.snake = Snake.Snake()
        self.gameTime = 0

    def createWorld(self):
        world = list()

        for row in range(self.wSize):
            row = list()
            for col in range(self.wSize):
                row.append(0)
            world.append(row)

        return np.array(world)

    def updateWorld(self):
        self.screenClear()
        self.printWorld()   # Show the user the snake location  
        self.resetWorld()   # Reset the world of prior snake locations
        snakeLoc = self.snake.getBodyLoc()
        for loc in snakeLoc:
            self.worldMat[loc[0]][loc[1]] = 1

        self.updateSnakePos()
        self.updateTime()

    def updateSnakePos(self):
        self.snake.move()

    def resetWorld(self):
        self.worldMat.fill(0)

    def printWorld(self):
        print(self.worldMat)

    def screenClear(self): 
    
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 

    def updateTime(self):
        self.gameTime += 1
        print(self.gameTime)