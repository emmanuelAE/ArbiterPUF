from model.Component import Component


class ParallelPath(Component):
    def __init__(self):
        """Create a Parallel Path and give it a delay that follow the normal distribution"""
        super().__init__()

    def challenge(self) -> float:
        return self.delay
