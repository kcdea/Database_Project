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
from volatility import volatility_page, volatility
from year_statistics import year_statistics_page, get_stats
import data
from query import query

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('year-statistics-graph', 'figure'),
    [Input('year-statistics-currency', 'value'),
     Input('year-statistics-country', 'value'),
     Input('year-statistics-year', 'value')])
def year_statistics(currency, country, year):
    if not currency or not country or not year:
        raise PreventUpdate
    year = year % 1000

    dff = get_stats(country, currency, year)

    fig = go.Figure(go.Scatter(
        x=dff['Instability'],
        y=dff['Exchange Rate'],
        mode='markers',
        text=dff['Month'],
        hovertemplate='Month: %{text}'
    ))

    fig.update_layout(
        xaxis={'title': 'Economic Instability'},
        yaxis={'title': 'Exchange Rate'}
    )

    return fig


@app.callback(
    Output('volatility-graph', 'figure'),
    [Input('volatility-currency', 'value'),
     Input('volatility-start', 'date'),
     Input('volatility-end', 'date'),
     Input('toggle', 'value'),
     Input('height', 'value')])
def volatility_disp(currency, start_date, end_date, option, height):
    if not currency or not start_date or not end_date or not height:
        raise PreventUpdate
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    dff = volatility(currency, start_date, end_date)

    fig_volatility = go.Figure()

    if option == 'last 12 hours':
        for i in ["actualPrice", "twelveHour", "twelveHourPlus", "twelveHourMinus", "twelveHourPlusPlus",
                  "twelveHourMinusMinus"]:
            fig_volatility.add_trace(go.Scatter(
                x=dff['datetime'],
                y=dff[i],
                mode='lines',
                name=i
            ))
    else:
        for i in ["actualPrice", "allTime", "allTimePlus", "allTimeMinus", "allTimePlusPlus", "allTimeMinusMinus"]:
            fig_volatility.add_trace(go.Scatter(
                x=dff['datetime'],
                y=dff[i],
                mode='lines',
                name=i
            ))
    
    fig_volatility.update_layout(height = int(height))
    
    return fig_volatility


@app.callback(
    Output('coef', 'children'),
    Output('currency-coef-graph-1', 'figure'),
    Output('currency-coef-graph-2', 'figure'),
    [Input('currency-coef-currency1', 'value'),
     Input('currency-coef-currency2', 'value'),
     Input('start', 'date'),
     Input('end', 'date')])
def currency_coefficient(c1, c2, coefStart, coefEnd):
    coefStart = datetime.datetime.strptime(coefStart, '%Y-%m-%d').date()
    coefEnd = datetime.datetime.strptime(coefEnd, '%Y-%m-%d').date()
    if not c1 or not c2:
        raise PreventUpdate

    both_crypto = False
    if c2 in data.CURRENCIES:
        both_crypto = True

    dff = correlationCoef(c1, c2, both_crypto, coefStart, coefEnd)
    result = 'Correlation Coefficient: {}'.format(dff['CorrelationCoefficient'][0])

    dff_1_query = "SELECT DMIX.{0}.DATE_TXT, DMIX.{0}.OPEN FROM DMIX.{0} WHERE TO_CHAR(DMIX.{0}.DATE_TXT, 'HH24') = 1".format(c1)
    dff_1_query = dff_1_query + " AND DMIX." + c1 + ".DATE_TXT >= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(coefStart.month).rjust(2, '0'), str(coefStart.day).rjust(2, '0'), str(coefStart.year).rjust(4, '0'))
    dff_1_query = dff_1_query + " AND DMIX." + c1 + ".DATE_TXT <= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(coefEnd.month).rjust(2, '0'), str(coefEnd.day).rjust(2, '0'), str(coefEnd.year).rjust(4, '0'))
    dff_1_query = dff_1_query + " ORDER BY DMIX.{0}.DATE_TXT ASC".format(c1)
    dff_1 = query(dff_1_query, ['Date', 'Price'])
    
    
    
    if both_crypto:
        dff_2_query = "SELECT DMIX.{0}.DATE_TXT, DMIX.{0}.OPEN FROM DMIX.{0} ".format(c2)
        dff_2_query = dff_2_query + "WHERE TO_CHAR(DMIX.{0}.DATE_TXT, 'HH24') = 1".format(c2)
        dff_2_query = dff_2_query + " AND DMIX." + c2 + ".DATE_TXT >= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(coefStart.month).rjust(2, '0'), str(coefStart.day).rjust(2, '0'), str(coefStart.year).rjust(4, '0'))
        dff_2_query = dff_2_query + " AND DMIX." + c2 + ".DATE_TXT <= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(coefEnd.month).rjust(2, '0'), str(coefEnd.day).rjust(2, '0'), str(coefEnd.year).rjust(4, '0'))
        dff_2_query = dff_2_query + " AND TO_CHAR(DMIX.{0}.DATE_TXT, 'HH24') = 1 ORDER BY DMIX.{0}.DATE_TXT ASC".format(c2)
        dff_2 = query(dff_2_query, ['Date', 'Price'])
    else:
        dff_2_query = "SELECT DATE_TXT, {} FROM DMIX.EXCHANGERATES".format(c2)
        dff_2_query = dff_2_query + " WHERE DMIX.EXCHANGERATES.DATE_TXT >= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(coefStart.month).rjust(2, '0'), str(coefStart.day).rjust(2, '0'), str(coefStart.year).rjust(4, '0'))
        dff_2_query = dff_2_query + " AND DMIX.EXCHANGERATES.DATE_TXT <= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(coefEnd.month).rjust(2, '0'), str(coefEnd.day).rjust(2, '0'), str(coefEnd.year).rjust(4, '0'))
        dff_2_query = dff_2_query + " ORDER BY DATE_TXT ASC".format(c2)
        dff_2 = query(dff_2_query, ['Date', 'Price'])

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
    [Input('percent-change-currency-1', 'value'),
     Input('percent-change-currency-2', 'value'),
     Input('percent-change-start', 'date'),
     Input('percent-change-end', 'date')])
def percent_change(currency1, currency2, start_date, end_date):
    # Do not update if there is an empty input
    if not currency1 or not currency2 or not start_date or not end_date:
        raise PreventUpdate
    # Ensure currencies is list
    #if type(currencies) is not list:
    #    currencies = [currencies]

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    dff = percentChange(currency1, currency2, start_date, end_date)

    fig = go.Figure()
    
    if currency1 == currency2:
        currency2Label = 'Copy of ' + currency1
    else:
        currency2Label = currency2
    
    fig.add_trace(go.Scatter(
        x=dff[currency1],
        y=dff[currency2Label],
        name=currency1 + ' vs ' + currency2,
        text = dff['datetime'],
        hovertemplate = '(%{x}, %{y}) @ %{text}',
        mode = 'markers'
    ))

    fig.update_layout(
        xaxis={'title': 'Price Percent Change - ' + currency1},
        yaxis={'title': 'Price Percent Change - ' + currency2}
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
    elif pathname == '/volatility':
        return volatility_page()
    elif pathname == '/instability_exchange_rates':
        return year_statistics_page()
    else:
        return home_page()


if __name__ == '__main__':
    app.run_server(debug=True)
