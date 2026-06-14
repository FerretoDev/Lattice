import numpy as np

def validate_bounds(x1: int, y1: int, x2: int, y2: int, width: int, height: int) -> None:
    """Raise if coordinates exceed the world boundaries."""
    if x1 < 0 or y1 < 0 or x2 >= width or y2 >= height:
        raise ValueError("Rectangle exceeds world boundaries")

def count_blocks(x1: int, y1: int, x2: int, y2: int) -> int:
    """Return the inclusive block count for a rectangle."""
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

def fill_direct(grid: np.ndarray, x1: int, y1: int, x2: int, y2: int, block: int, width: int, height: int) -> None:
    """Fill coordinates using direct NumPy slice assignment."""
    x_start, x_end = min(x1, x2), max(x1, x2)
    y_start, y_end = min(y1, y2), max(y1, y2)
    validate_bounds(x_start, y_start, x_end, y_end, width, height)
    grid[y_start : y_end + 1, x_start : x_end + 1] = int(block)
