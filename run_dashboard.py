import asyncio
import json
import socket
from contextlib import closing
from functools import partial

import pandas as pd
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.command.util import report_server_init_errors
from bokeh.server.server import Server

from covid_app import covid_app


def run_dashboard(plot_data_path, description_table_path, no_browser=None, port=None):
    """Start the dashboard pertaining to one or several databases.

    Args:
        plot_data_path (str or pathlib.Path): path to the json with the plotting data.
        description_table_path (str or pathlib.Path): path to the description table.
        no_browser (bool, optional): If True the dashboard does not open in the browser.
        port (int, optional): Port where to display the dashboard.

    """
    port = find_free_port() if port is None else int(port)
    no_browser = False if no_browser is None else bool(no_browser)

    with open(plot_data_path, "r") as f:
        plot_data = json.load(f)
    description = pd.read_csv(description_table_path)

    partialed = partial(covid_app, plot_data=plot_data, description=description)
    apps = {"/": Application(FunctionHandler(partialed))}

    _start_server(apps=apps, port=port, no_browser=no_browser)


def _start_server(apps, port, no_browser):
    """Create and start a bokeh server with the supplied apps.

    Args:
        apps (dict): mapping from relative paths to bokeh Applications.
        port (int): port where to show the dashboard.
        no_browser (bool): whether to show the dashboard in the browser

    """
    # necessary for the dashboard to work when called from a notebook
    asyncio.set_event_loop(asyncio.new_event_loop())

    # this is adapted from bokeh.subcommands.serve
    with report_server_init_errors(port=port):
        server = Server(apps, port=port)

        # On a remote server, we do not want to start the dashboard here.
        if not no_browser:

            def show_callback():
                server.show("/")

            server.io_loop.add_callback(show_callback)

        address_string = server.address if server.address else "localhost"

        print(
            "Bokeh app running at:",
            f"http://{address_string}:{server.port}{server.prefix}/",
        )
        server._loop.start()
        server.start()


def find_free_port():
    """Find a free port on the localhost.

    Adapted from https://stackoverflow.com/a/45690594

    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("localhost", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


if __name__ == "__main__":
    run_dashboard(
        plot_data_path="mock_plot_data.json",
        description_table_path="mock_data_description.csv",
        port=None,
    )
