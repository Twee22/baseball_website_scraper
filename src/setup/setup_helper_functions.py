from os import getcwd, mkdir
from os.path import isdir
import urllib3

def check_data_file_exists():
    path = getcwd() + "/data"

    if not isdir(path):
        mkdir(path)
        
def disable_warnings():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)