import csv
import os.path
import pickle
import random

from PUFProperties.properties import H, D, U, MU
from fileManagement import utilities
from model.ArbiterPUF import ArbiterPUF


class Simulator:
    def __init__(self, out_file_path):
        self.out_file_path = out_file_path
        self._csv_path = os.path.join(out_file_path, "csv")
        self._puf_instance_path = os.path.join(out_file_path, "puf_instances")

    @staticmethod
    def _create_csv_header(number_column):
        header = ["index"]
        for i in range(1, (number_column + 1)):
            header.append(f"c{i}")
        header.append("response")
        return header

    @staticmethod
    def create_random_challenge(nb_of_bit):
        challenge = []
        for i in range(nb_of_bit):
            challenge.append(random.randint(0, 1))
        return challenge

    def create_arbiter_puf(self, nb_of_puf=10, nb_of_crps=10_000, nb_of_stage=64):  # NOQA
        puf_instances = []
        csv_header = self._create_csv_header(nb_of_stage)
        warning = "** Warning **: this script while delete older csv file in csv directory and older " \
                  "puf instance object in puf_instance_object"
        question = "Do you want to continues ? Y or N"

        # the user response is N
        if not utilities.ask_confirmation(message=warning, question=question):
            print("Canceled")
            return

        # the user response is Y
        # deleting olds csv and puf objects
        print("\033[91m Deleting olds files ...\033[0m")
        utilities.delete_dir_file(self._csv_path)
        utilities.delete_dir_file(self._puf_instance_path)

        # Display info
        print(f"\t\t-----------------------------------------------\n\t\t\t\t\t- Simulation started -                "
              f"\n\t\t\tCreating {nb_of_puf} PUFs. each ArbiterPUF will generate \n"
              f"\t\t\t{nb_of_crps} CRPs\n\t\t-----------------------------------------------")

        for i in range(nb_of_puf):

            puf_instances.append(ArbiterPUF(nb_of_stage))

            # create the csv file for store puf crps # NOQA
            csv_file = open(f"{self._csv_path}/puf{i + 1}_CPRs.csv", 'w')
            csv_writer = csv.writer(csv_file)
            # write the header
            csv_writer.writerow(csv_header)

            # create the different CPRs of this instance of ArbiterPUF
            puf = puf_instances[i]
            print("\033[93m-- Starting CRPs creation and saving in csv file --\033[0m")
            for j in range(nb_of_crps):
                challenge_response = puf.challenge(self.create_random_challenge(nb_of_stage))
                _data = [bit for bit in puf.challenge_vector]
                # insertion of the index
                _data.insert(0, j + 1)
                _data.append(challenge_response)

                # write in the csv this instance csv file
                csv_writer.writerow(_data)

            # save the binary instance of our ArbiterPUF using pickle
            # WARNING: pickle isn't secure always unpickle data that you trust
            print(f"\033[93m-- Saving our puf object as puf_object{i + 1}.puf in puf_instance_object --\033[0m")
            pickle.dump(puf, open(f"{self._puf_instance_path}/puf_object{i + 1}.puf", "wb"))

        print(
            "\033[92m\t\t-----------------------------------------------\n\t\t\t\t\t- ArbiterPUF Simulation SUCCEED - "
            "\n\t\t-----------------------------------------------\033[0m")
        return

    def measure_puf_properties(self):
        # create one ArbiterPUF
        puf = ArbiterPUF(64)
        puf_response = []
        # use for measure Uniqueness
        puf_list = []
        # use for measure the mean of Uniqueness
        u_list = []
        # create 10 000 crps   # NOQA
        for i in range(10_000):
            puf_response.append(puf.challenge(self.create_random_challenge(64)))

        print("Measuring ArbiterPUF properties...")
        # Randomness
        p, h = H(puf_response)

        # Diffuseness
        d = D(10_000, puf_response)

        # Uniqueness
        # For the uniqueness, we'll use pufs instances store in the out_file_path/puf_instances if it empty # NOQA
        # or contains less than, we'll create 10 instances of puf to measure Uniqueness
        if utilities.number_of_file(self._puf_instance_path) < 10:
            print("No puf or enough puf stored in memory, Creation of 10 instances of arbiterPUF")
            for i in range(9):
                puf_list.append(ArbiterPUF(64))
            puf_list.append(puf)
        else:
            puf_list = utilities.load_puf_from_memory(self._puf_instance_path)
        # We challenge all our puf to get their responses
        puf_response = [puf.challenge(self.create_random_challenge(64)) for puf in puf_list]

        u = U(len(puf_list), puf_response)

        # Mean of Uniqueness
        # the measure the uniqueness of our puf 10_000 with 10_000 different challenge and return the mean
        for i in range(10_000):
            challenge = self.create_random_challenge(64)
            puf_response = [puf.challenge(challenge) for puf in puf_list]
            u_list.append(U(len(puf_list), puf_response))
        mu = MU(u_list)

        # Print result to user
        print("Randomness  : ", h)
        print("Diffuseness : ", d)
        print("Uniqueness  : ", u)
        print("MU          : ", mu)


