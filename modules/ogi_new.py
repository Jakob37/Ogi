#!/usr/bin/env python3

from modules import utils

def main(args, conf):

    time_entries_path = conf.get("file_paths", "data")
    projects_path = conf.get("file_paths", "projects")

    if args.object_type == "project":
        pass


    elif args.object_type == "category":
        
        cat_path = conf.get("file_paths", "categories")
        
        if args.category:
            print("--category flag ignored as it only is applicable for projects")

        new_category(cat_path, args.name)


def new_project(projects_path, category_path, new_project, category):
    
    current_projects = utils.check_project_exists(new_project, projects_path)

    with open(projects_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            current_projects.append(line.split('\t')[0])

    if new_project in current_projects:
        print("Project already exists!")
    else:
        cats = get_categories(category_path)
        
        if category is not None and category not in cats:
            print("Unvalid category, try again")
            print("Valid categories:")
            print_categories(category_path)
        else:
            with open(projects_path, 'a') as append_fh:
                print("Adding project {} with category {} to {}".format(new_project, category, projects_path))
                print("{}\t{}".format(new_project, category), file=append_fh)


def new_category(category_path, new_category):
    
    current_categories = get_categories(category_path)

    if new_category in current_categories:
        print("Category already exists!")
    else:
        with open(category_path, 'a') as append_fh:
            print("Adding new category {} to {}".format(new_category, category_path))
            print(new_category, file=append_fh)


def get_categories(cat_path):

    categories = list()
    with open(cat_path) as in_fh:
        for line in in_fh:
            line = line.rstrip()

            categories.append(line)
    return categories


def print_categories(cat_path):

    categories = get_categories(cat_path)
    for cat in categories:
        print(cat)






