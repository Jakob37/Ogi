# # import modules.entries.time_entry as time_entry
# # from modules.entries.project_entry import ProjectEntry
# # from modules.entries.category_entry import CategoryEntry
# # from modules.entries.work_type_entry import WorkTypeEntry
#
# from modules.database import database_utils
# from modules.utils import date_utils
#
#
# def get_time_entries(project=None, work_type=None, category=None, start_date=None, end_date=None):
#
#     """Return list of entries based on log file"""
#
#     from modules.entries.time_entry import TimeEntry
#
#     time_entries = list()
#     time_entries_str = database_utils.get_time_entries_as_strings()
#
#     for line in time_entries_str:
#         entry = TimeEntry.load_from_string(line)
#         if project is None or project == entry.project:
#             if category is None or category == entry.project.category:
#                 if work_type is None or work_type == entry.work_type:
#                     if date_utils.is_date_in_range(entry.date, start_date, end_date):
#                         time_entries.append(entry)
#
#     return time_entries
