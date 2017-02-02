
import ogi_config

from modules.plotting import barplots
from modules.plotting import web_utils
from modules.entries.time_entry import TimeEntry
from modules.entries.project_entry import ProjectEntry
from modules.utils import date_utils


def main(args):

    print("Hello world!")

    conf = ogi_config.get_config()

    # barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'barplot.png')
    # generate_project_summary_plot(barplot_path)

    barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'barplot.png')
    barplots.generate_day_summary_plot(barplot_path)

    week_entries_html = get_week_entries_html_lines()

    html_path = conf.get('file_paths', 'html')
    web_utils.generate_html(html_path, barplot_path, week_entries_html)

    if not args.do_not_show:
        web_utils.open_in_browser(html_path)


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











