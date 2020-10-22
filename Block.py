class Block:
    def __init__(self, spawnLoc, trajectory, adjacent, isHead = False):
        self.isHead = isHead
        self.location = spawnLoc
        self.trajectory = trajectory
        self.adjacentBody = adjacent
        self.trajectoryChange = False
        self.nextTrajectory = 0

    def __repr__(self):
        string = f"({self.location}{self.trajectory}{self.trajectoryChange})"
        return string

    # Used to update the location of the snake piece by one time step
    def move(self):
        if(self.trajectoryChange and not self.isHead):
            self.trajectory = self.nextTrajectory
        
        self.location = [x + y for x, y in zip(self.location, self.trajectory)]
        
    @property
    def location(self):
        return self._location

    @property
    def trajectory(self):
        return self._trajectory

    @property
    def trajectoryChange(self):
        return self._trajectoryChange

    @property
    def adjacentBody(self):
        return self._adjacentBody

    @property
    def nextTrajectory(self):
        return self._nextTrajectory

    @location.setter
    def location(self, loc):
        self._location = loc

    @trajectory.setter
    def trajectory(self, trajectory):
        self._trajectory = trajectory

    @trajectoryChange.setter
    def trajectoryChange(self, trajectoryChange):
        self._trajectoryChange = trajectoryChange

    @adjacentBody.setter
    def adjacentBody(self, body):
        self._adjacentBody = body

    @nextTrajectory.setter
    def nextTrajectory(self, trajectory):
        self._nextTrajectory = trajectory
