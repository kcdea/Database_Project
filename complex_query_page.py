import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import navbar

nav = navbar()


def complex_query_page():
    page = html.Div([
        nav,
        dcc.Graph(id='real-data-graph'),
        dcc.Dropdown(
            id='currency-selector',
            options=[{'label': i, 'value': i} for i in ['BTC', 'DASH', 'ETC', 'ETH', 'OMG', 'LTC', 'NEO', 'XMR']],
            value='BTC'
        )
    ])
    return page

