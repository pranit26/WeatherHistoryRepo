import configparser
import os

def get_config():
    config = configparser.ConfigParser()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(ROOT_DIR, 'config.txt')
    config.read_file(open(path))
    return config
