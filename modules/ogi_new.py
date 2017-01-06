#!/usr/bin/env python3

from modules import utils


def main(args, conf):

    if args.dry_run:
        print("DRY RUN - Simulated run, but nothing written")

    projects_path = conf.get("file_paths", "projects")
    cat_path = conf.get("file_paths", "categories")

    if args.object_type == "project":

        new_project(projects_path, cat_path, args.name, args.category, dry_run=args.dry_run)

    elif args.object_type == "category":
        
        if args.category:
            print("--category flag ignored as it only is applicable for projects")

        new_category(cat_path, args.name, dry_run=args.dry_run)


def new_project(projects_path, category_path, project_name, category=None, dry_run=False):
    
    project_exists = utils.check_project_exists(project_name, projects_path)

    if project_exists:
        print("Project already exists!")
    else:
        cats = get_categories(category_path)
        
        if category is not None and category not in cats:
            print("Unvalid category, try again")
            print("Valid categories:")
            print_categories(category_path)
        elif category is None:
            prompt = utils.prompt_yes_no("No category specified, will be categorized as 'uncategorized' [y/N]: ")

            if not prompt:
                print("User aborted, try again")
                exit(0)
            else:
                write_new_project(project_name, 'uncategorized', projects_path, dry_run=dry_run)

        else:
            write_new_project(project_name, category, projects_path, dry_run=dry_run)


def write_new_project(project_name, category_name, project_path, dry_run=False):

    with open(project_path, 'a') as append_fh:
        print("Adding project {} with category {} to {}".format(project_name, category_name, project_path))

        out_string = "{}\t{}".format(project_name, category_name)

        if not dry_run:
            print(out_string, file=append_fh)
        else:
            print("{}: {} to {}".format("Dry run", out_string, project_path))


def new_category(category_path, category_name, dry_run=False):
    
    current_categories = get_categories(category_path)

    if category_name in current_categories:
        print("Category already exists!")
    else:
        with open(category_path, 'a') as append_fh:
            print("Adding new category {} to {}".format(category_name, category_path))

            if not dry_run:
                print(category_name, file=append_fh)
            else:
                print("{}: {} to {}".format("Dry run", category_name, category_path))


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
