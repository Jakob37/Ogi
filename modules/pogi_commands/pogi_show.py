
import ogi_config

from modules.plotting import barplots
from modules.plotting import web_utils
from modules.entries.time_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry
from modules.utils import date_utils


def main(args):

    conf = ogi_config.get_config()

    if args.show_type == 'week':
        show_days(args, conf, date_range='week')
    elif args.show_type == 'month':
        show_days(args, conf, date_range='month')
    else:
        raise ValueError("Unknown show type: {}".format(args.show_type))


def show_days(args, conf, date_range='week'):

    ok_ranges = ['week', 'month']
    if date_range not in ok_ranges:
        raise ValueError("Range '{}' must be one of '{}'".format(date_range, ok_ranges))

    proj_barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'proj_barplot.png')
    barplots.generate_date_range_summary_plot(proj_barplot_path, summarize_on='project',
                                              date_range=date_range)

    cat_barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'cat_barplot.png')
    barplots.generate_date_range_summary_plot(cat_barplot_path, summarize_on='category',
                                              date_range=date_range)

    wt_barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'wt_barplot.png')
    barplots.generate_date_range_summary_plot(wt_barplot_path, summarize_on='work_type',
                                              date_range=date_range)

    week_entries_html = get_week_entries_html_lines()

    barplots_paths = [proj_barplot_path, cat_barplot_path, wt_barplot_path]

    html_path = conf.get('file_paths', 'html')
    web_utils.generate_html(html_path, barplots_paths, week_entries_html)

    if not args.do_not_show:
        web_utils.open_in_browser(html_path)


# def show_month(args, conf):
#
#     figures_path = conf.get('file_paths', 'figures')
#
#     day_proj_barplot_path = '{}/{}'.format(figures_path, 'test_barplot.png')
#
#     # What interval?
#     barplots.generate_date_range_summary_plot(day_proj_barplot_path, summarize_on='project', date_range='month')
#
#     html_path = conf.get('file_paths', 'html')
#     web_utils.generate_html(html_path, [day_proj_barplot_path])
#
#     if not args.do_not_show:
#         web_utils.open_in_browser(html_path)


def get_week_entries_html_lines():

    entry_lines = list()
    time_entries = TimeEntry.get_time_entries(start_date=date_utils.get_start_of_week())

    for e in sorted(time_entries, key=lambda x: x.date + x.time):
        nice_time = date_utils.get_nice_time_string(e.duration)
        entry_lines.append('{}\t{}\t{}\t{}\t{}'
                           .format(nice_time, e.date, e.time, e.project, e.message))

    html_lines = list()
    header_fields = ['time', 'date', 'duration', 'project', 'description']
    header = '\n'.join(['<th style="text-align:left">{}</th>'.format(field) for field in header_fields])
    html_lines.append(header)

    for entry_line in reversed(entry_lines):
        line_fields = ''.join(['<td style="text-align:left">{}</td>'.format(field) for field in entry_line.split('\t')])
        entry_line_string = '<tr>{}</tr>'.format(line_fields)

        html_lines.append(entry_line_string)

    return html_lines








