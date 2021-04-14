import datetime
from dateToTimestamp import dateToTimestamp
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import data
from query import query
from navbar import navbar


# currency1: any cryptocurrency
# currency2: any other cryptocurrency, or any currency other than USD
# crypto: boolean value that is True is currency2 is a cryptocurrency, False if currency2 is not a cryptocurrency
def correlationCoef(currency1, currency2, crypto, startDate=datetime.date(2012, 1, 1), endDate=datetime.date.today()):
        queryStr = ""
        if (crypto):
                if currency1 == currency2:
                        queryStr = "SELECT CORR(DMIX.{0}.OPEN, DMIX.{0}.OPEN) FROM DMIX.{0}".format(currency1)
                else:
                        queryStr = "SELECT CORR(DMIX." + currency1 + ".open, DMIX." + currency2 + ".open) FROM DMIX." + currency1 + " JOIN DMIX." + currency2 + " ON DMIX." + currency1 + ".date_txt = DMIX." + currency2 + ".date_txt"
                queryStr = queryStr + " WHERE DMIX." + currency1 + ".DATE_TXT >= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(startDate.month).rjust(2, '0'), str(startDate.day).rjust(2, '0'), str(startDate.year).rjust(4, '0'))
                queryStr = queryStr + " AND DMIX." + currency1 + ".DATE_TXT <= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(endDate.month).rjust(2, '0'), str(endDate.day).rjust(2, '0'), str(endDate.year).rjust(4, '0'))
        else:
                queryStr = "SELECT CORR(crypto_price, " + currency2 + ") FROM DMIX.EXCHANGERATES NATURAL JOIN (SELECT date_txt, DMIX." + currency1 + ".open AS crypto_price FROM DMIX." + currency1 + ")"
                queryStr = queryStr + " WHERE date_txt >= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(startDate.month).rjust(2, '0'), str(startDate.day).rjust(2, '0'), str(startDate.year).rjust(4, '0'))
                queryStr = queryStr + " AND date_txt <= TO_DATE('{0}-{1}-{2}', 'MM-DD-YYYY')".format(str(endDate.month).rjust(2, '0'), str(endDate.day).rjust(2, '0'), str(endDate.year).rjust(4, '0'))
        title = 'CorrelationCoefficient'
        headers = [title]
        return query(queryStr, headers)


# returns correlation coefficient (scalar value) between currency1 and currency2

def currency_correlation_page():
    sortedCurrencies = data.COUNTRY_CURRENCIES
    sortedCurrencies.sort()
    currency_options = sortedCurrencies + data.CURRENCIES
    layout = html.Div([
        navbar(),
        dbc.Row([
            dbc.Col([
                html.H6('Currency 1:'),
                dcc.Dropdown(
                    id='currency-coef-currency1',
                    options=[{'label': i, 'value': i} for i in data.CURRENCIES],
                    value='BTC'
                ),
                html.H6('Currency 2:'),
                dcc.Dropdown(
                    id='currency-coef-currency2',
                    options=[{'label': i, 'value': i} for i in currency_options],
                    value='GBP',
                ),
                html.Div([
                        html.Div([
                            html.H6('Start Date:'),
                            dcc.DatePickerSingle(
                                id='start',
                                min_date_allowed=data.MIN_DATE,
                                max_date_allowed=data.MAX_DATE,
                                date=data.DEFAULT_DATE
                            )],
                            style={'display': 'inline-block'}),
                        html.Div([
                            html.H6('End Date:'),
                            dcc.DatePickerSingle(
                                id='end',
                                min_date_allowed=data.MIN_DATE,
                                max_date_allowed=data.MAX_DATE,
                                date=data.MAX_DATE
                            )],
                            style={'display': 'inline-block'})])
            ], md=4),
            dbc.Col([
                html.H4(id='coef'),
                html.H6('Currency 1:'),
                dcc.Graph(id='currency-coef-graph-1'),
                html.H6('Currency 2:'),
                dcc.Graph(id='currency-coef-graph-2')
            ], md=8)
        ])
    ])
    return layout
