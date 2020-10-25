class Vision:
    def __init__(self, head: 'Point', state: 'np.array'):
        self.head = head
        self.worldState = state

    # Observes 
    def detectFood(self) -> list:
        pass

    def detectWall(self) -> list:
        pass

    def detectSelf(self) -> list:
        pass

    def targetDetected(self, target) -> bool:
        pass