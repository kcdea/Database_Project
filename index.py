import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd

from data import df
from home_page import home_page
from graph_page import graph_page
from info_page import info_page
from complex_query_page import complex_query_page
from navbar import navbar
from query import query

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('time-series-graph', 'figure'),
    [Input('min-year-selector', 'value'),
     Input('max-year-selector', 'value'),
     Input('country-selector', 'value')])
def update_graph(min_year_value, max_year_value, countries):

    # Prevents errors when an input is blank
    if not min_year_value or not max_year_value or not countries:
        raise PreventUpdate

    dff = df

    # Apply filters based on side options
    dff = dff[dff['Year'] <= max_year_value]
    dff = dff[dff['Year'] >= min_year_value]

    if type(countries) is not list:
        countries = [countries]
    dff = dff[dff['Entity'].isin(countries)]

    fig = px.line(
        data_frame=dff,
        x=dff['Year'],
        y=dff['Total population'],
        color=dff['Entity'],
        hover_name=dff['Entity'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


@app.callback(
    Output('real-data-graph', 'figure'),
    [Input('currency-selector', 'value')])
def test_graph(currency):
    my_query = 'SELECT DATE_TXT, CLOSE FROM DMIX.{} ORDER BY DATE_TXT ASC'.format(currency)
    column_headers = ['Time', 'Close Price']
    dff = query(my_query, column_headers)

    fig = px.line(
        data_frame=dff,
        x=dff['Time'],
        y=dff['Close Price'])

    return fig


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/graph_page':
        return graph_page()
    elif pathname == '/info_page':
        return info_page()
    elif pathname == '/complex_queries':
        return complex_query_page()
    else:
        return home_page()


if __name__ == '__main__':
    app.run_server(debug=True)
