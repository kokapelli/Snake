class Block:
    def __init__(self, spawnLoc, trajectory, adjacent, isHead = False):
        self.isHead = isHead
        self.location = spawnLoc
        self.trajectory = trajectory
        self.adjacentBody = adjacent
        self.trajectoryChange = False

    def __repr__(self):
        string = f"({self.location}{self.trajectory})"
        return string

    # Used to update the location of the snake piece by one time step
    def move(self):
        if(self.trajectoryChange and not self.isHead):
            self.setTrajectory(self.adjacentBody.getTrajectory())
        
        self.location = [x + y for x, y in zip(self.location, self.trajectory)]
        
    def getLoc(self):
        return self.location

    def getTrajectory(self):
        return self.trajectory 

    def getTrajectoryChange(self):
        return self.trajectoryChange

    def getAdjacentBody(self):
        return self.adjacentBody

    def setTrajectory(self, trajectory):
        self.trajectory = trajectory

    def setTrajectoryChange(self, boolean):
        self.trajectoryChange = boolean