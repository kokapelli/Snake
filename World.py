import numpy as np
import Snake as Snake
from Movement import Trajectory, Point
from random import randint

from os import system, name

INPUT_NODES = 32

class World:
    def __init__(self, worldSize: int, debug: bool, terminalMode: bool):
        self.debugMode       = debug
        self.terminalMode    = terminalMode
        self.worldSize       = worldSize
        self.state           = np.empty([self.worldSize, self.worldSize], dtype=int)
        self.snake           = Snake.Snake(self)
        self.snakePerception = list()
        self.gameTime        = 0
        self.gameState       = [self.gameTime, self.snake.size]
        self.alive           = True
        self.food            = None

        # AI related members
        # Time steps until game resets
        self.resetThresh = 100
        self.resetCount  = 0

        # Random choice of start direction upon initialization
        #self.trajectoryInput = list(Trajectory)[randint(0, len(list(Trajectory)))]
        self.trajectoryInput = Trajectory.LEFT

        if terminalMode: self.updateWorld()

    def updateWorld(self) -> None:
        self.resetWorld()       # Reset the world of prior snake locations
        self.updateGameState()  # Update the game timer and the current snake size
        self.updateSnakePos()   # Move the snake by one time unit
        
        if(self.gameOver()):    # Check for self collision or out out bounds
            self.alive = False
            print("Lost")
            return

        self.setSnake()         # Set the snake value in the console "world"
        self.updateFood()       # Set the food value in the console "world"
        self.observeSurroundings()
        
        if(self.debugMode):
            #self.screenClear()  # Clear screen for better "immersion"
            self.printWorld()   # Show the user the console snake location  
            print(self.snake)
            print(self.gameState, self.resetCount)
        #print("\n", self.snakePerception)
        #self.AIMovement()
        if(self.terminalMode):
            self.AIMovement()
            self.updateWorld()

    # Placeholder for the training movement
    def AIMovement(self):
        movementList = list(Trajectory)[:4]
        filteredMovementList = list(filter(lambda s: s != -self.trajectoryInput, movementList))
        randomTrajec = randint(0, (len(filteredMovementList)-1))
        self.trajectoryInput = list(filteredMovementList)[randomTrajec]

    def updateSnakePos(self) -> None:
        if(self.snake.head.trajectory != self.trajectoryInput):
            self.snake.head.trajectory = self.trajectoryInput
            
        self.snake.move()

    def resetWorld(self) -> None:
        self.state.fill(0)
        # Add Walls
        self.state[0].fill(9)
        self.state[self.worldSize-1].fill(9)
        for i in range(1, self.worldSize-1):
            self.state[i][0] = 9
            self.state[i][self.worldSize-1] = 9

    def gameOver(self) -> bool:
        return not self.OOB(self.snake.head.location) or self.selfCollide()
        
    def printWorld(self) -> None:
        print(self.state)
        print("\n")

    def setSnake(self) -> None:
        body = self.snake.body
        for b in body:
            x, y = b.location.to_int()
            self.state[x][y] = 1

    def observeSurroundings(self) -> None:
        self.snakePerception = list()
        for i, direction in enumerate(list(Trajectory)):
            f, s, w = self.snake.look(direction)
            self.snakePerception += [f, s, w]
        
        self.snakePerception += self.snake.head.trajectory.OHE()
        self.snakePerception += self.snake.getTailTrajectory().OHE()
        #print("\n", len(self.snakePerception), self.snakePerception)
        
    def updateGameState(self) -> None:
        self.gameState[0]  += 1
        self.gameState[1]   = self.snake.size
        self.resetCount    += 1
        if self.resetCount == self.resetThresh: self.alive = False
        
    # Consider refactoring further using Point
    def OOB(self, loc: 'Point') -> bool:
        x, y = loc.to_int()
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
            self.resetCount = 0

        else:
            x, y = self.food.to_int()
            self.state[x][y] = 2 # Console "world" food representation

    def screenClear(self) -> None: 
        if name == 'nt': 
            _ = system('cls') 
        else: 
            _ = system('clear') 