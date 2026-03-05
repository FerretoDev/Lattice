import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lattice.world import World

matplotlib.use("Agg")  # Use non-interactive backend for tests

"""Test the World class"""


def test_set_and_get_block():
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


def test_draw_returns_axes():
    world: World = World(5, 5)
    world.set_block(2, 3, 1)
    ax = world.draw()
    assert ax is not None
    plt.close("all")


def test_draw_uses_provided_axes():
    world: World = World(5, 5)
    _, ax = plt.subplots()
    result = world.draw(ax=ax)
    assert result is ax
    plt.close("all")


