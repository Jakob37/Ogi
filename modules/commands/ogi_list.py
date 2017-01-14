#!/usr/bin/env python3

import sys

import ogi_config

from modules.utils import utils
from modules.entries.project_entry import TimeEntry


def main(args):

    conf = ogi_config.get_config()
    output_path = conf.get("file_paths", "data")

    print("Path: " + output_path)

    if args.list_type == 'projects':
        list_projects(conf)
    elif args.list_type == 'categories':
        list_categories(conf)
    elif args.list_type == 'date_range':

        if not args.start_date:
            print("If date_range is specified you must provide --start_date and possibly --end_date (default today)")
            print("Format: ogi list date_range --start_date 170101 --end_date 170107")
            sys.exit(0)

    if args.start_date:
        start_date = args.start_date
    else:
        start_date = get_date_range_start(args)

    if args.end_date:
        end_date = args.end_date
    else:
        end_date = utils.get_current_date()

    time_entries = TimeEntry.parse_log_to_entries(output_path, start_date=start_date, end_date=end_date)

    print("Number time entries: {}".format(len(time_entries)))

    if args.summary:
        list_project_summary(time_entries, start_date, end_date)
    else:
        list_date_range(time_entries, start_date, end_date)


def get_date_range_start(args):

    current_date = utils.get_current_date()

    if args.list_type == 'day':
        return current_date
    elif args.list_type == 'week':
        return utils.get_previous_date(6)
    elif args.list_type == 'month':
        return utils.get_previous_date(29)
    elif args.list_type == 'year':
        return utils.get_previous_date(364)
    else:
        print("Unknown list type: {}".format(args.list_type))
        sys.exit(1)


def list_project_summary(time_entries, start_date, end_date):

    proj_dict = dict()

    for entry in time_entries:
        if proj_dict.get(entry.project) is None:
            proj_dict[entry.project] = entry.duration
        else:
            proj_dict[entry.project] += entry.duration

    print("Project summary for date range {} to {}".format(start_date, end_date))
    print("Projects\tTime".expandtabs(20))
    print("-" * 30)
    for proj in sorted(proj_dict, key=lambda x: proj_dict[x], reverse=True):
        print("{0}\t{1}".format(proj, proj_dict[proj]).expandtabs(20))


def list_date_range(time_entries, start_date, end_date):

    target_entries_dict = dict()

    print("Logged entries in date range {} to {}".format(start_date, end_date))

    for entry in time_entries:
        
        if target_entries_dict.get(entry.project) is None:
            target_entries_dict[entry.project] = [(entry.message, entry.duration, entry.date)]
        else:
            target_entries_dict[entry.project].append((entry.message, entry.duration, entry.date))

    for proj in sorted(target_entries_dict):

        if len(target_entries_dict[proj]) == 0:
            continue

        print("Project: {}".format(proj))

        for entry in target_entries_dict[proj]:
            message = entry[0]
            duration = entry[1]
            date = entry[2]

            print("* {} ({} minutes)".format(message, duration))


def list_projects(conf):

    proj_path = conf.get("file_paths", "projects")
    print("Projects currently saved in: {}".format(proj_path))

    with open(proj_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            print(line)


def list_categories(conf):

    cat_path = conf.get("file_paths", "categories")
    print("Categories currently saved in: {}".format(cat_path))

    with open(cat_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            print(line)
