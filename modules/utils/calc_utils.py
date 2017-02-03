
from modules.entries.project_entry import ProjectEntry
from modules.utils import date_utils


def calculate_homogeneity_measure(start_date, end_date):

    project_times = list()

    for project in ProjectEntry.get_project_list():

        proj_time = project.get_total_time(start_date=start_date, end_date=end_date)

        if proj_time > 0:
            project_times.append(proj_time)

    tot_time = sum(project_times)
    homogeneity = sum([time ** 2 for time in project_times]) / tot_time ** 2

    return homogeneity
