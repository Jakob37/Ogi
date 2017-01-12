#!/usr/bin/env python3

"""
Main class representing a project entry
"""

# from modules.utils import utils
import ogi_config

from modules.entries.time_entry import TimeEntry
from modules.database import database_utils


class ProjectEntry:

    def __init__(self, name, category=None):
        
        self.conf = ogi_config.get_config()
        self.name = name
        self.category = category
        self.entries = []

    def load_entries(self, entry_path):
        self.entries = TimeEntry.parse_log_to_entries(entry_path, project=self.name)

    @staticmethod
    def parse_log_to_projects(log_path, use_sql=True):

        """Return list of project objects based on log path"""

        projects = list()

        project_str = list()
        if not use_sql:
            with open(log_path) as in_fh:
                for line in in_fh:
                    line = line.rstrip()
                    project_str.append(line)
        else:
            project_str = database_utils.get_projects_as_strings()

        for line in project_str:
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
