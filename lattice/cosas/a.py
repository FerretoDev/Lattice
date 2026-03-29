import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

matplotlib.use("TkAgg")

# =========================
# Parámetros
# =========================
nx, ny = 40, 40
L = 1.0
dx = L / nx
dy = L / ny

alpha = 0.00005
dt = 0.01

# =========================
# Malla
# =========================
x = np.linspace(0, L, nx)
y = np.linspace(0, L, ny)
X, Y = np.meshgrid(x, y)

# Temperatura inicial
u = np.ones((nx, ny)) * 25
u[nx // 2, ny // 2] = 300  # 🔥 punto caliente

frames = []

# =========================
# Simulación
# =========================
for _ in range(200):
    u_new = u.copy()

    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            laplacian = (u[i + 1, j] - 2 * u[i, j] + u[i - 1, j]) / dx**2 + (
                u[i, j + 1] - 2 * u[i, j] + u[i, j - 1]
            ) / dy**2

            u_new[i, j] = u[i, j] + alpha * laplacian * dt

    u = u_new
    frames.append(u.copy())

# =========================
# Visualización 3D
# =========================
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")


def update(frame):
    ax.clear()

    U = frames[frame]

    # Superficie 3D
    ax.plot_surface(X, Y, U, cmap="hot", alpha=0.8)

    # Gradiente (flujo de calor)
    gy, gx = np.gradient(U)

    step = 4  # para no saturar de flechas

    ax.quiver(
        X[::step, ::step],
        Y[::step, ::step],
        U[::step, ::step],
        -gx[::step, ::step],
        -gy[::step, ::step],
        0,
        length=0.1,
        color="blue",
    )

    ax.set_zlim(20, 320)
    ax.set_title("Difusión de calor en 3D (hierro)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Temperatura")


anim = FuncAnimation(fig, update, frames=len(frames), interval=50)

plt.show()
