from modules.entries.time_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry
from modules.entries.category_entry import CategoryEntry


def main(args):

    print('hello!')

    if args.time_entries is not None:
        write_time_entries(args.time_entries, delim=args.delim)

    if args.projects is not None:
        write_project_entries(args.projects, delim=args.delim)

    if args.categories is not None:
        write_category_entries(args.categories, delim=args.delim)

    print('All specified writings to files done')


def write_time_entries(out_fp, delim='\t'):

    time_entries = TimeEntry.get_time_entries()

    print('Writing {} time entries to {}'.format(len(time_entries), out_fp))

    with open(out_fp, 'w') as out_fh:
        for entry in time_entries:
            print(entry.str(delim=delim), file=out_fh)


def write_project_entries(out_fp, delim='\t'):

    projects = ProjectEntry.get_project_list()

    print('Writing {} projects to {}'.format(len(projects), out_fp))

    with open(out_fp, 'w') as out_fh:
        for proj in projects:
            print(proj.str(delim=delim), file=out_fh)


def write_category_entries(out_fp, delim='\t'):

    categories = CategoryEntry.get_category_list()

    print('Writing {} categories to {}'.format(len(categories), out_fp))

    with open(out_fp, 'w') as out_fh:
        for cat in categories:
            print(cat, file=out_fh)
