#!/usr/bin/env python3

"""
Main class representing a project entry
"""

import modules.utils


class ProjectEntry:

    def __init__(self, conf, name, category=None):
        
        self.conf = conf
        self.name = name
        self.category = category
        self.entries = []

    def load_entries(self, entry_path):
        self.entries = modules.utils.parse_log_to_entries(self.conf, entry_path, project=self.name)

    def get_total_time(self):

        time_entries = [entry.duration for entry in self.entries]
        return sum(time_entries)

    def __str__(self):

        return '{name}\t{category}'.format(name=self.name, category=self.category)
