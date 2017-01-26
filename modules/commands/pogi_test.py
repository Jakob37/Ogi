
import webbrowser
import pandas as pd
import sys


from modules.entries.project_entry import ProjectEntry



def main(args):

    print("Hello world!")

    generate_plot()


def generate_plot():

    proj_list = ProjectEntry.get_project_list()

    names = list()
    time = list()
    categories = list()

    for proj in proj_list:

        names.append(proj.name)

        time.append(proj.get_total_time(in_hours=True))
        categories.append(proj.category)

    print(time)

    proj_df = pd.DataFrame({'names': names, 'time': time, 'categories': categories})

    time_thres = 2

    proj_df = proj_df.loc[proj_df['time'] >= time_thres]

    print(proj_df)

    proj_df = proj_df.set_index(['categories'])
    barplot = proj_df.pivot(columns='names', values='time').plot(kind='barh', stacked=True, width=0.6,)
    barplot.legend(loc='center right', bbox_to_anchor=(1.4, 0.5))

    box = barplot.get_position()
    barplot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    print(box)

    barplot_fig = barplot.get_figure()
    barplot_fig.savefig('test.png')




def generate_html():

    pass


def open_in_browser():

    """
    For documentation of the webbrowser module,
    see http://docs.python.org/library/webbrowser.html
    """
    new = 2  # open in a new tab, if possible

    # open a public URL, in this case, the webbrowser docs
    url = "http://docs.python.org/library/webbrowser.html"
    webbrowser.open(url, new=new)

    # open an HTML file on my own (Windows) computer
    url = "file://X:/MiscDev/language_links.html"
    webbrowser.open(url, new=new)

