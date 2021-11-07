from os import getcwd, mkdir
from os.path import isdir

def check_data_file_exists():
    path = getcwd() + "/data"

    if not isdir(path):
        mkdir(path)