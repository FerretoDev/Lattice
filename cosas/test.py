import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 🔧 Cambia esto si te falla:
matplotlib.use("TkAgg")  # o "Qt5Agg"

# Parámetros físicos
g = 9.81
L = 1.0
b = 0.2  # 🔥 fricción del aire (ajústalo: 0 = sin fricción)
dt = 0.05

# Condiciones iniciales
theta = np.pi / 3  # ángulo inicial más grande para ver efecto
omega = 0.0

theta_list = []

# Simulación
for _ in range(400):
    alpha = -(g / L) * np.sin(theta) - b * omega  # 🔥 fricción incluida
    omega += alpha * dt
    theta += omega * dt
    theta_list.append(theta)

# Coordenadas
x = L * np.sin(theta_list)
y = -L * np.cos(theta_list)

# Gráfica
fig, ax = plt.subplots()
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 0.2)
ax.set_aspect("equal")

(line,) = ax.plot([], [], "o-", lw=2)
(trace,) = ax.plot([], [], "--", lw=1)


def update(frame):
    line.set_data([0, x[frame]], [0, y[frame]])
    trace.set_data(x[:frame], y[:frame])
    return line, trace


anim = FuncAnimation(fig, update, frames=len(x), interval=50)

plt.title("Péndulo con fricción del aire")
plt.grid()
plt.show()
