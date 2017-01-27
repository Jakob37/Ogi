
import pandas as pd

from modules.entries.time_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry


def get_time_entry_dataframe(start_date=None, end_date=None):

    time_entries = TimeEntry.get_time_entries(start_date=start_date, end_date=end_date)

    project = list()
    duration = list()
    date = list()

    for entry in time_entries:
        project.append(entry.project)
        duration.append(entry.duration)
        date.append(entry.date)

    entry_df = pd.DataFrame({'project': project, 'duration': duration, 'date': date})
    return entry_df


def get_project_dataframe(start_date=None, end_date=None, in_hours=True, time_threshold=0.001):

    proj_list = ProjectEntry.get_project_list()

    names = list()
    time = list()
    categories = list()

    for proj in proj_list:

        names.append(proj.name)
        time.append(proj.get_total_time(start_date=start_date, end_date=end_date, in_hours=in_hours))
        categories.append(proj.category)

    proj_df = pd.DataFrame({'names': names, 'time': time, 'categories': categories})
    proj_df = proj_df.loc[proj_df['time'] >= time_threshold]

    return proj_df
