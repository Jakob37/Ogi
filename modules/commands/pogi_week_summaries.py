
from modules.entries.project_entry import ProjectEntry
from modules.utils import date_utils


def main(args):

    homogeneity_measure = calculate_homogeneity_measure()
    print('Current homogeneity: {:.2}'.format(homogeneity_measure))


def calculate_homogeneity_measure():

    project_times = list()

    for project in ProjectEntry.get_project_list():

        proj_time = project.get_total_time(start_date=date_utils.get_start_of_week())

        if proj_time > 0:
            project_times.append(proj_time)

    tot_time = sum(project_times)
    homogeneity = sum([time ** 2 for time in project_times]) / tot_time ** 2

    return homogeneity

    # print(project_times)
    # print(homogeneity)

