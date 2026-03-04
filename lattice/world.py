import numpy as np

"""
A simple 2D world representation using a grid. 
Each cell in the grid can hold a block type, represented by an integer.
"""
# slicing: Es la acción de dividir un todo en partes más pequeñas y manejables


# 0 is 'air'
# 1 is 'stone'
class World:

    # 'y' is the row index, and

    # 'x' is the column index.

    # Numpy arrays are indexed as [row: vertical, column: horizontal], which corresponds to [y, x] in our world representation.

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)

    def set_block(self, x: int, y: int, block: int):
        x = int(x) - 1
        y = int(y) - 1
        if (
            0 <= x < self.width and 0 <= y < self.height
        ):  # Check if the coordinates are within bounds
            self.grid[y, x] = block

    def get_block(self, x: int, y: int):
        x = int(x) - 1
        y = int(y) - 1
        if (
            0 <= x < self.width and 0 <= y < self.height
        ):  # Check if the coordinates are within bounds
            return self.grid[
                y, x
            ]  # Use [y, x] to access the grid since it's indexed as [row, column] not [x, y] for numpy arrays
        return None

    def fill_reactangle(
        self, x1: int, y1: int, x2: int, y2: int, block: int
    ):  # Fill a rectangular area with a specific block type
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.set_block(x, y, block)
