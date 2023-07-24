import math
import random
from abc import abstractmethod, ABC

class Component(ABC):
    """
    Abstract base class representing a single component of a PUF.
    Args : 
        delay : The time need to the signal to pass through the component (How much in s the component delay the siganl)

    Methods : 
        challenge() -> float : Abstract method that return the time need to the signal to pass through
                                the composant.  
    """
    def __init__(self):
        """Create a component with a delay that follow a normal distribution """
        self.delay = abs(random.normalvariate(0, 1.0))

    @abstractmethod
    def challenge(self) -> float:
        """
        Return the delay (The time need to the signal to pass through the component)
        """
        ...
