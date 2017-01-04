#/usr/bin/env python3

from modules.time_entry import TimeEntry


def parse_log_to_entries(log_path):

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
            time_entries.append(entry)

    return time_entries


