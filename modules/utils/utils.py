#!/usr/bin/env python3

import datetime

# from modules.entries.project_entry import ProjectEntry
# from modules.entries.time_entry import TimeEntry


# def parse_log_to_entries(log_path, project=None, start_date=None, end_date=None):
#
#     """Return list of entries based on log file"""
#
#     time_entries = list()
#
#     with open(log_path) as in_fh:
#         for line in in_fh:
#             line = line.rstrip()
#
#             entry = TimeEntry.load_from_string(line)
#             if project is None or project == entry.project:
#
#                 if is_date_in_range(entry.date, start_date, end_date):
#                     time_entries.append(entry)
#
#     return time_entries


# def parse_log_to_projects(log_path):
#
#     """Return list of project objects based on log path"""
#
#     projects = list()
#
#     with open(log_path) as in_fh:
#         for line in in_fh:
#             line = line.rstrip()
#
#             project, category = line.split('\t')
#             proj_entry = ProjectEntry(project, category)
#
#             projects.append(proj_entry)
#     return projects


# def check_project_exists(project_name, project_path):
#
#     project_entries = ProjectEntry.parse_log_to_projects(project_path)
#     project_names = [project.name for project in project_entries]
#
#     return project_name in project_names


def get_current_date():

    return "{0:%Y%m%d}".format(datetime.datetime.now())


def get_previous_date(number_days_previous):

    today = datetime.datetime.now()
    delta = datetime.timedelta(days=number_days_previous)
    previous_day = today - delta

    return "{0:%Y%m%d}".format(previous_day)


def is_date_in_range(target, start=None, end=None, debug=False):

    if start:
        in_start_range = int(target) >= int(start)
    else:
        in_start_range = True

    if end:
        in_end_range = int(target) <= int(end)
    else:
        in_end_range = True

    if debug:
        print("{} in [{} {}] - {}/{}".format(target, start, end, in_start_range, in_end_range))

    return in_start_range and in_end_range


def is_today_in_range(start, end):

    today = get_current_date()
    return is_date_in_range(today, start, end)
