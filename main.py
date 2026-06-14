from lattice.world import World
from lattice.blocks import STONE, SAND, WATER
from lattice.rules import SandGravityRule, WaterFlowRule

def main() -> None:
    print("Iniciando simulación 3D de Lattice...")
    
    # Crear mundo 3D (32x32x16)
    world = World(32, 32, depth=16)
    
    # Registrar reglas de simulación
    world.rule_registry.register(SandGravityRule(), priority=100)
    world.rule_registry.register(WaterFlowRule(), priority=200)
    
    # Crear base de piedra
    world.fill_box(0, 0, 0, 31, 0, 15, STONE)
    
    # Colocar bloques suspendidos
    world.set_block(15, 10, 8, SAND)
    world.set_block(15, 11, 8, SAND)
    world.set_block(16, 12, 8, WATER)
    
    print("Ejecutando 5 ticks...")
    for i in range(5):
        world.tick()
        print(f"Tick {i+1} completado.")
        
    print("Abriendo visualización 3D con PyVista...")
    world.show_3d()

if __name__ == "__main__":
    main()
