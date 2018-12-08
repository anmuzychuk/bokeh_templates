"""
Box Plot bokeh template

"""
from bokeh.models import ColumnDataSource
#from bokeh.models import HoverTool
from bokeh.plotting import figure


def BoxPlotFigure(summary, **kwargs):
    """Boxplot boke template

    :param summary: as object of Summary class

    """
    # smr = Summary(data, key, val, k)
    key = summary.key
    val = summary.xval
    smr = summary.summary_table
    print
    outliers = summary.outliers

    p = figure(background_fill_color="#f2f2f2", x_range=smr[key], **kwargs)

    # stem
    p.segment(smr[key], smr['stem_upper'], smr[key], smr['q3'], line_color="darkgray")
    p.segment(smr[key], smr['stem_lower'], smr[key], smr['q1'], line_color="darkgray")

    # box
    p.vbar(smr[key], 0.7, smr['q1'], smr['q3'], fill_color="white", line_color="darkgray")

    # whiskers (almost-0 height rects simpler than segments)
    p.rect(smr[key], smr['stem_upper'], 0.2, 0.01, line_color="darkgray")
    p.rect(smr[key], smr['stem_lower'], 0.2, 0.01, line_color="darkgray")
    p.rect(smr[key], smr['median'], 0.7, 0.01, line_color="indianred")

    # outliers
    if outliers.shape[0] > 0:
        source = ColumnDataSource(outliers)
        p.circle(key, val, size=6, color="darksalmon", fill_alpha=0.6, source=source)
        # hover = HoverTool(tooltips=[(key, "@{}".format(key)),
        #                             (val, "@{}".format(val))])
        # p.add_tools(hover)

    p.xaxis.major_label_text_font_size = "10pt"

    p.xaxis.axis_line_color = 'lightgrey'
    p.yaxis.axis_line_color = 'lightgrey'

    p.xaxis.minor_tick_line_alpha = 0
    p.yaxis.minor_tick_line_alpha = 0

    p.xaxis.major_tick_line_color = 'lightgrey'
    p.yaxis.major_tick_line_color = 'lightgrey'

    return p
