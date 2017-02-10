#!/usr/bin/env python3

"""
Main class representing a project entry
"""

import sys

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

    @classmethod
    def load_from_string(cls, project_string):

        """Generate object from tab-delimited string"""

        fields = project_string.split('\t')
        project_name = fields[0]
        category = fields[1]
        new_obj = cls(project_name, category=category)
        return new_obj

    def load_entries(self):
        self.entries = TimeEntry.get_time_entries(project=self.name)

    def get_entries(self, start_date=None, end_date=None):
        if len(self.entries) == 0:
            self.load_entries()

        if start_date is None:
            start_date = "0000000000"

        if end_date is None:
            end_date = "9999999999"

        filtered_list = [entry for entry in self.entries if start_date <= entry.date <= end_date]
        return filtered_list

    @staticmethod
    def get_project_list():

        projects = list()
        project_str = database_utils.get_projects_as_strings()

        for line in project_str:
            project, category = line.split('\t')
            proj_entry = ProjectEntry(project, category)

            projects.append(proj_entry)

        return projects

    @staticmethod
    def get_project_with_name(proj_name):

        projects = ProjectEntry.get_project_list()
        for proj in projects:
            if proj.name == proj_name:
                return proj
        print("Failed to find project: {}".format(proj_name))
        sys.exit(1)

    @staticmethod
    def check_project_exists(project_name):

        project_entries = ProjectEntry.get_project_list()
        project_names = [project.name for project in project_entries]

        return project_name in project_names

    def get_total_time(self, start_date=None, end_date=None, in_hours=False):

        if len(self.entries) == 0:
            self.load_entries()

        if start_date is None:
            start_date = '00000000'

        if end_date is None:
            end_date = '99999999'

        time_entries = list()
        for entry in self.entries:
            if start_date <= entry.date <= end_date:
                time_entries.append(entry)

        minutes = sum([entry.duration for entry in time_entries])

        if in_hours:
            return float("{0:.2f}".format(minutes / 60))
        else:
            return minutes

    def __str__(self):
        return self.str(delim="\t")

    def str(self, delim="\t"):

        return '{name}{delim}{category}'.format(name=self.name,
                                                delim=delim, category=self.category)
