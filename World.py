import numpy as np
import Snake as Snake
from Movement import Trajectory, Point
from random import randint

from os import system, name 

class World:
    def __init__(self, worldSize: int, debug: bool):
        self.debugMode = debug
        self.worldSize = worldSize
        self.state = np.empty([self.worldSize, self.worldSize], dtype=int)
        self.snake = Snake.Snake(self)
        self.gameTime = 0
        self.gameState = [self.gameTime, self.snake.size]
        self.alive = True
        self.food = None

        # Random choice of start direction upon initialization
        #self.trajectoryInput = list(Trajectory)[randint(0, len(list(Trajectory)))]
        self.trajectoryInput = Trajectory.LEFT

    def updateWorld(self) -> None:
        self.resetWorld()       # Reset the world of prior snake locations
        self.updateSnakePos()   # Move the snake by one time unit
        if(self.gameOver()):    # Check for self collision or out out bounds
            self.alive = False

        self.setSnake()         # Set the snake value in the console "world"
        self.updateFood()       # Set the food value in the console "world"
        self.updateGameState()  # Update the game timer and the current snake size

        if(self.debugMode):
            self.screenClear()  # Clear screen for better "immersion"
            self.printWorld()   # Show the user the console snake location  
            print(self.snake)
            print(self.gameState)

    def updateSnakePos(self) -> None:
        if(self.snake.head.trajectory != self.trajectoryInput):
            self.snake.head.trajectory = self.trajectoryInput
            
        self.snake.move()
        self.snake.look()

    def resetWorld(self) -> None:
        self.state.fill(0)
        # Add Walls where required
        self.state[0].fill(9)
        self.state[self.worldSize-1].fill(9)
        for i in range(1, self.worldSize-1):
            self.state[i][0] = 9
            self.state[i][self.worldSize-1] = 9

    def gameOver(self) -> bool:
        return not self.OOB() or self.selfCollide()
        
    def printWorld(self) -> None:
        print(self.state)
        print("\n")

    def setSnake(self) -> None:
        body = self.snake.body
        for b in body:
            x, y = b.location.to_int()
            self.state[x][y] = 1

    def setTrajectoryInput(self, newTrajectory: 'Point') -> None:
        self.trajectoryInput = newTrajectory

    def updateGameState(self) -> None:
        self.gameState[0] += 1
        self.gameState[1] = self.snake.size
        
    # Consider refactoring further using Point
    def OOB(self) -> bool:
        x, y = self.snake.head.location.to_int()
        return not ((x < 1 or x >= self.worldSize-1) or (y < 1 or y >= self.worldSize-1))
            
    def selfCollide(self) -> bool:
        return self.snake.checkCollision()

    def updateFood(self) -> None:
        if(self.food == None or self.snake.head.location == self.food):
            freeLocs = list(zip(*np.where(self.state == 0))) # Get map location where snake is not
            randInt = randint(0, len(freeLocs)-1)
            x, y = freeLocs[randInt]
            
            self.food = Point(x, y)
            self.snake.growSnake()

        else:
            x, y = self.food.to_int()
            self.state[x][y] = 2 # Console "world" food representation

    def screenClear(self) -> None: 
        if name == 'nt': 
            _ = system('cls') 
        else: 
            _ = system('clear') 