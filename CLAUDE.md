# CLAUDE Context

## Fecha
- 2 de abril de 2026

## Entorno
- OS: Windows
- Workspace root: C:/Users/Usuario/Dev/Lattice

## Estructura del proyecto
- LICENSE
- main.py
- pyproject.toml
- README.md
- lattice/
  - __init__.py
  - world.ipynb
  - world.py
  - cosas/
    - a.py
    - aa.py
    - p.py
    - test.py
    - visualizacion_3d_termperature.py
- lattice.egg-info/
  - dependency_links.txt
  - PKG-INFO
  - requires.txt
  - SOURCES.txt
  - top_level.txt
- tests/
  - world_test.py

## Estado de terminal
- Shell: pwsh
- Ultimo comando: & c:/Users/Usuario/Dev/Lattice/.venv/Scripts/Activate.ps1
- CWD: C:/Users/Usuario/Dev/Lattice
- Exit code: 0

## Archivo activo en editor
- lattice/world.py

## Cambios aplicados en esta sesion
- Se completo _fill_direct() en lattice/world.py:
  - Normaliza coordenadas.
  - Valida limites del mundo.
  - Rellena con slicing de NumPy usando conversion 1-based a 0-based.
- Se completo _fill_split() en lattice/world.py:
  - Normaliza coordenadas.
  - Valida limites.
  - Si el area supera MAX_BLOCKS, lanza ValueError("Insert less than 1000 blocks").
  - Si no supera el limite, delega en _fill_direct().
- Se actualizo fill_rectangle() en lattice/world.py:
  - Normaliza y valida coordenadas al inicio.
  - Calcula area con _counter_blocks() sobre coordenadas normalizadas.
  - Enruta a _fill_split() o _fill_direct() segun MAX_BLOCKS.

## Validacion
- Tests ejecutados: tests/world_test.py
- Resultado: 8 passed, 0 failed

## Nota de memoria de repositorio
- Archivo: /memories/repo/world-fill-rules.md
- Reglas guardadas:
  - fill_rectangle usa coordenadas 1-based y valida limites antes de escribir.
  - Si el area supera 1000 bloques, lanza ValueError("Insert less than 1000 blocks").
  - _fill_direct usa slicing NumPy con conversion 1-based -> 0-based.
