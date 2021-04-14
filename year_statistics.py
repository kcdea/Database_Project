from query import query
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import data

from navbar import navbar


def get_stats(country, currency, year):
    query_str = "SELECT DMIX.ECONOMICINSTABILITY.YEAR, DMIX.ECONOMICINSTABILITY.MONTH, " \
                "AVG(DMIX.ECONOMICINSTABILITY.{0}), AVG(DMIX.EXCHANGERATES.{1}) " \
                "FROM DMIX.EXCHANGERATES, DMIX.ECONOMICINSTABILITY " \
                "WHERE TO_CHAR(DMIX.EXCHANGERATES.DATE_TXT, 'YY') = DMIX.ECONOMICINSTABILITY.YEAR-2000 " \
                "AND TO_CHAR(DMIX.EXCHANGERATES.DATE_TXT, 'MM') = DMIX.ECONOMICINSTABILITY.MONTH " \
                "AND TO_CHAR(DMIX.EXCHANGERATES.DATE_TXT, 'YY') = {2}" \
                "GROUP BY DMIX.ECONOMICINSTABILITY.MONTH, DMIX.ECONOMICINSTABILITY.YEAR " \
                "ORDER BY DMIX.ECONOMICINSTABILITY.YEAR".format(country, currency, year)
    return query(query_str, ['Year', 'Month', 'Instability', 'Exchange Rate'])


def year_statistics_page():
    layout = html.Div([
        navbar(),
        dbc.Row([
            dbc.Col([html.H6('Country:'),
                     dcc.Dropdown(
                         id='year-statistics-country',
                         options=[{'label': i, 'value': i} for i in data.COUNTRIES],
                         value='Japan'
                     ),
                     html.H6('Currency:'),
                     dcc.Dropdown(
                         id='year-statistics-currency',
                         options=[{'label': i, 'value': i} for i in data.COUNTRY_CURRENCIES],
                         value='JPY'
                     ),
                     html.H6('Year:'),
                     dcc.Input(
                         id='year-statistics-year',
                         type='number',
                         min=2017,
                         max=2021,
                         value=2017,
                     )],
                    md=4),
            dbc.Col([
                dcc.Graph(id='year-statistics-graph')
            ])
        ])
    ])
    return layout
