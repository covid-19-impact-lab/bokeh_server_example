"""Create the master page that is shown when the dashboard is started.

This page shows which optimizations are scheduled, running, finished successfully or
failed. From here the user can monitor any running optimizations.

"""
from bokeh.layouts import Column
from bokeh.models import ColumnDataSource, Panel, Tabs
from bokeh.models.widgets import Div
from bokeh.plotting import figure


def covid_app(doc, plot_data, description):
    """Create the page with the master dashboard.

    Args:
        doc (bokeh.Document):
            document where the overview over the optimizations will be displayed
            by their current stage.
        plot_data (dict)
        description (pd.DataFrame)

    """
    tab_names = ["Overview", "Timeline"]
    tab_list = []
    for i, sec_title in enumerate(tab_names):
        subtopic = description["subtopic"].unique()[i]
        title = Div(text=subtopic.capitalize(), style={"font-size": "200%"})
        p = create_standard_figure(title="")
        source = ColumnDataSource(plot_data)
        p.line(source=source, x="x", y="y")
        col = Column(*[title, p])
        panel = Panel(child=col, title=sec_title, name=f"{sec_title}_panel",)
        tab_list.append(panel)

    tabs = Tabs(tabs=tab_list, name="tabs")
    doc.add_root(tabs)


def create_dashboard_link(name):
    """Create a link refering to *name*'s monitoring app.

    Args:
        name (str): Uniqe name of the database.

    Returns:
        div (bokeh.models.widgets.Div): Link to the database's monitoring page.
    """
    div_name = f"link_{name}"
    open_in_new_tab = r'target="_blank"'
    text = f"<a href=./{name} {open_in_new_tab}> {name}!</a>"
    div = Div(text=text, name=div_name, width=400)
    return div


def create_standard_figure(title, tooltips=None):
    """Return a styled, empty figure of predetermined height and width.

    Args:
        title (str): Title of the figure.
        tooltips (list): List of bokeh tooltips to add to the figure.

    Returns:
        fig (bokeh Figure)

    """
    fig = figure(plot_height=350, plot_width=700, title=title, tooltips=tooltips)
    fig.title.text_font_size = "15pt"
    fig.min_border_left = 50
    fig.min_border_right = 50
    fig.min_border_top = 20
    fig.min_border_bottom = 50
    fig.toolbar_location = None
    return fig
