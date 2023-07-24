from model.Component import Component

class CrossingPath(Component):
    def __init__(self):
        """
        A class that represent a Crossing Path in an Arbiter PUF.
        Args : None

        Methods:
                challenge(self) -> float, return the delay of the Crossing Path
        """
        super().__init__()

    def challenge(self) -> float:
        """
        return the delay of the Crossing Path
        """
        return self.delay

