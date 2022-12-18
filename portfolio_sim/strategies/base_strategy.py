class BaseStrategy:
    """
    Base Class for Strategies
    """

    def __init__(self, name: str) -> None:
        """
        Args:
            name: Name of the strategy
        """
        self.name = name
