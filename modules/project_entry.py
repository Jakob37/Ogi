#!/usr/bin/env python3

"""
Main class representing a project entry
"""

from modules import utils

class ProjectEntry:

    def __init__(self, name, category=None):
        

        self.name = name
        self.category = category


    def load_entries(entry_path):
        
        all_entries = utils.parse_log_to_entries(entry_path, project=self.name)





