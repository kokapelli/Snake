from World import World
from Snake import Snake
import time

if __name__ == "__main__":
    world = World()
    while(True):
        time.sleep(1.0)
        world.updateWorld()