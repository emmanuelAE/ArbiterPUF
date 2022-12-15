import random

from model.PUF import PUF
from model.Stage import Stage


class ArbiterPUF(PUF):
    """
    Arbiter ArbiterPUF. can be initialise like this:
    -> ArbiterPUF(number_of_stage) example: ArbiterPUF(64)
    -> ArbiterPUF(challenge_vector) example: ArbiterPUF([0,0,1,0,1,1])
    -> ArbiterPUF(serie_of_challenge) example: ArbiterPUF([0,1,1,0],[1,1,1,1],[0,0,0,0]])
    """
    def __init__(self, *args):
        # the attributes that can be use to create
        super().__init__()
        self.number_of_stage = None
        self.challenge_vector = None
        self.series_of_challenge = None

        # Our ArbiterPUF can be crate with the number_of_stage of state or with a challenge or with a serie of challenge
        if args == ():
            raise Exception("You have to specify the number of stage or a challenge or a serie of challenge")
        else:
            for arg in args:
                if type(arg) is list:
                    if type(arg[0]) is list:
                        print("** Creating the ArbiterPUF. Initialisation with a series of challenge **")
                        self.series_of_challenge = arg
                    else:
                        print("** Creating the ArbiterPUF. Initialisation with a challenge **")
                        self.challenge_vector = arg

                elif type(arg) in (int, float):
                    self.number_of_stage = arg
                    print(f"** Creating the ArbiterPUF. Initialisation with {self.number_of_stage} stages **")

                else:
                    raise Exception("This type of attribute is not accept for the creation of ArbiterPUF", arg)

        # case the user set more than one attribute
        _set_attribute = 0
        for attribute in (self.number_of_stage, self.challenge_vector, self.series_of_challenge):
            if attribute is not None:
                _set_attribute += 1
        if _set_attribute > 1:
            raise Exception("Only one parameter is need to create the ArbiterPUF ")

        if self.number_of_stage is None:
            self.number_of_stage = len(self.challenge_vector) if self.challenge_vector is not None \
                else len(self.series_of_challenge[0])
        # create now the different stage of the ArbiterPUF
        self.create_stage()

    def __challenge(self):
        path_1_time = 0.0
        path_2_time = 0.0

        for i in range(len(self.challenge_vector)):
            if i == 0:
                path_1_time += self.stage_list[i].up_multiplexer.delay
                path_2_time += self.stage_list[i].down_multiplexer.delay
            _temp = self.stage_list[i].stage_challenge(self.challenge_vector[i], self.challenge_vector[i - 1])

            path_1_time += _temp[0]
            path_2_time += _temp[1]
        # return the response of the path
        response_before_inter_error = self.arbiter.response(path_1_time, path_2_time)
        # The probability the the bit before internal error flit is very low < 1%
        return self.add_internal_error(response_before_inter_error)

    def challenge(self, challenge_vector: list = None):
        _temp = 0
        for challenge in (self.challenge_vector, self.series_of_challenge, challenge_vector):
            if challenge is None:
                _temp += 1
        if _temp == 3:
            self.challenge_vector = []
            for i in range(self.number_of_stage):
                self.challenge_vector.append(random.randint(0, 1))
            print(f"\033[91m** Warning **: A challenge was not specify a random challenge vector was used.\n"
                  "               Tkanks to specify a challenge if you want a specific response.\n"
                  f"                Random challenge: {self.challenge_vector}\033[0m")

        if challenge_vector is not None:
            self.challenge_vector = challenge_vector
        elif self.series_of_challenge is not None:
            return self.serie_challenge()

        return self.__challenge()

    def serie_challenge(self):
        fingerprint = ""
        for challenge_vector in self.series_of_challenge:
            self.challenge_vector = challenge_vector
            fingerprint += str(self.__challenge()) + " "
        return fingerprint

    def create_stage(self):
        """Create the different stage of our ArbiterPUF"""
        if self.number_of_stage is not None:
            for i in range(self.number_of_stage):
                self.stage_list.append(Stage())
        elif self.challenge_vector is not None:
            for i in range(len(self.challenge_vector)):
                self.stage_list.append(Stage())
        else:
            for i in range(len(self.series_of_challenge[0])):
                self.stage_list.append(Stage())

    # Features of good ArbiterPUF


