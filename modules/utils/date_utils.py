#!/usr/bin/env python3

import datetime


def get_date_as_str(date_obj):

    return "{0:%Y%m%d}".format(date_obj)


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


def get_start_of_week():

    current_date_str = get_current_date()
    current_date_obj = get_datestr_as_date(current_date_str)
    start = current_date_obj - datetime.timedelta(days=current_date_obj.weekday())

    return get_date_as_str(start)


def is_month_in_range(start, end):
    pass


def is_year_in_range(start, end):
    pass


def is_today_in_range(start, end):

    today = get_current_date()
    return is_date_in_range(today, start, end)


def get_datestr_as_date(date_str):

    """Format: YYYYMMDD"""

    return datetime.datetime.strptime(date_str, "%Y%m%d")


def get_week_from_str(date_str):

    date_obj = get_datestr_as_date(date_str)
    return date_obj.isocalendar()[1]
