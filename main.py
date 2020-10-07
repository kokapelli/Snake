from World import World
from Snake import Snake
import time
GAME_SPEED = 0.5

if __name__ == "__main__":
    world = World()
    while(world.isAlive()):
        time.sleep(GAME_SPEED)
        world.updateWorld()