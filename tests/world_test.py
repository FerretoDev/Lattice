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


# ------------------------------------------------------------------
# Chunk system
# ------------------------------------------------------------------


def test_all_chunks_loaded_by_default() -> None:
    world = World(32, 32, chunk_size=16)
    assert (0, 0) in world.loaded_chunks
    assert (1, 0) in world.loaded_chunks
    assert (0, 1) in world.loaded_chunks
    assert (1, 1) in world.loaded_chunks


def test_fill_raises_when_chunk_unloaded() -> None:
    world = World(32, 32, chunk_size=16)
    world.unload_chunk(1, 0)

    with pytest.raises(ValueError, match="Chunk \\(1, 0\\) is not loaded"):
        world.fill_rectangle(16, 0, 31, 15, 1)


def test_force_load_allows_fill() -> None:
    world = World(32, 32, chunk_size=16)
    world.unload_chunk(1, 0)
    world.force_load(1, 0)

    world.fill_rectangle(16, 0, 31, 15, 1)

    assert world.get_block(16, 0) == 1
    assert world.get_block(31, 15) == 1


def test_fill_raises_when_one_of_many_chunks_unloaded() -> None:
    world = World(64, 16, chunk_size=16)
    world.unload_chunk(2, 0)

    with pytest.raises(ValueError, match="not loaded"):
        world.fill_rectangle(0, 0, 63, 15, 1)


def test_get_chunk_returns_correct_coords() -> None:
    world = World(64, 64, chunk_size=16)
    assert world._get_chunk(0, 0) == (0, 0)
    assert world._get_chunk(15, 15) == (0, 0)
    assert world._get_chunk(16, 0) == (1, 0)
    assert world._get_chunk(0, 16) == (0, 1)
    assert world._get_chunk(63, 63) == (3, 3)


# ------------------------------------------------------------------
# Boundary edge cases
# ------------------------------------------------------------------


def test_fill_single_cell() -> None:
    world = World(10, 10)
    world.fill_rectangle(5, 5, 5, 5, 1)
    assert world.get_block(5, 5) == 1


def test_fill_top_left_corner() -> None:
    world = World(10, 10)
    world.fill_rectangle(0, 0, 0, 0, 1)
    assert world.get_block(0, 0) == 1


def test_fill_bottom_right_corner() -> None:
    world = World(10, 10)
    world.fill_rectangle(9, 9, 9, 9, 1)
    assert world.get_block(9, 9) == 1


def test_fill_raises_at_exact_boundary() -> None:
    world = World(10, 10)
    with pytest.raises(ValueError, match="Rectangle exceeds world boundaries"):
        world.fill_rectangle(0, 0, 10, 9, 1)  # x2 == width, out of bounds


def test_get_block_returns_none_outside_bounds() -> None:
    world = World(10, 10)
    assert world.get_block(-1, 0) is None
    assert world.get_block(0, -1) is None
    assert world.get_block(10, 0) is None
    assert world.get_block(0, 10) is None
