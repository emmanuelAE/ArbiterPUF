import math
import random
from abc import abstractmethod, ABC


class Component(ABC):
    def __init__(self):
        """Create a component with a delay that follow a normal distribution """
        self.delay = abs(random.normalvariate(0, 1.0))

    @abstractmethod
    def challenge(self) -> float:
        """Return the delay useful to treat the stimulus"""
        ...
