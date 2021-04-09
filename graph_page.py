import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from data import df, countries, min_year, max_year

from navbar import navbar

nav = navbar()

graph_body = html.Div([
    html.Div([
        dcc.Dropdown(
            id='country-selector',
            options=[{'label': i, 'value': i} for i in countries],
            multi=True,
            value=['United States', 'Canada']),
        html.Div([
            dcc.Input(
                id='min-year-selector',
                type='number',
                min=min_year,
                max=max_year,
                value=1800),
            dcc.Input(
                id='max-year-selector',
                type='number',
                min=min_year,
                max=max_year,
                value=max_year)],
            style={'display': 'inline-block'})],
        style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='time-series-graph')],
        style={'width': '65%', 'display': 'inline-block'})])


def graph_page():
    layout = html.Div([nav, graph_body])
    return layout
