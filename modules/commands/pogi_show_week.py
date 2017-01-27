
import ogi_config

from modules.plotting import barplots
from modules.plotting import web_utils


def main(args):

    print("Hello world!")

    conf = ogi_config.get_config()

    # barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'barplot.png')
    # generate_project_summary_plot(barplot_path)

    barplot_path = '{}/{}'.format(conf.get('file_paths', 'figures'), 'barplot.png')
    barplots.generate_day_summary_plot(barplot_path)

    html_path = conf.get('file_paths', 'html')
    web_utils.generate_html(html_path, barplot_path)

    if not args.do_not_show:
        web_utils.open_in_browser(html_path)
