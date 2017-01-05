#/usr/bin/env python3

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

    output_path = conf.get("file_paths", "data")
    test_output_path = conf.get("file_paths", "test_data")
    project_path = conf.get("file_paths", "projects")
    category_path = conf.get("file_paths", "categories")

    time_entry = TimeEntry(args.log_type, 
                           args.message,
                           args.focus,
                           args.date,
                           args.time,
                           args.project,
                           args.duration)


    if not args.testrun:

        project_exists = utils.check_project_exists(time_entry, project_path)
        if not project_exists:
            create_string = "{} does not exist, do you want to create it? [y/N]: ".format(time_entry.project)
            create_project = utils.prompt_yes_no(create_string)

            if not create_project:
                print("User aborted, try again")
                sys.exit(0)

            category = input("What category? (Empty for uncategorized): ")

            if category is None:
                category = "uncategorized"

            ogi_new.new_project(project_path, category_path, category, time_entry.project)

        with open(output_path, 'a') as append_fh:
            print(time_entry, file=append_fh)
            print("Following entry written to {}".format(output_path))
            print(time_entry)
    else:
        print("Test entry written")
        print(time_entry)
        with open(test_output_path, 'a') as append_fh:
            print(time_entry, file=append_fh)


#def check_project_exists(project_name, project_path):
#
#    """Check whether project exists, if no, prompt whether it should be added"""
#
#    project_entries = utils.parse_log_to_projects(project_path)
#
#    project_names = [project.name for project in project_entries]
#    return project_name in project_names


