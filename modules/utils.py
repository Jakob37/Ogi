#!/usr/bin/env python3

from modules.time_entry import TimeEntry
from modules.project_entry import ProjectEntry


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


def prompt_yes_no(prompt_string):

    """Return True or False based on if user responds with yes or no"""

    # Empty string is counted as 'no'
    yes = {'yes', 'ye', 'y'}
    no = {'no', 'n', ''}

    while True:
    
        choice = input(prompt_string).lower()

        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Invalid response, try again")




