import unittest
import datetime

from modules.utils import utils


class Test(unittest.TestCase):

    """
    Unit tests for utils
    """

    def test_get_current_date(self):

        current_date_string = "{0:%Y%m%d}".format(datetime.datetime.now())
        utils_current_date = utils.get_current_date()
        self.assertEqual(current_date_string, utils_current_date)

    def test_is_date_in_range(self):

        current = "170101"
        start = "161212"
        end = "181119"

        self.assertTrue(utils.is_date_in_range(current, start, end))


if __name__ == "__main__":
    unittest.main()