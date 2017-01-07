#!/usr/bin/env python3

import datetime


def get_current_date():

    """Get datestring for current date in format YYYYMMDD"""

    return "{0:%Y%m%d}".format(datetime.datetime.now())


def get_previous_date(number_days_previous):

    today = datetime.datetime.now()
    delta = datetime.timedelta(days=number_days_previous)
    previous_day = today - delta

    return "{0:%Y%m%d}".format(previous_day)


def is_date_in_range(target, start=None, end=None, debug=False):

    if start:
        in_start_range = int(target) >= int(start)
    else:
        in_start_range = True

    if end:
        in_end_range = int(target) <= int(end)
    else:
        in_end_range = True

    if debug:
        print("{} in [{} {}] - {}/{}".format(target, start, end, in_start_range, in_end_range))

    return in_start_range and in_end_range


def is_today_in_range(start, end):

    today = get_current_date()
    return is_date_in_range(today, start, end)
