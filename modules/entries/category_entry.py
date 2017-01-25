#!/usr/bin/env python3

from modules.database import database_utils


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

        categories = database_utils.get_categories_as_strings()
        return categories
