# Architecture (Evolving Structure)

This document describes the future-facing structure for Lattice as it evolves from a single core to a modular ecosystem.

---

## Lattice Ecosystem (Target)

```
LATTICE ECOSYSTEM
│
├── lattice-core/            # core engine (no graphics)
│   ├── world/
│   ├── chunks/
│   ├── rules/
│   ├── math/
│   ├── serialization/
│   └── api/
│
├── lattice-sim/             # concrete simulations
│   ├── terrain/
│   ├── fluids/
│   ├── cellular_automata/
│   └── experiments/
│
├── lattice-render/          # detached rendering
│   ├── 2d_matplotlib/
│   ├── pygame_viewer/
│   ├── voxel_3d/
│   └── shaders/
│
├── lattice-runtime/         # real-time execution
│   ├── tick_engine/
│   ├── scheduler/
│   ├── event_system/
│   └── chunk_streaming/
│
├── lattice-bridge/          # external integration
│   ├── python_api/
│   ├── java_bridge/
│   ├── minecraft_adapter/
│   ├── websocket_server/
│   └── grpc_interface/
│
├── lattice-java/            # Paper/Spigot plugin (not a mod)
│   ├── plugin/
│   ├── world_adapter/
│   ├── command_layer/
│   └── packet_sync/
│
├── lattice-tools/           # engineering tools
│   ├── world_editor/
│   ├── debug_viewer/
│   ├── profiler/
│   └── chunk_analyzer/
│
└── docs/
    ├── architecture.md
    ├── math_model.md
    ├── simulation_rules.md
    └── roadmap.md
```

---

## Principles

1. The core stays independent of render and runtime.
2. The bridge is explicit for external integrations.
3. The system evolves by phases without full rewrites.
