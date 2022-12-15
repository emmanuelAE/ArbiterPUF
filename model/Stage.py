from model.Component import Component
from model.CrossingPath import CrossingPath
from model.Multiplexer import Multiplexer
from model.ParallelPath import ParallelPath


class Stage(Component):
    """
    According to the course, a Stage is composed of two multiplexers
    """

    def __init__(self):
        super().__init__()
        # a Stage doesn't have a delay despite it's a component
        self.delay = 0.0
        self.parallel_path = ParallelPath()
        self.crossing_path = CrossingPath()

        # a stage is composed of 2 multiplexers one at the top and another down
        self.up_multiplexer: Multiplexer = Multiplexer()
        self.down_multiplexer: Multiplexer = Multiplexer()

    def challenge(self) -> float:
        raise Exception("to challenge a stage, use Stage.stage_challenge(int,int)")

    def stage_challenge(self, actual_challenge_bit: int, previous_challenge_bit: int) -> (float, float):
        """
        Add a delay to the corresponding path according to the actual bit challenge and the previous one
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
