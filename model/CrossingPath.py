from model.Component import Component


class CrossingPath(Component):
    def __init__(self):
        """Create a Crossing Path and give it a delay that follow the normal distribution"""
        super().__init__()

    def challenge(self) -> float:
        return self.delay

