from model.Component import Component
from model.CrossingPath import CrossingPath
from model.Multiplexer import Multiplexer
from model.ParallelPath import ParallelPath

# TODO : Take the delay of the multiplexer in account
# TODO : __repr__ method
class Stage(Component):
    """
    A class that represent a Stage in an Arbiter PUF. A Stage is composed of  Multiplexers, that decide which path the data will take,
    crossing path or parallel path

    Args : None
    
    Methods:
            challenge(self) -> Exception, raise an Exception because you can't challenge a Stage
            stage_challenge(self, actual_challenge_bit: int, previous_challenge_bit: int) -> tuple(float, float),
            return the additional delay of the path 1 and the path 2 according to the actual challenge bit and the
            previous challenge bit
            
    """

    def __init__(self):
        super().__init__()
        # A Stage doesn't have a delay even if it's a component
        self.delay = 0.0

        # Data can take 2 paths in a stage, the parallel path or the crossing path.
        # They are create a for the same challenge, a PUF must have the same result.
        self.parallel_path = ParallelPath()
        self.crossing_path = CrossingPath()

        # A stage is composed of 2 multiplexers one at the top and another down
        self.up_multiplexer: Multiplexer = Multiplexer()
        self.down_multiplexer: Multiplexer = Multiplexer()

    def challenge(self) -> float:
        """
        raise an Exception because you can't challenge a Stage with a challenge method but with stage_challenge(int,int)
        """
        raise Exception("to challenge a stage, use Stage.stage_challenge(int,int)")

    def stage_challenge(self, actual_challenge_bit: int, previous_challenge_bit: int) -> tuple(float, float):
        """
        params : actual_challenge_bit : int, previous_challenge_bit : int
        return the additional delay of the path 1 and the path 2 according to the actual challenge bit and the
        previous challenge bit
        """
        if previous_challenge_bit == 0:
            path_1_additional_delay = self.up_multiplexer.delay + self.parallel_path.challenge() \
                if actual_challenge_bit == 0 else self.up_multiplexer.delay + self.crossing_path.challenge()

            path_2_additional_delay = self.down_multiplexer.delay + self.parallel_path.challenge() \
                if actual_challenge_bit == 0 else self.down_multiplexer.delay + self.crossing_path.challenge()

        elif previous_challenge_bit == 1:
            path_1_additional_delay = self.down_multiplexer.delay + self.parallel_path.challenge() \
                if actual_challenge_bit == 0 else self.down_multiplexer.delay + self.crossing_path.challenge()

            path_2_additional_delay = self.up_multiplexer.delay + self.parallel_path.challenge() \
                if actual_challenge_bit == 0 else self.up_multiplexer.delay + self.crossing_path.challenge()

        else:
            raise Exception("Your challenge contains a data that isn't a bit here is", previous_challenge_bit)

        return path_1_additional_delay, path_2_additional_delay

    def __str__(self):
        return f"**** Stage ****\nup-multiplexer delay : {self.up_multiplexer.delay}\n" \
               f"down-multiplexer delay : {self.down_multiplexer.delay}"
