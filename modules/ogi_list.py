#!/usr/bin/env python3

import datetime

def main(args, conf):

    output_path = conf.get("file_paths", "data")

    proj_dict = dict()
    day_dict = dict()

    header_line = None

    with open(output_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            
            if header_line is None:
                header_line = line
                continue

            fields = line.split('\t')

            date = fields[0]
            time = fields[1]
            log_type = fields[2]
            focus = fields[3]
            duration = int(fields[4])
            message = fields[5]
            project = fields[6]
            
            if proj_dict.get(project) is None:
                proj_dict[project] = duration
                day_dict[project] = [(message, duration, date)]
                
            else:
                proj_dict[project] += duration
                day_dict[project].append((message, duration, date))

    if args.list_type == "project":
        list_projects(proj_dict)
    elif args.list_type == "today":
        list_day(day_dict)
    else:
        print("Unknown list type: {}".format(args.list_type))


def list_projects(proj_dict):

    print("Logged projects")
    print("Projects\tTime")
    for proj in sorted(proj_dict, key=lambda x:proj_dict[x], reverse=True):
        print("{}\t{}".format(proj, proj_dict[proj]))

def list_day(day_dict):

    print("Logged today")
    print("Project", "Entries")

    for proj in sorted(day_dict):

        if len(day_dict[proj]) == 0:
            continue

        print("> Project: {}".format(proj))

        for entry in day_dict[proj]:
            message = entry[0]
            duration = entry[1]
            date = entry[2]

            if date == "{0:%Y%m%d}".format(datetime.datetime.now()):


                print("{} ({} minutes)".format(message, duration))


