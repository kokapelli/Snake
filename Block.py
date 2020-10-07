class Block:
    def __init__(self, spawnLoc, trajectory, isHead = False):
        self.isHead = isHead
        self.location = spawnLoc
        self.trajectory = trajectory
        
        if(self.isHead):        # Snake representation 8#####, needs revision
            self.repr = '1'
        else:
            self.repr = '#'

    def move(self):
        self.location = (self.location[0] + self.trajectory[0], self.location[1] + self.trajectory[1])

    def getLoc(self):
        return self.location

    def getRepr(self):
        return self.repr