import datetime
from dateToTimestamp import dateToTimestamp
from query import query
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import data

from navbar import navbar


def percentChange(currency1, currency2, startDate=datetime.date(2012, 1, 1), endDate=datetime.date.today()):
    start = dateToTimestamp(startDate)
    end = dateToTimestamp(endDate)
    currencies = [currency1, currency2]
    
    queryStr = 'SELECT DMIX.{0}.DATE_TXT, '.format(currencies[0])
    if currency1 == currency2:
        queryStr = queryStr + '((DMIX.{0}.CLOSE - DMIX.{0}.OPEN) / DMIX.{0}.OPEN), '.format(currency1)
        queryStr = queryStr + '((DMIX.{0}.CLOSE - DMIX.{0}.OPEN) / DMIX.{0}.OPEN) AS COPYOF{0}'.format(currency1)
        queryStr = queryStr + ' FROM DMIX.{0}'.format(currency1)
    else:
        position = 0
        while position < len(currencies):
            if position != 0:
                queryStr = queryStr + ', '
            queryStr = queryStr + '((DMIX.{0}.CLOSE - DMIX.{0}.OPEN) / DMIX.{0}.OPEN)'.format(currencies[position])
            position = position + 1;
        position = 0
        queryStr = queryStr + ' FROM '
        while position < len(currencies):
            if position == 0:
                queryStr = queryStr + "DMIX." + currencies[position]
            else:
                queryStr = queryStr + ' INNER JOIN DMIX.{1} ON DMIX.{0}.DATE_TXT = DMIX.{1}.DATE_TXT'.format(currencies[0],
                                                                                                             currencies[
                                                                                                                 position])
            position = position + 1
    queryStr = queryStr + " WHERE {0}.DATE_TXT >= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY')".format(currencies[0], str(startDate.month).rjust(2, '0'), str(startDate.day).rjust(2, '0'), str(startDate.year).rjust(4, '0'))
    queryStr = queryStr + " AND {0}.DATE_TXT <= TO_DATE('{1}-{2}-{3}', 'MM-DD-YYYY')".format(currencies[0], str(endDate.month).rjust(2, '0'), str(endDate.day).rjust(2, '0'), str(endDate.year).rjust(4, '0'))
    for currency in currencies:
        queryStr = queryStr + ' AND DMIX.{0}.OPEN > 0'.format(currency)
    queryStr = queryStr + ' ORDER BY DMIX.{0}.DATE_TXT ASC'.format(currencies[0])

    headers = currencies
    if currency1 == currency2:
        headers[1] = 'Copy of ' + headers[1]
    headers.insert(0, "datetime")
    return query(queryStr, headers)


def percentChangePage():
    layout = html.Div([
        navbar(),
        dbc.Row([
            dbc.Col([html.H6('Crypto-Currencies:'),
                    dcc.Dropdown(
                        id='percent-change-currency-1',
                        options=[{'label': i, 'value': i} for i in data.CURRENCIES],
                        value='BTC',
                        multi=False
                    ),
                    dcc.Dropdown(
                        id='percent-change-currency-2',
                        options=[{'label': i, 'value': i} for i in data.CURRENCIES],
                        value='ETH',
                        multi=False
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Start Date:'),
                            dcc.DatePickerSingle(
                                id='percent-change-start',
                                min_date_allowed=data.MIN_DATE,
                                max_date_allowed=data.MAX_DATE,
                                date=data.DEFAULT_DATE
                            )],
                            style={'display': 'inline-block'}),
                        html.Div([
                            html.H6('End Date:'),
                            dcc.DatePickerSingle(
                                id='percent-change-end',
                                min_date_allowed=data.MIN_DATE,
                                max_date_allowed=data.MAX_DATE,
                                date=data.MAX_DATE
                            )],
                            style={'display': 'inline-block'})])],
                    md=4),
            dbc.Col([dcc.Graph(id='percent-change-graph')])
        ]),
        dbc.Row([
            html.Div([
                html.P("""
                    This page demonstrates the correlation, or lack thereof, between the price shifts of two cryptocurrencies.
                    Due to the nature of cryptocurrency as a collective platform without merit-based backing for its value,
                    changes in the price of one coin have been anecdotally known to create changes in the price of others. For instance,
                    Ethereum (ETH) and Bitcoin (BTC) are both built upon the Ethereum blockchain, meaning price changes of one modify the
                    amount of money in circulation in the blockchain, resulting in changes in the value of both currencies.
                    The graph shown above attempts to visualize this trend by showcasing the percent change in price for each hour of a currency's
                    data relative to that of another. The percent change in price is calculated internally for each row of data by finding the difference
                    between the closing and opening price of the currency in the given hour and dividing that by the opening price.
                    The degree to which changes in the price of two cryptocurrencies correlate can be visualized by how similar the data is to a line y = ax.
                    As an example, selecting the same currency twice places the data points along the line x=y, as the relationship between a currency's
                    percentage price changes and themselves is one-to-one. The more a relationship between two currencies deviates from this standard, outliers notwithstanding, the less
                    correlated their price shifts can be considered to be.
                    Hovering over a given data point will provide information on when it was collected, allowing for easier consideration of outliers and what may have caused them.
                    Key concepts covered for this query included the use of row-internal data calculations to determine overall trends in a data set and the comparison of two sets relative to each other in the same visualization.
                """)
            ],
            style = {'margin-left' : '30px', 'margin-right' : '30px'})
        ])
    ])
    return layout
