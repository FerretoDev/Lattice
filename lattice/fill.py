import numpy as np

def validate_bounds_3d(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, width: int, height: int, depth: int) -> None:
    """Raise if coordinates exceed the world boundaries."""
    if x1 < 0 or y1 < 0 or z1 < 0 or x2 >= width or y2 >= height or z2 >= depth:
        raise ValueError("Rectangle exceeds world boundaries")

def count_blocks_3d(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> int:
    """Return the inclusive block count for a 3D box."""
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1) * (abs(z2 - z1) + 1)

def fill_direct_3d(grid: np.ndarray, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, block: int, width: int, height: int, depth: int) -> None:
    """Fill coordinates using direct NumPy slice assignment."""
    x_start, x_end = min(x1, x2), max(x1, x2)
    y_start, y_end = min(y1, y2), max(y1, y2)
    z_start, z_end = min(z1, z2), max(z1, z2)
    validate_bounds_3d(x_start, y_start, z_start, x_end, y_end, z_end, width, height, depth)
    grid[z_start : z_end + 1, y_start : y_end + 1, x_start : x_end + 1] = int(block)

def fill_split_3d(grid: np.ndarray, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, block: int, max_blocks: int, width: int, height: int, depth: int) -> None:
    """Recursively split along the longest axis until each piece fits max_blocks."""
    x_start, x_end = min(x1, x2), max(x1, x2)
    y_start, y_end = min(y1, y2), max(y1, y2)
    z_start, z_end = min(z1, z2), max(z1, z2)
    validate_bounds_3d(x_start, y_start, z_start, x_end, y_end, z_end, width, height, depth)

    dx = x_end - x_start + 1
    dy = y_end - y_start + 1
    dz = z_end - z_start + 1
    total = dx * dy * dz

    if total <= max_blocks or (x_start == x_end and y_start == y_end and z_start == z_end):
        fill_direct_3d(grid, x_start, y_start, z_start, x_end, y_end, z_end, block, width, height, depth)
        return

    # Split along the longest axis
    if dx >= dy and dx >= dz:
        x_mid = (x_start + x_end) // 2
        fill_split_3d(grid, x_start, y_start, z_start, x_mid, y_end, z_end, block, max_blocks, width, height, depth)
        fill_split_3d(grid, x_mid + 1, y_start, z_start, x_end, y_end, z_end, block, max_blocks, width, height, depth)
    elif dy >= dx and dy >= dz:
        y_mid = (y_start + y_end) // 2
        fill_split_3d(grid, x_start, y_start, z_start, x_end, y_mid, z_end, block, max_blocks, width, height, depth)
        fill_split_3d(grid, x_start, y_mid + 1, z_start, x_end, y_end, z_end, block, max_blocks, width, height, depth)
    else:
        z_mid = (z_start + z_end) // 2
        fill_split_3d(grid, x_start, y_start, z_start, x_end, y_end, z_mid, block, max_blocks, width, height, depth)
        fill_split_3d(grid, x_start, y_start, z_mid + 1, x_end, y_end, z_end, block, max_blocks, width, height, depth)
