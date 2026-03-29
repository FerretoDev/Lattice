import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 🔧 backend (cambia si falla)
matplotlib.use("TkAgg")

# =========================
# Parámetros físicos (hierro aprox)
# =========================
L = 1.0
nx = 120
dx = L / nx

alpha = 0.00002  # 🔥 difusividad BAJA → retiene calor
dt = 0.01

k = 0.02  # pérdida al ambiente
T_amb = 25  # temperatura ambiente

# =========================
# Inicialización
# =========================
x = np.linspace(0, L, nx)

u = np.ones(nx) * T_amb
u[nx // 2] = 300  # 🔥 punto caliente (hierro calentado)

frames = []

# =========================
# Simulación
# =========================
for _ in range(600):
    u_new = u.copy()

    for i in range(1, nx - 1):
        diffusion = u[i + 1] - 2 * u[i] + u[i - 1]
        cooling = -k * (u[i] - T_amb)

        u_new[i] = u[i] + (alpha * diffusion / dx**2 + cooling) * dt

    u = u_new
    frames.append(u.copy())

# =========================
# Animación
# =========================
fig, ax = plt.subplots()
(line,) = ax.plot(x, frames[0])

ax.set_ylim(T_amb - 5, 320)
ax.set_title("Simulación de calor en hierro (alta retención)")
ax.set_xlabel("Posición")
ax.set_ylabel("Temperatura (°C)")


def update(frame):
    line.set_ydata(frames[frame])
    return (line,)


anim = FuncAnimation(fig, update, frames=len(frames), interval=120)

plt.grid()
plt.show()
