import random
from abc import abstractmethod, ABC

from model.Arbiter import Arbiter
from model.Stage import Stage


class AbstractPUF(ABC):
    def __init__(self):
        self.stage_list: [Stage] = []
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
