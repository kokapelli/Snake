import numpy as np

class Block:
    def __init__(self, 
                 spawnLoc: 'Point', 
                 trajectory: 'Point', 
                 adjacent: 'Block', 
                 isHead: bool= False):
                 
        self.isHead = isHead
        self.location = spawnLoc
        self.adjacentBody = adjacent
        self.trajectory = trajectory
        if(isHead):
            self.nextLocation = None
        else:
            self.nextLocation = self.adjacentBody.location

    def __repr__(self) -> str:
        string = f"({self.location})"
        return string

    def move(self) -> None:
        if(not self.isHead):
            self.location = self.nextLocation
            self.nextLocation = self.adjacentBody.location
        else:
            self.location = self.location + self.trajectory.value
        