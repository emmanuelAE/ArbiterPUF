from model.Component import Component

# TODO : __repr__ method, __str__ method.
class ParallelPath(Component):
    def __init__(self):
       """
       A class that represent a Parallel Path in an Arbiter PUF.
       Args : None
       
       Methods:
               challenge(self) -> float, return the delay of the Parallel Path
        """
       super().__init__()

    def challenge(self) -> float:
        """
        return the delay of the Parallel Path
        """
        return self.delay
