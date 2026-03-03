import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lattice.world import World

"""Test the World class"""


world = World(10, 10)
world.set_block(2, 3, 1)  # Setting block type 1 at (2, 3)
print(world.get_block(2, 3))  # Output: '1' (stone)
world.fill_reactangle(
    0, 0, 4, 4, 1
)  # Fill a rectangle from (0, 0) to (4, 4) with block type 1
print(world.get_block(1, 1))  # Output: '1' (stone)
print(world.get_block(5, 5))  # Output: '0' (air)
