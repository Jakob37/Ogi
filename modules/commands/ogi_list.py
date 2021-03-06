#!/usr/bin/env python3

import sys

import ogi_config

from modules.utils import date_utils
from modules.entries.time_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry
from modules.entries.category_entry import CategoryEntry
from modules.entries.work_type_entry import WorkTypeEntry

from modules.utils import calc_utils


def main(args):

    if args.list_type == 'all':
        list_all()
        sys.exit(0)
    elif args.list_type == 'last':
        list_last(args.number)
        sys.exit(0)
    elif args.list_type == 'projects':
        list_projects()
        sys.exit(0)
    elif args.list_type == 'categories':
        list_categories()
        sys.exit(0)
    elif args.list_type == 'work_types':
        list_work_types()
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

    time_entries = TimeEntry.get_time_entries(start_date=start_date,
                                              end_date=end_date,
                                              project=args.project,
                                              work_type=args.work_type,
                                              category=args.category)

    print("Number time entries: {}".format(len(time_entries)))

    if args.summary:
        list_project_summary(time_entries, start_date, end_date, list_alpha=args.list_alpha)
    elif args.limited:
        list_date_range_entries_only(time_entries, start_date, end_date)
    else:
        list_date_range(start_date, end_date, args, list_alpha=args.list_alpha)


def list_all():

    categories = CategoryEntry.get_category_list()
    work_types = WorkTypeEntry.get_work_type_list()
    projects = ProjectEntry.get_project_list()

    cat_strs = sorted([cat.name for cat in categories])
    wt_strs = sorted([wt.name for wt in work_types])
    proj_strs = sorted([proj.name for proj in projects])

    print("--- Projects ---\n{}".format(" ".join(proj_strs)))
    print("--- Categories ---\n{}".format(" ".join(cat_strs)))
    print("--- Work types ---\n{}".format(" ".join(wt_strs)))


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


def list_project_summary(time_entries, start_date, end_date, list_alpha=False):

    proj_dict = dict()
    total_duration = 0
    for entry in time_entries:
        if proj_dict.get(entry.project) is None:
            proj_dict[entry.project] = entry.duration
        else:
            proj_dict[entry.project] += entry.duration
        total_duration += entry.duration

    homogeneity = calc_utils.calculate_homogeneity_measure(start_date=start_date, end_date=end_date)

    print("Project summary for date range {} to {}".format(start_date, end_date))
    print("Total time spent: {}".format(date_utils.get_nice_time_string(total_duration)))
    print("Time period homogeneity: {:.3f}".format(homogeneity))
    print("\nProjects\tTime".expandtabs(20))
    print("-" * 30)

    if not list_alpha:
        def sort_func(x): return proj_dict[x]
    else:
        def sort_func(x): return x

    for proj in sorted(proj_dict, key=sort_func, reverse=not list_alpha):
        time = proj_dict[proj]
        time_string = date_utils.get_nice_time_string(time)
        print('{}\t{}'.format(proj, time_string).expandtabs(20))


def list_date_range(start_date, end_date, args, list_alpha=False):

    print("Logged entries in date range {} to {}".format(start_date, end_date))

    if args.project is None and args.category is None:
        projects = ProjectEntry.get_project_list()
    elif args.category is None:
        projects = [ProjectEntry.get_project_with_name(args.project)]
    else:
        projects = ProjectEntry.get_project_list(filter_category=args.category)

    if not list_alpha:
        def sort_func(x): return x.get_total_time(start_date, end_date, work_type=args.work_type)
    else:
        def sort_func(x): return x.name

    for proj in sorted(projects, key=sort_func, reverse=not list_alpha):

        if proj.get_total_time(start_date, end_date, work_type=args.work_type) > 0:
            proj_tot_time = date_utils.get_nice_time_string(proj.get_total_time(start_date, end_date,
                                                                                work_type=args.work_type))
            print("Project: {} ({})".format(proj.name, proj_tot_time))
            time_entries = proj.get_entries(start_date, end_date, work_type=args.work_type)

            print_time_sorted_entries(time_entries)


def list_date_range_entries_only(time_entries, start_date, end_date):

    """Output list of entries within target range, without grouping on project"""

    print("Logged entries in date range {} to {}".format(start_date, end_date))
    print_time_sorted_entries(time_entries)


def list_last(number=None):

    if number is None:
        number = 1

    time_entries = TimeEntry.get_time_entries()
    print_time_sorted_entries(time_entries, last_n=number)


def print_time_sorted_entries(time_entries, last_n=None):

    """Output given list of time entries in time sorted format"""

    print_strings = list()

    for entry in sorted(time_entries, key=lambda x: x.date + x.time):
        nice_time = date_utils.get_nice_time_string(entry.duration)
        print_strings.append("* {}\t{}\t{}\t{}".format(nice_time, entry.date, entry.time, entry.message).expandtabs(10))

    if last_n is not None:
        print_strings = print_strings[-last_n:]

    for print_string in print_strings:
        print(print_string)


def list_projects():

    project_list = ProjectEntry.get_project_list()

    print('{}\t{}\t{}'.format('Project', 'Category', 'Spent time').expandtabs(20))
    print('-' * 50)

    for proj in sorted(project_list, key=lambda x: x.get_total_time(), reverse=True):
        time_string = date_utils.get_nice_time_string(proj.get_total_time())
        print("{}\t{}".format(str(proj), time_string).expandtabs(20))


def list_categories():

    category_list = CategoryEntry.get_category_list()

    print('{}\t{}'.format('Category', 'Spent time'))
    print('-' * 50)

    for cat in sorted(category_list, key=lambda x: x.get_total_time(), reverse=True):
        time_string = date_utils.get_nice_time_string(cat.get_total_time())
        print("{}\t{}".format(cat.name, time_string).expandtabs(20))


def list_work_types():

    wt_list = WorkTypeEntry.get_work_type_list()

    print('{}\t{}'.format('Work type', 'Spent time').expandtabs(20))
    print('-' * 50)

    for wt in sorted(wt_list, key=lambda x: x.get_total_time(), reverse=True):
        time_string = date_utils.get_nice_time_string(wt.get_total_time())
        print("{}\t{}".format(wt.name, time_string).expandtabs(20))
