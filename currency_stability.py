import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from navbar import navbar
import data


def currency_stability_page():
    layout = html.Div([
        navbar(),
        dbc.Row([
            dbc.Col([html.H6('Crypto-Currencies:'),
                     dcc.Dropdown(
                         id='currency-stability-currencies',
                         options=[{'label': i, 'value': i} for i in data.CURRENCIES],
                         value=['BTC', 'DASH'],
                         multi=True
                     ),
                     html.H6('Country:'),
                      dcc.Dropdown(
                          id='currency-stability-countries',
                          options=[{'label': i, 'value': i} for i in data.COUNTRIES],
                          value='US',
                      ),
                     html.Div([
                         html.Div([
                             html.H6('Start Date:'),
                             dcc.DatePickerSingle(
                                 id='currency-stability-start',
                                 min_date_allowed=data.MIN_DATE,
                                 max_date_allowed=data.MAX_DATE,
                                 date=data.DEFAULT_DATE
                             )],
                             style={'display': 'inline-block'}),
                         html.Div([
                             html.H6('End Date:'),
                             dcc.DatePickerSingle(
                                 id='currency-stability-end',
                                 min_date_allowed=data.MIN_DATE,
                                 max_date_allowed=data.MAX_DATE,
                                 date=data.MAX_DATE
                             )],
                             style={'display': 'inline-block'})])],
                    md=4),
            dbc.Col([
                dcc.Graph(id='currency-stability-graph'),
                html.P("""This page demonstrates the correlation, or lack thereof, between various cryptocurrencies and the economic stability of various countries.
                Displayed on the x-axis is a scale which is used to quantify the perceived economic instability of the selected country. This index was historically collected monthly and considers a number of factors, namely the mention of terms which indicate economically unstable conditions pertaining to economically unstable conditions in a number of prominent journalistic publications.
                For further details regarding this index, please consult the data source (https://www.policyuncertainty.com/all_country_data.html) and its associated materials. All economic uncertaintly data utilized is derived from the sources listed therein, unless otherwise specified.
                Meanwhile, the Y axis displays the average price of the selected cryptocurrencies for the given month. These averages are calculated individually for the specified months combined into a single table that is then returned to the graph.
                The final result of this graph is a visualization of the relative correlation between a given country's economic instability and the prices of the selected cryptocurrencies. Each data point is graphed independently to demonstrate correlational rather than time-dependent trends.
                Key concepts covered for this query included use of the SQL "WITH", "AVG", AND "UNION" statements to create a table of monthly average values for the selected cryptocurrencies.""")
            ])
        ])
    ])
    return layout
