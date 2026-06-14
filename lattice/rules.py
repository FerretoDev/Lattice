from lattice.blocks import AIR, SAND, WATER

class RuleRegistry:
    """Registry for managing and ordering tick rules."""

    def __init__(self) -> None:
        self.rules: list[tuple[int, any]] = []

    def register(self, rule, priority: int = 100) -> None:
        """Register a simulation rule with a priority (lower runs first)."""
        self.rules.append((priority, rule))
        self.rules.sort(key=lambda x: x[0])

    @property
    def ordered_rules(self) -> list:
        return [r[1] for r in self.rules]


class SandGravityRule:
    """Simulates gravity for sand blocks in 2D and 3D."""

    def apply(self, world) -> None:
        # Iterate from bottom to top to avoid a block falling multiple spaces in one tick
        for z in range(world.depth):
            for y in range(1, world.height):
                for x in range(world.width):
                    if world.grid[z, y, x] == SAND:
                        # Check below
                        if world.grid[z, y - 1, x] == AIR:
                            world.grid[z, y - 1, x] = SAND
                            world.grid[z, y, x] = AIR


class WaterFlowRule:
    """Simulates gravity and horizontal flow for water blocks in 2D and 3D."""

    def apply(self, world) -> None:
        # Step 1: Flow down (iterate bottom to top)
        for z in range(world.depth):
            for y in range(1, world.height):
                for x in range(world.width):
                    if world.grid[z, y, x] == WATER:
                        if world.grid[z, y - 1, x] == AIR:
                            world.grid[z, y - 1, x] = WATER
                            world.grid[z, y, x] = AIR

        # Step 2: Flow horizontally (for cells already on solid ground)
        for z in range(world.depth):
            for y in range(world.height):
                for x in range(world.width):
                    if world.grid[z, y, x] == WATER:
                        # If below is not air (i.e. blocked)
                        if y == 0 or world.grid[z, y - 1, x] != AIR:
                            left_free = x > 0 and world.grid[z, y, x - 1] == AIR
                            right_free = x < world.width - 1 and world.grid[z, y, x + 1] == AIR
                            front_free = z > 0 and world.grid[z - 1, y, x] == AIR
                            back_free = z < world.depth - 1 and world.grid[z + 1, y, x] == AIR

                            if left_free:
                                world.grid[z, y, x - 1] = WATER
                                world.grid[z, y, x] = AIR
                            elif right_free:
                                world.grid[z, y, x + 1] = WATER
                                world.grid[z, y, x] = AIR
                            elif front_free:
                                world.grid[z - 1, y, x] = WATER
                                world.grid[z, y, x] = AIR
                            elif back_free:
                                world.grid[z + 1, y, x] = WATER
                                world.grid[z, y, x] = AIR
