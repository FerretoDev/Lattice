import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from lattice.blocks import BLOCK_COLORS
from lattice.chunks import ChunkManager
from lattice.fill import count_blocks_3d, fill_direct_3d, validate_bounds_3d
from lattice.io import deserialize_world, serialize_world
from lattice.rules import RuleRegistry


class World:
    """Represents a 3D grid world using 0-based coordinates, backwards compatible with 2D."""

    def __init__(self, width: int, height: int, depth: int = 1, chunk_size: int = 16) -> None:
        self.width = width
        self.height = height
        self.depth = depth
        self.chunk_size = chunk_size
        self.grid = np.zeros((depth, height, width), dtype=int)
        self.MAX_BLOCKS = 1000
        self.chunk_manager = ChunkManager(width, height, depth, chunk_size)
        self.rule_registry = RuleRegistry()

    # ------------------------------------------------------------------
    # Chunk system delegates (for backwards compatibility)
    # ------------------------------------------------------------------

    @property
    def loaded_chunks(self) -> set[tuple]:
        return self.chunk_manager.loaded_chunks

    def _chunks_in_axis(self, size: int) -> int:
        return self.chunk_manager._chunks_in_axis(size)

    def _get_chunk(self, x: int, y: int, z: int = 0) -> tuple:
        return self.chunk_manager._get_chunk(x, y, z)

    def force_load(self, cx: int, cy: int, cz: int | None = None) -> None:
        self.chunk_manager.force_load(cx, cy, cz)

    def unload_chunk(self, cx: int, cy: int, cz: int | None = None) -> None:
        self.chunk_manager.unload_chunk(cx, cy, cz)

    def _check_loaded(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> None:
        self.chunk_manager.check_loaded(x1, y1, z1, x2, y2, z2)

    # ------------------------------------------------------------------
    # Validation helpers delegates
    # ------------------------------------------------------------------

    def _validate_bounds(self, x1: int, y1: int, x2: int, y2: int) -> None:
        validate_bounds_3d(x1, y1, 0, x2, y2, 0, self.width, self.height, self.depth)

    def _count_blocks(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return count_blocks_3d(x1, y1, 0, x2, y2, 0)

    # ------------------------------------------------------------------
    # Fill internals
    # ------------------------------------------------------------------

    def _fill_direct(self, x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        self._fill_direct_3d(x1, y1, 0, x2, y2, 0, block)

    def _fill_direct_3d(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, block: int) -> None:
        fill_direct_3d(self.grid, x1, y1, z1, x2, y2, z2, block, self.width, self.height, self.depth)

    def _fill_split(self, x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        """Original 2D split method called from fill_rectangle (for backwards compatibility)."""
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

    def _fill_split_3d(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, block: int) -> None:
        """3D recursive split implementation."""
        x_start, x_end = min(x1, x2), max(x1, x2)
        y_start, y_end = min(y1, y2), max(y1, y2)
        z_start, z_end = min(z1, z2), max(z1, z2)
        validate_bounds_3d(x_start, y_start, z_start, x_end, y_end, z_end, self.width, self.height, self.depth)

        dx = x_end - x_start + 1
        dy = y_end - y_start + 1
        dz = z_end - z_start + 1
        total = dx * dy * dz

        if total <= self.MAX_BLOCKS or (x_start == x_end and y_start == y_end and z_start == z_end):
            self._fill_direct_3d(x_start, y_start, z_start, x_end, y_end, z_end, block)
            return

        # Split along the longest axis
        if dx >= dy and dx >= dz:
            x_mid = (x_start + x_end) // 2
            self._fill_split_3d(x_start, y_start, z_start, x_mid, y_end, z_end, block)
            self._fill_split_3d(x_mid + 1, y_start, z_start, x_end, y_end, z_end, block)
        elif dy >= dx and dy >= dz:
            y_mid = (y_start + y_end) // 2
            self._fill_split_3d(x_start, y_start, z_start, x_end, y_mid, z_end, block)
            self._fill_split_3d(x_start, y_mid + 1, z_start, x_end, y_end, z_end, block)
        else:
            z_mid = (z_start + z_end) // 2
            self._fill_split_3d(x_start, y_start, z_start, x_end, y_end, z_mid, block)
            self._fill_split_3d(x_start, y_start, z_mid + 1, x_end, y_end, z_end, block)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_block(self, x: int, y: int, z_or_block: int, block: int | None = None) -> None:
        if block is None:
            # 2D call: set_block(x, y, block)
            z = 0
            b = z_or_block
        else:
            # 3D call: set_block(x, y, z, block)
            z = z_or_block
            b = block
        
        x, y, z = int(x), int(y), int(z)
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            self.grid[z, y, x] = b

    def get_block(self, x: int, y: int, z: int = 0) -> int | None:
        x, y, z = int(x), int(y), int(z)
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            return self.grid[z, y, x]
        return None

    def tick(self) -> None:
        """Advance the world simulation by one tick."""
        for rule in self.rule_registry.ordered_rules:
            rule.apply(self)

    def fill_rectangle(self, x1: int, y1: int, x2: int, y2: int, block: int) -> None:
        """Fill an inclusive 2D rectangle (on z=0)."""
        x_start, x_end = min(x1, x2), max(x1, x2)
        y_start, y_end = min(y1, y2), max(y1, y2)
        self._validate_bounds(x_start, y_start, x_end, y_end)
        self._check_loaded(x_start, y_start, 0, x_end, y_end, 0)

        if self._count_blocks(x_start, y_start, x_end, y_end) >= self.MAX_BLOCKS:
            self._fill_split(x_start, y_start, x_end, y_end, block)
        else:
            self._fill_direct(x_start, y_start, x_end, y_end, block)

    def fill_box(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, block: int) -> None:
        """Fill an inclusive 3D box, routing to split or direct based on size."""
        x_start, x_end = min(x1, x2), max(x1, x2)
        y_start, y_end = min(y1, y2), max(y1, y2)
        z_start, z_end = min(z1, z2), max(z1, z2)
        validate_bounds_3d(x_start, y_start, z_start, x_end, y_end, z_end, self.width, self.height, self.depth)
        self._check_loaded(x_start, y_start, z_start, x_end, y_end, z_end)

        if count_blocks_3d(x_start, y_start, z_start, x_end, y_end, z_end) >= self.MAX_BLOCKS:
            self._fill_split_3d(x_start, y_start, z_start, x_end, y_end, z_end, block)
        else:
            self._fill_direct_3d(x_start, y_start, z_start, x_end, y_end, z_end, block)

    # ------------------------------------------------------------------
    # Serialization (Phase 2 Snapshot)
    # ------------------------------------------------------------------

    def to_json(self) -> str:
        """Serialize the current world state to a JSON string."""
        return serialize_world(self)

    @classmethod
    def from_json(cls, data_str: str) -> "World":
        """Deserialize a world snapshot from JSON and return a new instance."""
        return deserialize_world(data_str, cls)

    # ------------------------------------------------------------------
    # Visualization (2D Slice)
    # ------------------------------------------------------------------

    def show(self, show_chunks: bool = False, z_slice: int = 0) -> None:
        """Render a 2D slice of the world grid with matplotlib."""
        max_id = max(BLOCK_COLORS.keys())
        palette = [BLOCK_COLORS.get(i, "#FF00FF") for i in range(max_id + 1)]
        cmap = mcolors.ListedColormap(palette)

        fig, ax = plt.subplots(
            figsize=(max(6, self.width // 8), max(6, self.height // 8))
        )
        ax.imshow(
            self.grid[z_slice],
            cmap=cmap,
            vmin=0,
            vmax=max_id,
            origin="lower",
            interpolation="nearest",
        )

        if show_chunks:
            self._draw_chunk_overlay(ax)

        ax.set_title(f"World (z={z_slice})")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        plt.tight_layout()
        plt.show()

    def show_3d(self) -> None:
        """Render the 3D world grid using PyVista voxels."""
        try:
            import pyvista as pv
        except ImportError:
            raise ImportError("PyVista is required for 3D visualization. Install it first.")

        # Create uniform grid (ImageData)
        grid = pv.ImageData()
        # Dimensions are node counts, which are cell counts + 1
        grid.dimensions = (self.width + 1, self.height + 1, self.depth + 1)
        grid.spacing = (1.0, 1.0, 1.0)

        # PyVista cell data expects 1D array flattened in Fortran order
        # with layout: x varies fastest, then y, then z.
        # Our numpy grid shape is (depth, height, width) i.e. (z, y, x).
        # We transpose from (z, y, x) to (x, y, z) and flatten:
        flat_grid = self.grid.transpose(2, 1, 0).flatten()
        grid.cell_data["blocks"] = flat_grid

        # Filter out air blocks (ID 0)
        non_air = grid.threshold(0.5, scalars="blocks")

        plotter = pv.Plotter(title="Lattice 3D Voxel World")
        
        # Define colors list matching block IDs
        max_id = max(BLOCK_COLORS.keys())
        palette = [BLOCK_COLORS.get(i, "#FF00FF") for i in range(max_id + 1)]
        
        if non_air.n_cells > 0:
            plotter.add_mesh(
                non_air,
                scalars="blocks",
                cmap=palette,
                clim=[0, max_id],
                categories=True,
                show_scalar_bar=False,
                edge_color="black",
                show_edges=True
            )
        
        # Add a grid outline for the entire world size
        outline = grid.outline()
        plotter.add_mesh(outline, color="white", line_width=2)
        plotter.show()

    def _draw_chunk_overlay(self, ax: plt.Axes) -> None:
        chunks_x = self._chunks_in_axis(self.width)
        chunks_y = self._chunks_in_axis(self.height)
        for cy in range(chunks_y):
            for cx in range(chunks_x):
                # Check if the chunk is loaded at z=0 (or anywhere for the slice)
                # Keep it simple for backwards compatibility
                is_loaded = False
                for cz in range(self._chunks_in_axis(self.depth)):
                    chunk = (cx, cy) if self.depth == 1 else (cx, cy, cz)
                    if chunk in self.loaded_chunks:
                        is_loaded = True
                        break
                
                color = "lime" if is_loaded else "red"
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
