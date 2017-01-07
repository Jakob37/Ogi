import os
import configparser

CONF_NAME = "ogi.conf"

my_dir = os.path.dirname(os.path.realpath(__file__))
conf_path = "{}/{}".format(my_dir, CONF_NAME)

config = None
config_exists = os.path.isfile(conf_path)

if config_exists:
    config = configparser.ConfigParser()
    config.read(conf_path)


def check_config_exists():

    return config_exists


def get_config_path():

    return conf_path


def get_config():

    if not config_exists:
        raise Exception("Config file not found at expected path: {}, run setup command (ogi.py setup) to get started"
                        .format(conf_path))

    return config


def get_base_dir():
    return my_dir
