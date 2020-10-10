class Block:
    def __init__(self, spawnLoc, trajectory, isHead = False):
        self.isHead = isHead
        self.location = spawnLoc
        self.trajectory = trajectory
        self.postLocation = spawnLoc # Used to determine when a trajectory change takes place
        
        if(self.isHead):        # Snake representation 81111, needs revision
            self.repr = '8'
        else:
            self.repr = '1'

    # Used to update the location of the snake piece by one time step
    def move(self):
        self.location = [x + y for x, y in zip(self.location, self.trajectory)]
        
    def getLoc(self):
        return self.location

    def getTrajectory(self):
        return self.trajectory

    def getRepr(self):
        return self.repr
