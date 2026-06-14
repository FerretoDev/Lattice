from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from lattice.world import World
from lattice.blocks import AIR, STONE, GRASS, DIRT, SAND, WATER, BLOCK_COLORS
from lattice.rules import SandGravityRule, WaterFlowRule

app = FastAPI(title="Lattice Interactive Viewer")

# Initialize a default world
world = World(48, 48, chunk_size=16)
# Register the simulation rules
world.rule_registry.register(SandGravityRule(), priority=100)
world.rule_registry.register(WaterFlowRule(), priority=200)

# Request models
class BlockRequest(BaseModel):
    x: int
    y: int
    block: int

class FillRequest(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    block: int

class ChunkRequest(BaseModel):
    cx: int
    cy: int

class SnapshotRequest(BaseModel):
    data: str

class ResetRequest(BaseModel):
    width: int
    height: int
    chunk_size: int

# API Endpoints
@app.get("/api/world")
def get_world():
    return {
        "width": world.width,
        "height": world.height,
        "chunk_size": world.chunk_size,
        "MAX_BLOCKS": world.MAX_BLOCKS,
        "grid": world.grid.tolist(),
        "loaded_chunks": list(world.loaded_chunks),
        "block_colors": BLOCK_COLORS
    }

@app.post("/api/tick")
def tick_world():
    world.tick()
    return get_world()

@app.post("/api/block")
def set_block(req: BlockRequest):
    world.set_block(req.x, req.y, req.block)
    return {"status": "ok", "block": world.get_block(req.x, req.y)}

@app.post("/api/fill")
def fill_rect(req: FillRequest):
    try:
        world.fill_rectangle(req.x1, req.y1, req.x2, req.y2, req.block)
        return get_world()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/chunk/load")
def load_chunk(req: ChunkRequest):
    world.force_load(req.cx, req.cy)
    return {"status": "ok", "loaded_chunks": list(world.loaded_chunks)}

@app.post("/api/chunk/unload")
def unload_chunk(req: ChunkRequest):
    world.unload_chunk(req.cx, req.cy)
    return {"status": "ok", "loaded_chunks": list(world.loaded_chunks)}

@app.post("/api/snapshot/save")
def save_snapshot():
    return {"snapshot": world.to_json()}

@app.post("/api/snapshot/load")
def load_snapshot(req: SnapshotRequest):
    global world
    try:
        world = World.from_json(req.data)
        # Re-register rules on the new deserialized world
        world.rule_registry.register(SandGravityRule(), priority=100)
        world.rule_registry.register(WaterFlowRule(), priority=200)
        return get_world()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load snapshot: {str(e)}")

@app.post("/api/reset")
def reset_world(req: ResetRequest):
    global world
    if req.width <= 0 or req.height <= 0 or req.chunk_size <= 0:
        raise HTTPException(status_code=400, detail="Invalid dimensions")
    world = World(req.width, req.height, req.chunk_size)
    world.rule_registry.register(SandGravityRule(), priority=100)
    world.rule_registry.register(WaterFlowRule(), priority=200)
    return get_world()

# Serve static frontend files
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
