from Block import Block
from Movement import Point, Trajectory
import numpy as np


class Snake:
    def __init__(self, world):
        #Primarily used to get the world 
        # size and to establish a random spawn point
        self.world = world
        self.head = Block(Point(10, 10), Trajectory.LEFT, None, True)
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
        
    def move(self):
        for b in self.body:
            b.move()
        self.pushTrajectoryChange()
    
    def createInitSnake(self, bodyLen=1):
        #print(self.head)
        for _ in range(bodyLen):
            self.growSnake()

    def growSnake(self):
        end = self.body[-1]
        endCoord = end.location
        # Negate trajectory to place the new piece at the back of the snake
        endTrajectory = end.trajectory
        bodyPartCoord = endCoord + -endTrajectory.value
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


    def setHeadTrajectory(self, newTrajectory):
        self.head.trajectory = newTrajectory
        self.head.trajectoryChange = True

    def getBodyLoc(self):
        bodyLoc = list()
        for b in self.body:
            bodyLoc.append(b.location)

        return bodyLoc

    def describeSnake(self):
        for b in self.body:
            print(f"Coord: {b.location}  Trajectory: {b.trajectory}")

    def getBodyPartLocs(self):
        locs = list()
        # Convert locations to tuples to more easily find collisions
        for b in self.body:
            locs.append(b.location)
        return locs

    def checkCollision(self):
        locs = self.getBodyPartLocs()
        #print(locs, len(locs))
        return len(locs) != len(set(locs))
