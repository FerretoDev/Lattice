import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lattice.world import World

"""Test the World class"""


def test_set_and_get_block() -> None:
    world: World = World(10, 10)
    world.set_block(2, 3, 1)
    assert world.get_block(2, 3) == 1


def test_fill_rectangle():
    world: World = World(100, 100)

    world.fill_rectangle(1, 1, 30, 30, 1)
    assert world.get_block(1, 1) == 1
    assert world.get_block(31, 31) == 0  # Outside the rectangle


def test_fill_rectangle_exceeds_limit():
    world: World = World(100, 100)

    with pytest.raises(ValueError, match="Insert less than 1000 blocks"):
        world.fill_rectangle(1, 1, 40, 40, 1)  # 40x40 = 1600 blocks, exceeds limit


def test_fill_rectangle_exceeds_world_boundaries():
    world: World = World(100, 100)

    with pytest.raises(ValueError, match="Rectangle exceeds world boundaries"):
        world.fill_rectangle(1, 1, 101, 10, 1)  # x2=101 exceeds width=100


world = World(10000, 10000)
world.set_block(2, 3, 1)  # Setting block type 1 at (2, 3)
# print(world.get_block(2, 3))  # Output: '1' (stone)

# world.fill_rectangle(
#    1, 1, 4, 4, 1
# )  # Fill a rectangle from (0, 0) to (4, 4) with block type 1
# print(world.get_block(1, 1))  # Output: '1' (stone)
# print(world.get_block(5, 5))  # Output: '0' (air)


print(world.counter_blocks)
