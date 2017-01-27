
import webbrowser
import pandas as pd
import sys

import ogi_config
from modules.utils import date_utils
from modules.entries.project_entry import ProjectEntry
from modules.entries.time_entry import TimeEntry


def main(args):

    print("Hello world!")

    conf = ogi_config.get_config()

    # barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'barplot.png')
    # generate_project_summary_plot(barplot_path)

    barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'barplot.png')
    generate_day_summary_plot(barplot_path)

    html_path = conf.get('file_paths', 'html')
    generate_html(html_path, barplot_path)

    if args.open_in_browser:
        open_in_browser(html_path)


def generate_project_summary_plot(output_path, time_thres=2):

    """Horizontal stacked barplots with total project time"""

    proj_df = get_project_dataframe(time_threshold=time_thres)
    proj_df = proj_df.set_index(['categories'])

    barplot = proj_df.pivot(columns='names', values='time').plot(kind='barh', stacked=True, width=0.6,)

    set_right_hand_legend(barplot)

    barplot_fig = barplot.get_figure()
    barplot_fig.savefig(output_path)


def generate_day_summary_plot(output_path):

    """Vertical stacked barplots for each day"""

    te_df = get_time_entry_dataframe(start_date=date_utils.get_start_of_week())
    sub_df1 = te_df.groupby(['date', 'project']).sum().unstack()
    barplot = sub_df1.plot(kind='bar', stacked=True)

    set_right_hand_legend(barplot, x_width=0.6, y_height=0.9, y_shift=0.1, anchor_x=1.8)

    fig = barplot.get_figure()
    fig.savefig(output_path)


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


def set_right_hand_legend(barplot, x_width=0.8, y_height=1.0, anchor_x=1.6, y_shift=0.0):

    barplot.legend(loc='center right', bbox_to_anchor=(anchor_x, 0.5))
    box = barplot.get_position()
    barplot.set_position([box.x0, box.y0 + y_shift, box.width * x_width, box.height * y_height])


def generate_html(output_fp, plot_fp):

    html_string = """
<html>
<head>
<title>Ogi title!</title>
</head>
<body>
<p>Hello world!</p>
<img src="{barplot}">
</body>
</html>
        """.format(barplot=plot_fp)

    with open(output_fp, 'w') as out_fh:

        print(html_string, file=out_fh)


def open_in_browser(html_path):

    """
    For documentation of the webbrowser module,
    see http://docs.python.org/library/webbrowser.html
    """
    new = 2  # open in a new tab, if possible

    webbrowser.open(html_path, new=new)

    # open a public URL, in this case, the webbrowser docs
    # url = "http://docs.python.org/library/webbrowser.html"
    # webbrowser.open(url, new=new)

    # open an HTML file on my own (Windows) computer
    # url = "file://X:/MiscDev/language_links.html"
    # webbrowser.open(url, new=new)

