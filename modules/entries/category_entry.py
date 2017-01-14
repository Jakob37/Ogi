#!/usr/bin/env python3

from modules.database import database_utils


class CategoryEntry:

    def __init(self, name):

        self.name = name

    def __str__(self):

        return '{name}'.format(name=self.name)

    @staticmethod
    def parse_log_to_categories(category_log_path, use_sql=True):

        categories = list()

        if not use_sql:
            with open(category_log_path) as in_fh:
                for line in in_fh:
                    line = line.rstrip()
                    categories.append(line)
        else:
            categories = database_utils.get_categories_as_strings()

        return categories
