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


class DayEntry:

    HEADER = ['Date', 'Time', 'Type', 'Focus', 'Duration', 'Message', 'Project']

    ALERTNESS_PATTERN = r'^\d+$'
    SLEEP_TIME = r'^\d+(\.\d+)?$'
    EXTERNAL_PRESSURE = r'^\d+'
    INTERNAL_PRESSURE = r'^\d+'

    def __init__(self, description, alertness, sleep_time, external_pressure, internal_pressure,
                 date_str=None, time_str=None):

        self.conf = ogi_config.get_config()

        self.date = date_utils.setup_date_for_entry(date_str)
        self.time = date_utils.setup_time_for_entry(time_str)

        self.description = description
        self.alertness = alertness
        self.sleep_time = sleep_time
        self.external_pressure = external_pressure
        self.internal_pressure = internal_pressure
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
        work_type = fields[8]

        new_obj = cls(log_type, message,
                      focus=focus,
                      date_str=date,
                      time_str=time,
                      project=project,
                      duration=duration,
                      work_type=work_type,
                      quiet=True)
        return new_obj

    def verify_entry(self):

        if not re.match(self.ALERTNESS_PATTERN, str(self.alertness)):
            raise ValueError("Focus must fulfil pattern: {}, found: {}"
                             .format(self.ALERTNESS_PATTERN, self.alertness))

        if not re.match(self.SLEEP_TIME, str(self.sleep_time)):
            raise ValueError("Focus must fulfil pattern: {}, found: {}"
                             .format(self.SLEEP_TIME, self.sleep_time))

        if not re.match(self.EXTERNAL_PRESSURE, str(self.external_pressure)):
            raise ValueError("Focus must fulfil pattern: {}, found: {}"
                             .format(self.EXTERNAL_PRESSURE, self.external_pressure))

        if not re.match(self.INTERNAL_PRESSURE, str(self.internal_pressure)):
            raise ValueError("Focus must fulfil pattern: {}, found: {}"
                             .format(self.INTERNAL_PRESSURE, self.internal_pressure))

    def __str__(self):

        return self.str(delim="\t")

    def str(self, delim="\t"):

        return '{date}{d}{time}{d}{descr}{d}{alert}{d}{sleep}{d}{external}{d}{internal}' \
            .format(date=self.date,
                    time=self.time,
                    descr=self.description,
                    alert=self.alertness,
                    sleep=self.sleep_time,
                    external=self.external_pressure,
                    internal=self.internal_pressure,
                    d=delim)
