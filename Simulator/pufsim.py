import pickle
import random
import csv
from time import sleep


from PUFProperties.properties import D
from PUFProperties.properties import H
from PUFProperties.properties import U
from PUFProperties.properties import MU
from model.PUF import PUF
from fileManagement import utilities
from PUFsim.LoadPufFromMemory import loadPufFromMemory

NB_OF_CRPs = 10_000


# create the header like this : [index, c1, c2, ..... c64]
def create_header(number_of_stage):
    header = ["index"]
    for i in range(1, (number_of_stage + 1)):
        header.append(f"c{i}")
    header.append("response")
    return header


def create_random_challenge(nb_of_bit):
    challenge = []
    for i in range(nb_of_bit):
        
        challenge.append(random.randint(0, 1))
    return challenge


def ask_confirmation(message=None, question=None):
    print(f"\033[91m {message}")
    choice = input(f"{question}\033[0m\n")
    if 'Y' in choice or 'y' in choice:
        return True
    return False


def sim(number_of_stage: int = 64, number_of_PUF: int = 10, number_of_CRPs=10_000):
    PUF_instances = []
    # Header for all csv file
    _header = create_header(number_of_stage)

    if ask_confirmation("** Warning **: this script while delete older csv file in csv directory and older puf "
                        "instance object in puf_instance_object", "Do you want to continues ? Y or N"):
        # deleting olds csv and puf objects
        print("\033[91m Deleting olds files ...\033[0m")
        utilities.delete_dir_file("csv/")
        utilities.delete_dir_file("puf_instance_object/")

        # Display sim infos
        print(f"\t\t-----------------------------------------------\n\t\t\t\t\t- Simulation started -                "
              f"\n\t\t\tCreating {number_of_PUF} PUFs. each ArbiterPUF will generate \n"
              f"\t\t\t{number_of_CRPs} CRPs\n\t\t-----------------------------------------------")

        for i in range(number_of_PUF):
            PUF_instances.append(PUF(number_of_stage))

            # create the csv file for the path instance
            csv_file = open(f"csv/puf{i + 1}_CPRs.csv", 'w')
            csv_writer = csv.writer(csv_file)

            # write the header
            csv_writer.writerow(_header)

            # create the different CPRs of this instance of ArbiterPUF
            puf = PUF_instances[i]
            print("\033[93m-- Starting CRPs creation and saving in csv file --\033[0m")
            for j in range(number_of_CRPs):
                challenge_response = puf.challenge(create_random_challenge(number_of_stage))
                _data = [bit for bit in puf.challenge_vector]
                # insertion of the index
                _data.insert(0, j + 1)
                _data.append(challenge_response)

                # write in the csv this instance csv file
                csv_writer.writerow(_data)

            # save the binary instance of our ArbiterPUF using pickle
            # WARNING: pickle isn't secure always unpickle data that you trust
            print(f"\033[93m-- Saving our puf object as puf_object{i + 1}.puf in puf_instance_object --\033[0m")
            pickle.dump(puf, open(f"puf_instance_object/puf_object{i + 1}.puf", "wb"))

        print("\033[92m\t\t-----------------------------------------------\n\t\t\t\t\t- ArbiterPUF Simulation SUCCEED - "
              "\n\t\t-----------------------------------------------\033[0m")

    else:
        print("Canceled")


# Creating 10 PUFs of 64 stages. each PUFs return 10 000 CPRs saved in csv
# All PUFs create are saved in puf_instance_object
#sim(64, 10, 1)


def properties_sim():
    # create a ArbiterPUF for simulation
    puf = PUF(64)

    # properties calculation

    # H calculation
    puf_response = []

    for i in range(10_000):
        puf_response.append(puf.challenge(create_random_challenge(64)))
    p, h = H(puf_response)

    print("Evaluating ArbiterPUF properties...")
    sleep(2)
    print("p = {}, h = {}".format(p, h))
    print('d = ', D(10_000, puf_response))

    # Uniqueness

    if (len(utilities.get_dir_file_name("puf_instance_object/"))) == 0:
        print('NO ArbiterPUF INSTANCES : start puf generation ')
        sim(64, 10, 10_000)

    responses = []
    challenge = create_random_challenge(64)

    PUF_list = loadPufFromMemory()
    for puf in PUF_list:
        responses.append(puf.challenge(challenge_vector=challenge))

    NB_OF_PUFs = len(utilities.get_dir_file_name("puf_instance_object/"))

    print(NB_OF_PUFs)
    print(responses)
    u = U(NB_OF_PUFs, responses)
    print('u: ', u)

    Uks = []
    challenge_list = []
    responses = []
    for i in range(NB_OF_CRPs):
        challenge_list.append(create_random_challenge(64))

    for i in range(NB_OF_CRPs):
        for puf in PUF_list:
            responses.append(puf.challenge(challenge_vector=challenge))
        Uks.append(U(NB_OF_PUFs, responses))
    print("MU: ", MU(Uks))

properties_sim()




