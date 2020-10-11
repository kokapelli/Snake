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
        if(self.adjacentBody is not None):
            print("Adjacent",self.adjacentBody, self.trajectoryChange)
            if(self.trajectoryChange):
                self.trajectory = self.adjacentBody.getTrajectory()
                self.trajectoryChange = False

            self.location = [x + y for x, y in zip(self.location, self.trajectory)]

            if(self.adjacentBody.getTrajectoryChange()):
                self.setTrajectoryChange()
        else:
            self.location = [x + y for x, y in zip(self.location, self.trajectory)]

        
    def getLoc(self):
        return self.location

    def getTrajectory(self):
        return self.trajectory 

    def getTrajectoryChange(self):
        return self.trajectoryChange

    def setTrajectory(self, trajectory):
        self.trajectory = trajectory

    def setTrajectoryChange(self):
        self.trajectoryChange = True