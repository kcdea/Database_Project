import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from data import df
from home_page import home_page
from graph_page import graph_page
from info_page import info_page
from complex_query_page import complex_query_page
from navbar import navbar

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('time-series-graph', 'figure'),
    [Input('year-selector', 'value'),
     Input('country-selector', 'value')])
def update_graph(year_value, countries):

    dff = df[df['Year'] <= year_value]
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
