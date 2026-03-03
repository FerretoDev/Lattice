import numpy as np

"""
A simple 2D world representation using a grid. 
Each cell in the grid can hold a block type, represented by an integer.
"""


# 0 is 'air'
# 1 is 'stone'
class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)

    def set_block(self, x: int, z: int, block: int):
        if (
            0 <= x < self.width and 0 <= z < self.height
        ):  # Check if the coordinates are within bounds
            self.grid[z, x] = block

    def get_block(self, x: int, z: int):
        if (
            0 <= x < self.width and 0 <= z < self.height
        ):  # Check if the coordinates are within bounds
            return self.grid[z, x]
        return None

    def fill_reactangle(
        self, x1: int, z1: int, x2: int, z2: int, block: int
    ):  # Fill a rectangular area with a specific block type
        for z in range(min(z1, z2), max(z1, z2) + 1):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.set_block(x, z, block)
