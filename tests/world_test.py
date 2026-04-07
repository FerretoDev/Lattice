import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lattice.world import World


def test_set_and_get_block() -> None:
    world: World = World(10, 10)
    world.set_block(1, 2, 1)
    assert world.get_block(1, 2) == 1


def test_fill_rectangle_fills_inclusive_area() -> None:
    world: World = World(10, 10)

    world.fill_rectangle(1, 2, 3, 4, 1)

    for y in range(2, 5):
        for x in range(1, 4):
            assert world.get_block(x, y) == 1

    assert world.get_block(0, 0) == 0
    assert world.get_block(4, 5) == 0


def test_fill_rectangle_accepts_reversed_coordinates() -> None:
    world: World = World(10, 10)

    world.fill_rectangle(4, 5, 1, 2, 2)

    for y in range(2, 6):
        for x in range(1, 5):
            assert world.get_block(x, y) == 2


def test_fill_rectangle_splits_and_fills_large_area() -> None:
    world: World = World(100, 100)

    world.fill_rectangle(0, 0, 39, 39, 1)  # 40x40 = 1600 blocks, exceeds limit

    for y in range(0, 40):
        for x in range(0, 40):
            assert world.get_block(x, y) == 1

    assert world.get_block(40, 40) == 0


def test_fill_rectangle_raises_when_out_of_bounds() -> None:
    world: World = World(100, 100)

    with pytest.raises(ValueError, match="Rectangle exceeds world boundaries"):
        world.fill_rectangle(0, 0, 100, 9, 1)  # x2=100 exceeds width=100


def test_fill_rectangle_uses_direct_for_small_areas(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    world: World = World(10, 10)
    called: list[tuple[int, int, int, int, int]] = []

    def fake_fill_direct(x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        called.append((x1, y1, x2, y2, block))

    monkeypatch.setattr(world, "_fill_direct", fake_fill_direct)

    world.fill_rectangle(0, 0, 9, 9, 3)

    assert called == [(0, 0, 9, 9, 3)]


def test_fill_rectangle_uses_split_for_large_areas(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    world: World = World(50, 50)
    called: list[tuple[int, int, int, int, int]] = []

    def fake_fill_split(x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        called.append((x1, y1, x2, y2, block))

    monkeypatch.setattr(world, "_fill_split", fake_fill_split)

    world.fill_rectangle(0, 0, 49, 20, 4)

    assert called == [(0, 0, 49, 20, 4)]


def test_fill_rectangle_uses_split_for_exact_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    world: World = World(50, 50)
    called: list[tuple[int, int, int, int, int]] = []

    def fake_fill_split(x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        called.append((x1, y1, x2, y2, block))

    monkeypatch.setattr(world, "_fill_split", fake_fill_split)

    world.fill_rectangle(0, 0, 24, 39, 5)

    assert called == [(0, 0, 24, 39, 5)]
