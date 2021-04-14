import dash
import dash_core_components as dcc
import dash_html_components as html
import data
from query import query
from navbar import navbar


# currency1: any cryptocurrency
# currency2: any other cryptocurrency, or any currency other than USD
# crypto: boolean value that is True is currency2 is a cryptocurrency, False if currency2 is not a cryptocurrency
def correlationCoef(currency1, currency2, crypto):
    queryStr = ""
    if (crypto):
        queryStr = "SELECT CORR(DMIX." + currency1 + ".open, DMIX." + currency2 + ".open) FROM DMIX." + currency1 + " JOIN DMIX." + currency2 + " ON DMIX." + currency1 + ".timestamp = DMIX." + currency2 + ".timestamp"
    else:
        queryStr = "SELECT CORR(crypto_price, " + currency2 + ") FROM DMIX.EXCHANGERATES NATURAL JOIN (SELECT date_txt, AVG(DMIX." + currency1 + ".open) AS crypto_price FROM DMIX." + currency1 + " GROUP BY date_txt)"
    title = 'CorrelationCoefficient'
    headers = [title]
    return query(queryStr, headers)


# returns correlation coefficient (scalar value) between currency1 and currency2

def currency_correlation_page():
    currency_options = data.COUNTRY_CURRENCIES + data.CURRENCIES
    layout = html.Div([
        navbar(),
        html.Div([
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
            )
            ],
            style={'display': 'inline-block', 'width': '25%'}),
        html.Div([
            html.H4(id='coef'),
            html.H6('Currency 1:'),
            dcc.Graph(id='currency-coef-graph-1'),
            html.H6('Currency 1:'),
            dcc.Graph(id='currency-coef-graph-2'),
        ],
            style={'display': 'inline-block', 'width': '70%'})
    ])
    return layout
