from Block import Block
from Movement import Point, Trajectory
import numpy as np

class Snake:
    def __init__(self, world: np.array):
        self.world = world
        self.createInitSnake()

    def __repr__(self) -> str:
        string = ""
        for i in self.body:
            string += str(i)

        return string
        
    def move(self) -> None:
        for b in self.body:
            b.move()

    # Detect the distances to:
    # Food, Itself, Walls
    def look(self, direction: 'Trajectory') -> float:
        seen      = 0
        counter   = 1
        currSpot  = self.head.location
        wallDist  = None
        foodDist  = np.inf
        selfDist  = np.inf

        # Scuffed solution
        while(self.world.OOB(currSpot)):
            currSpot += direction.value
            x, y = currSpot.to_int()
            seen = self.world.worldState[x][y]

            # Generates sketchy values. Right next to food = 1, next 0.5 -> 0.33 -> 0.25 -> 0.2...
            if   seen == 2: foodDist = float("{:.4f}".format(1/counter)) # Normalizing
            elif seen == 1: selfDist = float("{:.4f}".format(1/counter)) # Normalizing
            elif seen == 9: wallDist = float("{:.4f}".format(1/counter)) # Normalizing
            else: self.world.worldState[x][y] = 8     # Display the sight of the snake

            counter += 1
        
        # Revamp at a later stage
        if foodDist == np.inf: foodDist = 1/foodDist
        if selfDist == np.inf: selfDist = 1/selfDist

        return foodDist, selfDist, wallDist
    
    def createInitSnake(self, bodyLen: int=1) -> None:
        startLoc  = Point(10, 10)
        self.head = Block(startLoc, Trajectory.UP, None, True)
        self.body = [self.head]
        self.size = 1

        for _ in range(bodyLen):
            self.growSnake()

    def growSnake(self) -> None:
        end = self.body[-1]
        # Negate trajectory to place the new piece at the back of the snake
        bodyPartCoord = end.location + -end.trajectory.value
        bodyPart = Block(bodyPartCoord, end.trajectory, end)
        self.body.append(bodyPart)
        self.size += 1

    def getBodyPartLocs(self) -> list:
        locs = list()
        for b in self.body:
            locs.append(b.location)
        return locs

    def checkCollision(self) -> bool:
        locs = self.getBodyPartLocs()
        return len(locs) != len(set(locs))

    def getTailTrajectory(self) -> list:
        b2 = self.body[-2].location
        b1 = self.body[-1].location
        diff = b2 - b1
        return Trajectory(diff)