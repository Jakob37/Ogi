#!/usr/bin/env python3

import sys

from modules.utils import prompt_utils
import ogi_config
from modules.entries.project_entry import ProjectEntry
from modules.entries.category_entry import CategoryEntry
from modules.database import database_utils


def main(args):

    conf = ogi_config.get_config()

    if args.dry_run:
        print("DRY RUN - Simulated run, but nothing written")

    if args.object_type == "project":
        new_project(args.name, args.category, dry_run=args.dry_run)

    elif args.object_type == "category":
        if args.category:
            print("--category flag ignored as it only is applicable for projects")

        new_category(args.name, dry_run=args.dry_run)


def new_project(project_name=None, category=None, dry_run=False):

    if project_name is None:
        proj_string = "Enter project name (empty to abort): "
        project_name = prompt_utils.prompt_for_name(proj_string)

    project_exists = ProjectEntry.check_project_exists(project_name)

    if project_exists:
        print("Project already exists! Try again with another name.")
        sys.exit(0)

    if category is None:
        cat_string = "Enter category for {} (empty for 'uncategorized'): ".format(project_name)
        category = prompt_utils.prompt_for_name(cat_string, default='uncategorized')

    cats = CategoryEntry.get_category_list()

    if category not in cats:

        create_cat_string = "Category does not exist, do you want to create it? "
        create_cat = prompt_utils.prompt_yes_no(create_cat_string, yes_default=True)

        if not create_cat:
            print("User aborted")
            sys.exit(0)

    new_category(category, silent_fail=True, dry_run=dry_run)
    write_new_project(project_name, category, dry_run=dry_run)


def write_new_project(project_name, category_name, dry_run=False):

    proj_entry = ProjectEntry(project_name, category_name)
    print("Adding project {} with category {}".format(project_name, category_name))
    out_string = "{}\t{}".format(project_name, category_name)

    if not dry_run:
        database_utils.insert_project_into_database(proj_entry)
    else:
        print("{}: {}".format("Dry run", out_string))


def new_category(category_name, dry_run=False, silent_fail=False):
    
    current_categories = database_utils.get_categories_as_strings()

    if category_name is None:
        cat_string = "Enter category name (empty to abort): "
        category_name = prompt_utils.prompt_for_name(cat_string)

    if category_name in current_categories:
        if not silent_fail:
            print("Category already exists!")
            sys.exit(0)
    else:
        print("Adding new category {}".format(category_name))

        if not dry_run:
            database_utils.insert_category_into_database(category_name)
        else:
            print("{}: {}".format("Dry run", category_name))


def get_categories(cat_path, use_sql=True):

    categories = list()

    if not use_sql:
        with open(cat_path) as in_fh:
            for line in in_fh:
                line = line.rstrip()
                categories.append(line)
    else:
        categories = database_utils.get_categories_as_strings()

    return categories


def print_categories(cat_path):

    categories = get_categories(cat_path)
    for cat in categories:
        print(cat)
