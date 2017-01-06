#!/usr/bin/env python3

import argparse
import re
import datetime
import configparser
import os
import sys


from modules.time_entry import TimeEntry
from modules import utils
from modules import ogi_new


def main(args, conf):

    if args.dry_run:
        print("DRY RUN - Simulated run, but nothing written")

    log_type = setup_log_type(conf, args.log_type)

    output_path = conf.get("file_paths", "data")
    project_path = conf.get("file_paths", "projects")
    category_path = conf.get("file_paths", "categories")

    time_entry = TimeEntry(conf,
                           log_type,
                           args.message,
                           args.focus,
                           args.date,
                           args.time,
                           args.project,
                           args.duration)

    project_exists = utils.check_project_exists(time_entry.project, project_path)
    if not project_exists:
        create_string = "{} does not exist, do you want to create it? ".format(time_entry.project)
        create_project = utils.prompt_yes_no(create_string)

        if not create_project:
            print("User aborted, try again")
            sys.exit(0)

        category = utils.prompt_for_name("What category? (Empty for uncategorized): ", default='uncategorized')

        if category is None:
            category = "uncategorized"

        ogi_new.new_project(project_path, category_path, category=category, project_name=time_entry.project)

    with open(output_path, 'a') as append_fh:

        if not args.dry_run:
            print(time_entry, file=append_fh)
        else:
            print("{}: {} to {}".format("Dry run", time_entry, output_path))

        print("Following entry written to {}".format(output_path))
        print(time_entry)


def setup_log_type(conf, args_log_type=None):

    if args_log_type is None:

        conf_log_type = conf.get('settings', 'default_log_type')
        print("Reading log type from config {}".format(conf_log_type))
        if conf_log_type not in TimeEntry.VALID_LOG_TYPES:
            raise Exception("Log type in config ({}) not valid log type ({})".format(conf_log_type, TimeEntry.VALID_LOG_TYPES))
        else:
            return conf_log_type
    else:
        return args_log_type
