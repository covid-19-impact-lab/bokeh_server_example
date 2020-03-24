# bokeh_server_example

Minimal example of a bokeh dashboard, mainly to find out how this can be hosted

## Installing dependencies

- Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/distribution/#download-section)
- Open a terminal in the root folder of this repo and type
    - `conda env create -f environment.yaml`
    - `conda activate covid-dashboard`


## Running the dashboard

Type `python run_dashboard.py` in a terminal in the root folder of this repo.

This will open a browser window with the minimal dashboard. If you want to specify
the port, do this at the end of `run_dashboard.py`.

## Background information

The dashboard runs on a [bokeh server](https://docs.bokeh.org/en/latest/docs/user_guide/server.html). The detailed server architecture is explained [here](https://docs.bokeh.org/en/latest/docs/dev_guide/server.html#devguide-server).

All the data needed in the dashboards is loaded once before the Bokeh server is started. It is stored in simple `.csv` and `.json` files. The session specific data is managed by the bokeh server. There is no need for a database to handle user requests.

The information shown in the plots is pre-calculated. Thus the main operation we perform are dictionary lookups, which are very fast. The whole application is probably not very resource intensive.

## Differences between the minimal example later version

- There will be a proper command line interface with options to specify the port
- The data files will be larger, but probably not large. Probably less than 1 MB.
