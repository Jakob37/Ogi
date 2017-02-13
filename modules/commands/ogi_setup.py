#!/usr/bin/env python3

import os
import sys
import configparser

from modules.utils import prompt_utils

from modules.database import database_utils
from modules.entries.time_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry
from modules.entries.category_entry import CategoryEntry
import ogi_config

DRY_RUN = False


def main(args):

    if args.dry_run:
        print("DRY RUN - Simulated run, but nothing written")

    check_config_exists()

    save_base_dir = get_save_directory()
    ensure_dir(save_base_dir)

    create_symlink()
    setup_config_file(save_base_dir)
    setup_database()

    if args.database_from_tsvs:
        enter_tsvs_to_database(args)

    print("All done!")


def check_config_exists():

    config_exists = ogi_config.check_config_exists()
    if config_exists:

        force_setup_message = "Configuration file already exists, do you want to overwrite? "
        force_setup = prompt_utils.prompt_yes_no(force_setup_message)

        if not force_setup:
            print("Not forcing setup, aborting")
            sys.exit(0)
        else:
            conf_path = ogi_config.get_config_path()
            print("Forcing setup, moving previous config file to: {}".format(conf_path + ".old"))

            if not DRY_RUN:
                os.rename(conf_path, conf_path + ".old")


def get_save_directory():

    save_dir_message = "\nPlease provide the directory where your Ogi data should be stored. " \
                       "If you are planning on using Ogi on multiple devices, it is recommended " \
                       "to specify a synced folder, such as a Dropbox-folder.\nSave path: "

    save_dir = prompt_utils.prompt_for_path(save_dir_message, prompt_confirmation=True)
    return save_dir


def ensure_dir(dir_path):

    print("Abspath: {}".format(os.path.abspath(dir_path)))

    d = os.path.dirname(dir_path + "/")
    if not os.path.exists(d):
        print("\nCreating directory at: {}".format(d))

        if not DRY_RUN:
            os.makedirs(d)


def create_symlink():

    symlink_message = "\nProvide directory for symlink for easy access to 'ogi' command. " \
                      "Leave empty if not desired (or on Windows system, for which symlinks aren't implemented yet.) " \
                      "Symlink path: "

    symlink_path = prompt_utils.prompt_for_path(symlink_message, return_none_for_empty=True)

    if symlink_path:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        top_dir = '/'.join(current_dir.split('/')[:-1])
        print("\nCreating symlink at: {}".format(symlink_path + "/ogi"))

        if not DRY_RUN:
            os.symlink(top_dir + "/ogi.py", symlink_path + "/ogi")
    else:
        print("\nNo symlink created")


def setup_config_file(base_save_dir, dry_run=False):

    config = configparser.RawConfigParser()

    config.add_section('file_paths')
    config.set('file_paths', 'sql_path', '%(output_base)s/ogi_data.sqlite')
    config.set('file_paths', 'output_base', base_save_dir)

    config.set('file_paths', 'figures', '%(output_base)s/figures')
    config.set('file_paths', 'html', '%(output_base)s/ogi.html')

    setup_config_file_settings(config)
    ogi_base_dir = ogi_config.get_base_dir()
    conf_path = '{}/{}'.format(ogi_base_dir, 'ogi.conf')

    print("Writing config file to {}".format(conf_path))

    with open(conf_path, 'w') as config_fh:
        if not dry_run:
            config.write(config_fh)
        else:
            print(config)


def setup_config_file_settings(config):

    log_type_string = "\nWhat is your preferred default logging unit? pomo (25 minutes) or block (custom length): "
    chosen_log_type = prompt_utils.prompt_for_name(log_type_string, return_none_for_empty=True)

    if chosen_log_type not in ['pomo', 'block']:
        print("Only valid are 'pomo' and 'block', set to block for now")
        print("You can adjust this later by editing the ogi.conf configuration file")
        chosen_log_type = 'block'

    if chosen_log_type == 'block':
        block_length_string = "What duration should your default work session be? (default 40): "
        work_length = prompt_utils.prompt_for_string(block_length_string, default="40")
    else:
        work_length = '40'

    try:
        int(work_length)
    except ValueError:
        print("Block duration must be integer number! Set to default value.")
        print("You can adjust this later by editing the ogi.conf configuration file")
        work_length = '40'

    config.add_section('settings')
    config.set('settings', 'default_log_type', chosen_log_type)
    config.set('settings', 'block_duration', work_length)

    config.set('settings', 'project_mandatory', True)
    config.set('settings', 'message_mandatory', True)
    config.set('settings', 'work_type_mandatory', True)


def load_entries_from_tsvs(time_entry_tsv, project_tsv, category_tsv):

    with open(time_entry_tsv) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            time_entry = TimeEntry.load_from_string(line)
            database_utils.insert_time_entry_into_database(time_entry)

    with open(project_tsv) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            proj_entry = ProjectEntry.load_from_string(line)
            database_utils.insert_project_into_database(proj_entry)

    with open(category_tsv) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            cat_entry = CategoryEntry.load_from_string(line)
            database_utils.insert_category_into_database(cat_entry)


def setup_database():

    """Setup SQLite database with tables used by Ogi at path specified by config file"""

    print("Setting up database...")
    conf = ogi_config.get_config(force_reload=True)
    database_path = conf.get('file_paths', 'sql_path')
    database_utils.setup_database(database_path)
    print("Database written to {}".format(database_path))


def enter_tsvs_to_database(args):

    """Insert entries from tsv-files to database"""

    te = args.time_entries
    pe = args.project_entries
    ce = args.category_entries

    if te is not None and pe is not None and ce is not None:
        print("Loading previous entries from tsvs")
        load_entries_from_tsvs(te, pe, ce)

        time_entries = len(TimeEntry.get_time_entries())
        proj_entries = len(ProjectEntry.get_project_list())
        cat_entries = len(CategoryEntry.get_category_list())
        print("{} time entries, {} project entries and {} category entries loaded"
              .format(time_entries, proj_entries, cat_entries))
    else:
        print("You need to specify --time_entries, --project_entries and --category_entries"
              " to load data from TSV files")
        sys.exit(1)


