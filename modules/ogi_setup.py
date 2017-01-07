#!/usr/bin/env python3

import os
import sys
import configparser

import ogi_config
from modules.utils import prompt_utils

DRY_RUN = False


def main(args):

    if args.dry_run:
        print("DRY RUN - Simulated run, but nothing written")

    global DRY_RUN
    DRY_RUN = args.dry_run

    check_config_exists()

    save_base_dir = get_save_directory()
    ensure_dir(save_base_dir)

    create_synlink()

    setup_config_file(save_base_dir)

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
                       "If you are planning on using Ogi on multiple devices, it is recommended" \
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


def create_synlink():

    symlink_message = "\nProvide directory for symlink for easy access to 'ogi' command. " \
                      "Leave empty if not desired.\nSymlink path: "

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
    config.set('file_paths', 'data_base', base_save_dir)
    config.set('file_paths', 'data', '%(data_base)s/ogi_data.tsv')
    config.set('file_paths', 'projects', '%(data_base)s/projects.tsv')
    config.set('file_paths', 'categories', '%(data_base)s/categories.tsv')

    config.add_section('settings')
    config.set('settings', 'default_log_type', 'block')
    config.set('settings', 'block_duration', '40')

    conf_path = '{}/{}'.format(base_save_dir, 'ogi.conf')

    print("Writing config file to {}".format(conf_path))

    with open(conf_path, 'w') as config_fh:
        if not dry_run:
            config.write(config_fh)
        else:
            print(config)
