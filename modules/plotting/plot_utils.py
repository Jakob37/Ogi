def set_right_hand_legend(df, barplot, x_width=0.8, y_height=1.0, anchor_x=1.6, y_shift=0.0, sub_col_names=False):

    legend_labels = list(df)

    if sub_col_names:
        legend_labels = [elem[1] for elem in list(df)]

    barplot.legend(legend_labels, loc='best')
    # barplot.legend(legend_labels, loc='center right', bbox_to_anchor=(anchor_x, 0.5))
    # box = barplot.get_position()
    # barplot.set_position([box.x0, box.y0 + y_shift, box.width * x_width, box.height * y_height])
