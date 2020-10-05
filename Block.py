class Block:
    def __init__(self, spawnLoc, trajectory):
        self.location = spawnLoc
        self.trajectory = trajectory

    def move(self):
        self.location = (self.location[0] + self.trajectory[0], self.location[1] + self.trajectory[1])

    def getLoc(self):
        return self.location