
from modules.utils import calc_utils
from modules.utils import date_utils


def main(args):

    homogeneity_measure = calc_utils.calculate_homogeneity_measure(start_date=date_utils.get_start_of_week(),
                                                                   end_date=date_utils.get_current_date())
    print('Current homogeneity: {:.2}'.format(homogeneity_measure))

