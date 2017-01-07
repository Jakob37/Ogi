#!/usr/bin/env python3

import datetime

import ogi_config

from modules.utils import utils


def main(args):

    conf = ogi_config.get_config()
    output_path = conf.get("file_paths", "data")
    time_entries = utils.parse_log_to_entries(output_path)

    if args.list_type == "project_summary":
        list_project_summary(time_entries)
    elif args.list_type == "today":
        list_day(time_entries)
    elif args.list_type == "projects":
        list_projects(conf)
    elif args.list_type == "categories":
        list_categories(conf)
    else:
        print("Unknown list type: {}".format(args.list_type))


def list_project_summary(time_entries):

    proj_dict = dict()

    for entry in time_entries:
        if proj_dict.get(entry.project) is None:
            proj_dict[entry.project] = entry.duration
        else:
            proj_dict[entry.project] += entry.duration

    print("Logged projects")
    print("Projects\tTime".expandtabs(20))
    print("-" * 30)
    for proj in sorted(proj_dict, key=lambda x: proj_dict[x], reverse=True):
        print("{0}\t{1}".format(proj, proj_dict[proj]).expandtabs(20))


def list_day(time_entries):

    day_dict = dict()

    today = "{0:%Y%m%d}".format(datetime.datetime.now())

    for entry in time_entries:
        
        if entry.date == today:
            if day_dict.get(entry.project) is None:
                day_dict[entry.project] = [(entry.message, entry.duration, entry.date)]
            else:
                day_dict[entry.project].append((entry.message, entry.duration, entry.date))

    print("Logged today")
    for proj in sorted(day_dict):

        if len(day_dict[proj]) == 0:
            continue

        print("Project: {}".format(proj))

        for entry in day_dict[proj]:
            message = entry[0]
            duration = entry[1]
            date = entry[2]

            if date == "{0:%Y%m%d}".format(datetime.datetime.now()):

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
