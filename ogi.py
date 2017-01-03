#/usr/bin/env python3

import argparse
import re
import datetime
import configparser
import os
import sys

CONF_NAME = "ogi.conf"


def load_module(modname, modpath):

    if sys.version_info.minor >= 5:
        import importlib.util
        spec = importlib.util.spec_from_file_location(modname, modpath)
        module_exec = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_exec)
        return module_exec
    else:
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(modname, modpath).load_module()


sysdir = os.path.dirname(os.path.realpath(__file__))

log_mod_name = "modules.ogi_log"
log_mod_path = "{}/{}".format(sysdir, "modules/ogi_log.py")
ogi_log = load_module(log_mod_name, log_mod_path)



def main():

    args = parse_arguments()

    my_dir = os.path.dirname(os.path.realpath(__file__))
    conf = parse_config("{}/{}".format(my_dir, CONF_NAME))


 
def parse_arguments():

    def default_func(args):
        print("Must specify tool (ogi <tool>)")
        parser.print_help()
        exit(1)

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=default_func)

    subparsers = parser.add_subparsers(help='Commands: log')

    parse_ogi_log(subparsers)

    print("parsed")


def parse_ogi_log(subparsers_object):

    def ogi_log(args):
        ogi_log.main(args, conf)

    subparser = subparsers_object.add_parser('log')
    subparser.set_defaults(func=ogi_log)

    subparser.add_argument('log_type', choices=['pomo', 'block', 'session'], 
                        default='block', nargs='?')
    subparser.add_argument('-m', '--message',
                        help='Description of performed task during logged time',
                        required=True)

    subparser.add_argument('-t', '--time', default=None,
                        help="Format: HHMM, defaults to current time")
    subparser.add_argument('-d', '--date', default=None,
                        help="Format: YYYYMMDD, defaults to current date")
    subparser.add_argument('-f', '--focus', default=100, type=int)
    subparser.add_argument('-u', '--duration', default=None)

    subparser.add_argument('-p', '--project', required=True)


def parse_config(conf_path):

    config = configparser.ConfigParser()
    config.read(conf_path)
    return config


if __name__ == "__main__":
    parse_arguments()

