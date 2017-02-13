#!/usr/bin/env python3

from modules.database import database_utils

from modules.entries.time_entry import TimeEntry


class WorkTypeEntry:

    def __init__(self, name):

        self.name = name
        self.entries = []

    def __str__(self):

        return '{name}'.format(name=self.name)

    def load_entries(self):
        self.entries = TimeEntry.get_time_entries(work_type=self.name)

    @classmethod
    def load_from_string(cls, work_type_string):

        """Generate object from tab-delimited string"""

        fields = work_type_string.split('\t')
        work_type_name = fields[0]
        new_obj = cls(work_type_name)
        return new_obj

    @staticmethod
    def check_work_type_exists(work_type_name):

        work_types = WorkTypeEntry.get_work_type_list()
        work_type_names = [w.name for w in work_types]
        return work_type_name in work_type_names

    @staticmethod
    def get_work_type_list():

        work_type_strings = database_utils.get_work_types_as_strings()
        work_types = [WorkTypeEntry(string) for string in work_type_strings]
        return work_types

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
