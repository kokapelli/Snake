import numpy as np
import Snake as Snake
import random

from os import system, name 

debug = False

class World:
    def __init__(self, worldSize, debug):
        self.debugMode = debug
        self.worldSize = worldSize
        self.world = self.createWorld()
        self.snake = Snake.Snake(self)
        self.gameTime = 0
        self.gameState = [self.gameTime, self.snake.getSnakeSize()]
        self.alive = True
        self.food = []
        # Start game by moving upwards, consider randomizing this value
        self.trajectoryInput = [0, -1]

    def createWorld(self):
        world = list()

        for row in range(self.worldSize):
            row = list()
            for col in range(self.worldSize):
                row.append(0)
            world.append(row)

        return np.array(world)

    def updateWorld(self):

        self.resetWorld()       # Reset the world of prior snake locations
        self.updateSnakePos()   # Move the snake by one time unit
        self.updateFood()
        self.updateGameState()

        if(not self.insideBoundary() or self.selfCollide()):
            print("You Lose")
            self.alive = False
            return

        
        self.setSnake()         # Set the sname value in the console "world"

        if(debug):
            self.screenClear()  # Clear screen for better "immersion"
            self.printWorld()   # Show the user the console snake location  
            print(self.snake)
            print(self.gameState)

    def updateSnakePos(self):
        if(self.snake.getHeadTrajectory() != self.trajectoryInput):
            #print(str(self.snake.getHeadTrajectory()) + " - " + str(self.trajectoryInput))
            self.snake.setHeadTrajectory(self.trajectoryInput)
        self.snake.move()

    def resetWorld(self):
        self.world.fill(0)

    def printWorld(self):
        print(self.world)
        print("\n")

    def setSnake(self):
        body = self.snake.getBody()
        for b in body:
            x, y = b.location
            self.world[x][y] = 1

    def setTrajectoryInput(self, newTrajectory):
        self.trajectoryInput = newTrajectory

    def updateGameState(self):
        self.gameState[0] += 1
        self.gameState[1] = self.snake.getSnakeSize()
        

    def insideBoundary(self):
        x, y = self.snake.getHeadLoc()
        #print(x < 0, x >= worldSize)
        #print(y < 0, y >= worldSize)
        #print(f"(x:{x}, y:{y})")
        if((x < 0 or x >= self.worldSize) or (y < 0 or y >= self.worldSize)):
            return False
        
        return True

    def selfCollide(self):
        return self.snake.checkCollision()


    # Ensure food does not spawn on snake
    def updateFood(self):
        # If the snake passes a food point, it grows and a new food spawns
        if(self.snake.getHeadLoc() == self.food or len(self.food) == 0):
            free = list(zip(*np.where(self.world == 0.))) # Get map location where snake is not
            randInt = random.randint(0, len(free))
            x, y = free[randInt]
            #print(f"food: {x, y}")
            coords = [x, y]
            self.snake.growSnake()

        elif(len(self.food) > 0):
            coords = self.food
        
        self.setFood(coords)

    def setFood(self, coords):
        self.food = coords
        x, y = coords
        self.world[x][y] = 2 # Temporary food representation

    def screenClear(self): 
    
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 

    @property
    def world(self):
        return self._world
    @property
    def alive(self):
        return self._alive 

    @property
    def snake(self):
        return self._snake

    @world.setter
    def world(self, world):
        self._world = world

    @snake.setter
    def snake(self, snake):
        self._snake = snake

    @alive.setter
    def alive(self, alive):
        self._alive = alive

    @property
    def worldSize(self):
        return self._worldSize

    @worldSize.setter
    def worldSize(self, s):
        self._worldSize = s
    