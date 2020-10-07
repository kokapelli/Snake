import numpy as np
import Snake as Snake
from os import system, name 

CLEAR_SCREEN = True

class World:
    def __init__(self):
        self.wSize = 25
        self.worldMat = self.createWorld()
        self.snake = Snake.Snake()
        self.gameTime = 0
        self.alive = True

    def createWorld(self):
        world = list()

        for row in range(self.wSize):
            row = list()
            for col in range(self.wSize):
                row.append(0)
            world.append(row)

        return np.array(world)

    def updateWorld(self):
        if(CLEAR_SCREEN):
            self.screenClear()  # Clear screen for better "immersion"
        self.resetWorld()       # Reset the world of prior snake locations
        self.updateSnakePos()   # Move the snake by one time unit
        if(not self.insideBoundary()):
            print("You Lose")
            self.alive = False
            return

        self.setSnake()         # Display snake in the "world"
        self.printWorld()       # Show the user the snake location  
        self.updateGameTime()

    def updateSnakePos(self):
        self.snake.move()

    def resetWorld(self):
        self.worldMat.fill(0)

    def printWorld(self):
        print(self.worldMat)

    def setSnake(self):
        body = self.snake.getBody()
        for b in body:
            x, y = b.getLoc()
            print(x, y)
            self.worldMat[x][y] = b.getRepr()

    def screenClear(self): 
    
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 

    def updateGameTime(self):
        self.gameTime += 1
        print(self.gameTime)

    def insideBoundary(self):
        x, y = self.snake.getHeadLoc()
        #print(x < 0, x >= self.wSize)
        #print(y < 0, y >= self.wSize)
        #print(f"(x:{x}, y:{y})")
        if((x < 0 or x >= self.wSize) or (y < 0 or y >= self.wSize)):
            return False
        
        return True

    def isAlive(self):
        return self.alive