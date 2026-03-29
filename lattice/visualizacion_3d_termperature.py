import numpy as np
import pyvista as pv

# Parámetros
nx, ny = 50, 50
alpha = 0.0001
dt = 0.01

# Grid
x = np.linspace(0, 1, nx)
y = np.linspace(0, 1, ny)

X, Y = np.meshgrid(x, y)

# Temperatura inicial
T = np.ones((nx, ny)) * 25
T[nx // 2, ny // 2] = 300

# Crear malla para PyVista
grid = pv.StructuredGrid(X, Y, np.zeros_like(X))

plotter = pv.Plotter()

for _ in range(200):
    T_new = T.copy()

    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            laplacian = (
                T[i + 1, j] + T[i - 1, j] + T[i, j + 1] + T[i, j - 1] - 4 * T[i, j]
            )

            T_new[i, j] = T[i, j] + alpha * laplacian * dt

    T = T_new

    # Actualizar visualización
    grid["Temperature"] = T.flatten(order="F")

    plotter.clear()
    plotter.add_mesh(grid, scalars="Temperature", cmap="hot")
    plotter.add_text("Simulación térmica", font_size=10)

    plotter.show(auto_close=False, interactive_update=True)
