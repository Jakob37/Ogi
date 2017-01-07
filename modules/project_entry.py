#!/usr/bin/env python3

"""
Main class representing a project entry
"""

from modules.utils import utils
import ogi_config


class ProjectEntry:

    def __init__(self, name, category=None):
        
        self.conf = ogi_config.get_config()
        self.name = name
        self.category = category
        self.entries = []

    def load_entries(self, entry_path):
        self.entries = utils.parse_log_to_entries(entry_path, project=self.name)

    def get_total_time(self):

        time_entries = [entry.duration for entry in self.entries]
        return sum(time_entries)

    def __str__(self):

        return '{name}\t{category}'.format(name=self.name, category=self.category)
