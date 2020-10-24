import numpy as np

class Block:
    def __init__(self, spawnLoc, trajectory, adjacent, isHead = False):
        self.isHead = isHead
        self.location = spawnLoc
        self.trajectory = trajectory
        self.adjacentBody = adjacent
        self.trajectoryChange = False
        self.nextTrajectory = trajectory

    def __repr__(self):
        string = f"({self.location}/{self.trajectory.name}/{self.trajectoryChange})"
        return string

    # Used to update the location of the snake piece by one time step
    def move(self):
        if(self.trajectoryChange and not self.isHead):
            self.trajectory = self.nextTrajectory
        self.location = self.location + self.trajectory.value
        #self.location = [x + y for x, y in zip(self.location, self.trajectory)]