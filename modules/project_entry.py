#!/usr/bin/env python3

"""
Main class representing a project entry
"""

from modules import utils

class ProjectEntry:

    def __init__(self, name, category=None):
        

        self.name = name
        self.category = category
        self.entries = []

    def load_entries(self, entry_path):
        
         self.entries = utils.parse_log_to_entries(entry_path, project=self.name)


    def get_total_time(self):

        time_entries = [entry.duration for entry in self.entries]
        return sum(time_entries)


    def __str__(self):

        return '{name}\t{category}'.format(self.name, self.total_time, self.category)

