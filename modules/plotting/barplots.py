
from modules.plotting import dataframes
from modules.plotting import plot_utils
from modules.utils import date_utils


def generate_project_summary_plot(output_path, title="no title", time_thres=2):

    """Horizontal stacked barplots with total project time"""

    proj_df = dataframes.get_project_dataframe(time_threshold=time_thres)
    proj_df = proj_df.set_index(['categories'])

    barplot = proj_df\
        .pivot(columns='names', values='time')\
        .plot(kind='barh', stacked=True, width=0.6, title=title)
    plot_utils.set_right_hand_legend(barplot)

    barplot_fig = barplot.get_figure()
    barplot_fig.savefig(output_path)


def generate_day_summary_plot(output_path, summarize_on='project'):

    """Vertical stacked barplots for each day"""

    allowed_summarize_on = ['project', 'category', 'work_type']
    if summarize_on not in allowed_summarize_on:
        print("Target summarize_on not valid: {}".format(summarize_on))

    te_df = dataframes.get_time_entry_dataframe(start_date=date_utils.get_start_of_week())

    sub_df1 = te_df.groupby(['date', summarize_on]).sum().unstack()

    title_string = summarize_on.capitalize().replace('_', ' ')
    y_label = 'Spent time (minutes)'
    x_label = 'Date'
    barplot = sub_df1.plot(kind='bar', stacked=True, title=title_string)
    barplot.set_xlabel(x_label)
    barplot.set_ylabel(y_label)
    plot_utils.set_right_hand_legend(sub_df1, barplot, x_width=0.6, y_height=0.9, y_shift=0.1, anchor_x=1.8, sub_col_names=True)

    fig = barplot.get_figure()
    fig.savefig(output_path)
