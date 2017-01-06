#!/usr/bin/env python3

import sys
import os
import configparser

from modules.time_entry import TimeEntry
from modules.project_entry import ProjectEntry

# CONF_NAME = 'ogi.conf'


def parse_log_to_entries(log_path, project=None):

    """Return list of entries based on log file"""

    time_entries = list()

    with open(log_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()

            entry = TimeEntry.load_from_string(line)
            if project is None or project == entry.project:
                time_entries.append(entry)

    return time_entries


def parse_log_to_projects(log_path):

    """Return list of project objects based on log path"""
    
    projects = list()

    with open(log_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()

            project, category = line.split('\t')
            proj_entry = ProjectEntry(project, category)

            projects.append(proj_entry)
    return projects


def check_project_exists(project_name, project_path):

    project_entries = parse_log_to_projects(project_path)
    project_names = [project.name for project in project_entries]

    return project_name in project_names


def prompt_yes_no(prompt_string, yes_default=False):

    """Return True or False based on if user responds with yes or no"""

    # Empty string is counted as 'no'
    yes = {'yes', 'ye', 'y'}
    no = {'no', 'n'}

    if yes_default:
        yes.add('')
        yes_no_string = '[Y/n] '
    else:
        no.add('')
        yes_no_string = '[y/N] '

    while True:
        choice = input(prompt_string + yes_no_string).lower()

        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Invalid response, try again")


def prompt_for_name(prompt_string, default=None, prompt_confirmation=False):

    """Ask user to provide name, or leave empty to abort"""

    while True:

        choice = input(prompt_string)

        if choice == '':
            if default is None:
                print("User aborted")
                sys.exit(0)
            else:
                choice = default

        if prompt_confirmation:

            yes_no_string = "{}, is that correct? ".format(choice)
            yes_answer = prompt_yes_no(yes_no_string, yes_default=True)

            if not yes_answer:
                print("No name provided, try again")
                sys.exit(0)

        return choice

