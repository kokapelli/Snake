class Vision():
    def __init__(self,
                 dist_to_wall: int,
                 dist_to_apple: int,
                 dist_to_self: int
                 ):

        self.dist_to_wall = dist_to_wall
        self.dist_to_apple = dist_to_apple
        self.dist_to_self = dist_to_self