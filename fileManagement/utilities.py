import csv
import os
import csv
import pickle


def ask_confirmation(message=None, question=None):
    print(f"\033[91m {message}")
    choice = input(f"{question}\033[0m\n")
    if 'Y' in choice or 'y' in choice:
        return True
    return False


def get_dir_file_name(dir_path):
    try:
        dir_list = os.listdir(dir_path)
        return dir_list
    except Exception as e:
        raise Exception("make sure that it's a directory please", e)


def delete_file(file_name):
    os.remove(file_name)


def delete_dir_file(dir_path):
    path = os.path.join(os.getcwd(), dir_path)
    file_list = get_dir_file_name(dir_path)
    for file_name in file_list:
        os.remove(os.path.join(path, file_name))


def number_of_file(dir_path):
    file_list = get_dir_file_name(dir_path)
    return len(file_list)


def load_csv_data_from_memory(dir_path):
    csv_file_list = get_dir_file_name(dir_path)
    data = []
    _data = []

    for csv_file in csv_file_list:
        with open(f"{os.path.join(os.getcwd(), os.path.join('csv/', csv_file))}", 'r', encoding='utf-8') as file:
            test = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            for row in test:
                _data.append(row)
            data.append(_data)

    return data


def load_puf_from_memory(file_path):
    try:
        puf_list = []
        user_response = ask_confirmation("", "Do you want print puf instance")
        for i in range(number_of_file(file_path)):
            # Warning: pickle isn't secured, only load data that you trust
            puf1 = pickle.load(open(f"{file_path}/puf_object{i + 1}.puf", "rb"))
            puf_list.append(puf1)
            if user_response:
                response = puf1.challenge()
                challenge = puf1.challenge_vector
                print(f"*** PUF {i + 1} ***")
                print("-- last CPRs datas --")
                print("stages",
                      [
                          f"**stage_x (up_mux_delay {stage.up_multiplexer.delay}, down_mux_delay {stage.down_multiplexer.delay} )** "
                          for stage in puf1.stage_list])
                print("challenge: ", challenge)
                print("response: ", response)

        return puf_list
    except Exception as e:
        raise Exception("Create puf before load them from the memory", e)
