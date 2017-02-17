#!/usr/bin/env python3

import sys
import re

import ogi_config
from modules.commands import ogi_new
from modules.entries.time_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry
from modules.entries.work_type_entry import WorkTypeEntry
from modules.utils import prompt_utils
from modules.database import database_utils
from modules.commands import ogi_edit


def main(args):

    conf = ogi_config.get_config()

    if args.dry_run:
        print("DRY RUN - Simulated run, but nothing written")

    parse_log_type = setup_log_type(conf, args.log_type)

    if args.override_last:
        ogi_edit.amend_last_entry(dry_run=args.dry_run)

    if parse_log_type == 'custom_session':
        log_type = 'session'
        duration = int(args.log_type)
    else:
        log_type = parse_log_type
        duration = args.duration

    time_entry = TimeEntry(log_type,
                           args.message,
                           focus=args.focus,
                           date_str=args.date,
                           time_str=args.time,
                           project=args.project,
                           duration=duration,
                           work_type=args.work_type)

    check_project(time_entry, dry_run=args.dry_run)
    check_work_type(time_entry, dry_run=args.dry_run)

    if not args.dry_run:
        write_time_entry(time_entry, conf, write_to_database=True, dry_run=args.dry_run)
    else:
        print("Dry run, would write {}".format(time_entry))


def check_project(time_entry, dry_run=False):

    project_exists = ProjectEntry.check_project_exists(time_entry.project)
    if not project_exists:
        create_string = "Project {} does not exist, do you want to create it? ".format(time_entry.project)
        create_project = prompt_utils.prompt_yes_no(create_string, yes_default=True)

        if not create_project:
            print("User aborted, try again")
            sys.exit(0)

        category = prompt_utils.prompt_for_name("What category? (Empty for uncategorized): ", default='uncategorized')

        if category is None:
            category = "uncategorized"

        if not dry_run:
            ogi_new.new_project(category=category, project_name=time_entry.project, print_current=True)
        else:
            print("Dry run, would write project {} with category {}".format(time_entry.project, category))


def check_work_type(time_entry, dry_run=False):

    """Verify whether assigned work type exists, and if not, ask if it should be added"""

    worktype_exists = WorkTypeEntry.check_work_type_exists(time_entry.work_type)
    if not worktype_exists:
        create_string = "Work type \"{}\" does not exist, do you want to create it? ".format(time_entry.work_type)

        current_worktypes = WorkTypeEntry.get_work_type_list()
        print("Existing categories: {}".format(" ".join([wt.name for wt in current_worktypes])))
        create_wt = prompt_utils.prompt_yes_no(create_string, yes_default=True)

        if not create_wt:
            print("User aborted, try again")
            sys.exit(0)

        if not dry_run:
            ogi_new.new_work_type(work_type_name=time_entry.work_type)
        else:
            print("Dry run, would write work type {}".format(time_entry.work_type))


def setup_log_type(conf, args_log_type=None):

    int_pattern = r'\d+'
    exception_string = "Log type in config \"{{}}\" not valid log type. " \
                       "Valid types are {valid_types} or numeric (i.e. \"15\")"\
        .format(valid_types=str(", ".join(TimeEntry.VALID_LOG_TYPES)))

    if args_log_type is None:

        conf_log_type = conf.get('settings', 'default_log_type')

        if conf_log_type not in TimeEntry.VALID_LOG_TYPES:
            raise Exception(exception_string.format(conf_log_type))
        else:
            return conf_log_type
    else:
        if re.match(int_pattern, str(args_log_type)):
            return 'custom_session'
        elif args_log_type not in TimeEntry.VALID_LOG_TYPES:
            raise Exception(exception_string.format(args_log_type))
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
        print('Writing new time entry to project "{}" at time {} with message "{}" and work type "{}"'
              .format(time_entry.project, time_entry.time, time_entry.message, time_entry.work_type))
        database_utils.insert_time_entry_into_database(time_entry)
