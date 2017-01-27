
import webbrowser
import pandas as pd
import sys

import ogi_config


from modules.entries.project_entry import ProjectEntry


def main(args):

    print("Hello world!")

    conf = ogi_config.get_config()

    barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'barplot.png')
    generate_plot(barplot_path)

    html_path = conf.get('file_paths', 'html')
    generate_html(html_path, barplot_path)

    if args.open_in_browser:
        open_in_browser(html_path)


def generate_plot(output_path):

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
    barplot_fig.savefig(output_path)


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

