import os
import configparser

CONF_NAME = "ogi.conf"

CONFIG = None

class OgiConfig:

    class __OgiConfig:
        def __init__(self):
            pass

        def __str__(self):



def get_config():

    if CONFIG is None:

        my_dir = os.path.dirname(os.path.realpath(__file__))
        conf_path = "{}/{}".format(my_dir, CONF_NAME)

        config = configparser.ConfigParser()
        config.read(conf_path)

        CONFIG = config

    return CONFIG
