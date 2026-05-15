import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

BLOCK_COLORS: dict[int, str] = {
    0: "#87CEEB",  # air
    1: "#808080",  # stone
    2: "#228B22",  # grass
    3: "#8B4513",  # dirt
    4: "#FFD700",  # sand
}


class World:
    """Represents a 2D grid world using 0-based coordinates."""

    def __init__(self, width: int, height: int, chunk_size: int = 16) -> None:
        self.width = width
        self.height = height
        self.chunk_size = chunk_size
        self.grid = np.zeros((height, width), dtype=int)
        self.MAX_BLOCKS = 1000
        self.loaded_chunks: set[tuple[int, int]] = set()
        self._load_all_chunks()

    # ------------------------------------------------------------------
    # Chunk system
    # ------------------------------------------------------------------

    def _chunks_in_axis(self, size: int) -> int:
        return (size + self.chunk_size - 1) // self.chunk_size

    def _load_all_chunks(self) -> None:
        for cy in range(self._chunks_in_axis(self.height)):
            for cx in range(self._chunks_in_axis(self.width)):
                self.loaded_chunks.add((cx, cy))

    def _get_chunk(self, x: int, y: int) -> tuple[int, int]:
        return (x // self.chunk_size, y // self.chunk_size)

    def force_load(self, cx: int, cy: int) -> None:
        self.loaded_chunks.add((cx, cy))

    def unload_chunk(self, cx: int, cy: int) -> None:
        self.loaded_chunks.discard((cx, cy))

    def _check_loaded(self, x1: int, y1: int, x2: int, y2: int) -> None:
        cx1, cy1 = self._get_chunk(x1, y1)
        cx2, cy2 = self._get_chunk(x2, y2)
        for cy in range(cy1, cy2 + 1):
            for cx in range(cx1, cx2 + 1):
                if (cx, cy) not in self.loaded_chunks:
                    raise ValueError(f"Chunk ({cx}, {cy}) is not loaded")

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _validate_bounds(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Raise if normalized (x1 <= x2, y1 <= y2) coords exceed the grid."""
        if x1 < 0 or y1 < 0 or x2 >= self.width or y2 >= self.height:
            raise ValueError("Rectangle exceeds world boundaries")

    def _count_blocks(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Return inclusive area for a normalized rectangle."""
        return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

    # ------------------------------------------------------------------
    # Fill internals
    # ------------------------------------------------------------------

    def _fill_direct(self, x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        x_start, x_end = min(x1, x2), max(x1, x2)
        y_start, y_end = min(y1, y2), max(y1, y2)
        self._validate_bounds(x_start, y_start, x_end, y_end)
        self.grid[y_start : y_end + 1, x_start : x_end + 1] = int(block)

    def _fill_split(self, x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        """Recursively split along the longest axis until each piece fits MAX_BLOCKS."""
        x_start, x_end = min(x1, x2), max(x1, x2)
        y_start, y_end = min(y1, y2), max(y1, y2)
        self._validate_bounds(x_start, y_start, x_end, y_end)

        total = (x_end - x_start + 1) * (y_end - y_start + 1)
        if total <= self.MAX_BLOCKS or (x_start == x_end and y_start == y_end):
            self._fill_direct(x_start, y_start, x_end, y_end, block)
            return

        if (x_end - x_start) >= (y_end - y_start):
            x_mid = (x_start + x_end) // 2
            self._fill_split(x_start, y_start, x_mid, y_end, block)
            self._fill_split(x_mid + 1, y_start, x_end, y_end, block)
        else:
            y_mid = (y_start + y_end) // 2
            self._fill_split(x_start, y_start, x_end, y_mid, block)
            self._fill_split(x_start, y_mid + 1, x_end, y_end, block)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_block(self, x: int, y: int, block: int) -> None:
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = block

    def get_block(self, x: int, y: int) -> int | None:
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x]
        return None

    def fill_rectangle(self, x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        """Fill an inclusive rectangle, routing to split or direct based on size."""
        x_start, x_end = min(x1, x2), max(x1, x2)
        y_start, y_end = min(y1, y2), max(y1, y2)
        self._validate_bounds(x_start, y_start, x_end, y_end)
        self._check_loaded(x_start, y_start, x_end, y_end)

        if self._count_blocks(x_start, y_start, x_end, y_end) >= self.MAX_BLOCKS:
            self._fill_split(x_start, y_start, x_end, y_end, block)
        else:
            self._fill_direct(x_start, y_start, x_end, y_end, block)

    # ------------------------------------------------------------------
    # Visualization
    # ------------------------------------------------------------------

    def show(self, show_chunks: bool = False) -> None:
        """Render the world grid with matplotlib."""
        max_id = max(BLOCK_COLORS.keys())
        palette = [BLOCK_COLORS.get(i, "#FF00FF") for i in range(max_id + 1)]
        cmap = mcolors.ListedColormap(palette)

        fig, ax = plt.subplots(figsize=(max(6, self.width // 8), max(6, self.height // 8)))
        ax.imshow(
            self.grid,
            cmap=cmap,
            vmin=0,
            vmax=max_id,
            origin="lower",
            interpolation="nearest",
        )

        if show_chunks:
            self._draw_chunk_overlay(ax)

        ax.set_title("World")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        plt.tight_layout()
        plt.show()

    def _draw_chunk_overlay(self, ax: plt.Axes) -> None:
        chunks_x = self._chunks_in_axis(self.width)
        chunks_y = self._chunks_in_axis(self.height)
        for cy in range(chunks_y):
            for cx in range(chunks_x):
                loaded = (cx, cy) in self.loaded_chunks
                color = "lime" if loaded else "red"
                rect = mpatches.Rectangle(
                    (cx * self.chunk_size - 0.5, cy * self.chunk_size - 0.5),
                    self.chunk_size,
                    self.chunk_size,
                    linewidth=1,
                    edgecolor=color,
                    facecolor="none",
                    alpha=0.6,
                )
                ax.add_patch(rect)
