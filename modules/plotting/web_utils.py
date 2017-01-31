import webbrowser


def generate_html(output_fp, plot_fp, week_entries_html):

    week_entries_string = '<table>{}</table>'.format('\n'.join(week_entries_html))

    html_string = """
<html>
<head>
<title>Ogi title!</title>
</head>
<body>
<p>Hello world!</p>
<img src="{barplot}">
{entry_lines}
</body>
</html>
        """.format(barplot=plot_fp, entry_lines=week_entries_string)

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