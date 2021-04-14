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
from currency_stability import currency_stability_page
from coinVSInstability import coinVSInstability
from correlation_coef import correlationCoef, currency_correlation_page
import data
from query import query

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('coef', 'children'),
    Output('currency-coef-graph-1', 'figure'),
    Output('currency-coef-graph-2', 'figure'),
    [Input('currency-coef-currency1', 'value'),
     Input('currency-coef-currency2', 'value')])
def currency_coefficient(c1, c2):
    if not c1 or not c2:
        raise PreventUpdate

    both_crypto = False
    if c2 in data.CURRENCIES:
        both_crypto = True

    dff = correlationCoef(c1, c2, both_crypto)
    result = 'Correlation Coefficient: {}'.format(dff['CorrelationCoefficient'][0])

    dff_1 = query("SELECT DATE_TXT, OPEN FROM DMIX.{} "
                  "WHERE TO_CHAR(DMIX.BTC.DATE_TXT, 'HH24') = 1 ORDER BY DATE_TXT ASC".format(c1),
                  ['Date', 'Price'])

    if both_crypto:
        dff_2 = query("SELECT DATE_TXT, OPEN FROM DMIX.{} "
                      "WHERE TO_CHAR(DMIX.BTC.DATE_TXT, 'HH24') = 1 ORDER BY DATE_TXT ASC".format(c2),
                      ['Date', 'Price'])
    else:
        dff_2 = query('SELECT DATE_TXT, {} FROM DMIX.EXCHANGERATES ORDER BY DATE_TXT ASC'.format(c2), ['Date', 'Price'])

    fig_1 = go.Figure(go.Scatter(
        x=dff_1['Date'],
        y=dff_1['Price'],
        mode='lines'))
    fig_2 = go.Figure(go.Scatter(
        x=dff_2['Date'],
        y=dff_2['Price'],
        mode='lines'))

    fig_1.update_layout(
        xaxis={'title': 'Date'},
        yaxis={'title': 'Price Percent Change'}
    )
    fig_2.update_layout(
        xaxis={'title': 'Date'},
        yaxis={'title': 'Price Percent Change'}
    )

    return result, fig_1, fig_2


@app.callback(
    Output('currency-stability-graph', 'figure'),
    [Input('currency-stability-currencies', 'value'),
     Input('currency-stability-countries', 'value'),
     Input('currency-stability-start', 'date'),
     Input('currency-stability-end', 'date')])
def currency_stability(currencies, countries, start_date, end_date):
    if not countries or not currencies or not start_date or not end_date:
        raise PreventUpdate
    if type(currencies) is not list:
        currencies = [currencies]

    countries = [countries]
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    dff = coinVSInstability(currencies.copy(), countries.copy(), start_date, end_date)

    fig = go.Figure()
    for i in currencies:
        fig.add_trace(go.Scatter(
            x=dff[countries[0]],
            y=dff[i],
            name=i,
            text=dff['month'],
            hovertemplate='%{text}',
            mode='markers'
        ))

    fig.update_layout(
        xaxis={'title': 'Instability Score'},
        yaxis={'title': 'Price'}
    )

    return fig


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

    dff = percentChange(currencies.copy(), start_date, end_date)

    fig = go.Figure()

    for i in currencies:
        fig.add_trace(go.Scatter(
            x=dff['datetime'],
            y=dff[i],
            mode='lines',
            name=i
        ))

    fig.update_layout(
        xaxis={'title': 'Date'},
        yaxis={'title': 'Price Percent Change'}
    )

    return fig


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/info_page':
        return info_page()
    elif pathname == '/percent_change':
        return percentChangePage()
    elif pathname == '/currency_stability':
        return currency_stability_page()
    elif pathname == '/currency_correlation':
        return currency_correlation_page()
    else:
        return home_page()


if __name__ == '__main__':
    app.run_server(debug=True)
