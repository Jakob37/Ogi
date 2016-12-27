#/usr/bin/env python3

import argparse
import re


def main():

    args = parse_arguments()

    time_entry = TimeEntry(args.log_type, args.message, args.focus, args.date, args.time)

    print(time_entry)


class TimeEntry:

    VALID_LOG_TYPES = ['pomo', 'block']
    FOCUS_PATTERN = r'^\d+$'
    DATE_PATTERN = r'^\d{6}$'
    TIME_PATTERN = r'^\d{4}$'
    HEADER = ['Date', 'Time', 'Type', 'Focus', 'Duration', 'Message']


    def __init__(self, log_type, message, focus=100, date_str=None, time_str=None):

        self.log_type = log_type
        self.message = message
        self.focus = focus
        self.date = self.setup_date(date_str)
        self.time = self.setup_time(time_str)

        self.duration = self.get_duration(self.log_type)

        self.verify_entry()

        print("Entry verification succeeded!")


    def get_duration(self, log_type):

        if log_type == 'pomo':
            return 25
        elif log_type == 'block':
            return 40
        else:
            raise Exception("Time not specified for log type: {}".format(log_type))


    def setup_date(self, date_str):

        """Get current date, or return existing string"""

        if date_str is None:
            pass
        else:
            return date_str

    def setup_time(self, time_str):

        """Get current time, or return existing string"""

        if time_str is None:
            pass
        else:
            return time_str

    def verify_entry(self):

        print(self.message)
        print(self.focus)
        print(self.date)
        print(self.time)

        if not self.log_type in self.VALID_LOG_TYPES:
            raise Exception("Invalid log type encountered: {}".format(self.log_type))

        if self.message == None:
            raise Exception("No description found. This field is mandatory.")

        if not re.match(self.FOCUS_PATTERN, str(self.focus)):
            raise Exception("Focus must fulfil pattern: {}, found: {}" \
                .format(self.FOCUS_PATTERN, self.focus))

        if not re.match(self.DATE_PATTERN, str(self.date)):
            raise Exception("Date must fulfil pattern: {}, found: {}" \
                .format(self.DATE_PATTERN, self.date))

        if not re.match(self.TIME_PATTERN, str(self.time)):
            raise Exception("Time must fulfil pattern: {}, found: {}" \
                .format(self.TIME_PATTERN, self.time))

    def __str__(self):

        return '{date}\t{time}\t{log_type}\t{focus}\t{duration}\t{message}' \
            .format(date=self.date,
                    time=self.time,
                    log_type=self.log_type,
                    focus=self.focus,
                    duration=self.duration,
                    message=self.message)


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('log_type', choices=['pomo', 'block'])
    parser.add_argument('-m', '--message',
                        help='Description of performed task during logged time')

    parser.add_argument('-t', '--time', default=None,
                        help="Format: HHMM, defaults to current time")
    parser.add_argument('-d', '--date', default=None,
                        help="Format: YYMMDD, defaults to current date")
    parser.add_argument('-f', '--focus', default=100, type=int)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
