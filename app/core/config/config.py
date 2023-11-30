import configparser
import logging
import os

class FileConfig:
    CONFIG_FILE_NAME = 'config.ini'

    def __init__(self):
        pass
        # file: str =None

    def load_config(self, path: str):
        config = configparser.ConfigParser()
        config_full_path = os.path.join(path, self.CONFIG_FILE_NAME)
        logging.info("| config file path: "+ config_full_path)
        config.read(config_full_path, encoding='utf-8')
        return config

    def set_file(self, path: str ="."):
        raise NotImplementedError
        # file = path + os.sep + self.CONFIG_FILE_NAME






