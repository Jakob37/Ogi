import os
import configparser

CONF_NAME = "ogi.conf"

my_dir = os.path.dirname(os.path.realpath(__file__))
conf_path = "{}/{}".format(my_dir, CONF_NAME)

config = configparser.ConfigParser()
config.read(conf_path)


def get_config():

    return config
