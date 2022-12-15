from model.Component import Component


class Multiplexer(Component):

    def __init__(self):
        """Create a Multiplexer and give it a delay that follow the normal distribution"""
        super().__init__()

    def challenge(self) -> float:
        """Add a to the path time the delay of the Multiplexer"""
        return self.delay
