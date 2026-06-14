class ChunkManager:
    """Manages loaded/unloaded chunks of the grid world."""

    def __init__(self, width: int, height: int, chunk_size: int = 16) -> None:
        self.width = width
        self.height = height
        self.chunk_size = chunk_size
        self.loaded_chunks: set[tuple[int, int]] = set()
        self._load_all_chunks()

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

    def check_loaded(self, x1: int, y1: int, x2: int, y2: int) -> None:
        cx1, cy1 = self._get_chunk(x1, y1)
        cx2, cy2 = self._get_chunk(x2, y2)
        for cy in range(cy1, cy2 + 1):
            for cx in range(cx1, cx2 + 1):
                if (cx, cy) not in self.loaded_chunks:
                    raise ValueError(f"Chunk ({cx}, {cy}) is not loaded")
block_colors_override = None # type: ignore
