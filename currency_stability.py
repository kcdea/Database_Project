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
            ])
        ]),
        dbc.Row([
            html.Div([
                html.P(
                    """\
                    This page demonstrates the distinction between various methods of calculating the standard deviation of a cryptocurrency, as well as the ability of said methods to demonstrate the volatility of said cryptocurrency.\n
                    Historically, stock traders have used the standard deviation of a stock's price in a preceding timeframe as a means of determining its "volatility", which is best defined as its range of probable price shifts in an upcoming market segment. 
                    Cryptocurrencies, like stocks, are also investments, and are often referred to as some of the most volatile investments traders can place their money in. Of course, as with any investment, high risks can yield high rewards, but awareness of these risks is critical to making an informed decision. \n
                    The graph shown above is able to make use of one of two running averages to demonstrate the standard deviation's ability to predict price shifts. In "All time" mode, a running average of all data within the specified range is used to determine the standard deviation at a given point. This prevents significant changes in predictions from occurring due to price spikes, but can become wildly inaccurate over long intervals.
                    "Last 12 hours" mode, on the other hand, utilizes a running average of the 12 hours of data preceding a given data point to determine the standard deviation. This allows the standard deviation to "forget" past trends to enable more accurate short-term predictions. However, this can result in gross overestimations of future value during moments of extreme volatility. \n
                    Regardless of which mode is chosen, the graph displays six lines over the selected time interval. The most jagged and erratic of these is the actual price graph of the currency, similarly to that shown on this website's homepage. Surrounding it are five lines, four of which appear to nearly mirror about a centerline. The "centerline" is the running average for the selected mode at a given data points.
                    Above and below this average are the first standard deviations from the mean. Due to the mathematical properties of standard deviation calculations and limitations of reliance on historical data, it can be assumed that there is a 68.1% chance for the following price point to fall within this range. \n
                    The two lines surrounding the first standard deviations are the second standard deviations. It can be assumed that there is a 95.3% chance for the following price point to fall within this range. \n
                    Key concepts covered for this query included the use of the Oracle SQL "OVER" clause to generate running averages, the use of the SQL "STDDEV" command to determine the standard deviation of a given data set, and combination of these results to generate appropriate statistical ranges for the data."""
                )
            ],
            style = {'margin-left' : '30px', 'margin-right' : '30px'})
        ])
    ])
    return layout
