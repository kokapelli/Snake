import numpy as np
import Snake as Snake
from typing import Tuple
from Movement import Trajectory, Point
from random import randint

from os import system, name

INPUT_NODES = 32

# Consider refactoring to have all 
# settings in config.json 
class World:
    def __init__(self, 
                 worldSize: int, 
                 debug: bool, 
                 binary: bool):

        self.debugMode   = debug
        self.binary      = binary
        self.worldSize   = worldSize
        self.snake       = Snake.Snake(self, binary)
        #[(Food, Snake, Wall)*8, Snake Direction, Tail Direction]
        self.worldState  = np.empty([self.worldSize, self.worldSize], dtype=int)
        self.stateSpace  = list()
        self.gameTime    = 0
        self.alive       = True
        self.food        = None
        self.totalReward = 0

        # AI related members
        self.resetThresh = 100 # Time steps until game resets
        self.resetCount  = 0   # Counter until game is reset (to prevent loops)
        self.reward      = 0   # AI Reward
        self.foodReward  = 100 # Score received for consuming food
        self.collPenalty = 500 # Collision Penalty
        self.timePenalty = 500 # Penalty if the snake never eats the food.

        # Random choice of start direction upon initialization
        #self.trajectoryInput = list(Trajectory)[randint(0, len(list(Trajectory)))]
        self.trajectoryInput = Trajectory.LEFT

        # *** Scuffed solution ***
        # Causes an update to take place in the world before the user can perform
        # an input. Snake spawn location must be changed accordingly.
        self.gameState   = [self.gameTime, self.snake.size, self.totalReward]
        self.updateWorld()

    def updateWorld(self) -> None:
        self.resetWorld()       # Reset the world of prior snake locations
        self.updateGameState()  # Update the game timer and the current snake size
        self.updateSnakePos()   # Move the snake by one time unit
        
        if(self.gameOver()):    # Check for self collision or out out bounds
            self.alive = False
            self.totalReward -= self.collPenalty
            self.reward      -= self.collPenalty
            return

        self.setSnake()         # Set the snake value in the console "world"
        self.updateFood()       # Set the food value in the console "world"
        self.observeSurroundings()
        
        if(self.debugMode):
            #self.screenClear()  # Clear screen for better "immersion"
            self.printWorld()   # Show the user the console snake location  
            print(self.snake)
            print(self.gameState, self.resetCount)
            print(self.stateSpace)

    def step(self, action: int) -> Tuple[list, int, bool]:
        parsedAction = None
        if action == 0:
            parsedAction = Trajectory.UP
        if action == 1:
            parsedAction = Trajectory.DOWN
        if action == 2:
            parsedAction = Trajectory.LEFT
        if action == 3:
            parsedAction = Trajectory.RIGHT

        if not self.snake.head.trajectory == -parsedAction: self.trajectoryInput = parsedAction
        self.updateWorld()

        return self.stateSpace, self.reward, self.alive

    def updateSnakePos(self) -> None:
        if(self.snake.head.trajectory != self.trajectoryInput):
            self.snake.head.trajectory = self.trajectoryInput
            
        self.snake.move()

    def resetWorld(self) -> None:
        self.worldState.fill(0)
        # Add Walls
        self.worldState[0].fill(9)
        self.worldState[self.worldSize-1].fill(9)
        for i in range(1, self.worldSize-1):
            self.worldState[i][0] = 9
            self.worldState[i][self.worldSize-1] = 9

    def gameOver(self) -> bool:
        return not self.OOB(self.snake.head.location) or self.selfCollide()
        
    def printWorld(self) -> None:
        print(self.worldState)
        print("\n")

    def setSnake(self) -> None:
        body = self.snake.body
        for b in body:
            x, y = b.location.to_int()
            self.worldState[x][y] = 1

    def observeSurroundings(self) -> None:
        self.stateSpace.clear()
        for i, direction in enumerate(list(Trajectory)):
            f, s, w = self.snake.look(direction)
            self.stateSpace      += [f, s, w]
        
        self.stateSpace      += self.snake.head.trajectory.OHE()
        self.stateSpace      += self.snake.getTailTrajectory().OHE()
        
    def updateGameState(self) -> None:
        self.reward         = 0
        self.gameState[0]  += 1
        self.gameState[1]   = self.snake.size
        self.gameState[2]   = self.totalReward
        self.resetCount    += 1
        if self.resetCount == self.resetThresh: 
            self.reward    -= self.timePenalty
            self.alive      = False
        
    # Consider refactoring further using Point
    def OOB(self, loc: 'Point') -> bool:
        x, y = loc.to_int()
        return not ((x < 1 or x >= self.worldSize-1) or (y < 1 or y >= self.worldSize-1))
            
    def selfCollide(self) -> bool:
        return self.snake.checkCollision()

    def updateFood(self) -> None:
        if(self.food == None or self.snake.head.location == self.food):
            freeLocs = list(zip(*np.where(self.worldState == 0))) # Get map location where snake is not
            randInt = randint(0, len(freeLocs)-1)
            x, y = freeLocs[randInt]
            
            self.food = Point(x, y)
            self.snake.growSnake()

            # AI related variables
            self.resetCount = 0
            if self.gameState[0] != 1: self.reward += self.foodReward
        else:
            x, y = self.food.to_int()
            self.worldState[x][y] = 2 # Console "world" food representation

    def screenClear(self) -> None: 
        if name == 'nt': 
            _ = system('cls') 
        else: 
            _ = system('clear') 