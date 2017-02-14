import webbrowser


def generate_html(output_fp, plot_fps, week_entries_html=None):

    if week_entries_html is not None:
        week_entries_string = '<table>{}</table>'.format('\n'.join(week_entries_html))
    else:
        week_entries_string = 'No time entries to show'

    barplot_scrs_base = '<img src="{}">' * len(plot_fps)
    barplot_html_string = barplot_scrs_base.format(*plot_fps)

    html_string = """
<html>
<head>
<title>Ogi title!</title>
</head>
<body>
<p>Hello world!</p>
{barplots}
{entry_lines}
</body>
</html>
        """.format(
                    barplots=barplot_html_string,
                    entry_lines=week_entries_string)

    with open(output_fp, 'w') as out_fh:
        print(html_string, file=out_fh)


def open_in_browser(html_path, open_new_window=False):

    """
    For documentation of the webbrowser module,
    see http://docs.python.org/library/webbrowser.html
    """

    if open_new_window:
        print('prevent new tab')
        new = 1
    else:
        print('new tab')
        new = 2  # open in a new tab, if possible

    webbrowser.open(html_path, new=new)

    # open a public URL, in this case, the webbrowser docs
    # url = "http://docs.python.org/library/webbrowser.html"
    # webbrowser.open(url, new=new)

    # open an HTML file on my own (Windows) computer
    # url = "file://X:/MiscDev/language_links.html"
    # webbrowser.open(url, new=new)
