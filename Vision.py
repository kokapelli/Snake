class Vision:
    def __init__(self, head: 'Point', world: 'np.array'):
        self.head = head
        self.worldState = world

    def detectFood(self):
        pass

    def detectWall(self):
        pass

    def detectSelf(self):
        pass