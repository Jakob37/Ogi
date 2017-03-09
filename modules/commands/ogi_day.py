
from modules.utils import prompt_utils
from modules.database import database_utils
from modules.entries.day_entry import DayEntry


def main(args):

    descr = prompt_utils.prompt_for_string('Description: ', default='')
    focus = prompt_utils.prompt_for_string('Focus: ', default='')
    alertness = prompt_utils.prompt_for_number('Alertness (percentage): ', require_int=True)
    sleep_time = prompt_utils.prompt_for_string('Sleep time (hours): ')
    life_intensity = prompt_utils.prompt_for_number('Life intensity (percentage): ', require_int=True)
    mental_load = prompt_utils.prompt_for_number('Mental load (percentage): ', require_int=True)
    clarity = prompt_utils.prompt_for_number('Clarity (percentage): ', require_int=True)

    day_entry = DayEntry(description=descr,
                         focus=focus,
                         alertness=alertness,
                         sleep_time=sleep_time,
                         external_pressure=life_intensity,
                         internal_pressure=mental_load,
                         clarity=clarity)

    # print(descr, focus, alertness, sleep_time, external_pressure, internal_pressure)

    if not args.dry_run:
        database_utils.insert_day_entry_into_database(day_entry)
    else:
        print('Would have inserted following to database:')
        print(day_entry)

