import random
from abc import abstractmethod, ABC
from typing import List
from model.Arbiter import Arbiter
from model.Stage import Stage

# TODO: Remove stage_list from PUF class because not all PUFs have stages
# TODO: Remove arbiter from PUF class because not all PUFs have an arbiter
# TODO: Change aging method to abstract because not all PUF have aging like the arbiter PUF
class PUF(ABC):
    """
    Abstract base class representing a single component of a PUF.
    Args :
        delay : The time need to the signal to pass through the component (How much in s the component delay the siganl)

    Methods :
        challenge() -> float : Abstract method that return the time need to the signal to pass through
                                the composant.
        aging() -> None : Method that simulate the aging of the PUF
    """
    def __init__(self):
        self.stage_list: List[Stage] = []
        self.arbiter = Arbiter()
        self.error_rate = random.random() / 10

    @abstractmethod
    def challenge(self, challenge_vector: list = None): ...

    def aging(self, new_error_rate=None):
        self.error_rate = 0.5 if new_error_rate is None else new_error_rate

    def add_internal_error(self, challenge_response_bit):
        _probability = random.random()
        if _probability <= self.error_rate:
            return 1 - challenge_response_bit
        return challenge_response_bit
