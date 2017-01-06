#!/usr/bin/env python3

import argparse
import configparser
import os

CONF_NAME = "ogi.conf"

from modules import ogi_log
from modules import ogi_list
from modules import ogi_new
from modules import utils
import ogi_config

sysdir = os.path.dirname(os.path.realpath(__file__))



def parse_arguments():

    def default_func(args, conf):
        print("Must specify tool (ogi <tool>)")
        parser.print_help()
        exit(1)

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=default_func)

    subparsers = parser.add_subparsers(help='Commands: log list new')

    parse_log(subparsers)
    parse_list(subparsers)
    parse_new(subparsers)

    args = parser.parse_args()
    # conf = parse_config()
    # GLOBAL_CONF = conf

    # conf = ogi_config.get_config()

    args.func(args)


def parse_log(subparsers_object):

    def ogi_log_func(args):
        ogi_log.main(args)

    subparser = subparsers_object.add_parser('log')
    subparser.set_defaults(func=ogi_log_func)

    subparser.add_argument('log_type', choices=['pomo', 'block', 'session'],
                           nargs='?')
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
    subparser.add_argument('--dry_run', action='store_true')


def parse_list(subparsers_object):

    def ogi_list_func(args):
        ogi_list.main(args)

    subparser = subparsers_object.add_parser('list')
    subparser.set_defaults(func=ogi_list_func)

    subparser.add_argument('list_type', choices=['project_summary', 'today', 'projects', 'categories'])


def parse_new(subparsers_object):

    """Subparser for new command"""

    def ogi_new_func(args):
        ogi_new.main(args)

    subparser = subparsers_object.add_parser('new')
    subparser.set_defaults(func=ogi_new_func)

    subparser.add_argument('object_type', choices=['project', 'category'])
    subparser.add_argument('-n', '--name')
    subparser.add_argument('-c', '--category')
    subparser.add_argument('--dry_run', action='store_true')


# def parse_config():
#
#     my_dir = os.path.dirname(os.path.realpath(__file__))
#     conf_path = "{}/{}".format(my_dir, CONF_NAME)
#
#     config = configparser.ConfigParser()
#     config.read(conf_path)
#     return config

if __name__ == "__main__":
    parse_arguments()

