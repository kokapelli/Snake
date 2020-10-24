import numpy as np
import Snake as Snake
from Movement import Trajectory, Point
from random import randint

from os import system, name 

class World:
    def __init__(self, worldSize, debug):
        self.debugMode = debug
        self.worldSize = worldSize
        self.state = self.createWorld()
        self.snake = Snake.Snake(self)
        self.gameTime = 0
        self.gameState = [self.gameTime, self.snake.size]
        self.alive = True
        self.food = None
        # Start game by moving upwards, consider randomizing this value
        self.trajectoryInput = Trajectory.UP

    def createWorld(self):
        world = list()

        for row in range(self.worldSize):
            row = list()
            for _ in range(self.worldSize):
                row.append(0)
            world.append(row)

        return np.array(world)

    def updateWorld(self):

        self.resetWorld()       # Reset the world of prior snake locations
        self.updateSnakePos()   # Move the snake by one time unit
        if(not self.insideBoundary() or self.selfCollide()):
            print("You Lose")
            self.alive = False
            return

        self.setSnake()         # Set the snake value in the console "world"
        self.updateFood()
        self.updateGameState()

        if(self.debugMode):
            self.screenClear()  # Clear screen for better "immersion"
            self.printWorld()   # Show the user the console snake location  
            print(self.snake)
            print(self.gameState)

    def updateSnakePos(self):
        if(self.snake.head.trajectory != self.trajectoryInput):
            #print(str(self.snake.head.trajectory) + " - " + str(self.trajectoryInput))
            self.snake.setHeadTrajectory(self.trajectoryInput)
        self.snake.move()

    def resetWorld(self):
        self.state.fill(0)

    def printWorld(self):
        print(self.state)
        print("\n")

    def setSnake(self):
        body = self.snake.body
        for b in body:
            x, y = b.location.to_int()
            self.state[x][y] = 1

    def setTrajectoryInput(self, newTrajectory):
        self.trajectoryInput = newTrajectory

    def updateGameState(self):
        self.gameState[0] += 1
        self.gameState[1] = self.snake.size
        
    def insideBoundary(self):
        x, y = self.snake.head.location.to_int()
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
        if(self.food == None or self.snake.head.location == self.food):
            freeLocs = list(zip(*np.where(self.state == 0))) # Get map location where snake is not
            randInt = randint(0, len(freeLocs))
            x, y = freeLocs[randInt]
            
            self.food = Point(x, y)
            self.snake.growSnake()

        else:
            x, y = self.food.to_int()
            self.state[x][y] = 2 # Console food representation

    def redirect(self, direction):
        if direction == 'UP':
            print("Up Key Pressed")
            self.trajectoryInput = Trajectory.UP
        elif direction == 'DOWN':
            print("Down Key Pressed")
            self.trajectoryInput = Trajectory.DOWN
        elif direction == 'RIGHT':
            print("Right Key Pressed")
            self.trajectoryInput = Trajectory.RIGHT
        elif direction == 'LEFT':
            print("Left Key Pressed")
            self.trajectoryInput = Trajectory.LEFT

    def screenClear(self): 
        if name == 'nt': 
            _ = system('cls') 
        else: 
            _ = system('clear') 