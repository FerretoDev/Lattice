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
    """Simulates gravity for sand blocks."""

    def apply(self, world) -> None:
        # Iterate from bottom to top to avoid a block falling multiple spaces in one tick
        for y in range(1, world.height):
            for x in range(world.width):
                if world.grid[y, x] == SAND:
                    # Check below
                    if world.grid[y - 1, x] == AIR:
                        world.grid[y - 1, x] = SAND
                        world.grid[y, x] = AIR


class WaterFlowRule:
    """Simulates gravity and horizontal flow for water blocks."""

    def apply(self, world) -> None:
        # Step 1: Flow down (iterate bottom to top)
        for y in range(1, world.height):
            for x in range(world.width):
                if world.grid[y, x] == WATER:
                    if world.grid[y - 1, x] == AIR:
                        world.grid[y - 1, x] = WATER
                        world.grid[y, x] = AIR

        # Step 2: Flow horizontally (for cells already on solid ground)
        # Note: To be deterministic and avoid bias, we can check left/right
        for y in range(world.height):
            for x in range(world.width):
                if world.grid[y, x] == WATER:
                    # If below is not air (i.e. blocked)
                    if y == 0 or world.grid[y - 1, x] != AIR:
                        left_free = x > 0 and world.grid[y, x - 1] == AIR
                        right_free = x < world.width - 1 and world.grid[y, x + 1] == AIR

                        if left_free and right_free:
                            # Flow left deterministically for now
                            world.grid[y, x - 1] = WATER
                            world.grid[y, x] = AIR
                        elif left_free:
                            world.grid[y, x - 1] = WATER
                            world.grid[y, x] = AIR
                        elif right_free:
                            world.grid[y, x + 1] = WATER
                            world.grid[y, x] = AIR
