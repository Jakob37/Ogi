import os
import configparser
import sys

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


def check_database_exists():

    if not check_config_exists():
        print("Config file not found, not able to check database")
        sys.exit(1)

    db_path = config.get('file_paths', 'sql_path')

    db_exists = os.path.isfile(db_path)

    if db_exists:
        return True
    else:
        print('Database not found at specified path: {}'.format(db_path))
        print('Please setup this properly by running the \'ogi setup\' command')
        sys.exit(1)


def get_config_path():

    return conf_path


def get_config():

    if not config_exists:
        raise Exception("Config file not found at expected path: {}, run setup command (ogi.py setup) to get started"
                        .format(conf_path))

    return config


def get_base_dir():
    return my_dir
