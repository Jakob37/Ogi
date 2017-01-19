import datetime
import re
import sys

import ogi_config
from modules.utils import date_utils
from modules.database import database_utils

"""
Main class representing a log entry performed in Ogi
Can either be created directly, or from a string represented
a printed TimeEntry-object
"""


class TimeEntry:

    VALID_LOG_TYPES = ['pomo', 'block', 'session']
    FOCUS_PATTERN = r'^\d+$'
    DURATION_PATTERN = r'^\d+$'
    DATE_PATTERN = r'^\d{8}$'
    TIME_PATTERN = r'^\d{4}$'
    PROJECT_PATTERN = r'^.+$'
    HEADER = ['Date', 'Time', 'Type', 'Focus', 'Duration', 'Message', 'Project']

    def __init__(self, log_type, message, focus=100, date_str=None,
                 time_str=None, project=None, duration=None, quiet=False):

        self.conf = ogi_config.get_config()

        self.log_type = log_type
        self.message = message
        self.focus = focus
        self.date = self.setup_date(date_str)
        self.time = self.setup_time(time_str)
        self.project = project

        self.duration = self.get_duration(log_type, duration, quiet=quiet)

        self.verify_entry()

    @classmethod
    def load_from_string(cls, ogi_string):

        """Generate object from printed string"""

        fields = ogi_string.split('\t')

        date = fields[0]
        time = fields[1]
        log_type = fields[2]
        focus = fields[3]
        duration = int(fields[4])
        message = fields[5]
        project = fields[6]

        new_obj = cls(log_type, message,
                      focus=focus,
                      date_str=date,
                      time_str=time,
                      project=project,
                      duration=duration,
                      quiet=True)
        return new_obj

    def get_log_type(self, log_type):

        if log_type in self.VALID_LOG_TYPES:
            return log_type
        else:
            return 'session'

    def get_duration(self, log_type, duration, quiet=False):

        if log_type == 'pomo':

            if duration is not None and not quiet:
                print('Warning: Duration is {}, but is ignored due to type being {}'
                      .format(duration, log_type))
            return 25

        elif log_type == 'block':

            if duration is not None and not quiet:
                print('Warning: Duration is {}, but is ignored due to type being {}'
                      .format(duration, log_type))

            duration = self.conf.get('settings', 'block_duration')

            if not re.match(self.DURATION_PATTERN, duration):
                raise Exception("Focus must fulfil pattern: {}, found: {}"
                                .format(self.DURATION_PATTERN, duration))
            return int(duration)

        elif duration is not None:
            return duration
        else:
            if log_type == 'session':
                print("You need to specify duration with --duration or -u flag when logging sessions")
                sys.exit(0)
            else:
                raise Exception("Time not specified for log type: {}".format(log_type))

    @staticmethod
    def setup_date(date_str):

        """Get current date, or return existing string"""

        if date_str is None:
            return "{0:%Y%m%d}".format(datetime.datetime.now())
        else:
            return date_str

    @staticmethod
    def setup_time(time_str):

        """Get current time, or return existing string"""

        if time_str is None:
            return "{0:%H%M}".format(datetime.datetime.now())
        else:
            return time_str

    def verify_entry(self):

        if self.log_type not in self.VALID_LOG_TYPES and self.log_type != 'session':
            raise Exception("Invalid log type encountered: {}".format(self.log_type))

        if not re.match(self.FOCUS_PATTERN, str(self.focus)):
            raise Exception("Focus must fulfil pattern: {}, found: {}"
                            .format(self.FOCUS_PATTERN, self.focus))

        if not re.match(self.DATE_PATTERN, str(self.date)):
            raise Exception("Date must fulfil pattern: {}, found: {}"
                            .format(self.DATE_PATTERN, self.date))

        if not re.match(self.TIME_PATTERN, str(self.time)):
            raise Exception("Time must fulfil pattern: {}, found: {}"
                            .format(self.TIME_PATTERN, self.time))

        if not re.match(self.PROJECT_PATTERN, str(self.project)):
            raise Exception("Project must fulfil pattern: {}, found: {}"
                            .format(self.PROJECT_PATTERN, self.project))

    def __str__(self):

        return '{date}\t{time}\t{log_type}\t{focus}\t{duration}\t{message}\t{project}' \
            .format(date=self.date,
                    time=self.time,
                    log_type=self.log_type,
                    focus=self.focus,
                    duration=self.duration,
                    message=self.message,
                    project=self.project)

    @staticmethod
    def parse_log_to_entries(project=None, start_date=None, end_date=None):

        """Return list of entries based on log file"""

        time_entries = list()
        time_entries_str = database_utils.get_time_entries_as_strings()

        for line in time_entries_str:
            entry = TimeEntry.load_from_string(line)
            if project is None or project == entry.project:

                if date_utils.is_date_in_range(entry.date, start_date, end_date):
                    time_entries.append(entry)

        return time_entries
