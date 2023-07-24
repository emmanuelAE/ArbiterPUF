from model.Component import Component


class Multiplexer(Component):

    def __init__(self):
        """
        A class that represent a Multiplexer in an Arbiter PUF.
        """
        super().__init__()

    def challenge(self) -> float:
        """
        return the delay of the Multiplexer
        """
        return self.delay
