import numpy as np

"""
A simple 2D world representation using a grid. 
Each cell in the grid can hold a block type, represented by an integer.
"""
# slicing: Es la acción de dividir un todo en partes más pequeñas y manejables


# 0 is 'air'
# 1 is 'stone'
class World:
    # 'y' is the row index, and 'x' is the column index.

    # Numpy arrays are indexed as [row: vertical, column: horizontal], which corresponds to [y, x] in our world representation.

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.MAX_BLOCKS = 1000

    def _counter_blocks(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ):
        counter_blocks: int = 0
        for y in range(min(y1, y2), max(y1, y2) + 1):  # row
            for x in range(min(x1, x2), max(x1, x2) + 1):  # column
                counter_blocks += 1  # Increment the block counter for each block set
        return counter_blocks

    def _fill_split(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        block: int,
    ) -> None:
        x_start = min(x1, x2)
        x_end = max(x1, x2)
        y_start = min(y1, y2)
        y_end = max(y1, y2)

        if x_start < 1 or y_start < 1 or x_end > self.width or y_end > self.height:
            raise ValueError("Rectangle exceeds world boundaries")

        total = (x_end - x_start + 1) * (y_end - y_start + 1)
        if total > self.MAX_BLOCKS:
            raise ValueError("Insert less than 1000 blocks")

        self._fill_direct(x_start, y_start, x_end, y_end, block)

    def _fill_direct(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        block: int,
    ) -> None:
        x_start = min(x1, x2)
        x_end = max(x1, x2)
        y_start = min(y1, y2)
        y_end = max(y1, y2)

        if x_start < 1 or y_start < 1 or x_end > self.width or y_end > self.height:
            raise ValueError("Rectangle exceeds world boundaries")

        # Translate 1-based coordinates to 0-based slicing.
        self.grid[y_start - 1 : y_end, x_start - 1 : x_end] = int(block)

    def set_block(self, x: int, y: int, block: int) -> None:
        # Client or for programmer, the coordinates are 1-based, but internally we use 0-based indexing for the grid
        x = int(x) - 1
        y = int(y) - 1
        if (
            0 <= x < self.width and 0 <= y < self.height
        ):  # Check if the coordinates are within bounds
            self.grid[y, x] = block

    def get_block(self, x: int, y: int) -> int | None:
        x = int(x) - 1
        y = int(y) - 1
        if (
            0 <= x < self.width and 0 <= y < self.height
        ):  # Check if the coordinates are within bounds
            return self.grid[
                y, x
            ]  # Use [y, x] to access the grid since it's indexed as [row, column] not [x, y] for numpy arrays
        return None

    def fill_rectangle(
        # Server or for programmer, the coordinates are 1-based, but internally we use 0-based indexing for the grid
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        block: int,
    ) -> None:  # Fill a rectangular area with a specific block type
        x_start = min(x1, x2)
        x_end = max(x1, x2)
        y_start = min(y1, y2)
        y_end = max(y1, y2)

        if x_start < 1 or y_start < 1 or x_end > self.width or y_end > self.height:
            raise ValueError("Rectangle exceeds world boundaries")

        total = self._counter_blocks(x_start, y_start, x_end, y_end)

        if total > self.MAX_BLOCKS:
            self._fill_split(x_start, y_start, x_end, y_end, block)
            return

        self._fill_direct(x_start, y_start, x_end, y_end, block)
