#!/usr/bin/env python3

from modules.database import database_utils
from modules.entries.project_entry import ProjectEntry


class CategoryEntry:

    def __init__(self, name):

        self.name = name

    def __str__(self):

        return '{name}'.format(name=self.name)

    @classmethod
    def load_from_string(cls, cat_string):

        """Generate object from tab-delimited string"""

        fields = cat_string.split('\t')
        category_name = fields[0]
        new_obj = cls(category_name)
        return new_obj

    @staticmethod
    def get_category_list():

        categories = [CategoryEntry(cat_str) for cat_str in database_utils.get_categories_as_strings()]
        return categories

    def get_total_time(self):

        projs = ProjectEntry.get_project_list(filter_category=self.name)
        return sum([proj.get_total_time() for proj in projs])
