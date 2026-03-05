import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.counter_blocks = 0

    def set_block(self, x: int, y: int, block: int):
        # Client or for programmer, the coordinates are 1-based, but internally we use 0-based indexing for the grid
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

    def fill_rectangle(
        # Server or for programmer, the coordinates are 1-based, but internally we use 0-based indexing for the grid
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        block: int,
    ):  # Fill a rectangular area with a specific block type

        # absolute value: abs() is a built-in function in Python that returns the absolute value of a number. The absolute value of a number is its distance from zero on the number line, regardless of direction. For example, abs(-5) would return 5, and abs(5) would also return 5.
        fill_height = abs(y2 - y1) + 1  # Calculate the height of the rectangle
        fill_width = abs(x2 - x1) + 1  # Calculate the width of the rectangle

        if x1 < 1 or y1 < 1 or x2 > self.width or y2 > self.height:
            raise ValueError("Rectangle exceeds world boundaries")

        if fill_height * fill_width > 1000:
            raise ValueError("Insert less than 1000 blocks")

        for y in range(min(y1, y2), max(y1, y2) + 1):  # row
            for x in range(min(x1, x2), max(x1, x2) + 1):  # column
                self.set_block(x, y, block)
                self.counter_blocks += (
                    1  # Increment the block counter for each block set
                )

    def draw(self, ax=None):
        """Render the world grid using a heatmap with visible grid lines.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Axes to draw on. If None, a new figure and axes are created.

        Returns
        -------
        matplotlib.axes.Axes
            The axes with the rendered grid.
        """
        if ax is None:
            _, ax = plt.subplots()

        sns.heatmap(
            self.grid,
            cmap="binary",
            cbar=False,
            linewidths=1,
            linecolor="gray",
            square=True,
            xticklabels=range(1, self.width + 1),  # type: ignore
            yticklabels=range(1, self.height + 1),  # type: ignore
            ax=ax,
        )

        return ax
