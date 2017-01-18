#!/usr/bin/env python3

import sys

import ogi_config
from modules.commands import ogi_new
from modules.entries.time_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry
from modules.utils import prompt_utils
from modules.database import database_utils


def main(args):

    conf = ogi_config.get_config()

    if args.dry_run:
        print("DRY RUN - Simulated run, but nothing written")

    log_type = setup_log_type(conf, args.log_type)

    time_entry = TimeEntry(log_type,
                           args.message,
                           args.focus,
                           args.date,
                           args.time,
                           args.project,
                           args.duration)

    print("Ready to attempt writing time entry")

    write_time_entry(time_entry, conf, write_to_database=True, dry_run=args.dry_run)

    print("Entry written, done for now (fix before merging back into master)")

    project_exists = ProjectEntry.check_project_exists(time_entry.project)
    if not project_exists:
        create_string = "{} does not exist, do you want to create it? ".format(time_entry.project)
        create_project = prompt_utils.prompt_yes_no(create_string, yes_default=True)

        if not create_project:
            print("User aborted, try again")
            sys.exit(0)

        category = prompt_utils.prompt_for_name("What category? (Empty for uncategorized): ", default='uncategorized')

        if category is None:
            category = "uncategorized"

        ogi_new.new_project(category=category, project_name=time_entry.project)


def setup_log_type(conf, args_log_type=None):

    if args_log_type is None:

        conf_log_type = conf.get('settings', 'default_log_type')
        print("Reading log type from config {}".format(conf_log_type))
        if conf_log_type not in TimeEntry.VALID_LOG_TYPES:
            raise Exception("Log type in config ({}) not valid log type ({})"
                            .format(conf_log_type, TimeEntry.VALID_LOG_TYPES))
        else:
            return conf_log_type
    else:
        return args_log_type


def write_time_entry(time_entry, conf, write_to_database=False, dry_run=False):

    if not write_to_database:

        output_path = conf.get('file_paths', 'sql_path')
        with open(output_path, 'a') as append_fh:

            if not dry_run:
                print(time_entry, file=append_fh)
            else:
                print("{}: {} to {}".format("Dry run", time_entry, output_path))

            print("Following entry written to {}".format(output_path))
            print(time_entry)
    else:

        print("In write_time_entry")

        database_utils.insert_time_entry_into_database(time_entry)

