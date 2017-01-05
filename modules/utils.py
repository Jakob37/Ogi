#!/usr/bin/env python3

from modules.time_entry import TimeEntry


def parse_log_to_entries(log_path, project=None):

    """Return list of entries based on log file"""

    time_entries = list()
    header = None

    with open(log_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()

            if header == None:
                header = line
                continue

            entry = TimeEntry.load_from_string(line)
            if project is None or project == entry.project:
                time_entries.append(entry)
            

    return time_entries


def prompt_yes_no(prompt_string):

    """Return True or False based on if user responds with yes or no"""

    # Empty string is counted as 'no'
    yes = set(['yes', 'ye', 'y'])
    no = set(['no', 'n', ''])

    while True:
    
        choice = input(prompt_string).lower()

        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Invalid response, try again")




