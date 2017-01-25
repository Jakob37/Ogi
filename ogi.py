#!/usr/bin/env python3

import argparse
import os
import sys

from modules.commands import ogi_log
from modules.commands import ogi_new
from modules.commands import ogi_setup
from modules.commands import ogi_list
from modules.commands import ogi_write
from modules.commands import ogi_edit

import ogi_config

CONF_NAME = "ogi.conf"
sysdir = os.path.dirname(os.path.realpath(__file__))


def parse_arguments():

    def default_func(args):
        print("Must specify tool (ogi <tool>)")
        parser.print_help()
        exit(1)

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=default_func)

    subparsers = parser.add_subparsers(help='Commands:')

    parse_log(subparsers)
    parse_list(subparsers)
    parse_new(subparsers)
    parse_setup(subparsers)
    parse_write(subparsers)
    parse_edit(subparsers)

    args = parser.parse_args()
    args.func(args)


def verify_files_setup(args):

    print("In verify")

    conf_exists = ogi_config.check_config_exists()
    conf_path = ogi_config.get_config_path()

    if not conf_exists:
        print("Config file not found in: {}".format(conf_path))
        print("You need to set this up, either manually or by running the command './ogi setup'")
        sys.exit(1)

    expected_field_not_present = ogi_config.get_expected_field_not_present()

    if len(expected_field_not_present) > 0:
        print("Configuration file lacks following required fields")
        for field in expected_field_not_present:
            print("Category: {} Value: {}".format(field[0], field[1]))
        sys.exit(1)


    print(conf_exists)

    # -> Check config file is valid - Containing required fields
    # -> Check that the database is set up - That the file actually exists

    return False


def parse_log(subparsers_object):

    def ogi_log_func(args):
        verify_files_setup(args)
        ogi_log.main(args)

    subparser = subparsers_object.add_parser('log')
    subparser.set_defaults(func=ogi_log_func, which='log')

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
        verify_files_setup(args)
        ogi_list.main(args)

    subparser = subparsers_object.add_parser('list')
    subparser.set_defaults(func=ogi_list_func, which='list')

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
        verify_files_setup(args)
        ogi_new.main(args)

    subparser = subparsers_object.add_parser('new')
    subparser.set_defaults(func=ogi_new_func, which='new')

    subparser.add_argument('object_type', choices=['project', 'category'])
    subparser.add_argument('-n', '--name')
    subparser.add_argument('-c', '--category')
    subparser.add_argument('--dry_run', action='store_true')


def parse_write(subparsers_object):

    """Subparser for output writing command"""

    def ogi_write_func(args):
        verify_files_setup(args)
        ogi_write.main(args)

    subparser = subparsers_object.add_parser('write')
    subparser.set_defaults(func=ogi_write_func, which='write')

    subparser.add_argument('--time_entries')
    subparser.add_argument('--projects')
    subparser.add_argument('--categories')
    subparser.add_argument('--delim', default='\t')


def parse_setup(subparsers_object):

    """Setup command"""

    def ogi_setup_func(args):
        ogi_setup.main(args)

    subparser = subparsers_object.add_parser('setup')
    subparser.set_defaults(func=ogi_setup_func, which='setup')

    subparser.add_argument('--dry_run', action='store_true')
    subparser.add_argument('--database_test', action='store_true')

    subparser.add_argument('--database_from_tsvs', action='store_true')
    subparser.add_argument('--time_entries')
    subparser.add_argument('--project_entries')
    subparser.add_argument('--category_entries')


def parse_edit(subparsers_object):

    """Setup command"""

    def ogi_edit_func(args):
        verify_files_setup(args)
        ogi_edit.main(args)

    subparser = subparsers_object.add_parser('edit')
    subparser.set_defaults(func=ogi_edit_func, which='edit')

    edit_options = ['amend_last_entry']
    subparser.add_argument('edit_type', choices=edit_options)

    subparser.add_argument('--dry_run', action='store_true')


if __name__ == "__main__":
    parse_arguments()
