#!/usr/bin/env python3

from modules.database import database_utils


class CategoryEntry:

    def __init(self, name):

        self.name = name

    def __str__(self):

        return '{name}'.format(name=self.name)

    @staticmethod
    def get_category_list():

        categories = database_utils.get_categories_as_strings()
        return categories
