#!/usr/bin/env python3

import argparse
import os

from modules.commands import ogi_log
from modules.commands import ogi_new
from modules.commands import ogi_setup
from modules.commands import ogi_list
from modules.commands import ogi_write

CONF_NAME = "ogi.conf"
sysdir = os.path.dirname(os.path.realpath(__file__))


def parse_arguments():

    def default_func(args):
        print("Must specify tool (ogi <tool>)")
        parser.print_help()
        exit(1)

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=default_func)

    subparsers = parser.add_subparsers(help='Commands: log list new')

    parse_log(subparsers)
    parse_list(subparsers)
    parse_new(subparsers)
    parse_setup(subparsers)
    parse_write(subparsers)

    args = parser.parse_args()

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
                           default="")

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

    list_options = ['day', 'week', 'month', 'year', 'projects', 'categories', 'date_range', 'prev_days']
    subparser.add_argument('list_type', choices=list_options)

    subparser.add_argument('--summary', '-s', help='Show a condensed format', action='store_true')
    subparser.add_argument('--limited', '-l', help='Show only time entries', action='store_true')
    subparser.add_argument('--start_date', help='Custom start date for date_range')
    subparser.add_argument('--end_date', help='Custom end date for date_range')
    subparser.add_argument('--number', '-n', help='Number of entires for prev_days option', type=int)


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


def parse_write(subparsers_object):

    """Subparser for output writing command"""

    def ogi_write_func(args):
        ogi_write.main(args)

    subparser = subparsers_object.add_parser('write')
    subparser.set_defaults(func=ogi_write_func)

    subparser.add_argument('--time_entries')
    subparser.add_argument('--projects')
    subparser.add_argument('--categories')
    subparser.add_argument('--delim', default='\t')


def parse_setup(subparsers_object):

    """Setup command"""

    def ogi_setup_func(args):
        ogi_setup.main(args)

    subparser = subparsers_object.add_parser('setup')
    subparser.set_defaults(func=ogi_setup_func)

    subparser.add_argument('--dry_run', action='store_true')
    subparser.add_argument('--database_test', action='store_true')
    subparser.add_argument('--database_from_tsvs', action='store_true')


if __name__ == "__main__":
    parse_arguments()
