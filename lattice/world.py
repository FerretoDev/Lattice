import numpy as np

"""
A simple 2D world representation using a grid. 
Each cell in the grid can hold a block type, represented by an integer.
"""
# slicing: Es la acción de dividir un todo en partes más pequeñas y manejables


# 0 is 'air'
# 1 is 'stone'
class World:
    """Represents a 2D grid world using 0-based coordinates."""

    # 'y' is the row index, and 'x' is the column index.

    # Numpy arrays are indexed as [row: vertical, column: horizontal], which corresponds to [y, x] in our world representation.

    def __init__(self, width: int, height: int) -> None:
        """Create an empty world with the given width and height."""
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
        """Return the inclusive area size for the rectangle defined by two points."""
        return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

    def _fill_split(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        block: int,
    ) -> None:
        """Recursively split large rectangles and fill each valid sub-rectangle."""
        x_start = min(x1, x2)
        x_end = max(x1, x2)
        y_start = min(y1, y2)
        y_end = max(y1, y2)

        if x_start < 0 or y_start < 0 or x_end >= self.width or y_end >= self.height:
            raise ValueError("Rectangle exceeds world boundaries")

        total = (x_end - x_start + 1) * (y_end - y_start + 1)
        if total <= self.MAX_BLOCKS:
            # Reuse the direct path once the size check passes.
            self._fill_direct(x_start, y_start, x_end, y_end, block)
            return

        if x_start == x_end and y_start == y_end:
            self._fill_direct(x_start, y_start, x_end, y_end, block)
            return

        if (x_end - x_start) >= (y_end - y_start):
            x_mid = (x_start + x_end) // 2
            self._fill_split(x_start, y_start, x_mid, y_end, block)
            self._fill_split(x_mid + 1, y_start, x_end, y_end, block)
            return

        y_mid = (y_start + y_end) // 2
        self._fill_split(x_start, y_start, x_end, y_mid, block)
        self._fill_split(x_start, y_mid + 1, x_end, y_end, block)

    def _fill_direct(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        block: int,
    ) -> None:
        """Fill a rectangle directly with NumPy slicing after bounds validation."""
        x_start = min(x1, x2)
        x_end = max(x1, x2)
        y_start = min(y1, y2)
        y_end = max(y1, y2)

        if x_start < 0 or y_start < 0 or x_end >= self.width or y_end >= self.height:
            raise ValueError("Rectangle exceeds world boundaries")

        # NumPy slicing is inclusive on the start and exclusive on the end, so add 1 there.
        self.grid[y_start : y_end + 1, x_start : x_end + 1] = int(block)

    def set_block(self, x: int, y: int, block: int) -> None:
        """Set a single cell value if the coordinates are inside world bounds."""
        x = int(x)
        y = int(y)
        if (
            0 <= x < self.width and 0 <= y < self.height
        ):  # Check if the coordinates are within bounds
            # The world uses 0-based coordinates directly.
            self.grid[y, x] = block

    def get_block(self, x: int, y: int) -> int | None:
        """Return a cell value for valid coordinates, otherwise None."""
        x = int(x)
        y = int(y)
        if (
            0 <= x < self.width and 0 <= y < self.height
        ):  # Check if the coordinates are within bounds
            # Access follows NumPy's [row, column] convention.
            return self.grid[
                y, x
            ]  # Use [y, x] to access the grid since it's indexed as [row, column] not [x, y] for numpy arrays
        return None

    def fill_rectangle(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        block: int,
    ) -> None:  # Fill a rectangular area with a specific block type
        """Fill an inclusive rectangle using direct fill or recursive splitting."""
        x_start = min(x1, x2)
        x_end = max(x1, x2)
        y_start = min(y1, y2)
        y_end = max(y1, y2)

        if x_start < 0 or y_start < 0 or x_end >= self.width or y_end >= self.height:
            raise ValueError("Rectangle exceeds world boundaries")

        # Count cells before choosing the write strategy.
        total = self._counter_blocks(x_start, y_start, x_end, y_end)

        if total >= self.MAX_BLOCKS:
            self._fill_split(x_start, y_start, x_end, y_end, block)
            return

        self._fill_direct(x_start, y_start, x_end, y_end, block)
