import datetime
import re

"""
Main class representing a log entry performed in Ogi
Can either be created directly, or from a string represented
a printed TimeEntry-object
"""

class TimeEntry:

    VALID_LOG_TYPES = ['pomo', 'block']
    FOCUS_PATTERN = r'^\d+$'
    DATE_PATTERN = r'^\d{8}$'
    TIME_PATTERN = r'^\d{4}$'
    PROJECT_PATTERN = r'^.+$'
    HEADER = ['Date', 'Time', 'Type', 'Focus', 'Duration', 'Message', 'Project']


    def __init__(self, log_type, message, focus=100, date_str=None, 
                 time_str=None, project=None, duration=None):

        self.log_type = log_type
        self.message = message
        self.focus = focus
        self.date = self.setup_date(date_str)
        self.time = self.setup_time(time_str)
        self.project = project

        self.duration = self.get_duration(self.log_type, duration)

        self.verify_entry()

        print("Entry verification succeeded!")


    def get_log_type(self, log_type):

        if log_type in VALID_LOG_TYPES:
            return log_type
        else:
            return 'session'


    def get_duration(self, log_type, duration):

        if log_type == 'pomo':

            if duration is not None:
                print('Warning: Duration is {}, but is ignored due to type being {}'.format(log_type))
            return 25

        elif log_type == 'block':

            if duration is not None:
                print('Warning: Duration is {}, but is ignored due to type being {}'.format(log_type))
            return 40

        elif duration is not None:
            return duration
        else:
            raise Exception("Time not specified for log type: {}".format(log_type))


    def setup_date(self, date_str):

        """Get current date, or return existing string"""

        if date_str is None:
            return "{0:%Y%m%d}".format(datetime.datetime.now())
        else:
            return date_str

    def setup_time(self, time_str):

        """Get current time, or return existing string"""

        if time_str is None:
            return "{0:%H%M}".format(datetime.datetime.now())
        else:
            return time_str

    def verify_entry(self):

        print(self.message)
        print(self.focus)
        print(self.date)
        print(self.time)

        if not self.log_type in self.VALID_LOG_TYPES and self.log_type != 'session':
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

        if not re.match(self.PROJECT_PATTERN, str(self.project)):
            raise Exception("Project must fulfil pattern: {}, found: {}" \
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


