import json
import numpy as np

def serialize_world(world) -> str:
    """Serialize the world state to a JSON string."""
    data = {
        "width": world.width,
        "height": world.height,
        "depth": world.depth,
        "chunk_size": world.chunk_size,
        "MAX_BLOCKS": world.MAX_BLOCKS,
        "grid": world.grid.tolist(),
        "loaded_chunks": list(world.loaded_chunks)
    }
    return json.dumps(data)

def deserialize_world(data_str: str, world_cls) -> any:
    """Deserialize the world state from a JSON string and return a new World instance."""
    data = json.loads(data_str)
    depth = data.get("depth", 1)
    world = world_cls(data["width"], data["height"], depth, data["chunk_size"])
    world.MAX_BLOCKS = data["MAX_BLOCKS"]
    world.grid = np.array(data["grid"], dtype=int)
    world.chunk_manager.loaded_chunks = {tuple(c) for c in data["loaded_chunks"]} # type: ignore
    return world
