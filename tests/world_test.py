import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lattice.world import World


def test_set_and_get_block() -> None:
    world: World = World(10, 10)
    world.set_block(2, 3, 1)
    assert world.get_block(2, 3) == 1


def test_fill_rectangle_fills_inclusive_area() -> None:
    world: World = World(10, 10)

    world.fill_rectangle(2, 3, 4, 5, 1)

    for y in range(3, 6):
        for x in range(2, 5):
            assert world.get_block(x, y) == 1

    assert world.get_block(1, 1) == 0
    assert world.get_block(5, 6) == 0


def test_fill_rectangle_accepts_reversed_coordinates() -> None:
    world: World = World(10, 10)

    world.fill_rectangle(5, 6, 2, 3, 2)

    for y in range(3, 7):
        for x in range(2, 6):
            assert world.get_block(x, y) == 2


def test_fill_rectangle_raises_when_area_exceeds_limit() -> None:
    world: World = World(100, 100)

    with pytest.raises(ValueError, match="Insert less than 1000 blocks"):
        world.fill_rectangle(1, 1, 40, 40, 1)  # 40x40 = 1600 blocks, exceeds limit


def test_fill_rectangle_raises_when_out_of_bounds() -> None:
    world: World = World(100, 100)

    with pytest.raises(ValueError, match="Rectangle exceeds world boundaries"):
        world.fill_rectangle(1, 1, 101, 10, 1)  # x2=101 exceeds width=100


def test_fill_rectangle_uses_direct_for_small_areas(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    world: World = World(10, 10)
    called: list[tuple[int, int, int, int, int]] = []

    def fake_fill_direct(x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        called.append((x1, y1, x2, y2, block))

    monkeypatch.setattr(world, "_fill_direct", fake_fill_direct)

    world.fill_rectangle(1, 1, 10, 10, 3)

    assert called == [(1, 1, 10, 10, 3)]


def test_fill_rectangle_uses_split_for_large_areas(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    world: World = World(50, 50)
    called: list[tuple[int, int, int, int, int]] = []

    def fake_fill_split(x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        called.append((x1, y1, x2, y2, block))

    monkeypatch.setattr(world, "_fill_split", fake_fill_split)

    world.fill_rectangle(1, 1, 50, 21, 4)

    assert called == [(1, 1, 50, 21, 4)]
