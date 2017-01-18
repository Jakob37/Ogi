#!/usr/bin/env python3

import sys

import ogi_config

from modules.utils import date_utils
from modules.entries.project_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry
from modules.entries.category_entry import CategoryEntry


def main(args):

    if args.list_type == 'projects':
        list_projects()
        sys.exit(0)
    elif args.list_type == 'categories':
        list_categories()
        sys.exit(0)
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
        end_date = date_utils.get_current_date()

    time_entries = TimeEntry.parse_log_to_entries(start_date=start_date, end_date=end_date)

    print("Number time entries: {}".format(len(time_entries)))

    if args.summary:
        list_project_summary(time_entries, start_date, end_date)
    else:
        list_date_range(time_entries, start_date, end_date)


def get_date_range_start(args):

    current_date = date_utils.get_current_date()

    if args.list_type == 'day':
        return current_date
    elif args.list_type == 'week':
        return date_utils.get_start_of_week()
    elif args.list_type == 'prev_days':

        if not args.number:
            print("prev_days option requires you to specify --number or -n flag")
            sys.exit(1)

        return date_utils.get_previous_date(args.number)
    elif args.list_type == 'month':
        return date_utils.get_start_of_month()
    elif args.list_type == 'year':
        return date_utils.get_start_of_year()
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

        time = proj_dict[proj]
        time_string = date_utils.get_nice_time_string(time)
        print('{}\t{}'.format(proj, time_string).expandtabs(20))


def list_date_range(time_entries, start_date, end_date):

    target_entries_tuples_dict = dict()

    print("Logged entries in date range {} to {}".format(start_date, end_date))

    for entry in time_entries:
        
        if target_entries_tuples_dict.get(entry.project) is None:
            target_entries_tuples_dict[entry.project] = [(entry.message, entry.duration, entry.date)]
        else:
            target_entries_tuples_dict[entry.project].append((entry.message, entry.duration, entry.date))

    for proj in sorted(target_entries_tuples_dict):

        if len(target_entries_tuples_dict[proj]) == 0:
            continue

        print("Project: {}".format(proj))

        for entry in target_entries_tuples_dict[proj]:
            message = entry[0]
            duration = entry[1]
            date = entry[2]

            print("* {} ({} minutes)".format(message, duration))


def list_projects():

    project_list = ProjectEntry.get_project_list()

    print('{}\t{}\t{}'.format('Project', 'Category', 'Spent time').expandtabs(20))
    print('-' * 50)

    for proj in sorted(project_list, key=lambda x: x.get_total_time(), reverse=True):
        time_string = date_utils.get_nice_time_string(proj.get_total_time())
        print("{}\t{}".format(str(proj), time_string).expandtabs(20))


def list_categories():

    print("list_categories")

    category_list = CategoryEntry.get_category_list()

    print(category_list)

    for cat in category_list:
        print(cat)

