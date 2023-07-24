from model.Component import Component

class Arbiter(Component):
    """
    A class that represent an Arbiter of a Arbiter path. It decide which path is the fastest
    Args : None

    Methods: 
            response(self, path_1_time: float, path_2_time: float) -> int, return 1 if path_1_time >= path_2_time else 0
    """
    def __init__(self):
        super().__init__()
        # the arbiter haven't delay
        self.delay = 0.0

    def challenge(self) -> Exception:
        raise Exception("You can't challenge the Arbiter")

    # TODO : Make this function Bool (true, false)
    def response(self, path_1_time: float, path_2_time: float) -> int:
        """
        params : path_1_time : float, path_2_time : float
        return  1 if path_1_time >= path_2_time else 0
        """
        return 1 if path_1_time >= path_2_time else 0
