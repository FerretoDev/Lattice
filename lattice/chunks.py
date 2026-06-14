class ChunkManager:
    """Manages loaded/unloaded chunks of the 3D grid world."""

    def __init__(self, width: int, height: int, depth: int = 1, chunk_size: int = 16) -> None:
        self.width = width
        self.height = height
        self.depth = depth
        self.chunk_size = chunk_size
        self.loaded_chunks: set[tuple] = set()
        self._load_all_chunks()

    def _chunks_in_axis(self, size: int) -> int:
        return (size + self.chunk_size - 1) // self.chunk_size

    def _load_all_chunks(self) -> None:
        cx_max = self._chunks_in_axis(self.width)
        cy_max = self._chunks_in_axis(self.height)
        cz_max = self._chunks_in_axis(self.depth)
        
        for cz in range(cz_max):
            for cy in range(cy_max):
                for cx in range(cx_max):
                    if self.depth == 1:
                        self.loaded_chunks.add((cx, cy))
                    else:
                        self.loaded_chunks.add((cx, cy, cz))

    def _get_chunk(self, x: int, y: int, z: int = 0) -> tuple:
        if self.depth == 1:
            return (x // self.chunk_size, y // self.chunk_size)
        return (x // self.chunk_size, y // self.chunk_size, z // self.chunk_size)

    def force_load(self, cx: int, cy: int, cz: int | None = None) -> None:
        if self.depth == 1 or cz is None:
            self.loaded_chunks.add((cx, cy))
        else:
            self.loaded_chunks.add((cx, cy, cz))

    def unload_chunk(self, cx: int, cy: int, cz: int | None = None) -> None:
        if self.depth == 1 or cz is None:
            self.loaded_chunks.discard((cx, cy))
        else:
            self.loaded_chunks.discard((cx, cy, cz))

    def check_loaded(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> None:
        cx1, cy1 = x1 // self.chunk_size, y1 // self.chunk_size
        cx2, cy2 = x2 // self.chunk_size, y2 // self.chunk_size
        cz1 = z1 // self.chunk_size
        cz2 = z2 // self.chunk_size
        
        for cz in range(cz1, cz2 + 1):
            for cy in range(cy1, cy2 + 1):
                for cx in range(cx1, cx2 + 1):
                    chunk = (cx, cy) if self.depth == 1 else (cx, cy, cz)
                    if chunk not in self.loaded_chunks:
                        raise ValueError(f"Chunk {chunk} is not loaded")
