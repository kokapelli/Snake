from Block import Block

class Snake:
    def __init__(self):
        # Spawn the head at x:10, y:10. Have it move up, one block at a time
        # (-1, 0) Move Up 
        # (1, 0) Move Down
        # (0, -1) Move Left
        # (0, 1) Move Right
        
        self.head = Block((10, 10), (0,-1))
        self.body = [self.head]
        self.length = 1

    def move(self):
        for b in self.body:
            b.move()

    def getBodyLoc(self):
        bodyLoc = list()
        for b in self.body:
            bodyLoc.append(b.getLoc())

        return bodyLoc