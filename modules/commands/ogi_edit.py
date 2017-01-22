

from modules.database import database_utils
from  modules.utils import prompt_utils


def main(args):

    if args.edit_type == 'amend_last_entry':
        amend_last_entry(dry_run=args.dry_run)
    else:
        print("No valid argument specified")


def amend_last_entry(dry_run=False):

    last_entry = database_utils.get_last_time_entry_string()
    prompt_string = "Delete entry: \"{}\", ".format(last_entry)
    proceed_delete = prompt_utils.prompt_yes_no(prompt_string)

    if proceed_delete:
        if not dry_run:
            print("Deleting...")
            database_utils.delete_last_time_entry()
        else:
            print("Would have deleted entry, stopping for dry-run")
    else:
        print("Stopped, not deleting")
