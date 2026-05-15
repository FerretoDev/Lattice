# Lattice

A discrete grid-based simulation engine inspired by constrained voxel operations and Minecraft-style world mechanics.

---

# Vision

Lattice is a simulation framework focused on:

- discrete spatial worlds,
- chunk-based loading,
- constrained fill operations,
- procedural terrain systems,
- and extensible voxel-like simulation mechanics.

The project started as an abstraction of Minecraft `/fill` and `/forceload` mechanics into a programmable simulation engine.

---

# Core Concepts

## Discrete World

The world is represented as a finite lattice (grid) using NumPy arrays.

Current implementation:
- 2D grid
- integer block IDs
- inclusive coordinate fills

Future:
- N-dimensional support
- full 3D voxel worlds

---

## Chunk System

The world is partitioned into chunks.

Purpose:
- simulate Minecraft-like loaded/unloaded regions
- optimize future large-scale simulations
- enable streaming and dynamic loading

Current status:
- planned / in progress

---

## Constrained Fill Operations

Large fill operations are constrained by a maximum block limit.

Inspired by:
- Minecraft `/fill` limits
- spatial partitioning algorithms

Current strategy:
- recursive spatial subdivision
- split along the longest axis

Future:
- optimal partition strategies
- quadtree/octree subdivision

---

# Current Architecture

## Main Class

```python
class World:
```

Responsibilities:

* manage grid state
* validate bounds
* perform fill operations
* manage chunk loading
* provide visualization hooks

---

## Current Internal Methods

### Direct Fill

```python
_fill_direct(...)
```

Performs actual NumPy slicing assignment.

---

### Recursive Split Fill

```python
_fill_split(...)
```

Recursively partitions oversized regions.

---

### Block Counting

```python
_count_blocks(...)
```

Computes inclusive rectangle area.

---

# Project Roadmap

---

# Phase 1 — Stable 2D Core

## Goals

* robust 2D world
* constrained fills
* chunk loading
* visualization
* tests

## Tasks

### World Core

* [x] Create NumPy-based grid
* [x] Implement block setting/getting (`set_block`, `get_block`)
* [x] Implement rectangle fill (`fill_rectangle`)
* [x] Add fill limits (`MAX_BLOCKS = 1000`)
* [x] Add recursive fill splitting (`_fill_split` — splits along longest axis)
* [x] Add direct fill via NumPy slicing (`_fill_direct`)
* [x] Add block counter (`_counter_blocks`)

### Refactoring

* [x] Extract `_validate_bounds` — single method called by `fill_rectangle`, `_fill_direct`, `_fill_split`
* [x] Remove duplicated validation logic
* [x] Improve naming consistency (`_counter_blocks` → `_count_blocks`)

### Chunk System

* [x] Add `chunk_size` (constructor param, default 16)
* [x] Add `loaded_chunks` (set of `(cx, cy)` tuples)
* [x] Implement `_get_chunk`
* [x] Implement `force_load` / `unload_chunk`
* [x] Implement `_check_loaded`
* [x] Integrate chunk validation into `fill_rectangle`

### Visualization

* [x] Add matplotlib visualization (`show()`)
* [x] Add custom block colormap (`BLOCK_COLORS` palette)
* [x] Add chunk overlay debug view (`show(show_chunks=True)`)

### Testing

* [x] Test `set_block` / `get_block`
* [x] Test direct fill (inclusive area)
* [x] Test reversed coordinates
* [x] Test recursive fill for large areas (40×40 = 1600 blocks)
* [x] Test out-of-bounds raises `ValueError`
* [x] Test routing to `_fill_direct` for small areas
* [x] Test routing to `_fill_split` for large areas
* [x] Test routing to `_fill_split` at exact limit
* [x] Test all chunks loaded by default
* [x] Test fill raises when chunk unloaded
* [x] Test `force_load` re-enables fill
* [x] Test multi-chunk fill fails if one chunk is unloaded
* [x] Test `_get_chunk` returns correct coords
* [x] Test single cell fill
* [x] Test corner fills (top-left, bottom-right)
* [x] Test exact boundary raises `ValueError`
* [x] Test `get_block` returns `None` outside bounds

---

# Phase 2 — Dimensional Generalization

## Goals

Generalize the engine to support N-dimensional worlds.

## Tasks

* [ ] Replace width/height with generic shape
* [ ] Use tuple-based indexing
* [ ] Generate dynamic slices
* [ ] Generalize fill operations
* [ ] Benchmark performance

---

# Phase 3 — Dynamic Simulation

## Goals

Transform Lattice from static editor into simulation engine.

## Tasks

* [ ] Add tick system
* [ ] Add gravity blocks
* [ ] Add fluid propagation
* [ ] Add cellular automata rules
* [ ] Add chunk streaming

---

# Phase 4 — Procedural Generation

## Goals

Generate terrain and structures procedurally.

## Tasks

* [ ] Add Perlin noise terrain
* [ ] Add biome system
* [ ] Add height maps
* [ ] Add cave generation
* [ ] Add structure generation

---

# Phase 5 — Visualization & Rendering

## Goals

Interactive visualization and eventually real-time rendering.

## Tasks

### 2D

* [ ] Add Pygame renderer
* [ ] Add camera controls
* [ ] Add chunk visualization

### 3D

* [ ] Evaluate Ursina
* [ ] Evaluate Panda3D
* [ ] Implement voxel rendering
* [ ] Add real-time chunk streaming

---

# Technical Notes

## Coordinate Convention

World coordinates:

* x → horizontal
* y → vertical

NumPy indexing:

```python
grid[y, x]
```

All fill operations are inclusive.

---

# Design Principles

## 1. Separation of Responsibilities

Public methods:

* validate and orchestrate

Internal methods:

* perform direct operations

---

## 2. Extensibility First

The project should evolve naturally toward:

* 3D worlds
* simulation rules
* procedural generation

without rewriting the engine from scratch.

---

## 3. Visualization Is Secondary

The simulation core must remain independent from rendering systems.

Rendering should be replaceable.

---

# Current Tech Stack

## Core

* Python
* NumPy

## Testing

* pytest

## Exploration / Visualization

* Jupyter Notebook
* matplotlib

---

# Ideas for Future Research

* spatial partition optimization
* quadtree/octree structures
* procedural terrain mathematics
* lattice-based physics
* cellular automata
* chunk streaming systems
* constrained optimization for fill partitioning

---

# Long-Term Goal

Lattice should become:

> a modular discrete simulation framework capable of supporting voxel worlds, procedural terrain, and dynamic rule-based simulations.

Not merely a Minecraft clone.
