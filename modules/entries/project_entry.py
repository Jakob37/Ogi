#!/usr/bin/env python3

"""
Main class representing a project entry
"""

# from modules.utils import utils
import ogi_config

from modules.entries.time_entry import TimeEntry


class ProjectEntry:

    def __init__(self, name, category=None):
        
        self.conf = ogi_config.get_config()
        self.name = name
        self.category = category
        self.entries = []

    def load_entries(self, entry_path):
        self.entries = TimeEntry.parse_log_to_entries(entry_path, project=self.name)

    @staticmethod
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

    @staticmethod
    def check_project_exists(project_name, project_path):

        project_entries = ProjectEntry.parse_log_to_projects(project_path)
        project_names = [project.name for project in project_entries]

        return project_name in project_names

    def get_total_time(self):

        time_entries = [entry.duration for entry in self.entries]
        return sum(time_entries)

    def __str__(self):

        return '{name}\t{category}'.format(name=self.name, category=self.category)
