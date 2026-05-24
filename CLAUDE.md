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
- implemented in the 2D core; streaming remains planned

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

See [ROADMAP.md](ROADMAP.md) for the dependency-ordered phases and [PLAN.md](PLAN.md) for the current 30-day plan.

Architecture reference: [docs/architecture.md](docs/architecture.md).

---

# Ecosystem Scope (Target)

Lattice is evolving into a small engine stack:

* lattice-core (Python): simulation and rules
* lattice-visual (Python): 2D/3D viewers and tools
* lattice-bridge (Python/Java): data exchange and control channel
* lattice-engine-java (Java): Minecraft Java plugin integration (Paper/Spigot), not a mod

---

# Proposed Monorepo Layout

```
lattice/
│
├── core-python/
│   ├── lattice/
│   │   ├── world.py
│   │   ├── chunks.py
│   │   ├── blocks.py
│   │   ├── rules.py
│   │   ├── fill.py
│   │   └── io.py
│   ├── tests/
│   ├── notebooks/
│   └── pyproject.toml
│
├── visual-python/
│   ├── renderer_2d.py
│   ├── renderer_3d.py
│   ├── camera.py
│   └── app.py
│
├── bridge/
│   ├── api_spec.json
│   ├── serializer.py
│   ├── server.py
│   └── client_java.proto
│
├── java-minecraft/
│   ├── src/main/java/
│   └── build.gradle.kts
│
├── docs/
│   ├── CLAUDE.md
│   ├── architecture.md
│   ├── roadmap.md
│   └── math_model.md
│
└── README.md
```

---

# Roadmap (Dependency Order)

# Phase 1 — Stable 2D Core (Done)

## Goals

* robust 2D world
* constrained fills
* chunk loading
* visualization hooks
* tests

## Status

* [x] World grid, fill logic, validation
* [x] Chunk loading and validation
* [x] Matplotlib viewer with chunk overlay
* [x] pytest coverage for core behaviors

---

# Phase 2 — Clean Architecture (Next)

## Goals

Make the core extensible and modular without rewriting.

## Tasks

* [ ] Split modules: world, chunks, fill, rules, io
* [ ] Centralize validation and bounds handling
* [ ] Define a stable public API surface
* [ ] Add lightweight serialization (JSON or npy) for world snapshots

---

# Phase 3 — Rules and Simulation (Next)

## Goals

Introduce tick-based updates and simple rule systems.

## Tasks

* [ ] Add tick loop (`world.tick()`)
* [ ] Add rule registry and ordering
* [ ] Implement basic materials (sand, water)
* [ ] Add deterministic update tests

---

# Phase 4 — Visualization (2D Interactive)

## Goals

Real-time interaction and debugging overlays.

## Tasks

* [ ] Add Pygame renderer
* [ ] Add camera controls (pan/zoom)
* [ ] Add chunk debug overlay

---

# Phase 5 — 3D Voxel Core (Future)

## Goals

Extend the engine to 3D grids and chunks.

## Tasks

* [ ] Generalize to N-dim (shape tuples)
* [ ] 3D chunks and bounds
* [ ] 3D fill and rule updates
* [ ] Choose a 3D viewer (Ursina/Panda3D/moderngl)

---

# Phase 6 — Minecraft Java Plugin Integration (Future)

## Goals

Connect Lattice to a Minecraft Java plugin (Paper/Spigot), not a mod.

## Tasks

* [ ] Define bridge protocol (REST or socket)
* [ ] Implement Python server and Java client
* [ ] Map Lattice fill to plugin-side chunk edits
* [ ] Add sync tests with mock worlds

---

# 30-Day Plan (Realistic)

## Week 1

* Refactor into modules (Phase 2 start)
* Add snapshot serialization

## Week 2

* Stabilize public API
* Fill/chunk rules tests

## Week 3

* Add basic tick system
* Implement 1-2 simple rules

## Week 4

* Prototype interactive 2D viewer
* Decide bridge protocol for Java plugin

---

# Technical Notes

## Ignored Directories

* `cosas/`: This folder is used exclusively for personal practice, temporary tests, and random experiments. It should be ignored in the context of the main project.

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
