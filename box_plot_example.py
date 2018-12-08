
from bokeh.plotting import show, output_file

from bokeh_templates import BoxPlotFigure
from bokeh_templates.utils import Summary, generate_data


df = generate_data()
summary = Summary(df, 'group', 'score', 1.5)

# print(summary.key)
TOOLS = "box_zoom,reset,save"

p = BoxPlotFigure(summary, toolbar_location="right", tools=TOOLS,
                  title="This is ggplot2-like boxplot powered by bokeh!")

output_file("boxplot.html", title="boxplot.py example")
show(p)
