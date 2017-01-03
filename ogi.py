#/usr/bin/env python3

import argparse
import re
import datetime
import configparser
import os
import sys

CONF_NAME = "ogi.conf"

from modules import ogi_log
from modules import ogi_list

sysdir = os.path.dirname(os.path.realpath(__file__))


def parse_arguments():

    def default_func(args, conf):
        print("Must specify tool (ogi <tool>)")
        parser.print_help()
        exit(1)

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=default_func)

    subparsers = parser.add_subparsers(help='Commands: log list')

    parse_ogi_log(subparsers)
    parse_list(subparsers)

    args = parser.parse_args()
    conf = parse_config()

    args.func(args, conf)



def parse_ogi_log(subparsers_object):

    def ogi_log_func(args, conf):
        ogi_log.main(args, conf)

    subparser = subparsers_object.add_parser('log')
    subparser.set_defaults(func=ogi_log_func)

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

    subparser.add_argument('--testrun', action='store_true')


def parse_list(subparsers_object):

    def ogi_list_func(args, conf):
        ogi_list.main(args, conf)

    subparser = subparsers_object.add_parser('list')
    subparser.set_defaults(func=ogi_list_func)


def parse_config():

    my_dir = os.path.dirname(os.path.realpath(__file__))
    conf_path = "{}/{}".format(my_dir, CONF_NAME)

    config = configparser.ConfigParser()
    config.read(conf_path)
    return config


if __name__ == "__main__":
    parse_arguments()

