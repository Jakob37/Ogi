#!/usr/bin/env python3

from modules.database import database_utils


class WorkTypeEntry:

    def __init__(self, name):

        self.name = name

    def __str__(self):

        return '{name}'.format(name=self.name)

    @classmethod
    def load_from_string(cls, work_type_string):

        """Generate object from tab-delimited string"""

        fields = work_type_string.split('\t')
        work_type_name = fields[0]
        new_obj = cls(work_type_name)
        return new_obj

    @staticmethod
    def get_work_type_list():

        work_types = database_utils.get_work_types_as_strings()
        return work_types
