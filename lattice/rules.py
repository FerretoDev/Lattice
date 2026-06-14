class RuleRegistry:
    """Registry for managing tick rules."""

    def __init__(self) -> None:
        self.rules: list = []

    def register(self, rule) -> None:
        """Register a simulation rule."""
        self.rules.append(rule)
