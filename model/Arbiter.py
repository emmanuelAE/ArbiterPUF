from model.Component import Component


class Arbiter(Component):
    def __init__(self):
        super().__init__()
        # the arbiter have no delay
        self.delay = 0.0

    def challenge(self) -> float:
        raise Exception("You can't challenge the Arbiter")

    def response(self, path_1_time: float, path_2_time: float) -> int:
        """Simply compare the 2 path time and return (0 or 1) in consequence """
        if path_1_time >= path_2_time:
            return 1
        return 0
