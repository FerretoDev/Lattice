import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

matplotlib.use("TkAgg")

# =========================
# Parámetros
# =========================
nx, ny = 30, 30
dx = dy = 0.02

alpha = 0.00005  # difusión
dt = 0.01

# Reacción química (simplificada)
k = 0.1  # velocidad reacción
Q = 500  # calor generado

# =========================
# Inicialización
# =========================
T = np.ones((nx, ny)) * 25  # temperatura
C = np.ones((nx, ny))  # concentración

# punto inicial caliente
T[nx // 2, ny // 2] = 200

frames = []

# =========================
# Simulación
# =========================
for _ in range(200):
    T_new = T.copy()
    C_new = C.copy()

    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            # Laplaciano (difusión)
            laplacian = (T[i + 1, j] - 2 * T[i, j] + T[i - 1, j]) / dx**2 + (
                T[i, j + 1] - 2 * T[i, j] + T[i, j - 1]
            ) / dy**2

            # Reacción química
            reaction = k * C[i, j]
            heat_source = Q * reaction

            # Actualización
            T_new[i, j] = T[i, j] + (alpha * laplacian + heat_source) * dt
            C_new[i, j] = C[i, j] - reaction * dt

    T = T_new
    C = C_new

    frames.append(T.copy())

# =========================
# Visualización 3D
# =========================
x = np.linspace(0, 1, nx)
y = np.linspace(0, 1, ny)
X, Y = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")


def update(frame):
    ax.clear()
    ax.plot_surface(X, Y, frames[frame], cmap="hot")
    ax.set_zlim(20, 400)
    ax.set_title("Simulación termo-química (mini Termica Neo)")


anim = FuncAnimation(fig, update, frames=len(frames), interval=50)

plt.show()
