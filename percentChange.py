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
        ])
    ])
    return layout
