#!/usr/bin/env python3

import os
import sys


def prompt_yes_no(prompt_string, yes_default=False):

    """Return True or False based on if user responds with yes or no"""

    # Empty string is counted as 'no'
    yes = {'yes', 'ye', 'y'}
    no = {'no', 'n'}

    if yes_default:
        yes.add('')
        yes_no_string = '[Y/n] '
    else:
        no.add('')
        yes_no_string = '[y/N] '

    while True:
        choice = input(prompt_string + yes_no_string).lower()

        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Invalid response, try again")


def prompt_for_name(prompt_text, default=None, prompt_confirmation=False, return_none_for_empty=False):

    """Ask user to provide name, or leave empty to abort"""

    choice = prompt_for_string(prompt_text, return_none_for_empty=return_none_for_empty, default=default)

    if prompt_confirmation:

        yes_no_string = "{}, is that correct? ".format(choice)
        yes_answer = prompt_yes_no(yes_no_string, yes_default=True)

        if not yes_answer:
            print("No name provided, try again")
            sys.exit(0)

    return choice


def prompt_for_path(prompt_text, prompt_confirmation=True, return_none_for_empty=False):

    """Ask user to provide name, or leave empty to abort"""

    choice = prompt_for_string(prompt_text)

    if choice == '' and return_none_for_empty:
        return None

    full_path = os.path.abspath(choice)

    if prompt_confirmation:

        yes_no_string = "{}, is that correct? ".format(full_path)
        yes_answer = prompt_yes_no(yes_no_string, yes_default=True)

        if not yes_answer:
            print("No path provided, try again")
            sys.exit(0)

    return full_path


def prompt_for_string(prompt_text, return_none_for_empty=False, default=None):

    choice = input(prompt_text)

    if choice == '':

        if return_none_for_empty:

            print("return none for empty")
            return None

        elif default is None:
            print("No input provided, aborted")
            sys.exit(0)
        else:
            choice = default

    return choice
