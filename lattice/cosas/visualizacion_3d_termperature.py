"""
Simulación de difusión térmica 2D con visualización 3D.

Este módulo implementa una simulación de ecuación de calor usando diferencias finitas
y visualiza los resultados con PyVista, usando la temperatura como altura Z.
"""

import numpy as np
import pyvista as pv

# ============= PARÁMETROS DE CONFIGURACIÓN =============
# Dimensiones de la malla
NX, NY = 100, 100

# Parámetros físicos
CONDUCTIVIDAD_TERMICA = 0.0001  # α (alpha)
DT = 0.01  # paso de tiempo
NUM_ITERACIONES = 200

# Temperatura inicial en todo el dominio (°C)
TEMP_INICIAL = 25.0

# Temperatura de la fuente (centro)
TEMP_FUENTE = 300.0

# Rango del dominio
X_MAX, Y_MAX = 1.0, 1.0

# Parámetros de visualización
ESCALA_Z = 0.5  # Factor para escalar altura Z según temperatura


def calcular_laplaciano_vectorizado(T):
    """
    Calcula el Laplaciano discreto de forma vectorizada.
    
    Aproximación por diferencias finitas:
    ∇²T = (T[i+1,j] + T[i-1,j] + T[i,j+1] + T[i,j-1] - 4*T[i,j]) / Δx²
    
    Args:
        T: Matriz de temperatures (NX, NY)
    
    Returns:
        Laplaciano de T para nodos interiores
    """
    laplacian = np.zeros_like(T)
    laplacian[1:-1, 1:-1] = (
        T[2:, 1:-1] +          # T[i+1, j]
        T[:-2, 1:-1] +         # T[i-1, j]
        T[1:-1, 2:] +          # T[i, j+1]
        T[1:-1, :-2] -         # T[i, j-1]
        4 * T[1:-1, 1:-1]      # -4*T[i, j]
    )
    return laplacian


def paso_tiempo(T, alpha, dt):
    """
    Realiza un paso de tiempo en la simulación térmica.
    
    Ecuación: T_new = T + α * ∇²T * dt
    
    Args:
        T: Matriz de temperaturas actual
        alpha: Coeficiente de conductividad térmica
        dt: Paso de tiempo
        
    Returns:
        Matriz de temperaturas actualizada
    """
    laplacian = calcular_laplaciano_vectorizado(T)
    T_new = T + alpha * laplacian * dt
    
    # Mantener condiciones de frontera (bordes sin cambio)
    T_new[0, :] = T[0, :]
    T_new[-1, :] = T[-1, :]
    T_new[:, 0] = T[:, 0]
    T_new[:, -1] = T[:, -1]
    
    return T_new


def crear_grid_inicial(nx, ny, x_max, y_max):
    """
    Crea el grid estructurado inicial para PyVista.
    
    Args:
        nx, ny: Número de nodos en x e y
        x_max, y_max: Límites del dominio
        
    Returns:
        Tuple de (X, Y, grid_pyvista)
    """
    x = np.linspace(0, x_max, nx)
    y = np.linspace(0, y_max, ny)
    X, Y = np.meshgrid(x, y)
    
    # Z inicial en 0, se actualizará con la temperatura
    Z = np.zeros_like(X)
    grid = pv.StructuredGrid(X, Y, Z)
    
    return X, Y, grid


def crear_condicion_inicial(nx, ny, temp_base, temp_fuente):
    """
    Crea la matriz de temperaturas inicial.
    
    Args:
        nx, ny: Dimensiones
        temp_base: Temperatura del dominio
        temp_fuente: Temperatura en el centro
        
    Returns:
        Matriz de temperaturas inicial
    """
    T = np.ones((nx, ny)) * temp_base
    T[nx // 2, ny // 2] = temp_fuente
    return T


def actualizar_visualizacion(plotter, grid, X, Y, T, escala_z, iteracion):
    """
    Actualiza la visualización sin recrear el plotter.
    
    Args:
        plotter: Objeto Plotter de PyVista
        grid: Grid estructurado
        X, Y: Coordenadas de malla
        T: Matriz de temperaturas
        escala_z: Factor de escala para altura Z
        iteracion: Número de iteración actual
    """
    # Usar temperatura como altura Z
    Z = (T - np.min(T)) / (np.max(T) - np.min(T) + 1e-6) * escala_z
    
    # Actualizar las coordenadas del grid
    grid.points = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])
    grid["Temperature"] = T.flatten(order="F")
    
    # Limpiar y redibujar
    plotter.clear()
    plotter.add_mesh(grid, scalars="Temperature", cmap="hot", show_edges=False)
    
    # Actualizar texto con información
    plotter.add_text(
        f"Iteración: {iteracion} | T_max: {T.max():.1f}°C | T_min: {T.min():.1f}°C",
        font_size=12,
        color="white"
    )


def simular_difusion_termica(
    nx=NX,
    ny=NY,
    alpha=CONDUCTIVIDAD_TERMICA,
    dt=DT,
    num_iter=NUM_ITERACIONES,
    temp_inicial=TEMP_INICIAL,
    temp_fuente=TEMP_FUENTE,
    escala_z=ESCALA_Z,
    visualizar=True
):
    """
    Ejecuta la simulación completa de difusión térmica.
    
    Args:
        nx, ny: Dimensiones de la malla
        alpha: Coeficiente de conductividad térmica
        dt: Paso de tiempo
        num_iter: Número de iteraciones
        temp_inicial: Temperatura base inicial
        temp_fuente: Temperatura de la fuente (centro)
        escala_z: Factor de escala para visualización 3D
        visualizar: Si True, muestra la visualización
    """
    # Inicializar
    X, Y, grid = crear_grid_inicial(nx, ny, X_MAX, Y_MAX)
    T = crear_condicion_inicial(nx, ny, temp_inicial, temp_fuente)
    
    if visualizar:
        plotter = pv.Plotter()
        # Inicializar datos de temperatura en el grid
        grid["Temperature"] = T.flatten(order="F")
        plotter.add_mesh(grid, scalars="Temperature", cmap="hot", show_edges=False)
        plotter.set_scale(zscale=2)
        plotter.view_xy()
    
    # Simulación
    print(f"Iniciando simulación: {num_iter} iteraciones, {nx}×{ny} grid")
    
    for iteracion in range(num_iter):
        T = paso_tiempo(T, alpha, dt)
        
        if visualizar and iteracion % 10 == 0:  # Actualizar cada 10 iteraciones
            actualizar_visualizacion(plotter, grid, X, Y, T, escala_z, iteracion)
        
        if iteracion % 50 == 0:
            print(f"  Iteración {iteracion}: T_max={T.max():.1f}°C, T_min={T.min():.1f}°C")
    
    if visualizar:
        plotter.show()
    
    return T, X, Y


if __name__ == "__main__":
    # Ejecutar simulación
    T_final, X, Y = simular_difusion_termica()
