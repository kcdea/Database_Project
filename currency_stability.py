import dash
import dash_html_components as html
import dash_core_components as dcc

from navbar import navbar
import data


def currency_stability_page():
    layout = html.Div([
        navbar(),
        html.Div([
            html.H6('Countries:'),
            dcc.Dropdown(
                id='currency-stability-countries',
                options=[{'label': i, 'value': i} for i in data.COUNTRIES],
                value=['US', 'CHINA'],
                multi=True
            ),
            html.H6('Crypto-Currencies:'),
            dcc.Dropdown(
                id='currency-stability-currencies',
                options=[{'label': i, 'value': i} for i in data.CURRENCIES],
                value=['BTC', 'DASH'],
                multi=True
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
                    style={'display': 'inline-block'}),
            ])],
            style={'display': 'inline-block', 'width': '25%'}),
        html.Div([
            dcc.Graph(id='currency-stability-graph')
        ],
            style={'display': 'inline-block', 'width': '70%'})
    ])
    return layout
