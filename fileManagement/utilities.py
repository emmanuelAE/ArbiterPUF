import csv
import os
import csv


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

