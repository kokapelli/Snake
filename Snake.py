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
    def look(self) -> dict:
        targetDistances = dict
        for i in list(Trajectory):
            if i == Trajectory(-self.head.trajectory.value): continue
                
            print(i)
    
        return targetDistances
    
    def createInitSnake(self, bodyLen: int=1) -> None:
        startLoc = Point(10, 10)
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
