from Block import Block
import numpy as np


class Snake:
    def __init__(self, world):
        # (-1, 0) Move Up 
        # (1, 0) Move Down
        # (0, -1) Move Left
        # (0, 1) Move Right

        #Primarily used to get the world 
        # size and to establish a random spawn point
        self.world = world
        self.head = Block([10, 10], [0, -1], None, True)
        self.body = [self.head]
        self.size = 1
        self.createInitSnake()

    def __repr__(self):
        string = ""
        for i in self.body:
            if(not i.isHead):
                string += f"<-{i}"
            else:
                string += str(i)

        return string
    
    
    def createInitSnake(self, bodyLen=1):
        for _ in range(bodyLen):
            self.growSnake()

    def move(self):
        for b in self.body:
            b.move()
        self.pushTrajectoryChange()


    def growSnake(self):
        end = self.body[-1]
        endCoord, endTrajectory = self.getEndPiece(end)
        # Negate trajectory to place the new piece at the back of the snake
        bodyPartCoord = [x + y for x, y in zip(endCoord, np.negative(endTrajectory))]
        bodyPart = Block(bodyPartCoord, endTrajectory, end)
        self.body.append(bodyPart)
        self.size += 1

    def pushTrajectoryChange(self):
        # As trajectory changes are done in reverse, the last element must be removed manually
        if(self.body[-1].trajectoryChange):
            self.body[-1].trajectoryChange = False

        # Trajectory changes are applied reversed as to solve an otherwise cascading trajectory effect
        for b in list(reversed(self.body)):
            if(b.isHead):
                continue
            if(b.adjacentBody.trajectoryChange):
                b.adjacentBody.trajectoryChange = False
                b.trajectoryChange = True
                b.nextTrajectory = b.adjacentBody.trajectory

    def getSnakeSize(self):
        return self.size

    def getHeadLoc(self):
        return self.head.location

    def getHeadTrajectory(self):
        return self.head.trajectory
        
    def getBody(self):
        return self.body

    def setHeadTrajectory(self, newTrajectory):
        self.head.trajectory = newTrajectory
        self.head.trajectoryChange = True


    def getBodyLoc(self):
        bodyLoc = list()
        for b in self.body:
            bodyLoc.append(b.location)

        return bodyLoc

    def getEndPiece(self, end):
        endCoord = end.location
        endTrajectory = np.array(end.trajectory) # type change to negate array cleaner
        
        return endCoord, endTrajectory

    def describeSnake(self):
        for b in self.body:
            print(f"Coord: {b.location}  Trajectory: {b.trajectory}")

    def getBodyPartLocs(self):
        locs = list()
        # Convert locations to tuples to more easily find collisions
        for b in self.body:
            locs.append((b.location[0], b.location[1]))
        return locs

    def checkCollision(self):
        locs = self.getBodyPartLocs()
        #print(locs, len(locs))
        return len(locs) != len(set(locs))
