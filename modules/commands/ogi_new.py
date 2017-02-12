#!/usr/bin/env python3

import sys

from modules.utils import prompt_utils
import ogi_config
from modules.entries.project_entry import ProjectEntry
from modules.entries.category_entry import CategoryEntry
from modules.entries.work_type_entry import WorkTypeEntry
from modules.database import database_utils


def main(args):

    if args.dry_run:
        print("DRY RUN - Simulated run, but nothing written")

    if args.object_type == "project":
        new_project(args.name, args.category, dry_run=args.dry_run, print_current=True)

    elif args.object_type == "category":
        if args.category:
            print("--category flag ignored as it only is applicable for projects")

        new_category(args.name, dry_run=args.dry_run, print_current=True)

    elif args.object_type == "work_type":
        new_work_type(args.name, dry_run=args.dry_run)

    else:
        print("Unknown object type: {}".format(args.object_type))


def new_project(project_name=None, category=None, dry_run=False, print_current=False):

    if print_current:
        existing_projects = [proj.name for proj in ProjectEntry.get_project_list()]
        print("Existing categories: {}".format(" ".join(existing_projects)))

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

    cat_names = [cat.name for cat in CategoryEntry.get_category_list()]

    if category not in cat_names:

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


def new_work_type(work_type_name, dry_run=False, silent_fail=False):

    """Add new worktype to database"""

    current_worktypes = WorkTypeEntry.get_work_type_list()

    if work_type_name is None:
        wt_string = "Enter work type (empty to abort): "
        work_type_name = prompt_utils.prompt_for_name(wt_string)

    if work_type_name in current_worktypes:
        if not silent_fail:
            print("Work type already exists!")
            sys.exit(0)
    else:
        print("Adding new work type {}".format(work_type_name))

        entry = WorkTypeEntry(work_type_name)

        if not dry_run:
            database_utils.insert_work_type_entry_into_database(entry)
        else:
            print("{}: {}".format("Dry run", entry))


def new_category(category_name, dry_run=False, silent_fail=False, print_current=False):
    
    current_categories = database_utils.get_categories_as_strings()

    if print_current:
        print("Existing categories: {}".format(" ".join(current_categories)))

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
            new_category_entry = CategoryEntry(category_name)
            database_utils.insert_category_into_database(new_category_entry)
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
