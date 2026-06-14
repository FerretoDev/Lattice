# Lattice Roadmap

This roadmap reflects the current state of the project and the dependency order for future work.

---

## Ecosystem Scope (Target)

Lattice is evolving into a small engine stack:

- lattice-core (Python): simulation and rules
- lattice-visual (Python): 2D/3D viewers and tools
- lattice-bridge (Python/Java): data exchange and control channel
- lattice-engine-java (Java): Minecraft Java plugin integration (Paper/Spigot), not a mod

---

## Current Status

Phase 1 is complete for the 2D core. Chunks, constrained fills, and tests are in place.

---

## Roadmap (Dependency Order)

### Phase 1 — Stable 2D Core (Done)

- World grid, fill logic, validation
- Chunk loading and validation
- Matplotlib viewer with chunk overlay
- pytest coverage for core behaviors

### Phase 2 — Clean Architecture (Done)

Goals:
- Make the core extensible and modular without rewriting

Key tasks:
- [x] Split modules: world, chunks, fill, rules, io
- [x] Centralize validation and bounds handling
- [x] Define a stable public API surface
- [x] Add lightweight serialization (JSON or npy) for world snapshots

### Phase 3 — Rules and Simulation (Done)

Goals:
- Introduce tick-based updates and simple rule systems

Key tasks:
- [x] Add tick loop (`world.tick()`)
- [x] Add rule registry and ordering
- [x] Implement basic materials (sand, water)
- [x] Add deterministic update tests

### Phase 4 — Visualization (2D Interactive) (Done)

Goals:
- Real-time interaction and debugging overlays

Key tasks:
- [x] Add interactive web frontend (replaced Pygame)
- [x] Add camera controls (pan/zoom)
- [x] Add chunk debug overlay

### Phase 5 — 3D Voxel Core (Next)

Goals:
- Extend the engine to 3D grids and chunks

Key tasks:
- Generalize to N-dim (shape tuples)
- 3D chunks and bounds
- 3D fill and rule updates
- Choose a 3D viewer (Ursina/Panda3D/moderngl)

### Phase 6 — Minecraft Java Plugin Integration (Future)

Goals:
- Connect Lattice to a Minecraft Java plugin (Paper/Spigot), not a mod

Key tasks:
- Define bridge protocol (REST or socket)
- Implement Python server and Java client
- Map Lattice fill to plugin-side chunk edits
- Add sync tests with mock worlds

---

## Guardrails (Order Matters)

- Do not start Java plugin work before Phase 2-4 foundations.
- Do not jump to 3D until the 2D simulation and API are stable.

---

## Documentation

- Evolving architecture: [docs/architecture.md](docs/architecture.md)
