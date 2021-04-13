import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import datetime

from home_page import home_page
from info_page import info_page
from percentChange import percentChangePage, percentChange
from query import query

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('percent-change-graph', 'figure'),
    [Input('percent-change-currencies', 'value'),
     Input('percent-change-start', 'date'),
     Input('percent-change-end', 'date')])
def percent_change(currencies, start_date, end_date):
    # Do not update if there is an empty input
    if not currencies or not start_date or not end_date:
        raise PreventUpdate
    # Ensure currencies is list
    if type(currencies) is not list:
        currencies = [currencies]

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    temp = currencies.copy()
    dff = percentChange(temp, start_date, end_date)

    fig = go.Figure()

    for i in currencies:
        fig.add_trace(go.Scatter(
            x=dff['datetime'],
            y=dff[i],
            mode='lines',
            name=i
        ))

    return fig


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/info_page':
        return info_page()
    elif pathname == '/percent_change':
        return percentChangePage()
    else:
        return home_page()


if __name__ == '__main__':
    app.run_server(debug=True)
