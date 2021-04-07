import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import navbar

nav = navbar()


def complex_query_page():
    page = html.Div([
        nav,
        html.P('This is where the complex queries will be, whatever that means....')
    ])
    return page

